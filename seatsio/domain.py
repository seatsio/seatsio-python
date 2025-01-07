from datetime import date

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
        self.validation = data.get("validation")
        self.venue_type = data.get("venueType")
        self.zones = Zone.create_list(data.get("zones"))


class Zone:

    def __init__(self, data):
        self.key = data.get("key")
        self.label = data.get("label")

    def __eq__(self, other):
        return self.key == other.key and \
            self.label == other.label

    @classmethod
    def create_list(cls, lst):
        if lst is not None:
            return list(map(Zone, lst))


class ChartValidation:

    def __init__(self, data):
        self.errors = data.get("errors")
        self.warnings = data.get("warnings")


class Category:

    def __init__(self, key, label, color, accessible=False):
        self.key = key
        self.label = label
        self.color = color
        self.accessible = accessible

    def __eq__(self, other):
        return self.key == other.key and \
            self.label == other.label and \
            self.color == other.color and \
            self.accessible == other.accessible

    def __hash__(self):
        return hash((self.key, self.label, self.color, self.accessible))

    @classmethod
    def create(cls, data):
        return Category(data.get("key"), data.get("label"), data.get("color"), data.get("accessible"))

    @classmethod
    def create_list(cls, lst):
        if lst is not None:
            return list(map(Category.create, lst))


class Event:
    def __init__(self, data):
        self.id = data.get("id")
        self.key = data.get("key")
        self.name = data.get("name")
        self.date = None if data.get("date") is None else date.fromisoformat(data.get("date"))
        self.chart_key = data.get("chartKey")
        self.table_booking_config = TableBookingConfig.create(data.get("tableBookingConfig"))
        self.supports_best_available = data.get("supportsBestAvailable")
        self.for_sale_config = ForSaleConfig.create(data.get("forSaleConfig"))
        self.created_on = parse_date(data.get("createdOn"))
        self.updated_on = parse_date(data.get("updatedOn"))
        self.channels = Channel.createList(data.get("channels"))
        self.is_top_level_season = data.get("isTopLevelSeason")
        self.is_partial_season = data.get("isPartialSeason")
        self.is_event_in_season = data.get("isEventInSeason")
        self.top_level_season_key = data.get("topLevelSeasonKey")
        self.object_categories = data.get("objectCategories")
        self.categories = Category.create_list(data.get("categories"))
        self.is_in_the_past = data.get("isInThePast")
        self.partial_season_keys_for_event = data.get("partialSeasonKeysForEvent")

    @classmethod
    def create_list(cls, lst):
        if lst is None:
            return None
        else:
            result = []
            for e in lst:
                result.append(event_from_json(e))
            return result

    def is_season(self):
        return False


class Season(Event):
    def __init__(self, data):
        Event.__init__(self, data)
        self.partial_season_keys = data.get("partialSeasonKeys")
        self.events = Event.create_list(data.get("events"))

    def is_season(self):
        return True


def event_from_json(json):
    if json.get("isSeason"):
        return Season(json)
    else:
        return Event(json)


class ForSaleConfig:
    def __init__(self, data):
        self.for_sale = data.get("forSale")
        self.objects = data.get("objects")
        self.area_places = data.get("areaPlaces")
        self.categories = data.get("categories")

    def __eq__(self, other):
        return self.for_sale == other.for_sale and \
            self.objects == other.objects and \
            self.area_places == other.area_places and \
            self.categories == other.categories

    def __hash__(self):
        return hash((self.for_sale, self.objects, self.area_places, self.categories))

    @classmethod
    def create(cls, param):
        if param is not None:
            return ForSaleConfig(param)

    def to_json(self):
        json = {"forSale": self.for_sale}
        if self.objects is not None:
            json["objects"] = self.objects
        if self.area_places is not None:
            json["areaPlaces"] = self.area_places
        if self.categories is not None:
            json["categories"] = self.categories
        return json

    @classmethod
    def create_new(cls, for_sale, objects=None, area_places=None, categories=None):
        return ForSaleConfig({"forSale": for_sale, "objects": objects, "areaPlaces": area_places, "categories": categories})


class TableBookingConfig:
    def __init__(self, mode, tables=None):
        self.mode = mode
        self.tables = tables

    def __eq__(self, other):
        return self.mode == other.mode and \
            self.tables == other.tables

    def __hash__(self):
        return hash((self.mode, self.tables))

    def to_json(self):
        json = {"mode": self.mode}
        if self.tables is not None:
            json["tables"] = self.tables
        return json

    @classmethod
    def inherit(cls):
        return TableBookingConfig('INHERIT')

    @classmethod
    def all_by_table(cls):
        return TableBookingConfig('ALL_BY_TABLE')

    @classmethod
    def all_by_seat(cls):
        return TableBookingConfig('ALL_BY_SEAT')

    @classmethod
    def custom(cls, tables):
        return TableBookingConfig('CUSTOM', tables)

    @classmethod
    def create(cls, data):
        return TableBookingConfig(data.get("mode"), data.get("tables"))


