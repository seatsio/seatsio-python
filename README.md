# seatsio-python, the official Seats.io Python SDK

[![Build](https://github.com/seatsio/seatsio-python/workflows/Build/badge.svg)](https://github.com/seatsio/seatsio-python/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/seatsio.svg)](https://badge.fury.io/py/seatsio)

This is the official Python SDK for the [Seats.io V2 REST API](https://docs.seats.io/docs/api-overview), supporting Python 3.10 or newer. 

## Installing

```
pip install seatsio
```

Or:

```
uv add seatsio
```

## Versioning

seatsio-python follows semver since v50.2.0.


## Usage

### General instructions

To use this library, you'll need to create a `seatsio.Client`:

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-workspace-secret-key")
...
```

You can find your _workspace secret key_ in the [settings section of the workspace](https://app.seats.io/workspace-settings).

The region should correspond to the region of your account:

- `seatsio.Region.EU()`: Europe
- `seatsio.Region.NA()`: North-America
- `seatsio.Region.SA()`: South-America
- `seatsio.Region.OC()`: Oceania

If you're unsure about your region, have a look at your [company settings page](https://app.seats.io/company-settings).

### Creating a chart and an event

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-workspace-secret-key")
chart = client.charts.create()
event = client.events.create(chart.key)
```

### Booking objects

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-workspace-secret-key")
client.events.book(event.key, ["A-1", "A-2"])
```

### Releasing objects

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-workspace-secret-key")
client.events.release(event.key, ["A-1", "A-2"])
```

### Booking objects that have been held

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-workspace-secret-key")
client.events.book(event.key, ["A-1", "A-2"], hold_token="a-hold-token")
```

### Changing object status

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-workspace-secret-key")
client.events.change_object_status("<EVENT KEY>", ["A-1", "A-2"], "my-custom-status")
```

### Retrieving object category and status (and other information)

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-workspace-secret-key")
object_infos = client.events.retrieve_object_infos(event.key, ["A-1", "A-2"])

print(object_infos["A-1"].category_key)
print(object_infos["A-1"].category_label)
print(object_infos["A-1"].status)

print(object_infos["A-2"].category_key)
print(object_infos["A-2"].category_label)
print(object_infos["A-2"].status)
```

### Listing a chart's categories

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-workspace-secret-key")
category_list = client.charts.list_categories(<chart key>)
for category in category_list:
  print(category.label)
```

### Updating a category

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-workspace-secret-key")
client.charts.update_category(chart_key=chart.key, category_key=1, label="Updated label", color="#bbbbbb", accessible=True)
```

### Listing all charts

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-workspace-secret-key")
charts = client.charts.list()
for chart in charts:
  print("Chart: " + chart.key)
```

Note: `list()` returns a `PagedIterator`, which under the hood calls the seats.io API to fetch charts page by page. So multiple API calls may be done underneath to fetch all charts.

### Listing charts page by page

E.g. to show charts in a paginated list on a dashboard.

Each page contains an `items` array of charts, and `next_page_starts_after` and `previous_page_ends_before` properties. Those properties are the chart IDs after which the next page starts or the previous page ends.

```python
# ... user initially opens the screen ...

firstPage = client.charts.list_first_page()
for chart in firstPage.items:
  print("Chart: " + chart.key)
```

```python
# ... user clicks on 'next page' button ...

nextPage = client.charts.list_page_after(firstPage.next_page_starts_after)
for chart in nextPage.items:
  print("Chart: " + chart.key)
```

```python
# ... user clicks on 'previous page' button ...

previousPage = client.charts.list_page_before(nextPage.previous_page_ends_before)
for chart in previousPage.items:
  print("Chart: " + chart.key)
```

### Creating a workspace

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-company-admin-key")
client.workspaces.create("a workspace")
```

### Creating a chart and an event with the company admin key

```python
import seatsio
# company admin key can be found on https://app.seats.io/company-settings
# workspace public key can be found on https://app.seats.io/workspace-settings
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-company-admin-key", workspace_key="my-workspace-public-key")
chart = client.charts.create()
event = client.events.create(chart.key)
```

## Error handling

When an API call results in a 4xx or 5xx error (e.g. when a chart could not be found), a SeatsioException is raised.

This exception contains a message string describing what went wrong, and also these properties:

- `errors`: a list of errors (containing a code and a message) that the server returned. In most cases, this list will contain only one element.
- `requestId`: the identifier of the request you made. Please mention this to us when you have questions, as it will make debugging easier.
- `idempotency_key`: the `Idempotency-Key` sent with a `POST`, `PUT` or `DELETE` request (see [Idempotency](#idempotency)), or `None` for other requests.
- `idempotency_key_honored`: whether the server honored that key, according to the `Idempotency-Key-Status` header of the response; `None` when there was no response or the response didn't say.
- `replayed`: `True` when the server didn't execute the request again, but replayed the response of an earlier request with the same key.

`outcome_is_unknown()` tells you whether the request may or may not have been executed: it's `True` when the response was lost after the request was sent (a read timeout, a connection reset), when the server answered with a 5xx, or when it answered `409` with error code `IDEMPOTENCY_KEY_IN_USE` after the client ran out of retries (an earlier request with the same key was still being processed). It's `False` when the request never reached the server (connection refused, connect timeout, DNS or TLS failure) and for every other 4xx.

`is_safe_to_retry_with_same_key()` tells you whether you can make the same call again with the same key (see [Idempotency](#idempotency)) without risking executing it twice, and whether that could give a different result.

If the server returns an error response without an error code (for example, an empty `errors` list), `errors` is empty and `requestId` is still set if the response contains one. If the response body is not a JSON object, `errors` and `requestId` are `None`.

## Idempotency

**NOTE**: Idempotency is currently in a soft launch: it is enabled per company and not yet publicly available. Contact seats.io support to have it enabled for your company.

Every `POST`, `PUT` and `DELETE` request is sent with an `Idempotency-Key` header (a v4 UUID, generated by the client). The server only acts on the key for `POST` and `DELETE` requests; it ignores it on a `PUT`, and doesn't report a status for it. If idempotency is enabled for your company, the server executes a request with a given key only once, and replays the original response when it receives the same request again. The server keeps a key for 10 minutes.

Each response to a `POST` or `DELETE` says what the server did with the key, in the `Idempotency-Key-Status` header: `executed`, `replayed`, `in-use` (an earlier request with the same key is still being processed), `reused` (the key was used for a different request) or `ignored` (idempotency isn't enabled, so the server executed the request without looking at the key).

If the connection fails after the server executed a request but before you received the response, you don't know whether the operation succeeded. The exception contains the key, and tells you whether retrying with that key is safe:

```python
try:
    client.events.create(chart_key)
except SeatsioException as e:
    # True when the request never reached the server, or when its outcome is unknown (a lost response, a 5xx,
    # a 409 IDEMPOTENCY_KEY_IN_USE) and the server honors idempotency keys for it
    if e.is_safe_to_retry_with_same_key():
        client.with_idempotency_key(e.idempotency_key).events.create(chart_key)
```

Retry promptly: after 10 minutes, the server has forgotten the key. The retried request must be identical to the original one, otherwise the server returns an error `422`. Every `POST`, `PUT` and `DELETE` made with the client returned by `with_idempotency_key()` sends that key, so use it for one operation only. You can also supply your own key (e.g. `str(uuid.uuid4())`); it must be a v4 UUID, otherwise `with_idempotency_key()` raises a `ValueError`.

### Automatic retries

The client retries a `POST`, `PUT` or `DELETE` with the same key:

- when the server answers `429`, or `409` with error code `IDEMPOTENCY_KEY_IN_USE`;
- when the request never reached the server (connection refused, connect timeout, DNS or TLS failure);
- when the response was lost after the request was sent, but only if the server has confirmed that it honors idempotency keys for that operation. The client remembers the `Idempotency-Key-Status` of the last response for each operation (for example "book objects in an event", whatever the event), so the first call of an operation is never retried after a lost response, and calls of an operation that answered `ignored` aren't either. A `PUT` is never retried after a lost response, because the server doesn't confirm that it honors keys for it.

All these retries count against `max_retries`: it's the maximum number of retries of a call, whatever the reason (5 by default; `0` turns retries off). Once a request may have reached the server, the client also doesn't start a retry more than 5 minutes after the first attempt, well within the lifetime of the key. A `422` and an invalid key are never retried. The clients returned by `with_idempotency_key()` and `with_workspace_key()` (a client for another workspace of the same company) share the settings and the memory of the client they were made from. Reuse one client, and derive the others from it, instead of creating a new `Client` per request: a new client starts with an empty memory.

There is a small remaining risk: if idempotency is switched off for your company between the last response that said an operation honors keys and a lost response, the retry can execute the operation a second time. The next response with `ignored` corrects the client's memory, so this window is short.

A `KeyboardInterrupt` (or any other exception) raised while the client waits before a retry ends the call: no further attempt is made. This applies to all retries, including those after a `429`.

## Rate limiting - exponential backoff

This library supports [exponential backoff](https://en.wikipedia.org/wiki/Exponential_backoff).

When you send too many concurrent requests, the server returns an error `429 - Too Many Requests`. The client reacts to this by waiting for a while, and then retrying the request.
If the request still fails with an error `429`, it waits a little longer, and try again. By default this happens 5 times, before giving up (after approximately 15 seconds).

We throw a `RateLimitExceededException` (which is a subclass of `SeatsioException`) when exponential backoff eventually fails.

To change the maximum number of retries, create the `Client` as follows:

```python
import seatsio
client = seatsio.Client(seatsio.Region.EU(), secret_key="my-workspace-secret-key", max_retries=3)
```

Passing in 0 disables exponential backoff completely. In that case, the client will never retry a failed request, also not after a lost response (see [Automatic retries](#automatic-retries)).
