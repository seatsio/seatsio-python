class CreateWorkspaceRequest:
    def __init__(self, name, is_test=None, for_sale_mode=None):
        self.name = name
        if is_test is not None:
            self.isTest = is_test
        if for_sale_mode is not None:
            self.forSaleMode = for_sale_mode
