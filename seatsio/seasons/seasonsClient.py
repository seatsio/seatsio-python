from seatsio.domain import Season, Event
from seatsio.seasons.updateSeasonRequest import UpdateSeasonRequest


class SeasonsClient:

    def __init__(self, http_client, seatsio_client):
        self.http_client = http_client
        self.seatsio_client = seatsio_client

    def create(self, chart_key, key=None, name=None, number_of_events=None, event_keys=None, table_booking_config=None,
               object_categories=None, categories=None, channels=None, for_sale_config=None, for_sale_propagated=None):
        request = {}
        if chart_key:
            request['chartKey'] = chart_key
        if key:
            request['key'] = key
        if name:
            request['name'] = name
        if number_of_events:
            request['numberOfEvents'] = number_of_events
        if event_keys:
            request['eventKeys'] = event_keys
        if table_booking_config is not None:
            request['tableBookingConfig'] = table_booking_config.to_json()
        if object_categories is not None:
            request["objectCategories"] = object_categories
        if categories is not None:
            request["categories"] = categories
        if channels is not None:
            request['channels'] = channels
        if for_sale_config is not None:
            request['forSaleConfig'] = for_sale_config.to_json()
        if for_sale_propagated is not None:
            request['forSalePropagated'] = for_sale_propagated

        response = self.http_client.url("/seasons").post(request)
        return Season(response.json())

    def update(self, key, event_key=None, name=None, table_booking_config=None, object_categories=None,
               categories=None, for_sale_propagated=None):
        request = UpdateSeasonRequest(event_key, name, table_booking_config, object_categories, categories, for_sale_propagated)
        self.http_client.url("/events/{key}", key=key).post(request)

    def create_partial_season(self, top_level_season_key, partial_season_key=None, name=None, event_keys=None):
        request = {}
        if partial_season_key:
            request['key'] = partial_season_key
        if name:
            request['name'] = name
        if event_keys:
            request['eventKeys'] = event_keys

        response = self.http_client.url("/seasons/{top_level_season_key}/partial-seasons",
                                        top_level_season_key=top_level_season_key).post(request)
        return Season(response.json())

    def retrieve(self, key):
        return self.seatsio_client.events.retrieve(key)

    def create_events(self, key, event_keys=None, number_of_events=None):
        request = {}
        if event_keys:
            request['eventKeys'] = event_keys
        if number_of_events:
            request['numberOfEvents'] = number_of_events
        response = self.http_client.url("/seasons/{key}/actions/create-events", key=key).post(request)
        return Event.create_list(response.json().get('events'))

    def add_events_to_partial_season(self, top_level_season_key, partial_season_key, event_keys):
        request = {'eventKeys': event_keys}

        response = self.http_client.url(
            "/seasons/{top_level_season_key}/partial-seasons/{partial_season_key}/actions/add-events",
            top_level_season_key=top_level_season_key, partial_season_key=partial_season_key).post(request)
        return Season(response.json())

    def remove_event_from_partial_season(self, top_level_season_key, partial_season_key, event_key):
        response = self.http_client.url(
            "/seasons/{top_level_season_key}/partial-seasons/{partial_season_key}/events/{event_key}",
            top_level_season_key=top_level_season_key, partial_season_key=partial_season_key,
            event_key=event_key).delete()
        return Season(response.json())
