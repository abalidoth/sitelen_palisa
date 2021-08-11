from PIL import Image, ImageDraw, ImageFilter

import numpy as np

from json import load

with open("seg_coords.json", "r") as f:
    seg_coords = load(f)



seg_coords = {k:tuple(tuple(i) for i in v) for k,v in seg_coords.items()}

w,h = 150,200

hole_size = 4

grid_opacity = 50

glow_amount=6

def make_sitelen_img(lit_segs, w=w, h=h):
    on_seg = Image.new("RGBA",(w,h),(0,0,0,0))
    off_seg = Image.new("RGBA",(w,h),(0,0,0,0))
    on_seg_d = ImageDraw.Draw(on_seg)
    off_seg_d = ImageDraw.Draw(off_seg)

    binary_mask = [[((y%(2*hole_size)==0) or ((x+(hole_size)*((y//(2*hole_size))%2))%(2*hole_size)==0)) for x in range(w)] for y in range(h)]

    for seg_name, seg_poly in seg_coords.items(): 
        if seg_name in lit_segs:
            on_seg_d.polygon(seg_poly, fill=(0,255,255,255))
        else:
            off_seg_d.polygon(seg_poly, fill=(0,255,255,30))

    out_image = Image.new(mode="RGBA",size=(w,h), color=(0,20,20,255))
    out_image = Image.alpha_composite(out_image, on_seg)

    out_image = out_image.filter(ImageFilter.GaussianBlur(glow_amount)) #apply glow

    out_image = Image.alpha_composite(out_image, on_seg)
    out_image = Image.alpha_composite(out_image, off_seg)

    grid_array=np.array(binary_mask)[:,:,np.newaxis]*(np.ones([1,1,4]))*grid_opacity
    grid_array[:,:,:3]=0
    grid = Image.fromarray(grid_array.astype("uint8"))
    grid = grid.filter(ImageFilter.GaussianBlur(0.5))

    out_image = Image.alpha_composite(out_image, grid)

    return out_image

