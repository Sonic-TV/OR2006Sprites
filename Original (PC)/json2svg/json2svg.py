#!/usr/bin/python
# Python3 script
# Made by Envido32
# Quick script to analize all the atlas.json files on the texture dumps
# Creates a SVG file with the same name and the rectanbles of each texture.
# To use just copy the texture dump folders on the load directory
# ej: "load\spr_SPRANI_CLAR_RANK_Sxst\F043316B_1024x512_atlas.json"
# Output: "save\spr_SPRANI_CLAR_RANK_Sxst\F043316B_1024x512.svg"

import drawsvg as draw      # python -m pip install drawsvg
import json
import os

if __name__ == "__main__":
    print(" >>> Outrun2006 textures to SVG <<< ")
    print(" >>> Please wait... <<< ")

    # Look on the directory for atlas.json files
    top_dir = os.getcwd()
    all_dirs = os.listdir(top_dir + "\\load")
    json_files = []
    for this_dir in all_dirs:
        work_dir = top_dir + "\\load\\" + this_dir
        all_files = os.listdir(work_dir)
        for this_file in all_files:
            name,ext = this_file.split('.')
            if ext == "json":
                file_path = this_dir + "\\" + this_file
                json_files.append(file_path)
    
    for this_file in json_files:
        file_path = os.path.dirname(this_file)
        file_name = os.path.basename(this_file)
        #file_path = "load/spr_sprani_CLAR_RANK_Exst/"
        #file_name = "8B52FEEC_1024x512_atlas.json"
        hash,wxh,ext = file_name.split('_')

        load_file = top_dir + "\\load\\" + this_file
        with open(load_file,"r") as f:
            data = json.load(f)
        
        # Create canvas
        w,h = wxh.split('x')
        #w = data.get('width')      # Sometimes doesn't match
        #h = data.get('height')     # Should always match
        '''
        if(int(w) != data.get('width') ):   # TODO: Check half or double?
            if(int(w) != 2*data.get('width') ):
                print("Warn - W-half")
            if((2*int(w)) != data.get('width') ):
                print("Warn - W-double")
        '''
        if(int(h) != data.get('height') ):
            print("Warn - H")
        d = draw.Drawing(w,h)
        
        # Draw a rectangle
        for this_region in data.get('regions'):
            rect = this_region.get('rect')
            px = rect[0]
            py = rect[1]
            pw = rect[2]
            pl = rect[3]
            idx = this_region.get('idx')
            r = draw.Rectangle(px, py, pw, pl, stroke='black', fill='red', fill_opacity=0.1, id=idx)
            title = this_region.get('name')
            r.append_title(title)  # Add a tooltip
            d.append(r)

        d.set_pixel_scale(1)  # Set number of pixels per geometry unit
        save_dir = top_dir + "\\save\\" + file_path
        # Create output dir
        try:
            os.makedirs(save_dir)
        except:
            #print("[", save_dir, "] already exists")
            pass

        svg_file = hash + "_" + wxh + ".svg"
        svg_file = save_dir + "\\" + svg_file
        d.save_svg(svg_file)
    