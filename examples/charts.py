import seatsio

# create a seats.io client
client = seatsio.Client(secret_key = "my-secret-key")

# create a chart
chart = client.charts.create()

# find all my charts
my_charts = client.charts.list().retrieve()

# retrieve a single chart
a_single_chart = client.charts.retrieve("chart_key")