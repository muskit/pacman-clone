import sys
import pygame as pg

def process_events(game):
    for ev in pg.event.get():
        print(ev)
        if ev.type == pg.QUIT:
            sys.exit()