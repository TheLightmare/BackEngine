import time
import pypresence

import pygame as pg

import PointClick
from settings import *
import button
import utils

pg.init()

#Discord Rich Presence. Yes that's useless but hey, 4 lines of code !
#TODO : make RPC moddable
RPC = pypresence.Presence(CLIENT_ID)
RPC.connect()
duration = time.time()
RPC.update(state="Level 0", details="Lost in the Backrooms", large_image="backrooms", start=duration)


#TODO : add point-and-click mechanic (ffs that will be hurtful to make...)
class Game():
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("BackEngine")

        self.rooms = utils.load_rooms()
        self.events = utils.load_events()
        self.actions = utils.load_actions()
        self.text_font = pg.font.Font(FONT_FOLDER + FONT_NAME, 30)
        self.title_font = pg.font.Font(FONT_FOLDER + FONT_NAME, 60)

        self.previous_room = self.rooms[0]
        self.current_room = utils.load_save(self.rooms)
        pg.mixer.music.load(MUSIC_FOLDER + self.current_room.music + ".wav")
        pg.mixer.music.play(-1)

        self.isInEvent = False
        self.current_event = None
        self.sanity = 100

    # player death management
    def death(self):
        time.sleep(5)
        pg.mixer.music.stop()
        self.screen.fill(BLACK)

        utils.print_text(self.screen, "death won't save you.", HEIGHT/2, self.title_font, RED)
        pg.display.flip()
        time.sleep(5)

        self.load_room("Backrooms", False)
        self.sanity = 100

    # parse and execute custom actions (loaded from actions.txt file)
    def do_custom_action(self, action):
        for act in self.actions:
            if act[0] == action:
                utils.print_text(self.screen, act[1], (3 / 4) * HEIGHT, self.text_font, WHITE)
                if act[2] == "DEATH":
                    self.sanity = 0
                pg.display.flip()


    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                utils.save_game(self.current_room)
                self.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE :
                    utils.save_game(self.current_room)
                    self.playing = False
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

        utils.print_text(self.screen, name, 40, self.title_font, RED)
        utils.print_text(self.screen, text, (3/4) * HEIGHT, self.text_font, WHITE)

        surface = utils.load_picture(picture)
        width = surface.get_width()
        heigth = surface.get_height()

        pg.draw.rect(self.screen, RED, (WIDTH / 2 - width / 2 - 15, 115, width + 30, heigth + 30), 3)
        self.screen.blit(surface, (WIDTH / 2 - width / 2, 130))


    def display_room(self):
        self.screen.fill(BLACK)
        name = self.current_room.name
        text = self.current_room.text
        picture = self.current_room.picture

        utils.print_text(self.screen, name, 40, self.title_font, WHITE)
        utils.print_text(self.screen, text, (3/4) * HEIGHT, self.text_font, WHITE)

        surface = utils.load_picture(picture)
        width = surface.get_width()
        heigth = surface.get_height()

        pg.draw.rect(self.screen, WHITE, (WIDTH/2 - width/2 - 15, 115, width + 30, heigth + 30), 3)
        self.screen.blit(surface, (WIDTH/2 - width/2, 130))

    def load_room(self, name, eventCheck):
        for room in self.rooms:
            if room.name == name :
                self.previous_room = self.current_room
                self.current_room = room

        # update discord Rich Presence status
        utils.update_rpc(RPC, self.current_room, duration)

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

        # music switcher ! if the room has same music as previous one, it justs continues ! magic !
        if self.previous_room.music != self.current_room.music :
            try :
                pg.mixer.music.load(MUSIC_FOLDER + self.current_room.music + ".wav")
            except :
                pg.mixer.music.load(MUSIC_FOLDER + "default.wav")
            pg.mixer.music.play(-1)

        self.display_room()
        self.load_room_actions()


    def do_action(self, action):
        # possible actions inside of rooms
        if action == "go_left":
            self.load_room(self.current_room.neighbours[0], True)
        elif action == "go_forward":
            self.load_room(self.current_room.neighbours[1], True)
        elif action == "go_right":
            self.load_room(self.current_room.neighbours[2], True)
        elif action == "go_back":
            self.load_room(self.previous_room.name, True)
        elif action == "examine":
            PointClick.load_point_click(self.screen, self)
        # possible actions inside of events
        elif action == "continue" :
            self.isInEvent = False
            self.current_event = None
            self.load_room(self.current_room, False)
        # custom actions (often room-specific)
        else :
            self.do_custom_action(action)

        if self.sanity <= 0 :
            self.death()


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


# the actual engine lmao
g = Game()
g.run()
pg.quit()