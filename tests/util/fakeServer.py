import json
import socket
import threading
from collections import deque


class Reply:
    def __init__(self, status, headers=None, body=""):
        self.status = status
        self.headers = headers or {}
        self.body = body

    def with_header(self, name, value):
        return Reply(self.status, {**self.headers, name: value}, self.body)


# The client sends the request, then the connection closes before the response starts.
LOST_RESPONSE = object()


def status(code):
    return Reply(code)


def key_status(reply_or_code, value):
    reply = status(reply_or_code) if isinstance(reply_or_code, int) else reply_or_code
    return reply.with_header("Idempotency-Key-Status", value)


def json_reply(code, body):
    return Reply(code, {"Content-Type": "application/json"}, body)


def error(code, error_code):
    return json_reply(code, json.dumps(
        {"errors": [{"code": error_code, "message": error_code}], "requestId": "aRequestId"}))


class RecordedRequest:
    def __init__(self, method, target, headers, body):
        self.method = method
        self.target = target
        self.headers = headers
        self.body = body

    def header_values(self, name):
        return [value for (key, value) in self.headers if key.lower() == name.lower()]

    def header(self, name):
        values = self.header_values(name)
        return values[0] if values else None


class FakeServer:
    """
    A local HTTP server that answers each request with the next queued reply, on a connection of its own.
    A dispatcher, if set, makes the reply instead of the queue.
    """

    def __init__(self):
        self.requests = []
        self.dispatcher = None
        self._replies = deque()
        self._socket = None
        self._thread = None
        self._stopped = threading.Event()
        self.port = None

    def start(self, port=0):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", port))
        sock.listen(16)
        sock.settimeout(0.05)
        self._socket = sock
        self.port = sock.getsockname()[1]
        self._stopped.clear()
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()
        return self

    def close(self):
        if self._socket is None:
            return
        self._stopped.set()
        self._thread.join()
        self._socket.close()
        self._socket = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def url(self, path=""):
        return "http://127.0.0.1:%d%s" % (self.port, path)

    def enqueue(self, *replies):
        self._replies.extend(replies)

    def enqueue_times(self, times, reply):
        self._replies.extend([reply] * times)

    @property
    def request_count(self):
        return len(self.requests)

    def sent_idempotency_keys(self):
        return [r.header("Idempotency-Key") for r in self.requests]

    def _serve(self):
        while not self._stopped.is_set():
            try:
                connection, _ = self._socket.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            try:
                self._handle(connection)
            except OSError:
                pass
            finally:
                connection.close()

    def _handle(self, connection):
        connection.settimeout(5)
        data = connection.recv(65536)
        if data.startswith(b"\x16"):
            # a TLS handshake: answer in plain HTTP, which fails the handshake
            connection.sendall(b"HTTP/1.1 400 Bad Request\r\nConnection: close\r\nContent-Length: 0\r\n\r\n")
            return
        while b"\r\n\r\n" not in data:
            chunk = connection.recv(65536)
            if not chunk:
                return
            data += chunk
        head, body = data.split(b"\r\n\r\n", 1)
        lines = head.decode("iso-8859-1").split("\r\n")
        method, target, _ = lines[0].split(" ", 2)
        headers = [tuple(part.strip() for part in line.split(":", 1)) for line in lines[1:]]
        length = int(next((value for (name, value) in headers if name.lower() == "content-length"), "0"))
        while len(body) < length:
            chunk = connection.recv(65536)
            if not chunk:
                return
            body += chunk
        request = RecordedRequest(method, target, headers, body)
        self.requests.append(request)

        if self.dispatcher is not None:
            reply = self.dispatcher(request)
        elif self._replies:
            reply = self._replies.popleft()
        else:
            reply = Reply(599, {}, "no reply queued")
        if reply is LOST_RESPONSE:
            return
        body_bytes = reply.body.encode("utf-8") if isinstance(reply.body, str) else reply.body
        response = "HTTP/1.1 %d Status\r\n" % reply.status
        for name, value in reply.headers.items():
            response += "%s: %s\r\n" % (name, value)
        response += "Content-Length: %d\r\nConnection: close\r\n\r\n" % len(body_bytes)
        connection.sendall(response.encode("iso-8859-1") + body_bytes)


def free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class FakeClock:
    def __init__(self):
        self.current = 0.0
        self.sleeps = 0
        self.on_sleep = lambda: None

    def now(self):
        return self.current

    def sleep(self, seconds):
        self.sleeps += 1
        self.current += seconds
        self.on_sleep()