class Channel:
    def __init__(self, name, color, index, key=None, objects=None):
        self.key = key
        self.name = name
        self.color = color
        self.index = index
        self.objects = objects

    def __eq__(self, other):
        return self.key == other.key and \
            self.name == other.name and \
            self.color == other.color and \
            self.index == other.index and \
            self.objects == other.objects

    def __hash__(self):
        return hash((self.key, self.name, self.color, self.index, self.objects))

    @classmethod
    def create(cls, param):
        if param is not None:
            return Channel(param.get('name'), param.get('color'), param.get('index'), param.get('key'), param.get('objects'))

    @classmethod
    def createList(cls, param):
        if param is not None:
            return list(map(Channel.create, param))


class ChartReport:
    def __init__(self, response_body):
        self.items = {}
        for key, value in response_body.items():
            self.items[key] = []
            for item in value:
                self.items[key].append(ChartObjectInfo(item))

    def get(self, key):
        return self.items.get(key)


class ChartObjectInfo:
    def __init__(self, item_data):
        self.label = item_data.get("label")
        self.labels = item_data.get("labels")
        self.ids = item_data.get("ids")
        self.category_label = item_data.get("categoryLabel")
        self.category_key = item_data.get("categoryKey")
        self.section = item_data.get("section")
        self.entrance = item_data.get("entrance")
        self.capacity = item_data.get("capacity")
        self.book_as_a_whole = item_data.get("bookAsAWhole")
        self.object_type = item_data.get("objectType")
        self.left_neighbour = item_data.get('leftNeighbour')
        self.right_neighbour = item_data.get('rightNeighbour')
        self.distance_to_focal_point = item_data.get('distanceToFocalPoint')
        self.num_seats = item_data.get('numSeats')
        self.is_accessible = item_data.get("isAccessible")
        self.is_companion_seat = item_data.get("isCompanionSeat")
        self.has_restricted_view = item_data.get("hasRestrictedView")
        self.zone = item_data.get("zone")
        self.floor = item_data.get("floor")



class EventReport:
    def __init__(self, response_body):
        self.items = {}
        for key, value in response_body.items():
            self.items[key] = []
            for item in value:
                self.items[key].append(EventObjectInfo(item))

    def get(self, key):
        return self.items.get(key)


class EventObjectInfo:
    FREE = "free"
    BOOKED = "booked"
    HELD = "reservedByToken"
    RESALE = "resale"

    def __init__(self, item_data):
        self.status = item_data.get("status")
        self.label = item_data.get("label")
        self.labels = item_data.get("labels")
        self.ids = item_data.get("ids")
        self.category_label = item_data.get("categoryLabel")
        self.category_key = item_data.get("categoryKey")
        self.ticket_type = item_data.get("ticketType")
        self.order_id = item_data.get("orderId")
        self.for_sale = item_data.get("forSale")
        self.hold_token = item_data.get("holdToken")
        self.section = item_data.get("section")
        self.entrance = item_data.get("entrance")
        self.num_booked = item_data.get("numBooked")
        self.num_free = item_data.get("numFree")
        self.num_held = item_data.get("numHeld")
        self.capacity = item_data.get("capacity")
        self.book_as_a_whole = item_data.get("bookAsAWhole")
        self.object_type = item_data.get("objectType")
        self.extra_data = item_data.get("extraData")
        self.is_accessible = item_data.get("isAccessible")
        self.is_companion_seat = item_data.get("isCompanionSeat")
        self.has_restricted_view = item_data.get("hasRestrictedView")
        self.displayed_object_type = item_data.get("displayedObjectType")
        self.left_neighbour = item_data.get('leftNeighbour')
        self.right_neighbour = item_data.get('rightNeighbour')
        self.is_available = item_data.get('isAvailable')
        self.channel = item_data.get('channel')
        self.distance_to_focal_point = item_data.get('distanceToFocalPoint')
        self.holds = item_data.get('holds')
        self.num_seats = item_data.get('numSeats')
        self.variable_occupancy = item_data.get('variableOccupancy')
        self.min_occupancy = item_data.get('minOccupancy')
        self.max_occupancy = item_data.get('maxOccupancy')
        self.season_status_overridden_quantity = item_data.get('seasonStatusOverriddenQuantity')
        self.num_not_for_sale = item_data.get('numNotForSale')
        self.zone = item_data.get('zone')
        self.floor = item_data.get('floor')


