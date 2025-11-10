class EditForSaleConfigForEventsRequest:
    def __init__(self, events):
        self.events = {}
        for key in events:
            event_config = events.get(key)
            event_dict = {}
            if event_config.get("for_sale"):
                event_dict["forSale"] = event_config["for_sale"]
            if event_config.get("not_for_sale"):
                event_dict["notForSale"] = event_config["not_for_sale"]
            if event_dict:
                self.events[key] = event_dict