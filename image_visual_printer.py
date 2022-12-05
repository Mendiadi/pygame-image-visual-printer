import threading
import numpy
from PIL import Image
import pygame
import time
import tkinter
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText


def get_image(image_path):
    image = Image.open(image_path, "r")
    print(image)
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
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values, width, height, pad


def perform(pad, pixel_values, win, w, h, size, time_):
    ptr = 0
    for j in range(h):
        time.sleep(time_)
        for i in range(w):
            pixel = pixel_values[i][j]
            pygame.draw.rect(win, pixel, (pad * i, pad * j, size, size))
            ptr += 1


def paint_image(win, path):
    image = get_image(path)
    if not image:
        font = pygame.font.SysFont("arial", 30)
        render = font.render("sorry the image file format doesnt supported", False, (0, 0, 0))
        win.blit(render, (100, 500))
        return 1
    pixel_values, w, h, pad = image
    perform(pad, pixel_values, win, w, h, 1, 0.01)
    perform(pad, pixel_values, win, w, h, 3, 0.02)
    perform(pad, pixel_values, win, w, h, pad, 0.05)


def paint_images(win, images):
    for image in images:
        print(image)
        if paint_image(win, image) == 1:
            time.sleep(2)
        win.fill("white")
        time.sleep(2)


def main(win):
    pygame.init()
    fps = 60
    run = True
    clock = pygame.time.Clock()
    win.fill("white")

    while run:
        pygame.display.set_caption(f"FPS {int(clock.get_fps())}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


root = tkinter.Tk()
root.title("IMAGE PRINTER VISUAL")


def run_paint(images):
    root.destroy()
    win = pygame.display.set_mode((1000, 1000))

    threading.Thread(target=paint_images, args=(win, images), daemon=True).start()
    main(win)


names = []


def parse_path(str_):
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
    global names, t_box
    names = filedialog.askopenfilenames()
    names = list(filter(lambda x: x.endswith("jpg") or x.endswith("png")
                                  or x.endswith("JPG") or x.endswith("PNG"), names))
    print(names)
    t_box.config(state="normal")
    t_box.insert(0.0, "\n".join([parse_path(name) for name in names]))
    t_box.config(state="disabled")


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
tkinter.Label(root, text="in this case we will let you know ang skip process to next image",
              font="none 12 bold", bg=bg_color).pack(pady=5)
tkinter.Button(root, text="upload", command=upload, bg="green",
               font="none 10 bold", height=1, width=10, fg="white").pack(pady=10)
t_box = ScrolledText(root, height=15, state="disabled", font="none 12",
                     bg="grey", fg="blue")
t_box.pack()
btn = tkinter.Button(root, text="start", command=lambda: run_paint(names), bg="red",
                     font="none 10", height=1, width=10, fg="white")
btn.pack(pady=10)
root.mainloop()
