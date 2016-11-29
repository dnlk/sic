import threading
import time
import tkinter as tk

from PIL import Image, ImageTk

from sic import imageprocessing


PICTURE_PATH = 'C:/Users/Dan/Desktop/Projects/hackathon/sic/sic\mandelbrot.jpg'

GUI_WIDTH = 900
GUI_HEIGHT = 600

loaded_picture = imageprocessing.load_image(PICTURE_PATH)
pic_width = loaded_picture[0]
pic_height = loaded_picture[1]
pic_data_rgbs = loaded_picture[2]


def button_click():

    print('hi mom!')


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):



        # self.hi_there = tk.Button(self)
        # self.hi_there["text"] = "Hello World\n(click me)"
        # # self.hi_there["command"] = play_audio
        # self.hi_there.pack(side="top")



        img = Image.open(PICTURE_PATH)
        img = img.resize((GUI_WIDTH, GUI_HEIGHT), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)


        self.label = tk.Label(self, image=img_tk, width=GUI_WIDTH, height=GUI_HEIGHT)
        self.label.image = img_tk
        # self.label.geometry('300x200')
        self.label.pack(side="top")
        #
        # self.img_button1 = tk.Button(self, text='foo', image=img_tk, width=50, height=50)
        # self.img_button1.image = img_tk
        # self.img_button1["command"] = button_click
        # self.img_button1.pack(side="top")
        #
        # self.img_button2 = tk.Button(self, text='foo', image=img_tk, width=50, height=50)
        # self.img_button2.image = img_tk
        # # self.img_button2["command"] = play_audio
        # self.img_button2.pack(side="top")
        #
        # self.img_button3 = tk.Button(self, text='foo', image=img_tk, width=50, height=50)
        # self.img_button3.image = img_tk
        # # self.img_button3["command"] = play_audio
        # self.img_button3.pack(side="top")
        #
        # self.img_button4 = tk.Button(self, text='foo', image=img_tk, width=50, height=50)
        # self.img_button4.image = img_tk
        # # self.img_button4["command"] = play_audio
        # self.img_button4.pack(side="top")



        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                       command=root.destroy)
        # self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")



def motion(event):
    x, y = event.x, event.y
    adjusted_x = x / GUI_WIDTH * pic_width
    adjusted_y = y / GUI_HEIGHT * pic_height
    idx = GUI_WIDTH * int(adjusted_y) + int(adjusted_x)
    # idx = int(adjusted_y) + int(adjusted_x) * GUI_HEIGHT
    rgb = pic_data_rgbs[idx]
    print('{}, {} - ajdusted - {}, {} - rgb - {}'.format(x, y, adjusted_x, adjusted_y, rgb))


if __name__ == '__main__':


    root = tk.Tk()
    root.geometry("{width}x{height}".format(width=GUI_WIDTH, height=GUI_HEIGHT))
    root.bind('<Motion>', motion)
    app = Application(master=root)
    app.mainloop()



