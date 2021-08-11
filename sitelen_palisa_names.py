import sys

import pygame
from pygame.locals import *

import sitelen_palisa_maker as spm
from json import load, dump
from collections import defaultdict




pygame.init()

ui_scale = 3

with open("seg_coords.json", "r") as f:
    raw_seg_coords = load(f)

seg_coords = {
    k:tuple((i*ui_scale, j*ui_scale) for i,j in v)
for k,v in raw_seg_coords.items()}

num_to_name = sorted(list(seg_coords.keys()))
name_to_num = {j:i for i,j in enumerate(num_to_name)}


width, height = spm.w*ui_scale, spm.h*ui_scale

with open("nimi.json", "r") as f:
    nimi = defaultdict(list, load(f))

lit_segs = {n:False for n in num_to_name}



screen = pygame.display.set_mode((width, height))
# screensurf = pygame.display.get_surface()

typed=""

font = pygame.font.Font(None, 50)

# Game loop.
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            c = screen.get_at(event.pos)[0]
            if c < 14:
                c_n = num_to_name[c]
                lit_segs[c_n] = not lit_segs[c_n]
        if event.type == KEYDOWN:
                if event.unicode.isalpha() or event.unicode in "~*{}_":
                    typed += (event.unicode).lower()
                elif event.key == K_BACKSPACE:
                    typed = typed[:-1]
                elif event.key == K_RETURN:
                    segs = sorted([k for k,v in lit_segs.items() if v])
                    if segs:
                        nimi[typed]=segs
                    else:
                        nimi.pop(typed,None) #remove key from nimi if no segs lit
                    with open("nimi.json","w") as f:
                        dump(dict(nimi), f, sort_keys=True, indent=2)
                    typed=""

    screen.fill((14, 20, 20))

        
    for name, coords in seg_coords.items():
        pygame.draw.polygon(
            screen,
            [
                name_to_num[name],
                lit_segs[name]*200 + 50,
                lit_segs[name]*200 + 50
            ],
            coords
        )
    

    block = font.render(typed, True, (255, 255, 255))
    rect = block.get_rect()
    rect.center = [75*ui_scale,10*ui_scale]
    screen.blit(block, rect)

    pygame.display.flip()