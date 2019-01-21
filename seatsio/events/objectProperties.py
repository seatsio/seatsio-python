class ObjectProperties:
    def __init__(self, object_id, extra_data=None, ticket_type=None, quantity=None):
        if extra_data:
            self.extraData = extra_data
        self.objectId = object_id
        if ticket_type:
            self.ticketType = ticket_type
        if quantity:
            self.quantity = quantity
