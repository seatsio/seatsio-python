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
        self.validation = data.get("validation")
        self.social_distancing_rulesets = {k: SocialDistancingRuleset.create(v) for k, v in
                                           data.get("socialDistancingRulesets").items()}


class ChartValidation:

    def __init__(self, data):
        self.errors = data.get("errors")
        self.warnings = data.get("warnings")


class Category:

    def __init__(self, key, label, color, accessible = False):
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
        self.chart_key = data.get("chartKey")
        self.table_booking_config = TableBookingConfig.create(data.get("tableBookingConfig"))
        self.supports_best_available = data.get("supportsBestAvailable")
        self.for_sale_config = ForSaleConfig.create(data.get("forSaleConfig"))
        self.created_on = parse_date(data.get("createdOn"))
        self.updated_on = parse_date(data.get("updatedOn"))
        self.channels = Channel.createList(data.get("channels"))
        self.social_distancing_ruleset_key = data.get("socialDistancingRulesetKey")
        self.is_top_level_season = data.get("isTopLevelSeason")
        self.is_partial_season = data.get("isPartialSeason")
        self.is_event_in_season = data.get("isEventInSeason")
        self.top_level_season_key = data.get("topLevelSeasonKey")
        self.object_categories = data.get("objectCategories")
        self.categories = Category.create_list(data.get("categories"))

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

    @classmethod
    def create(cls, param):
        if param is not None:
            return ForSaleConfig(param)


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


class SocialDistancingRuleset:
    def __init__(self, name, number_of_disabled_seats_to_the_sides=0, disable_seats_in_front_and_behind=False,
                 disable_diagonal_seats_in_front_and_behind=False, number_of_disabled_aisle_seats=0, max_group_size=0,
                 max_occupancy_absolute=0,
                 max_occupancy_percentage=0, one_group_per_table=False, fixed_group_layout=False,
                 disabled_seats=[], enabled_seats=[], index=0):
        self.name = name
        self.number_of_disabled_seats_to_the_sides = number_of_disabled_seats_to_the_sides
        self.disable_seats_in_front_and_behind = disable_seats_in_front_and_behind
        self.disable_diagonal_seats_in_front_and_behind = disable_diagonal_seats_in_front_and_behind
        self.number_of_disabled_aisle_seats = number_of_disabled_aisle_seats
        self.max_group_size = max_group_size
        self.max_occupancy_absolute = max_occupancy_absolute
        self.max_occupancy_percentage = max_occupancy_percentage
        self.one_group_per_table = one_group_per_table
        self.fixed_group_layout = fixed_group_layout
        self.disabled_seats = disabled_seats
        self.enabled_seats = enabled_seats
        self.index = index

    @classmethod
    def fixed(cls, name, disabled_seats=[], index=0):
        return SocialDistancingRuleset(name, index=index, disabled_seats=disabled_seats)

    @classmethod
    def rule_based(cls, name, number_of_disabled_seats_to_the_sides=0, disable_seats_in_front_and_behind=False,
                   disable_diagonal_seats_in_front_and_behind=False, number_of_disabled_aisle_seats=0, max_group_size=0,
                   max_occupancy_absolute=0,
                   max_occupancy_percentage=0, one_group_per_table=False, disabled_seats=[], enabled_seats=[], index=0):
        return SocialDistancingRuleset(name,
                                       number_of_disabled_seats_to_the_sides=number_of_disabled_seats_to_the_sides,
                                       disable_seats_in_front_and_behind=disable_seats_in_front_and_behind,
                                       disable_diagonal_seats_in_front_and_behind=disable_diagonal_seats_in_front_and_behind,
                                       number_of_disabled_aisle_seats=number_of_disabled_aisle_seats,
                                       max_group_size=max_group_size,
                                       max_occupancy_absolute=max_occupancy_absolute,
                                       max_occupancy_percentage=max_occupancy_percentage,
                                       one_group_per_table=one_group_per_table,
                                       fixed_group_layout=False,
                                       disabled_seats=disabled_seats,
                                       enabled_seats=enabled_seats,
                                       index=index)

    def __eq__(self, other):
        return self.name == other.name and \
               self.number_of_disabled_seats_to_the_sides == other.number_of_disabled_seats_to_the_sides and \
               self.disable_seats_in_front_and_behind == other.disable_seats_in_front_and_behind and \
               self.disable_diagonal_seats_in_front_and_behind == other.disable_diagonal_seats_in_front_and_behind and \
               self.number_of_disabled_aisle_seats == other.number_of_disabled_aisle_seats and \
               self.max_group_size == other.max_group_size and \
               self.max_occupancy_absolute == other.max_occupancy_absolute and \
               self.max_occupancy_percentage == other.max_occupancy_percentage and \
               self.one_group_per_table == other.one_group_per_table and \
               self.fixed_group_layout == other.fixed_group_layout and \
               self.disabled_seats == other.disabled_seats and \
               self.enabled_seats == other.enabled_seats and \
               self.index == other.index

    def __hash__(self):
        return hash((self.name, self.number_of_disabled_seats_to_the_sides, self.disable_seats_in_front_and_behind,
                     self.disable_diagonal_seats_in_front_and_behind, self.number_of_disabled_aisle_seats,
                     self.max_group_size, self.max_occupancy_absolute, self.max_occupancy_percentage,
                     self.fixed_group_layout, self.one_group_per_table, self.disabled_seats, self.enabled_seats,
                     self.index))

    @classmethod
    def create(cls, param):
        if param is not None:
            return SocialDistancingRuleset(
                param.get('name'),
                param.get('numberOfDisabledSeatsToTheSides'),
                param.get('disableSeatsInFrontAndBehind'),
                param.get('disableDiagonalSeatsInFrontAndBehind'),
                param.get('numberOfDisabledAisleSeats'),
                param.get('maxGroupSize'),
                param.get('maxOccupancyAbsolute'),
                param.get('maxOccupancyPercentage'),
                param.get('oneGroupPerTable'),
                param.get('fixedGroupLayout'),
                param.get('disabledSeats'),
                param.get('enabledSeats'),
                param.get('index')
            )


