class EventRequest:
    def __init__(self, chart_key, event_key=None, book_whole_tables=None):
        if chart_key:
            self.chartKey = chart_key
        if event_key:
            self.eventKey = event_key
        if book_whole_tables is not None:
            self.bookWholeTables = book_whole_tables
