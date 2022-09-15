import pygame as pg
from settings import *
import room
import time
import event


def load_save(roomlist):
    with open("save.txt") as f:
        current_room = f.readline()
    for room in roomlist :
        if room.name == current_room :
            return room


def save_game(current_room):
    with open("save.txt", "w") as f:
        f.write(current_room.name)


def print_text(screen, text, height, font, color):
    """
    prints centered text on the screen
    :param screen:
    :param text:
    :param height:
    :param font:
    :param color:
    :return:
    """
    # erases previous text if necessary
    pg.draw.rect(screen, BLACK, (0, height - 20, WIDTH, HEIGHT + 100))

    lines = text.split("|")
    for i in range(0, len(lines)) :
        textsurface = font.render(lines[i], False, color)
        textrect = textsurface.get_rect(center=(WIDTH / 2, height))
        screen.blit(textsurface, textrect)
        height += 35

# ==== MAGIC-LOAD-EVERYTHING-O'MATIC ===


def load_rooms():
    """
    loads all the rooms from the rooms.txt file
    :return: returns a list of all Room objects
    """
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


def load_events():
    """
    loads all the events from the events.txt file
    :return: list with all Event objects initialized
    """
    events = []
    with open("events.txt") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 8):
            #extract all the useful information
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


def load_actions():
    """
    loads all custom actions from actions.txt file
    :return: returns a dictionary of all actions [name : (text, effect)]
    """
    actions = []
    with open("actions.txt") as f :
        lines = f.readlines()
        for i in range(0, len(lines), 4):
            name = lines[i].strip()
            text = lines[i+1].strip()
            effect = lines[i+2].strip()
            actions.append([name, text, effect])

    return actions


def load_picture(name):
    """
    function just for loading an image, with error management
    :param name: name of the pic
    :return: pygame picture object
    """
    try :
        picture = pg.image.load(IMAGE_FOLDER + name + ".png")
    except :
        picture = pg.image.load(IMAGE_FOLDER + "Backrooms.png")
    return picture


# updating discord RPC (so everyone knows whatever the fuck you're doing in my engine >:) )
def update_rpc(RPC, current_room, duration):
    RPC.update(state="Level 0", details="Lost in the " + current_room.name, large_image="backrooms", start=duration)