class ChartReport:
    def __init__(self, response_body):
        self.items = {}
        for key, value in iteritems(response_body):
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


class EventReport:
    def __init__(self, response_body):
        self.items = {}
        for key, value in iteritems(response_body):
            self.items[key] = []
            for item in value:
                self.items[key].append(EventObjectInfo(item))

    def get(self, key):
        return self.items.get(key)


class EventObjectInfo:
    FREE = "free"
    BOOKED = "booked"
    HELD = "reservedByToken"

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
        self.is_disabled_by_social_distancing = item_data.get('isDisabledBySocialDistancing')
        self.channel = item_data.get('channel')
        self.distance_to_focal_point = item_data.get('distanceToFocalPoint')
        self.holds = item_data.get('holds')
        self.num_seats = item_data.get('numSeats')


class UsageSummaryForAllMonths:
    def __init__(self, json):
        self.items = list(map(lambda x: UsageSummaryForMonth(x), json))


class UsageSummaryForMonth(object):
    def __init__(self, json):
        self.month = Month.from_json(json.get("month"))
        self.numUsedObjects = json.get("numUsedObjects")
        self.numFirstBookings = json.get("numFirstBookings")
        self.numFirstBookingsByStatus = json.get("numFirstBookingsByStatus")
        self.numFirstBookingsOrSelections = json.get("numFirstBookingsOrSelections")


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
    def __init__(self, json):
        self.items = list(map(lambda x: UsageDetails(x), json))


class UsageDetails:
    def __init__(self, json):
        self.workspace = json.get("workspace")
        self.usage_by_chart = list(map(lambda x: UsageByChart(x), json.get("usageByChart")))


class UsageByChart:
    def __init__(self, json):
        if json.get("chart") is not None:
            self.chart = UsageChart(json.get("chart"))
        self.usageByEvent = list(map(lambda x: UsageByEvent(x), json.get("usageByEvent")))


class UsageChart:
    def __init__(self, json):
        self.name = json.get("name")
        self.key = json.get("key")


class UsageByEvent:
    def __init__(self, json):
        self.event = UsageEvent(json.get("event"))
        self.num_used_objects = json.get("numUsedObjects")
        self.num_first_bookings = json.get("numFirstBookings")
        self.num_object_selections = json.get("numObjectSelections")


class UsageEvent:
    def __init__(self, json):
        self.id = json.get("id")
        self.key = json.get("key")


class UsageDetailsForEventInMonth:
    def __init__(self, json):
        self.items = list(map(lambda x: UsageForObject(x), json))


class UsageForObject:
    def __init__(self, json):
        self.object = json.get("object")
        self.num_first_bookings = json.get("numFirstBookings")
        self.first_booking_date = parse_date(json.get("firstBookingDate"))
        self.num_first_selections = json.get("numFirstSelections")
        self.num_first_bookings_or_selections = json.get("numFirstBookingsOrSelections")


class Subaccount:

    def __init__(self, data):
        self.id = data.get("id")
        self.secret_key = data.get("secretKey")
        self.designer_key = data.get("designerKey")
        self.public_key = data.get("publicKey")
        self.name = data.get("name")
        self.active = data.get("active")


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
        for key, value in iteritems(data.get("objectDetails")):
            self.objectDetails[key] = EventObjectInfo(value)


class ChangeObjectStatusResult:
    def __init__(self, data):
        self.objects = {}
        for key, value in iteritems(data.get("objects")):
            self.objects[key] = EventObjectInfo(value)
