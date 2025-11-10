class EditForSaleConfigRequest:
    def __init__(self, for_sale, not_for_sale):
        if for_sale:
            self.forSale = for_sale
        if not_for_sale:
            self.notForSale = not_for_sale
