from datetime import datetime


# TODO make nice function for time formatting

class Chart:

    def __init__(self, data):
        self.id = data.get("id")
        self.key = data.get("key")
        self.status = data.get("status")
        self.name = data.get("name")
        self.publishedVersionThumbnailUrl = data.get("publishedVersionThumbnailUrl")
        self.draftVersionThumbnailUrl = data.get("draftVersionThumbnailUrl")
        self.events = Event.create_list(data.get("events"))
        self.tags = data.get("tags")
        self.archived = data.get("archived")


class Event:
    def __init__(self, data):
        self.id = data.get("id")
        self.key = data.get("key")
        self.chartKey = data.get("chartKey")
        self.bookWholeTables = data.get("bookWholeTables")
        self.forSaleConfig = ForSaleConfig.create(data.get("forSaleConfig"))
        self.createdOn = datetime.strptime(data.get("createdOn"), "%Y-%m-%dT%H:%M:%S.%fZ")
        updated_on = data.get("updatedOn")
        if updated_on:
            self.updatedOn = datetime.strptime(updated_on, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            self.updatedOn = None

    @classmethod
    def create_list(cls, lst):
        if lst:
            result = []
            for e in lst:
                result.append(Event(e))
            return result
        else:
            return None


class ForSaleConfig:
    def __init__(self, data):
        self.for_sale = data.get("forSale")
        self.objects = data.get("objects")
        self.categories = data.get("categories")

    @classmethod
    def create(cls, param):
        if param is not None:
            return ForSaleConfig(param)


class EventReport:
    def __init__(self, response_body):
        self.items = {}
        for key, value in response_body.iteritems():
            self.items[key] = []
            for item in value:
                self.items[key].append(EventReportItem(item))

    def get(self, key):
        return self.items.get(key)


class EventReportItem:
    def __init__(self, item_data):
        self.status = item_data.get("status")
        self.label = item_data.get("label")
        self.category_label = item_data.get("categoryLabel")
        self.category_key = item_data.get("categoryKey")
        self.ticket_type = item_data.get("ticketType")
        self.order_id = item_data.get("orderId")
        self.for_sale = item_data.get("forSale")
        self.section = item_data.get("section")
        self.entrance = item_data.get("entrance")
        self.num_booked = item_data.get("numBooked")
        self.capacity = item_data.get("capacity")


class Subaccount:

    def __init__(self, data):
        self.id = data.get("id")
        self.secretKey = data.get("secretKey")
        self.designerKey = data.get("designerKey")
        self.publicKey = data.get("publicKey")
        self.name = data.get("name")
        self.active = data.get("active")


class HoldToken:

    def __init__(self, data):
        self.hold_token = data.get("holdToken")
        self.expires_at = datetime.strptime(data.get("expiresAt"), "%Y-%m-%dT%H:%M:%S.%fZ")


class ObjectStatus:
    FREE = "free"
    BOOKED = "booked"
    HELD = "reservedByToken"

    def __init__(self, data):
        self.status = data.get("status")
        self.hold_token = data.get("holdToken")
        self.order_id = data.get("orderId")
        self.ticket_type = data.get("ticketType")
        self.quantity = data.get("quantity")
        self.extra_data = data.get("extraData")


class StatusChange:
    def __init__(self, data):
        self.id = data.get("id")
        self.status = data.get("status")
        self.date = datetime.strptime(data.get("date"), "%Y-%m-%dT%H:%M:%S.%fZ")
        self.objectLabel = data.get("objectLabel")
        self.eventId = data.get("eventId")
        self.extraData = data.get("extraData")


class ObjectProperties:
    def __init__(self, object_id, extra_data=None, ticket_type=None, quantity=None):
        if extra_data:
            self.extraData = extra_data
        self.objectId = object_id
        if ticket_type:
            self.ticketType = ticket_type
        if quantity:
            self.quantity = quantity


class BestAvailableObjects:
    def __init__(self, data):
        self.next_to_each_other = data.get("nextToEachOther")
        self.objects = data.get("objects")
