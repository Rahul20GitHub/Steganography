import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import math


image_display_size = 300, 300

LARGEFONT = ("Verdana", 35)

global path_image
global path_image1
global path_image2
global path_image3

encoded_image_path = "./encoded.png"
decoded_image_path = "./decoded.png"

n_bits = 2
MAX_COLOR_VALUE = 256
MAX_BIT_VALUE = 8

def make_image(data, resolution):
    image = Image.new("RGB", resolution)
    image.putdata(data)

    return image


def remove_n_least_significant_bits(value, n):
    value = value >> n
    return value << n


def get_n_least_significant_bits(value, n):
    value = value << MAX_BIT_VALUE - n
    value = value % MAX_COLOR_VALUE
    return value >> MAX_BIT_VALUE - n


def get_n_most_significant_bits(value, n):
    return value >> MAX_BIT_VALUE - n


def shit_n_bits_to_8(value, n):
    return value << MAX_BIT_VALUE - n



class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        # label of frame Layout 2
        label = ttk.Label(self, text="STEGANOGRAPHY", font=("Stencil",54))
        label.place(x=115,y=20)

        #image logo
        gif = "./imglogo.png"
        load_img = Image.open(gif)
        load_img.thumbnail((300, 300), Image.ANTIALIAS)
        np_load_image = np.asarray(load_img)
        np_load_image = Image.fromarray(np.uint8(np_load_image))
        render = ImageTk.PhotoImage(np_load_image)
        img = Label(self, image=render)
        img.image = render
        img.place(x=40, y=150)

        gif = "./textlogo.png"
        load_img = Image.open(gif)
        load_img.thumbnail((300, 300), Image.ANTIALIAS)
        np_load_image = np.asarray(load_img)
        np_load_image = Image.fromarray(np.uint8(np_load_image))
        render = ImageTk.PhotoImage(np_load_image)
        img = Label(self, image=render)
        img.image = render
        img.place(x=450, y=150)

        ## button to show frame 2 with text layout2
        button1 = ttk.Button(self, text="Image", command=lambda: controller.show_frame(Page1))
        button1.place(x=140,y=450)
        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Text",command=lambda: controller.show_frame(Page2))
        button2.place(x=570,y=450)


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="             Image", font=LARGEFONT)
        label.grid(row=0, column=300, padx=10, pady=10)

        # Ecode code
        button2 = ttk.Button(self, text="Home Page",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

        def encode():
            global path_image
            # use the tkinter filedialog library to open the file using a dialog box.
            # obtain the image of the path
            path_image = filedialog.askopenfilename()
            # load the image using the path
            load_image = Image.open(path_image)
            # set the image into the GUI using the thumbnail function from tkinter
            load_image.thumbnail((280, 280), Image.ANTIALIAS)
            # load the image as a numpy array for efficient computation and change the type to unsigned integer
            np_load_image = np.asarray(load_image)
            np_load_image = Image.fromarray(np.uint8(np_load_image))
            render = ImageTk.PhotoImage(np_load_image)
            img = Label(self, image=render)
            img.image = render
            img.place(x=100, y=70)

            global path_image1
            # use the tkinter filedialog library to open the file using a dialog box.
            # obtain the image of the path
            path_image1 = filedialog.askopenfilename()
            # load the image using the path
            load_imagee = Image.open(path_image1)
            # set the image into the GUI using the thumbnail function from tkinter
            load_imagee.thumbnail((280, 280), Image.ANTIALIAS)
            # load the image as a numpy array for efficient computation and change the type to unsigned integer
            np_load_image = np.asarray(load_imagee)
            np_load_image = Image.fromarray(np.uint8(np_load_image))
            render = ImageTk.PhotoImage(np_load_image)
            img = Label(self, image=render)
            img.image = render
            img.place(x=380, y=70)

            image_to_hide = Image.open(path_image)
            image_to_hide_in = Image.open(path_image1)
            width, height = image_to_hide.size

            hide_image = image_to_hide.load()
            hide_in_image = image_to_hide_in.load()

            data = []

            for y in range(height):
                for x in range(width):
                    # (107, 3, 10)
                    # most sig bits
                    r_hide, g_hide, b_hide = hide_image[x, y]

                    r_hide = get_n_most_significant_bits(r_hide, n_bits)
                    g_hide = get_n_most_significant_bits(g_hide, n_bits)
                    b_hide = get_n_most_significant_bits(b_hide, n_bits)

                    # remove lest n sig bits
                    r_hide_in, g_hide_in, b_hide_in = hide_in_image[x, y]

                    r_hide_in = remove_n_least_significant_bits(r_hide_in, n_bits)
                    g_hide_in = remove_n_least_significant_bits(g_hide_in, n_bits)
                    b_hide_in = remove_n_least_significant_bits(b_hide_in, n_bits)

                    data.append((r_hide + r_hide_in, g_hide + g_hide_in, b_hide + b_hide_in))

            make_image(data, image_to_hide.size).save(encoded_image_path)

            success_label = Label(self, text="Encryption Successful!",
                                  font=("Times New Roman", 20))
            success_label.place(x=280, y=250)

        # decode
        def decode():
            global path_image2
            # use the tkinter filedialog library to open the file using a dialog box.
            # obtain the image of the path
            path_image2 = filedialog.askopenfilename()
            # load the image using the path
            load_images = Image.open(path_image2)
            # set the image into the GUI using the thumbnail function from tkinter
            load_images.thumbnail((300, 300), Image.ANTIALIAS)
            # load the image as a numpy array for efficient computation and change the type to unsigned integer
            np_load_image = np.asarray(load_images)
            np_load_image = Image.fromarray(np.uint8(np_load_image))
            render = ImageTk.PhotoImage(np_load_image)
            img = Label(self, image=render)
            img.image = render
            img.place(x=87, y=350)

            image_to_decode = Image.open(path_image2)
            width, height = image_to_decode.size
            encoded_image = image_to_decode.load()

            data = []

            for y in range(height):
                for x in range(width):
                    r_encoded, g_encoded, b_encoded = encoded_image[x, y]

                    r_encoded = get_n_least_significant_bits(r_encoded, n_bits)
                    g_encoded = get_n_least_significant_bits(g_encoded, n_bits)
                    b_encoded = get_n_least_significant_bits(b_encoded, n_bits)

                    r_encoded = shit_n_bits_to_8(r_encoded, n_bits)
                    g_encoded = shit_n_bits_to_8(g_encoded, n_bits)
                    b_encoded = shit_n_bits_to_8(b_encoded, n_bits)

                    data.append((r_encoded, g_encoded, b_encoded))

            make_image(data, image_to_decode.size).save(decoded_image_path)

            global path_image3
            # use the tkinter filedialog library to open the file using a dialog box.
            # obtain the image of the path
            path_image3 = "./decoded.png"
            # load the image using the path
            load_imagees = Image.open(path_image3)
            # set the image into the GUI using the thumbnail function from tkinter
            load_imagees.thumbnail((300, 300), Image.ANTIALIAS)
            # load the image as a numpy array for efficient computation and change the type to unsigned integer
            np_load_image = np.asarray(load_imagees)
            np_load_image = Image.fromarray(np.uint8(np_load_image))
            render = ImageTk.PhotoImage(np_load_image)
            img = Label(self, image=render)
            img.image = render
            img.place(x=380, y=350)

            success_label = ttk.Label(self, text="Decryption Successful!",
                                      font=("Times New Roman", 20))
            success_label.place(x=280, y=530)

        # button to show frame 2 with text
        # layout2
        main_button = ttk.Button(self, text="Encrypt", command=encode)
        #main_button.place(x=280, y=15)
        main_button.grid(row=6, column=1, padx=10, pady=10)

        main_button = ttk.Button(self, text="Decrypt", command=decode)
        main_button.grid(row=10, column=1, padx=10, pady=10)
        # button to show frame 3 with text
        # layout3
# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="             Text", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        txt = Text(self, wrap=WORD, width=30)
        txt.place(x=440, y=67, height=200)

        def on_click():
            # Step 1.5
            global path_image
            # use the tkinter filedialog library to open the file using a dialog box.
            # obtain the image of the path
            path_image = filedialog.askopenfilename()
            # load the image using the path
            load_image = Image.open(path_image)
            # set the image into the GUI using the thumbnail function from tkinter
            load_image.thumbnail(image_display_size, Image.ANTIALIAS)
            # load the image as a numpy array for efficient computation and change the type to unsigned integer
            np_load_image = np.asarray(load_image)
            np_load_image = Image.fromarray(np.uint8(np_load_image))
            render = ImageTk.PhotoImage(np_load_image)
            img = Label(self, image=render)
            img.image = render
            img.place(x=98, y=67)

        def encrypt_data_into_image():
            # Step 2
            global path_image
            data = txt.get(1.0, "end-1c")
            # load the image
            img = cv2.imread(path_image)
            # break the image into its character level. Represent the characters in ASCII.
            data = [format(ord(i), '08b') for i in data]
            _, width, _ = img.shape
            # algorithm to encode the image
            PixReq = len(data) * 3

            RowReq = PixReq / width
            RowReq = math.ceil(RowReq)

            count = 0
            charCount = 0
            # Step 3
            for i in range(RowReq + 1):
                # Step 4
                while (count < width and charCount < len(data)):
                    char = data[charCount]
                    charCount += 1
                    # Step 5
                    for index_k, k in enumerate(char):
                        if ((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (
                                k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                            img[i][count][index_k % 3] -= 1
                        if (index_k % 3 == 2):
                            count += 1
                        if (index_k == 7):
                            if (charCount * 3 < PixReq and img[i][count][2] % 2 == 1):
                                img[i][count][2] -= 1
                            if (charCount * 3 >= PixReq and img[i][count][2] % 2 == 0):
                                img[i][count][2] -= 1
                            count += 1
                count = 0
            # Step 6
            # Write the encrypted image into a new file
            cv2.imwrite("encrypted_image.png", img)
            # Display the success label.
            success_label = Label(self, text="Encryption Successful!",font=("Times New Roman", 20))
            success_label.place(x=300, y=290)

        def decrypt():
            global path_image1
            path_image1 = filedialog.askopenfilename()
            # load the image and convert it into a numpy array and display on the GUI.
            load = Image.open(path_image1)
            load.thumbnail(image_display_size, Image.ANTIALIAS)
            load = np.asarray(load)
            load = Image.fromarray(np.uint8(load))
            render = ImageTk.PhotoImage(load)
            img = Label(self, image=render)
            img.image = render
            img.place(x=98, y=350)
            # Algorithm to decrypt the data from the image
            img = cv2.imread(path_image1)
            data = []
            stop = False
            for index_i, i in enumerate(img):
                i.tolist()
                for index_j, j in enumerate(i):
                    if ((index_j) % 3 == 2):
                        # first pixel
                        data.append(bin(j[0])[-1])
                        # second pixel
                        data.append(bin(j[1])[-1])
                        # third pixel
                        if (bin(j[2])[-1] == '1'):
                            stop = True
                            break
                    else:
                        # first pixel
                        data.append(bin(j[0])[-1])
                        # second pixel
                        data.append(bin(j[1])[-1])
                        # third pixel
                        data.append(bin(j[2])[-1])
                if (stop):
                    break

            message = []
            # join all the bits to form letters (ASCII Representation)
            for i in range(int((len(data) + 1) / 8)):
                message.append(data[i * 8:(i * 8 + 8)])
            # join all the letters to form the message.
            message = [chr(int(''.join(i), 2)) for i in message]
            message = ''.join(message)
            message_label = Label(self, text=message, font=("Times New Roman", 20,))
            message_label.place(x=500, y=410)

        button2 = ttk.Button(self, text="Home Page",command=lambda: controller.show_frame(StartPage))
        button2.grid(row=1, column=1, padx=10, pady=10)

        on_click_button = ttk.Button(self, text="Choose Image", command=on_click)
        on_click_button.grid(row=2, column=1, padx=10, pady=10)

        encrypt_button = ttk.Button(self, text="Encode",command=encrypt_data_into_image)
        encrypt_button.grid(row=3, column=1, padx=10, pady=10)

        main_button = ttk.Button(self, text="Decrypt", command=decrypt)
        main_button.grid(row=4, column=1, padx=10, pady=10)


# Driver Code
app = tkinterApp()
app.geometry('800x600')
app.title("Navigation Demo")
app.mainloop()
