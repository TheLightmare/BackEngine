class Room():
    def __init__(self, name, neightbours, text, actions, music, picture):
        self.name = name
        self.buttons = []
        self.text = text
        self.music = music
        self.picture = picture

        if neightbours == "0":
            self.neighbours = []
        else :
            self.neighbours = neightbours

        if actions == "0":
            self.actions = []
        else:
            self.actions = actions

