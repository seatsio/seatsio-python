from six import iteritems

from seatsio.util import parse_date


class Chart:

    def __init__(self, data):
        self.id = data.get("id")
        self.key = data.get("key")
        self.status = data.get("status")
        self.name = data.get("name")
        self.published_version_thumbnail_url = data.get("publishedVersionThumbnailUrl")
        self.draft_version_thumbnail_url = data.get("draftVersionThumbnailUrl")
        self.events = Event.create_list(data.get("events"))
        self.tags = data.get("tags")
        self.archived = data.get("archived")


class Event:
    def __init__(self, data):
        self.id = data.get("id")
        self.key = data.get("key")
        self.chart_key = data.get("chartKey")
        self.book_whole_tables = data.get("bookWholeTables")
        self.supports_best_available = data.get("supportsBestAvailable")
        self.for_sale_config = ForSaleConfig.create(data.get("forSaleConfig"))
        self.created_on = parse_date(data.get("createdOn"))
        self.updated_on = parse_date(data.get("updatedOn"))

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


class ChartReport:
    def __init__(self, response_body):
        self.items = {}
        for key, value in iteritems(response_body):
            self.items[key] = []
            for item in value:
                self.items[key].append(ChartReportItem(item))

    def get(self, key):
        return self.items.get(key)


class ChartReportItem:
    def __init__(self, item_data):
        self.label = item_data.get("label")
        self.labels = item_data.get("labels")
        self.category_label = item_data.get("categoryLabel")
        self.category_key = item_data.get("categoryKey")
        self.section = item_data.get("section")
        self.entrance = item_data.get("entrance")
        self.capacity = item_data.get("capacity")
        self.object_type = item_data.get("objectType")


class EventReport:
    def __init__(self, response_body):
        self.items = {}
        for key, value in iteritems(response_body):
            self.items[key] = []
            for item in value:
                self.items[key].append(EventReportItem(item))

    def get(self, key):
        return self.items.get(key)


class EventReportItem:
    def __init__(self, item_data):
        self.status = item_data.get("status")
        self.label = item_data.get("label")
        self.labels = item_data.get("labels")
        self.category_label = item_data.get("categoryLabel")
        self.category_key = item_data.get("categoryKey")
        self.ticket_type = item_data.get("ticketType")
        self.order_id = item_data.get("orderId")
        self.for_sale = item_data.get("forSale")
        self.hold_token = item_data.get("holdToken")
        self.section = item_data.get("section")
        self.entrance = item_data.get("entrance")
        self.num_booked = item_data.get("numBooked")
        self.capacity = item_data.get("capacity")
        self.object_type = item_data.get("objectType")
        self.extra_data = item_data.get("extraData")


class Account:
    def __init__(self, data):
        self.secret_key = data.get("secretKey")
        self.designer_key = data.get("designerKey")
        self.public_key = data.get("publicKey")
        self.email = data.get("email")
        self.settings = AccountSettings.create(data.get("settings"))


class AccountSettings:
    def __init__(self, data):
        self.draftChartDrawingsEnabled = data.get("draftChartDrawingsEnabled")
        self.chartValidation = ChartValidationSettings.create(data.get("chartValidation"))

    @classmethod
    def create(cls, param):
        if param is not None:
            return AccountSettings(param)


class ChartValidationSettings:
    def __init__(self, data):
        self.validateDuplicateLabels = data.get("VALIDATE_DUPLICATE_LABELS")
        self.validateObjectsWithoutCategories = data.get("VALIDATE_OBJECTS_WITHOUT_CATEGORIES")
        self.validateUnlabeledObjects = data.get("VALIDATE_UNLABELED_OBJECTS")

    @classmethod
    def create(cls, param):
        if param is not None:
            return ChartValidationSettings(param)


class Subaccount:

    def __init__(self, data):
        self.id = data.get("id")
        self.secret_key = data.get("secretKey")
        self.designer_key = data.get("designerKey")
        self.public_key = data.get("publicKey")
        self.name = data.get("name")
        self.email = data.get("email")
        self.active = data.get("active")


class HoldToken:

    def __init__(self, data):
        self.hold_token = data.get("holdToken")
        self.expires_at = parse_date(data.get("expiresAt"))
        self.expires_in_seconds = data.get("expiresInSeconds")


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
        self.date = parse_date(data.get("date"))
        self.object_label = data.get("objectLabel")
        self.event_id = data.get("eventId")
        self.extra_data = data.get("extraData")


class BestAvailableObjects:
    def __init__(self, data):
        self.next_to_each_other = data.get("nextToEachOther")
        self.objects = data.get("objects")
        self.labels = data.get("labels")


class ChangeObjectStatusResult:
    def __init__(self, data):
        self.labels = data.get("labels")
