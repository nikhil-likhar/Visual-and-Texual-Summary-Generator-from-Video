# import os
# Trans_Folder = "Transcripts"
# folder_address = "./"+Trans_Folder
# name_list = os.listdir(folder_address)
# print(name_list.sort())
# # print(name_list)


from tkinter import *
from PIL import ImageTk, Image
import os
import tkinter.font as fnt
a = 0

Padx = 220
Pady = 20
Text_Padx = 100

# light theme
# BGcolor = "#EEEEEE"
# FGcolor = "#000000"

# dark theme
BGcolor = "#272727"
FGcolor = "#ffffff"
# grey
color1 = "#747474"

# red
color2 = "#FF652F"

# yellow
color3 = "#FFE400"

# green
color4 = "#14A76C"

BFSize = 12
BFFamily = "Verdana"
BFont = (BFFamily, BFSize)
pad = 7
pad2 = 2

global counter
counter = -1
# path, dirs, files = next(os.walk("./data"))
# if(a == 0):
#     file_count = len(files)
#     print(file_count)
#     a = 1


def forward(img_no):
    global label
    global button_forward
    global button_back
    global button_exit
    global counter
    global file_count

    heading.grid_remove()
    cover_img.grid_remove()
    print("\nAt Slide ", img_no+1)

    counter = counter+1
    heading.grid_remove()
    # label.grid_forget()
    my_string_var.set(List_text[img_no])

    label = Label(image=List_images[img_no],  bg=BGcolor)
    text = Label(root, textvariable=my_string_var,
                 font=('Verdana', 12), pady=20, wraplength=1300, fg=FGcolor, bg=BGcolor)

    button_forward = Button(root, text="Forward",  bg=color4, font=BFont,
                            command=lambda: forward(img_no+1))

    button_back = Button(root, text="Back",  bg=color3, font=BFont,
                         command=lambda: back(img_no-1))

    if img_no == file_count-1:
        print("\nReached End\n_______________________________________________\n\n")
        button_forward = Button(root, text="Forward", state=DISABLED)

    button_back.grid(row=0, column=0, padx=Padx, pady=Pady,
                     ipadx=5, ipady=5, sticky="nsew")
    button_exit.grid(row=0, column=1, padx=Padx, pady=Pady,
                     ipadx=5, ipady=5, sticky="nsew")
    button_forward.grid(row=0, column=2, padx=Padx, pady=Pady,
                        ipadx=5, ipady=5, sticky="nsew")

    label.grid(row=1, column=0, columnspan=3, padx=Padx)
    text.grid(row=4, column=0, columnspan=10, padx=Text_Padx)


def back(img_no):
    global label
    global button_forward
    global button_back
    global button_exit

    print("\nAt Slide ", img_no+1)

    heading.grid_remove()
    # label.grid_forget()

    my_string_var.set(List_text[img_no])
    label = Label(image=List_images[img_no],  bg=BGcolor)
    text = Label(root, textvariable=my_string_var,
                 font=('Verdana', 12), pady=20, wraplength=1300, fg=FGcolor, bg=BGcolor)

    button_forward = Button(root, text="Forward", bg=color4, font=BFont,
                            command=lambda: forward(img_no + 1))
    button_back = Button(root, text="Back", bg=color3,  font=BFont,
                         command=lambda: back(img_no - 1))
    # print(img_no)

    if img_no == 0:
        print("\nReached Start\n_______________________________________________\n\n")
        button_back = Button(root, text="Back", state=DISABLED)

    button_back.grid(row=0, column=0, padx=Padx, pady=Pady,
                     ipadx=5, ipady=5, sticky="nsew")
    button_exit.grid(row=0, column=1, padx=Padx, pady=Pady,
                     ipadx=5, ipady=5, sticky="nsew")
    button_forward.grid(row=0, column=2, padx=Padx, pady=Pady,
                        ipadx=5, ipady=5, sticky="nsew")
    label.grid(row=1, column=0, columnspan=3, padx=Padx)
    text.grid(row=4, column=0, columnspan=10, padx=Text_Padx)


root = Tk()
root.config(bg=BGcolor)
root.title("KeyFrames Summary")
root.geometry("1920x1080")

print("\n\n\n\n\n\t________ Key Frames and Summarizer (Part by) Output Displayer _________\n\n\n\n")

file_name = "Agile"

Img_Folder = file_name+"/data"
folder_address = "./"+Img_Folder

print("____ Image Folder : {} ____".format(folder_address))
img_list = os.listdir(folder_address)

img_list.append("Summary.jpg")
file_count = len(img_list)
# image = Image.open("./data/frame1.jpg")
# image = image.resize((854, 480), Image.ANTIALIAS)
# image_no_1 = ImageTk.PhotoImage(image)

List_text = []
List_images = []

for i in range(file_count):
    if(i == file_count-1):
        img_name = img_list[i]
    else:
        img_name = folder_address+"/"+img_list[i]
    # print(img_name)
    image = Image.open(img_name)
    image = image.resize((854, 480), Image.ANTIALIAS)
    List_images.append(ImageTk.PhotoImage(image))


Summ_Folder = file_name+"/Summary"
folder_address = "./"+Summ_Folder

print("\n\n____ Summary Folder : {} ____\n\n\n\n".format(folder_address))
sum_list = os.listdir(folder_address)


for i in range(file_count):
    file = open(folder_address+"/"+sum_list[i], "r")
    text = file.read()
    file.close
    List_text.append(text)

cover_img = Label(image=List_images[0],  bg=BGcolor)
my_string_var = StringVar()
splited = sum_list[0].split("-")
# my_string_var.set("Summary of File : "+str(splited[0]))


heading = Label(root, text="Summary of File : "+str(splited[0]),
                font=('Verdana', 30), pady=30, wraplength=1300, fg=FGcolor, bg=BGcolor)

heading.grid(row=1, column=0, columnspan=3, padx=Text_Padx)
cover_img.grid(row=4, column=0, columnspan=3, padx=Padx)
button_back = Button(root, text="Back", command=back, bg=color3,  font=BFont,
                     state=DISABLED)

button_exit = Button(root, text="Exit", bg=color2,  font=BFont,
                     command=root.quit)

button_forward = Button(root, text="Forward",  bg=color4,  font=BFont,
                        command=lambda: forward(0))

# grid function is for placing the buttons in the frame
button_back.grid(row=0, column=0, padx=Padx, pady=Pady,
                 ipadx=5, ipady=5, sticky="nsew")
button_exit.grid(row=0, column=1, padx=Padx, pady=Pady,
                 ipadx=5, ipady=5, sticky="nsew")
button_forward.grid(row=0, column=2, padx=Padx, pady=Pady,
                    ipadx=5, ipady=5, sticky="nsew")


root.mainloop()
