class CreateSingleEventRequest:
    def __init__(self, chart_key, event_key=None, book_whole_tables=None, table_booking_modes=None):
        if chart_key:
            self.chartKey = chart_key
        if event_key:
            self.eventKey = event_key
        if book_whole_tables is not None:
            self.bookWholeTables = book_whole_tables
        if table_booking_modes is not None:
            self.tableBookingModes = table_booking_modes