class UsageSummaryForAllMonths:
    def __init__(self, json):
        self.usage = list(map(lambda x: UsageSummaryForMonth(x), json.get("usage")))
        self.usage_cutoff_date = parse_date(json.get("usageCutoffDate"))


class UsageSummaryForMonth(object):
    def __init__(self, json):
        self.month = Month.from_json(json.get("month"))
        self.numUsedObjects = json.get("numUsedObjects")


class Month(object):
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def serialize(self):
        return str(self.year) + '-' + str(self.month).rjust(2, '0')

    @classmethod
    def from_json(cls, json):
        return Month(json.get("year"), json.get("month"))


class UsageDetailsForMonth:
    @classmethod
    def from_json(cls, json):
        return list(map(lambda x: UsageDetails(x), json))


class UsageDetails:
    def __init__(self, json):
        self.workspace = json.get("workspace")
        self.usage_by_chart = list(map(lambda x: UsageByChart(x), json.get("usageByChart")))


class UsageByChart:
    def __init__(self, json):
        if json.get("chart") is not None:
            self.chart = UsageChart(json.get("chart"))
        self.usage_by_event = list(map(lambda x: UsageByEvent(x), json.get("usageByEvent")))


class UsageChart:
    def __init__(self, json):
        self.name = json.get("name")
        self.key = json.get("key")


class UsageByEvent:
    def __init__(self, json):
        self.event = UsageEvent(json.get("event"))
        self.num_used_objects = json.get("numUsedObjects")


class UsageEvent:
    def __init__(self, json):
        self.id = json.get("id")
        self.key = json.get("key")


class UsageDetailsForEventInMonth:
    @classmethod
    def from_json(cls, json):
        if len(json) == 0 or "usageByReason" not in json[0]:
            return list(map(lambda x: UsageForObjectV1(x), json))
        else:
            return list(map(lambda x: UsageForObjectV2(x), json))


class UsageForObjectV1:
    def __init__(self, json):
        self.object = json.get("object")
        self.num_first_bookings = json.get("numFirstBookings")
        self.first_booking_date = parse_date(json.get("firstBookingDate"))
        self.num_first_selections = json.get("numFirstSelections")
        self.num_first_bookings_or_selections = json.get("numFirstBookingsOrSelections")


class UsageForObjectV2:
    def __init__(self, json):
        self.object = json.get("object")
        self.num_usedObjects = json.get("numUsedObjects")
        self.usage_by_reason = json.get("usageByReason")


class Workspace:

    def __init__(self, data):
        self.id = data.get("id")
        self.name = data.get("name")
        self.key = data.get("key")
        self.secret_key = data.get("secretKey")
        self.is_test = data.get("isTest")
        self.is_active = data.get("isActive")
        self.is_default = data.get("isDefault")

    @classmethod
    def create(cls, param):
        if param is not None:
            return Workspace(param)


class EventLogItem:

    def __init__(self, data):
        self.id = data.get("id")
        self.type = data.get("type")
        self.timestamp = parse_date(data.get("timestamp"))
        self.data = data.get("data")

    @classmethod
    def create(cls, param):
        if param is not None:
            return EventLogItem(param)


class HoldToken:

    def __init__(self, data):
        self.hold_token = data.get("holdToken")
        self.expires_at = parse_date(data.get("expiresAt"))
        self.expires_in_seconds = data.get("expiresInSeconds")
        self.workspace_key = data.get("workspaceKey")


class StatusChange:
    def __init__(self, data):
        self.id = data.get("id")
        self.status = data.get("status")
        self.date = parse_date(data.get("date"))
        self.object_label = data.get("objectLabel")
        self.event_id = data.get("eventId")
        self.extra_data = data.get("extraData")
        self.origin = StatusChangeOrigin(data['origin'])
        self.is_present_on_chart = data.get("isPresentOnChart")
        self.not_present_on_chart_reason = data.get("notPresentOnChartReason")
        self.hold_token = data.get("holdToken")


class StatusChangeOrigin:
    def __init__(self, data):
        self.type = data.get("type")
        self.ip = data.get("ip")


class BestAvailableObjects:
    def __init__(self, data):
        self.next_to_each_other = data.get("nextToEachOther")
        self.objects = data.get("objects")
        self.objectDetails = {}
        for key, value in data.get("objectDetails").items():
            self.objectDetails[key] = EventObjectInfo(value)


class ChangeObjectStatusResult:
    def __init__(self, data):
        self.objects = {}
        for key, value in data.get("objects").items():
            self.objects[key] = EventObjectInfo(value)
