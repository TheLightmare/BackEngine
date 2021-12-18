import pygame as pg
from settings import *
import room
import button
import event

pg.init()


def load_events():
    events = []
    with open("events.txt") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 8):
            sanity_level = lines[i+2].strip().split(",")
            (picture, sound) = lines[i+3].strip().split(",")
            chance = lines[i+4].strip()
            (location, isUnique) = lines[i+5].strip().split(",")
            actions = lines[i+6].strip().split(",")
            if isUnique == "True":
                isUnique = True
            else:
                isUnique = False
            events.append(event.Event(lines[i].strip(), lines[i+1].strip(), sanity_level, picture,
                                      sound, actions, int(chance), location, isUnique))
    return events


def load_rooms():
    rooms = []
    with open("rooms.txt") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 5):
            roomtext = lines[i].strip().split(" ")
            roomtext.append(lines[i+1].strip())
            roomtext.append(lines[i+2].strip())
            roomtext.append(lines[i+3].strip())
            neighbours = roomtext[1].split(",")
            actions = roomtext[3].split(",")
            (music, picture) = roomtext[4].split(",")
            rooms.append(room.Room(roomtext[0], neighbours,
                                   roomtext[2], actions, music, picture))
    return rooms


def load_picture(name):
    try :
        picture = pg.image.load(IMAGE_FOLDER + name + ".png")
    except :
        picture = pg.image.load(IMAGE_FOLDER + "Backrooms.png")
    return picture


def print_text(screen, text, height, font, color):
    textsurface = font.render(text, False, color)
    textrect = textsurface.get_rect(center=(WIDTH / 2, height))
    screen.blit(textsurface, textrect)


class Game():
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        self.rooms = load_rooms()
        self.events = load_events()
        self.text_font = pg.font.Font(FONT_FOLDER + FONT_NAME, 30)
        self.title_font = pg.font.Font(FONT_FOLDER + FONT_NAME, 60)

        self.previous_room = self.rooms[0]
        self.current_room = self.rooms[1]
        pg.mixer.music.load(MUSIC_FOLDER + self.current_room.music + ".wav")
        pg.mixer.music.play(-1)

        self.isInEvent = False
        self.current_event = None
        self.sanity = 100

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE :
                    pg.quit()
            if not self.isInEvent :
                for button in self.current_room.buttons :
                    button.click(event)
            if self.isInEvent and self.current_event is not None :
                for button in self.current_event.buttons :
                    button.click(event)

    def load_room_actions(self):
        for i in range(len(self.current_room.actions)):
            action = self.current_room.actions[i]
            self.current_room.buttons.append(button.Button(self,
                                                           action,
                                                           action.replace("_", " "),
                                                           (WIDTH/3 - len(action)*6 + i*200, HEIGHT - 90),
                                                           self.text_font,
                                                           feedback= action))

    def load_event_actions(self, event):
        for i in range(len(event.actions)):
            action = event.actions[i]
            event.buttons.append(button.Button(self,
                                              action,
                                              action.replace("_", " "),
                                              (WIDTH/3 - len(action)*6 + i*200, HEIGHT - 90),
                                              self.text_font,
                                              feedback=action))

    def display_event(self, event):
        self.screen.fill(BLACK)
        name = event.name
        text = event.text
        picture = event.picture

        print_text(self.screen, name, 40, self.title_font, RED)
        print_text(self.screen, text, (3/4) * HEIGHT, self.text_font, WHITE)

        surface = load_picture(picture)
        width = surface.get_width()
        heigth = surface.get_height()

        pg.draw.rect(self.screen, RED, (WIDTH / 2 - width / 2 - 15, 115, width + 30, heigth + 30), 3)
        self.screen.blit(surface, (WIDTH / 2 - width / 2, 130))


    def display_room(self):
        self.screen.fill(BLACK)
        name = self.current_room.name
        text = self.current_room.text
        picture = self.current_room.picture

        print_text(self.screen, name, 40, self.title_font, WHITE)
        print_text(self.screen, text, (3/4) * HEIGHT, self.text_font, WHITE)

        surface = load_picture(picture)
        width = surface.get_width()
        heigth = surface.get_height()

        pg.draw.rect(self.screen, WHITE, (WIDTH/2 - width/2 - 15, 115, width + 30, heigth + 30), 3)
        self.screen.blit(surface, (WIDTH/2 - width/2, 130))

    def load_room(self, name, eventCheck):
        for room in self.rooms:
            if room.name == name :
                self.previous_room = self.current_room
                self.current_room = room

        # look if for possible events
        if not self.isInEvent and eventCheck:
            for event in self.events :
                if event.trigger(self):
                    self.isInEvent = True
                    self.current_event = event
                    self.display_event(event)
                    self.load_event_actions(event)
                    pg.mixer.music.load(SOUND_FOLDER + event.sound + ".wav")
                    pg.mixer.music.play(1)
                    return

        if self.previous_room.music != self.current_room.music :
            try :
                pg.mixer.music.load(MUSIC_FOLDER + self.current_room.music + ".wav")
            except :
                pg.mixer.music.load(MUSIC_FOLDER + "default.wav")
            pg.mixer.music.play(-1)

        self.display_room()
        self.load_room_actions()


    def do_action(self, action):
        if action == "go_left":
            self.load_room(self.current_room.neighbours[0], True)
        elif action == "go_forward":
            self.load_room(self.current_room.neighbours[1], True)
        elif action == "go_right":
            self.load_room(self.current_room.neighbours[2], True)
        elif action == "go_back":
            self.load_room(self.previous_room.name, True)

        if action == "continue" :
            self.isInEvent = False
            self.current_event = None
            self.load_room(self.current_room, False)


    def run(self):
        self.playing = True
        self.load_room(self.current_room.name, True)
        while self.playing :
            self.event_handler()
            if self.current_event is None and not self.isInEvent :
                for b in self.current_room.buttons :
                    b.show()
            if self.current_event is not None and self.isInEvent :
                for b in self.current_event.buttons :
                    b.show()
            pg.display.flip()

g = Game()
g.run()
