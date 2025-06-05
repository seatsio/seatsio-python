from uuid import UUID


class RemoveTicketBuyerIdsResponse:

    def __init__(self, data):
        self.removed = [UUID(uuid) for uuid in data.get("removed", [])]
        self.not_present = [UUID(uuid) for uuid in data.get("notPresent", [])]
