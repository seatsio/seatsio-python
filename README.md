# seatsio-python, the official Seats.io Python client library

[![Build Status](https://travis-ci.org/seatsio/seatsio-python.svg?branch=master)](https://travis-ci.org/seatsio/seatsio-python)

This is the official Python client library for the [Seats.io V2 REST API](https://docs.seats.io/docs/api-overview), supporting python 2.7, and python 3.3 - 3.7. 

## Installing

```
pip install seatsio
```

## Versioning

seatsio-python only uses major version numbers: v5, v6, v7 etc. Each release - backwards compatible or not - receives a new major version number.

The reason: we want to play safe and assume that each release _might_ break backwards compatibility.

## Examples

### Creating a chart and an event

```python
import seatsio
client = seatsio.Client(secret_key="my-secret-key") # can be found on https://app.seats.io/settings
chart = client.charts.create()
event = client.events.create(chart.key)
```

### Booking objects

```python
import seatsio
client = seatsio.Client(secret_key="my-secret-key")
client.events.book(event.key, ["A-1", "A-2"])
```

### Releasing objects

```python
import seatsio
client = seatsio.Client(secret_key="my-secret-key")
client.events.release(event.key, ["A-1", "A-2"])
```

### Booking objects that have been held

```python
import seatsio
client = seatsio.Client(secret_key="my-secret-key")
client.events.book(event.key, ["A-1", "A-2"], hold_token="a-hold-token")
```

### Changing object status

```python
import seatsio
client = seatsio.Client(secret_key="my-secret-key")
client.events.change_object_status("<EVENT KEY>", ["A-1", "A-2"], "my-custom-status")
```

### Listing all charts

```python
import seatsio
client = seatsio.Client(secret_key="my-secret-key")
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

## Error handling

When an API call results in a 4xx or 5xx error (e.g. when a chart could not be found), a SeatsioException is raised.

This exception contains a message string describing what went wrong, and also two other properties:

- `Errors`: a list of errors (containing a code and a message) that the server returned. In most cases, this list will contain only one element.
- `RequestId`: the identifier of the request you made. Please mention this to us when you have questions, as it will make debugging easier.
