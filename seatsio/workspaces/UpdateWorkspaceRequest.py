class UpdateWorkspaceRequest:
    def __init__(self, name, for_sale_mode=None):
        self.name = name
        if for_sale_mode is not None:
            self.forSaleMode = for_sale_mode
