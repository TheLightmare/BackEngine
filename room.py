
# this class only exists for clarity, no methods whatsoever
class Room():
    def __init__(self, name, neighbours, text, actions, music, picture):
        self.name = name
        self.buttons = []
        self.text = text
        self.music = music
        self.picture = picture

        if neighbours == "0":
            self.neighbours = []
        else :
            self.neighbours = neighbours

        if actions == "0":
            self.actions = []
        else:
            self.actions = actions

