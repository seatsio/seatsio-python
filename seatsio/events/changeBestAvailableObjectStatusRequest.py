class ChangeBestAvailableObjectStatusRequest:
    def __init__(self, number, categories, extra_data, status, hold_token, order_id):
        best_available = {"number": number}
        if categories:
            best_available["categories"] = categories
        if extra_data:
            best_available["extraData"] = extra_data
        self.bestAvailable = best_available
        self.status = status
        if hold_token:
            self.holdToken = hold_token
        if order_id:
            self.orderId = order_id
