# writen by adi mendel 5/12/2022
# feel free to look, use, modify, and learn from it

import threading
import numpy
from PIL import Image
import pygame
import time
import tkinter
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

# global var to end program
RUNNING = 1


def get_pixels(image_path):
    """
    take image path and return its pixels in rgb 2d array
    steps:
    1.open image via pillow
    2.grab width and height
    3. init pad to value that fit my window size
    4. verify image size and modify if its will greater from window size
    5. grab the pixels list
    6. verify image mode
    7. convert the pixels list to 2d array of rgb values
    the pixels is just big list of numbers
    show with numpy reshape we can convert them to the real rgb for each pixel
    :param image_path: path
    :return:
    """
    image = Image.open(image_path, "r")
    width, height = image.size
    pad = 10
    if not (width < 200 or height < 200):
        pad = 5
        image = image.resize((200, 200))
        width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == "RGB":
        channels = 3
    elif image.mode == "L":
        channels = 1
    else:
        return None
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values, width, height, pad


def perform(pad, pixel_values, win, w, h, size, time_):
    """
    drawing the pixels to pygame surface
    :param pad: the distance between pixels
    :param pixel_values: matrix of RGB pixels
    :param win: surface
    :param w: width of the image
    :param h: height of the image
    :param size: size of its rect represent pixel
    :param time_: time to sleep to slow the process
    :return:
    """
    ptr = 0
    for j in range(h):
        time.sleep(time_)
        for i in range(w):
            pixel = pixel_values[i][j]
            pygame.draw.rect(win, pixel, (pad * i, pad * j, size, size))
            ptr += 1

def print_text_to_screen(text,win):
    """
    this function just print text to the surface
    :param text: string to show
    :param win: surface
    :return:
    """
    font = pygame.font.SysFont("arial", 30)
    render = font.render(text, False, (0, 0, 0))
    win.blit(render, (100, 500))

def paint_image(win, path):
    """
    take the image path
    and try to convert the picture to pixels
    if fail its show error and return
    else grab the data to representing the image and
    call perform to visual nicely
    :param win: surface
    :param path: image path
    :return:
    """
    image = get_pixels(path)
    if not image:
        print_text_to_screen("sorry the image file format doesnt supported",win)
        return
    pixel_values, w, h, pad = image
    perform(pad, pixel_values, win, w, h, 1, 0.01)
    perform(pad, pixel_values, win, w, h, 3, 0.02)
    perform(pad, pixel_values, win, w, h, pad, 0.05)


def paint_images(win, images):
    """
    starting point of the visual
    runs through all the images
    and perform paint for each image

    :param win: surface
    :param images: list of images
    :return:
    """
    for image in images:
        paint_image(win, image)
        time.sleep(2)
        win.fill("white")

    print_text_to_screen("visual done. quiting...",win)
    time.sleep(2)
    global RUNNING
    RUNNING = 0

def main(win):
    """
    main pygame loop
    :param win: surface destination
    :return:
    """
    global RUNNING
    pygame.init()
    fps = 60

    clock = pygame.time.Clock()
    win.fill("white")

    while RUNNING:
        pygame.display.set_caption(f"FPS {int(clock.get_fps())}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = 0
                break

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

# initial tkinter window for filedialog and nice basic gui setup

root = tkinter.Tk()
root.title("IMAGE PRINTER VISUAL")


def run_paint(images):
    """
    starting the main pygame program and run the visual thread
    :param images: images names
    :return:
    """
    root.destroy()
    win = pygame.display.set_mode((1000, 1000))

    threading.Thread(target=paint_images, args=(win, images), daemon=True).start()
    main(win)

# global var names to store the files images names
names = []


def parse_path(str_):
    """
    takes file path and return only the specific name with format
    :param str_: some file path
    :return:
    """
    ptr = len(str_) - 1
    name = []
    for _ in range(len(str_)):
        if str_[ptr] == "/":
            break

        name.append(str_[ptr])
        ptr -= 1
    name.reverse()
    return "".join(name)


def upload():
    """
    runs if user clicks upload btn on tkinter gui
    its opens askfiledialog and let you choose images to show
    then insert the results names after parsing to the text box
    :return:
    """
    global names, t_box
    names = filedialog.askopenfilenames()
    names = list(filter(lambda x: x.endswith("jpg") or x.endswith("png")
                                  or x.endswith("JPG") or x.endswith("PNG"), names))
    t_box.config(state="normal")
    t_box.insert(0.0, "\n".join([parse_path(name) for name in names]))
    t_box.config(state="disabled")

# init all widgets for tkinter gui
bg_color = "cyan"
root.geometry("600x600")
root.config(bg=bg_color)
tkinter.Label(root, text="IMAGE PRINTER VISUAL", font="none 12 bold", bg=bg_color).pack(pady=5)
tkinter.Label(root, text="Choose a images to Upload", font="none 12 bold", bg=bg_color).pack(pady=5)
tkinter.Label(root, text="you can choose as many as you want", font="none 12 bold", bg=bg_color).pack(pady=5)
tkinter.Label(root, text="if you choose none image format file it will automatic ignore that",
              font="none 12 bold", bg=bg_color).pack(pady=5)
tkinter.Label(root, text="notice that not all images types are allowed",
              font="none 12 bold", bg=bg_color).pack(pady=5)
tkinter.Label(root, text="in this case we will let you know and skip process to next image",
              font="none 12 bold", bg=bg_color).pack(pady=5)
tkinter.Button(root, text="upload", command=upload, bg="green",
               font="none 10 bold", height=1, width=10, fg="white").pack(pady=10)
t_box = ScrolledText(root, height=15, state="disabled", font="none 12",
                     bg="light grey", fg="blue")
t_box.pack()
btn = tkinter.Button(root, text="start", command=lambda: run_paint(names), bg="red",
                     font="none 10", height=1, width=10, fg="white")
btn.pack(pady=10)
root.mainloop()

