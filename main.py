from PIL import Image
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import os.path
import os, sys
import colorsys
import tkinter as tk
from tkinter import filedialog


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
characters_img = Image.open(resource_path("characters.png"))
characters = {
    "a": [0,  5], 
    "b": [1,  5],
    "c": [2,  5],
    "d": [3,  5],
    "e": [4,  5],
    "f": [5,  5],
    "g": [6,  5],
    "h": [7,  5],
    "i": [8,  3],
    "j": [9,  5],
    "k": [10, 5],
    "l": [11, 5],
    "m": [12, 5],
    "n": [13, 5],
    "o": [14, 5],
    "p": [15, 5],
    "q": [16, 5],
    "r": [17, 5],
    "s": [18, 5],
    "t": [19, 5],
    "u": [20, 5],
    "v": [21, 5],
    "w": [22, 5],
    "x": [23, 5],
    "y": [24, 5],
    "z": [25, 5],
    ".": [26, 1],
    "!": [27, 1],
    "?": [28, 5],
    " ": [29, 3],
    "+": [30, 5],
    "-": [31, 5],
}

scale = 10
max_scale = 20


def lerp(a, b, weight):
    return (1 - weight) * a + weight * b;

def lerpi(a, b, weight):
    return int(round(lerp(a, b, weight)))



def img_pil_to_dpg(image):
    dpg_image = []
    for i in range(0, image.height):
        for j in range(0, image.width):
            pixel = image.getpixel((j, i))
            dpg_image.append(pixel[0] / 255)
            dpg_image.append(pixel[1] / 255)
            dpg_image.append(pixel[2] / 255)
            dpg_image.append(1.0)
    return dpg_image


def init():
    width, height, data = characters_img.width, characters_img.height, img_pil_to_dpg(characters_img)
    
    with dpg.texture_registry(show=False):
        dpg.add_dynamic_texture(width=width, height=height, default_value=data, tag="preview_texture")


def save_callback():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(initialdir="./", filetypes=[(".png",".png")])

    if not file_path.endswith(".png"):
        file_path += ".png"

    image = generate_preview()

    image.save(file_path)


def swap_colors():
    secondary_color = dpg.get_value("secondary_color")
    dpg.set_value("secondary_color", dpg.get_value("primary_color"))
    dpg.set_value("primary_color", secondary_color)
    update()


def generate_preview():
    value = str(dpg.get_value("text")).lower()
    
    primary_color   = dpg.get_value("primary_color")
    secondary_color = dpg.get_value("secondary_color")

    padding         = dpg.get_value("padding")
    text_gap        = dpg.get_value("text_gap")
    text_color      = dpg.get_value("text_color")
    shadow_color    = dpg.get_value("shadow_color")
    shadow_color[3] = dpg.get_value("shadow_alpha")

    display_mode = dpg.get_value("display_mode")

    for i in range(len(primary_color)):
        primary_color[i] = round(primary_color[i])
    for i in range(len(secondary_color)):
        secondary_color[i] = round(secondary_color[i])
    for i in range(len(text_color)):
        text_color[i] = round(text_color[i])
    for i in range(len(shadow_color)):
        shadow_color[i] = round(shadow_color[i])
    
    primary_color   = tuple(primary_color)
    secondary_color = tuple(secondary_color)
    text_color      = tuple(text_color)
    shadow_color    = tuple(shadow_color)

    height = 5 + padding * 2
    width = padding * 2 - text_gap + 1
    for i in value:
        if not i in characters.keys():
            continue
        width += characters[i][1] + text_gap
    
    image = Image.new("RGB", (width, height))

    generate_background(image, primary_color, secondary_color, display_mode)
    generate_text(image, text_gap, padding, text_color, shadow_color)

    return image

def generate_background(image, primary_color, secondary_color, mode = ""):
    match (mode):
        case "half":
            for x in range(image.width):
                for y in range(image.height):
                    if y > image.height / 2:
                        image.putpixel((x, y), secondary_color)
                        continue
                    image.putpixel((x, y), primary_color)
        case "horizontal-gradient":
            for x in range(image.width):
                t = 0
                if x > 0:
                    t = (x) / (image.width - 1)
                h1,s1,v1 = primary_color[0:3]
                h2,s2,v2 = secondary_color[0:3]
                color = (lerp(h1,h2,t),lerp(s1,s2,t),lerp(v1,v2,t))
                color = (round(color[0]),round(color[1]),round(color[2]))
                for y in range(image.height):
                    image.putpixel((x, y), color)
        case "vertical-gradient":
            for y in range(image.height):
                t = 0
                if y > 0:
                    t = (y) / (image.height - 1)
                h1,s1,v1 = primary_color[0:3]
                h2,s2,v2 = secondary_color[0:3]
                color = (lerp(h1,h2,t),lerp(s1,s2,t),lerp(v1,v2,t))
                color = (round(color[0]),round(color[1]),round(color[2]))
                for x in range(image.width):
                    image.putpixel((x, y), color)
        case "horizontal-gradient-hsv":
            for x in range(image.width):
                t = 0
                if x > 0:
                    t = (x) / (image.width - 1)
                h1,s1,v1 = colorsys.rgb_to_hsv(primary_color[0],primary_color[1],primary_color[2])
                h2,s2,v2 = colorsys.rgb_to_hsv(secondary_color[0],secondary_color[1],secondary_color[2])
                color = colorsys.hsv_to_rgb(lerp(h1,h2,t),lerp(s1,s2,t),lerp(v1,v2,t))
                color = (round(color[0]),round(color[1]),round(color[2]))
                for y in range(image.height):
                    image.putpixel((x, y), color)
        case "vertical-gradient-hsv":
            for y in range(image.height):
                t = 0
                if y > 0:
                    t = (y) / (image.height - 1)
                h1,s1,v1 = colorsys.rgb_to_hsv(primary_color[0],primary_color[1],primary_color[2])
                h2,s2,v2 = colorsys.rgb_to_hsv(secondary_color[0],secondary_color[1],secondary_color[2])
                color = colorsys.hsv_to_rgb(lerp(h1,h2,t),lerp(s1,s2,t),lerp(v1,v2,t))
                color = (round(color[0]),round(color[1]),round(color[2]))
                for x in range(image.width):
                    image.putpixel((x, y), color)
        case _:
            for x in range(image.width):
                for y in range(image.height):
                    image.putpixel((x, y), primary_color)

            

