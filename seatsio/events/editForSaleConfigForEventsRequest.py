class EditForSaleConfigForEventsRequest:
    def __init__(self, events):
        self.events = {}
        for key in events:
            self.events[key] = {}
            if events.get(key).get("for_sale"):
                self.events[key]["forSale"] = events[key]["for_sale"]
            if events.get(key).get("not_for_sale"):
                self.events[key]["notForSale"] = events[key]["not_for_sale"]