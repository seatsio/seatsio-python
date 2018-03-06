import unirest

from seatsio.exceptions import SeatsioException


def get(url, secretKey):
    try:
        response = unirest.get(url, auth=(secretKey, ''))
        if response.code >= 400:
            raise SeatsioException("other field1", "requestId")
        else:
            return response
    except RuntimeError:
        raise SeatsioException("other field2", "requestId")
