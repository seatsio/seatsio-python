class ForSaleRequest:
    def __init__(self, objects, categories):
        if objects:
            self.objects = objects
        if categories:
            self.categories = categories
