


class BaseController:

    def __init__(self, panel):

        self.panel = panel

    def initialize(self):
        pass

    def handle_event(self, event):
        pass

    def set_state(self, state):
        pass