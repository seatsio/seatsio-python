class CreateWorkspaceRequest:
    def __init__(self, name, is_test=None):
        self.name = name
        if is_test is not None:
            self.isTest = is_test
