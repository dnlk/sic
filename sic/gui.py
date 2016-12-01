import threading
import Tkinter as tk

from PIL import Image, ImageTk

from sic import image

GUI_WIDTH = 900
GUI_HEIGHT = 600


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master=master)
        # super(Application, self).__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        img = Image.open(image.IMAGE_PATH)
        img = img.resize((GUI_WIDTH, GUI_HEIGHT), Image.ANTIALIAS)

        self.img_tk = ImageTk.PhotoImage(img)

        self.label = tk.Label(self, image=self.img_tk, width=GUI_WIDTH, height=GUI_HEIGHT)
        self.label.img_tk = self.img_tk
        self.label.pack()


class MotionDetector(object):

    def __init__(self):
        self.x = 0
        self.y = 0

    def motion(self, event):
        x, y = event.x, event.y
        adjusted_x = int(1.0 * x / GUI_WIDTH * image.WIDTH)
        adjusted_y = int(1.0 * y / GUI_HEIGHT * image.HEIGHT)

        self.x = adjusted_x
        self.y = adjusted_y

        # For debugging
        # idx = image.get_idx(adjusted_x, adjusted_y)
        # rgb = image.IMG_DATA[idx]
        # print('gui - {}, {} - ajdusted - {}, {} - rgb - {}'.format(x, y, adjusted_x, adjusted_y, rgb))


class GuiThread(threading.Thread):

    def __init__(self, motion_detector):
        self.motion_detector = motion_detector
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.root = tk.Tk()
        self.root.geometry("{width}x{height}".format(width=GUI_WIDTH, height=GUI_HEIGHT))
        self.root.bind('<Motion>', self.motion_detector.motion)
        self.app = Application(master=self.root)
        self.app.mainloop()


if __name__ == '__main__':

    root = tk.Tk()
    root.geometry("{width}x{height}".format(width=GUI_WIDTH, height=GUI_HEIGHT))
    motion_detector = MotionDetector()
    root.bind('<Motion>', motion_detector.motion)
    app = Application(master=root)
    app.mainloop()
