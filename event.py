import random


# event class, allowing for flexibility around making random or scripted events
#TODO : conditional events and event chains
#TODO : event probability even with single rooms
class Event():
    def __init__(self, name, text, sanity_level, picture, sound, actions, chance, location, isUnique):
        self.name = name
        self.text = text
        self.actions = actions
        self.sound = sound
        self.chance = chance
        self.picture = picture
        self.isUnique = isUnique
        self.location = location
        self.sanity_level = (int(sanity_level[0]), int(sanity_level[1]))
        self.buttons = []

        self.active = True

    # check if event can be triggered
    def trigger(self, game):
        if not self.active :
            return False
        if self.sanity_level[0] > game.sanity or self.sanity_level[1] < game.sanity :
            return False
        if self.location != "0" and self.location != game.current_room.name :
            return False

        chance = random.randint(0, 100)

        if self.location == "0" and self.chance > chance:
            if self.isUnique :
                self.active = False
            return True

        if self.location != "0" and self.chance > chance and self.location == game.current_room.name:
            if self.isUnique :
                self.active = False

        if self.location != "0" and self.location == game.current_room.name:
            if self.isUnique:
                self.active = False
            return True


    def execute(self):
        pass
