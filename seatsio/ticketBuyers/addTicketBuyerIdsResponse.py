from uuid import UUID


class AddTicketBuyerIdsResponse:

    def __init__(self, data):
        self.added = [UUID(uuid) for uuid in data.get("added", [])]
        self.already_present = [UUID(uuid) for uuid in data.get("alreadyPresent", [])]
