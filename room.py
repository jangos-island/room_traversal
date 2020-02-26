# Implement a class to hold room information.
class Room:
    def __init__(self, room):
        self.id = room["room_id"]
        self.title = room["title"]
        self.description = room["description"]
        self.coordinates = room["coordinates"]
        self.exits = room["exits"]
        self.elevation = room["elevation"]
        self.terrain = room["terrain"]

    def __str__(self):
        return f"\n{self.id} - {self.title}"

    def print_room_description(self):
        return f"\n{self.description}"

    def get_exits(self):
        return self.exits
    
    def get_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "coordinates": self.coordinates,
            "exits": self.exits,
            "elevation": self.elevation,
            "terrain": self.terrain
        }

