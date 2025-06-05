from uuid import UUID

from seatsio.pagination.pageFetcher import PageFetcher
from seatsio.pagination.pagedIterator import PagedIterator
from seatsio.ticketBuyers.addTicketBuyerIdsResponse import AddTicketBuyerIdsResponse
from seatsio.ticketBuyers.removeTicketBuyerIdsResponse import RemoveTicketBuyerIdsResponse


class TicketBuyersClient:

    def __init__(self, http_client):
        self.http_client = http_client

    def add(self, ids):
        filtered_ids = [str(uuid) for uuid in ids if uuid is not None]
        response = self.http_client \
            .url("/ticket-buyers") \
            .post({"ids": filtered_ids})
        return AddTicketBuyerIdsResponse(response.json())

    def remove(self, ids):
        filtered_ids = [str(i) for i in ids if i is not None]
        response = self.http_client \
            .url("/ticket-buyers") \
            .delete({"ids": filtered_ids})
        return RemoveTicketBuyerIdsResponse(response.json())

    def list_all(self):
        return PagedIterator(PageFetcher(UUID, self.http_client, "/ticket-buyers"))
