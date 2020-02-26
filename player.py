class Player:
    def __init__(self):
        self.current_room = None

    def play(self, initial_room):
        self.current_room = initial_room

    def travel(self, to_room):
        self.current_room = to_room
