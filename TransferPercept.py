class TransferPercept:

    def __init__(self, wumpus_environment):
        self.environment = wumpus_environment

    def get_bump(self):
        return self.environment.get_bump()

    def get_glitter(self):
        return self.environment.get_glitter()

    def get_breeze(self):
        return self.environment.get_breeze()

    def get_stench(self):
        return self.environment.get_stench()

    def get_scream(self):
        return self.environment.get_scream()