def generate_text(image, text_gap, padding, color, shadow_color):
    text = str(dpg.get_value("text")).lower()
    height = 5
    a = []
    for i in range(len(text)):
        if not text[i] in characters.keys():
            continue
        a.append([characters[text[i]][0], characters[text[i]][1]])
    pos = padding
    for i in range(len(a)):
        char = a[i]
        width = char[1]
        for x in range(width):
            for y in range(height):
                if characters_img.getpixel((x + 5 * char[0], y)) == (0, 0, 0, 255):
                    continue
                image.putpixel((x + pos, y + padding), color)

                t = shadow_color[3] / 100
                bg = image.getpixel((x + pos + 1, y + padding))
                shadow = (lerp(bg[0],shadow_color[0],t),lerp(bg[1],shadow_color[1],t),lerp(bg[2],shadow_color[2],t))
                shadow = (round(shadow[0]),round(shadow[1]),round(shadow[2]))
                image.putpixel((x + pos + 1, y + padding), shadow)
        pos += width + text_gap

def scale_preview(preview):
    global scale
    scale = int(dpg.get_viewport_width() / preview.width)

    if scale > max_scale:
        scale = max_scale

    image = Image.new("RGB", (preview.width * scale, preview.height * scale))
    for x in range(preview.width):
        for y in range(preview.height):
            for x2 in range(scale):
                for y2 in range(scale):
                    image.putpixel((x2 + x * scale, y2 + y * scale), preview.getpixel((x, y)))
    preview.close()
    return image


def update_preview(last_texture_id, preview):
    if not dpg.does_item_exist("preview_texture"):
        return last_texture_id
    if dpg.does_item_exist(last_texture_id):
        dpg.delete_item(last_texture_id)
    texture_id = dpg.generate_uuid()
    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=preview.width, height=preview.height, default_value=img_pil_to_dpg(preview), tag=texture_id)
    if not dpg.does_item_exist("preview_image"):
        return texture_id
    dpg.configure_item("preview_image", width=preview.width, height=preview.height, texture_tag=texture_id)       
    return texture_id

last_texture_id = 0

def update():
    preview = generate_preview()
    preview = scale_preview(preview)

    global last_texture_id
    last_texture_id = update_preview(last_texture_id, preview)


dpg.create_context()
dpg.create_viewport(title="Rank Tag Generator", width=1600, height=900)
dpg.setup_dearpygui()

init()

with dpg.window(tag="Primary Window",horizontal_scrollbar=True):
    colors = dpg.add_group(horizontal=True)
    dpg.add_color_picker(parent=colors, label="Shadow Color",    tag="shadow_color",    width=180, height=170, callback=update, default_value=(0, 0, 0))
    dpg.add_color_picker(parent=colors, label="Primary Color",   tag="primary_color",   width=180, height=180, callback=update, default_value=(255, 0, 0))
    dpg.add_color_picker(parent=colors, label="Secondary Color", tag="secondary_color", width=180, height=180, callback=update, default_value=(0, 255, 0))
    dpg.add_color_picker(parent=colors, label="Text Color",      tag="text_color",      width=180, height=180, callback=update, default_value=(255, 255, 255))

    group = dpg.add_group(horizontal=True)
    dpg.add_slider_int(parent=group, label="Shadow Alpha", tag="shadow_alpha",width=180,height=10,callback=update,clamped=True,min_value=0,max_value=100,default_value=50)
    dpg.add_button(label="Swap Primary And Secondary", callback=swap_colors)
    
    dpg.add_input_int(label="Text Gap", tag="text_gap", default_value=1, callback=update, min_value=0)
    dpg.add_input_int(label="Padding", tag="padding", default_value=1, callback=update, min_value=0)
    dpg.add_radio_button(label="Display Mode", items=["default", "half", "horizontal-gradient", "vertical-gradient", "horizontal-gradient-hsv", "vertical-gradient-hsv"], tag="display_mode", callback=update)
    
    dpg.add_input_text(label="Text", tag="text", callback=update, default_value="Rank")
    dpg.add_image(texture_tag="preview_texture", tag="preview_image")
    dpg.add_button(label="Save", callback=save_callback, width=200, height=40)


dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
update()
dpg.start_dearpygui()
dpg.destroy_context()