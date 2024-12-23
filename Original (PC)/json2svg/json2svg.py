#!/usr/bin/python
# Python3 script
# Made by Envido32

import drawsvg as draw      # python -m pip install drawsvg
import json
import os

# Config Constants 
#debug = True       #DEBUG
debug = False       #DEBUG

if __name__ == "__main__":
    print(" >>> Outrun2006 textures to SVG <<< ")

    '''
    dir_work = os.getcwd()
    all_files = os.listdir(cfg.dir_songs)
    json_files = []
    for filename in all_files:
        name,ext = filename.split('.')

        if ext == "json":
            json_files.append(name)
    '''

    with open("load/spr_sprani_CLAR_RANK_Exst/8B52FEEC_1024x512_atlas.json","r") as f:
        data = json.load(f)
    
    w = data.get('width')*2
    h = data.get('height')

    d = draw.Drawing(w, h)
    
    # Draw a rectangle
    for this_region in data.get('regions'):
        #this_region = data.get('regions')[0]
        rect = this_region.get('rect')
        px = rect[0]
        py = rect[1]
        pw = rect[2]
        pl = rect[3]
        r = draw.Rectangle(px, py, pw, pl, stroke='black', fill='red', fill_opacity=0.1)
        d.append(r)

    d.set_pixel_scale(1)  # Set number of pixels per geometry unit
    d.save_svg('example.svg')
    