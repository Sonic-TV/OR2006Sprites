#!/usr/bin/python
# Python3 script
# Made by Envido32
# Quick script to analize all the atlas.json files on the texture dumps
# Creates a SVG file with the same name and the rectanbles of each texture.
# To use just copy the texture dump folders on the load directory
# Input:  "load\spr_SPRANI_CLAR_RANK_Sxst\F043316B_1024x512_atlas.json"
# Output: "save\spr_SPRANI_CLAR_RANK_Sxst\F043316B_1024x512.svg"

import drawsvg       # python -m pip install drawsvg
import json
import os
import csv

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
    
    aux = len(json_files)
    if aux > 0:
        print(" >>> Precessing " + str(aux) + " files... <<< ")
    else:
        print("<ERROR>: No JSON files found in directory.")
        print(all_dirs)
    
    with open('or2textures.csv', mode='w', newline='') as csv_file:
        fields = [
        'path',
        'hash',
        'w_fixed',
        'h_fixed',
        'idx',
        'sprite',
        'status',

        'rx',
        'ry',
        'rw',
        'rl',

        'orx',
        'ory',
        'rotated',

        'type',
        'image',
        'width',
        'height',
        'fill_rate',
        'grid_height',
        'grid_width',
        'padding_x',
        'padding_y',
        'pot',
        'regions_count',
        'rotations',
        'using_grid'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        
        for this_file in json_files:
            file_path = os.path.dirname(this_file)
            file_name = os.path.basename(this_file)
            hash,wxh,ext = file_name.split('_')

            load_file = top_dir + "\\load\\" + this_file
            with open(load_file,"r") as f:
                data = json.load(f)
            
            # Create canvas
            w,h = wxh.split('x')
            #w = data.get('width')      # Sometimes doesn't match
            #h = data.get('height')     # Should always match
            if(int(w) != data.get('width') ):   # TODO: Check half or double?
                aux = int(w)/data.get('width')
                #print("Warn - W: " + str(aux))
            if(int(h) != data.get('height') ):
                print("Warn - H")
            d = drawsvg.Drawing(w,h)
            
            # Draw a rectangle
            for this_region in data.get('regions'):
                rect = this_region.get('rect')
                rx = rect[0]
                ry = rect[1]
                rw = rect[2]
                rl = rect[3]
                idx = this_region.get('idx')
                r = drawsvg.Rectangle(rx, ry, rw, rl, stroke='black', fill='red', fill_opacity=0.1, id=idx)
                title = this_region.get('name')
                r.append_title(title)  # Add a tooltip
                d.append(r)

                # Save data to CSV
                writer.writerow({
                    'fill_rate':	data.get('fill_rate'),
                    'grid_height':	data.get('grid_height'),
                    'grid_width':	data.get('grid_width'),
                    'height':	    data.get('height'),
                    'image':	    data.get('image'),
                    'type':	        data.get('name'),
                    'padding_x':	data.get('padding_x'),
                    'padding_y':	data.get('padding_y'),
                    'pot':	        data.get('pot'),
                    'regions_count':data.get('regions_count'),
                    'rotations':	data.get('rotations'),
                    'using_grid':	data.get('using_grid'),
                    'width':	    data.get('width'),

                    'hash':	        hash,
                    'w_fixed':	    w,
                    'h_fixed':	    h,
                    'path':	        file_path,

                    'idx':	        this_region.get('idx'),
                    'sprite':	this_region.get('name'),
                    'orx':	        this_region.get('origin')[0],
                    'ory':	        this_region.get('origin')[1],
                    'rx':	        this_region.get('rect')[0],
                    'ry':	        this_region.get('rect')[1],
                    'rw':	        this_region.get('rect')[2],
                    'rl':	        this_region.get('rect')[3],
                    'rotated':	    this_region.get('rotated'),
                    'status':	    'red'
                    })

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
    print(" >>> All files preccessed! <<< ")
    