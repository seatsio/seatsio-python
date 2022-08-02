# seatsio-python, the official Seats.io Python client library

[![Build](https://github.com/seatsio/seatsio-python/workflows/Build/badge.svg)](https://github.com/seatsio/seatsio-python/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/seatsio.svg)](https://badge.fury.io/py/seatsio)

This is the official Python client library for the [Seats.io V2 REST API](https://docs.seats.io/docs/api-overview), supporting Python 3.7+. 

## Installing

```
pip install seatsio
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

This exception contains a message string describing what went wrong, and also two other properties:

- `Errors`: a list of errors (containing a code and a message) that the server returned. In most cases, this list will contain only one element.
- `RequestId`: the identifier of the request you made. Please mention this to us when you have questions, as it will make debugging easier.
- 
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

Passing in 0 disables exponential backoff completely. In that case, the client will never retry a failed request.
