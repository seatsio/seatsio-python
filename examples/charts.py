import seatsio

# create a seats.io client
client = seatsio.Client(secret_key="my-secret-key")

# create a chart
chart = client.charts.create()

# find my charts
all_my_charts = client.charts.list()
charts_with_name = client.charts.list(chart_filter="Theatre")
tagged_charts = client.charts.list(tag="WestEnd")
charts_with_events = client.charts.list(expand_events=True)

# retrieve a single chart
a_single_chart = client.charts.retrieve("chart_key")
