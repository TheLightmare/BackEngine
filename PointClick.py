import pygame as pg
import settings
from utils import *

# supposed to manage everything about the Point And Click gameplay
import utils


def load_point_click(screen, game):
    room = game.current_room
    image = room.picture

    # blit the point and click screen
    screen.fill(BLACK)
    pic_surface = utils.load_picture(image)
    width = pic_surface.get_width()
    height = pic_surface.get_height()
    pg.draw.rect(screen, WHITE, (WIDTH / 2 - width / 2 - 15, 115, width + 30, height + 30), 3)
    screen.blit(pic_surface, (WIDTH / 2 - width / 2, 130))

    print("Loaded Point and Click Screen")
