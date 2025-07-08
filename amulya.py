import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import numpy as np
import cv2 as cv
import os.path
import random
import webbrowser

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")

numpy_file = np.load("pts_in_hull.npy")
Caffe_net = cv.dnn.readNetFromCaffe("colorization_deploy_v2.prototxt", "colorization_release_v2.caffemodel")
numpy_file = numpy_file.transpose().reshape(2, 313, 1, 1)

dir_add = os.getcwd()
file_path = "E:/Project/color/icons/linkedin.png"
link_ico = customtkinter.CTkImage(Image.open(file_path))
file_path = "E:/Project/color/icons/upload.png"
upload_ico = customtkinter.CTkImage(Image.open(file_path))
file_path = "E:/Project/color/icons/arrow.png"
color_ico = customtkinter.CTkImage(Image.open(file_path))
file_path = "E:/Project/color/icons/open.png"
open_ico = customtkinter.CTkImage(Image.open(file_path))
file_path = "E:/Project/color/icons/document.png"
document_ico = customtkinter.CTkImage(Image.open(file_path))
file_path = "E:/Project/color/icons/logo.png"
logo = customtkinter.CTkImage(Image.open(file_path))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Black & White Image Colorization")
        self.geometry(f"{1200}x{640}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.image = None
        self.image2 = None
        self.image3 = None
        self.image4 = None

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="NSEW")
        self.sidebar_frame.grid_rowconfigure((2,3,4), weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Colorization", image=logo, compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, rowspan=2, padx=20, pady=(20, 10))

        self.address_label = customtkinter.CTkLabel(self.sidebar_frame, text="Output Directory:", anchor="s")
        self.address_label.grid(row=3, column=0, padx=20, sticky="S")
        self.address = customtkinter.CTkTextbox(self.sidebar_frame, height=200)
        self.address.insert("0.0", dir_add+"\images")
        self.address.grid(row=4, column=0, padx=20, pady=10, sticky="NSEW")
        self.address_btn = customtkinter.CTkButton(self.sidebar_frame, text="Browse", command=self.pick_address)
        self.address_btn.grid(row=4, column=0, sticky="S")
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(30, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main frame and buttons
        self.frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.frame.grid(row=0, column = 1, rowspan=4, sticky="NSEW", padx=15, pady=15)
        
        # create right sidebar
        self.right_frame = customtkinter.CTkFrame(self)
        self.right_frame.grid(row=0, column=2, rowspan=3, sticky="NSEW")
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.rowconfigure(1, weight=1)
        
        self.tabview = customtkinter.CTkTabview(self.right_frame, width=200, corner_radius=10)
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

        self.tabview.add("Quote 1")
        self.tabview.add("Quote 2")
        self.tabview.add("Quote 3")
        
        text_var = tkinter.StringVar(value=self.reload_quote())
        self.quote_label1 = customtkinter.CTkLabel(self.tabview.tab("Quote 1"), textvariable=text_var, wraplength=185)
        self.quote_label1.place(relx=0.05, rely=0.05)
        text_var2 = tkinter.StringVar(value=self.reload_quote())
        self.quote_label2 = customtkinter.CTkLabel(self.tabview.tab("Quote 2"), textvariable=text_var2, wraplength=185)
        self.quote_label2.place(relx=0.05, rely=0.05)
        text_var3 = tkinter.StringVar(value=self.reload_quote())
        self.quote_label3 = customtkinter.CTkLabel(self.tabview.tab("Quote 3"), textvariable=text_var3, wraplength=185)
        self.quote_label3.place(relx=0.05, rely=0.05)

        self.about = customtkinter.CTkFrame(self.right_frame, corner_radius=10, height = 10)
        self.about.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")

        ash = customtkinter.CTkButton(self.about, text="Ashay H N", image=link_ico, command=self.open_browser_ash, fg_color="transparent")
        ash.place(relx=0.5, rely=0.25, anchor="center")
        akh = customtkinter.CTkButton(self.about, text="Akhil Ashok", image=link_ico, command=self.open_browser_akh, fg_color="transparent")
        akh.place(relx=0.5, rely=0.45, anchor="center")
        doc = customtkinter.CTkButton(self.about, text="KLE Document", image=document_ico, command=self.open_doc, fg_color="transparent")
        doc.place(relx=0.5, rely=0.75, anchor="center")
        
        # create canvas for image
        self.frame.columnconfigure(1, weight = 4)
        self.frame.rowconfigure(0, weight=15)
        self.frame.rowconfigure(1, weight=1)
        
        self.canvas = tkinter.Canvas(self.frame, bg = self.frame["bg"])
        self.canvas.grid(row=0, column=1, sticky="NSEW", padx=15, pady = 15)

        self.btn_frame = customtkinter.CTkFrame(self.frame, height = 65)
        self.btn_frame.grid(row=1, column=1, sticky="NSEW", padx = 10, pady = 10)

        upload_btn = customtkinter.CTkButton(self.btn_frame, text="Upload", image=upload_ico, height=50, fg_color="transparent", command=self.uploadImage)
        color_btn = customtkinter.CTkButton(self.btn_frame, text="Color", image=color_ico, fg_color="transparent", command=self.color)
        open_btn = customtkinter.CTkButton(self.btn_frame, text="Open", image=open_ico, fg_color="transparent", command=self.open_output)
        upload_btn.place(relx = 0.25, rely=0.5, anchor="center")
        color_btn.place(relx = 0.75, rely=0.25, anchor="center")
        open_btn.place(relx = 0.75, rely=0.75, anchor="center")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def pick_address(self):
        new_addr = filedialog.askdirectory(initialdir=os.getcwd())
        self.address.delete("0.0", "end")
        self.address.insert("0.0", new_addr)

    def open_browser_ash(self):
        webbrowser.open("www.linkedin.com/in/AshayHN")

    def open_browser_akh(self):
        webbrowser.open("www.linkedin.com/in/akhil-ashok-a-79604520a")

    def open_doc(self):
        os.system("start " + "Report.docx")

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def reload_quote(self):
            fname="Sentence.txt"
            lines = open(fname).read().splitlines()
            return random.choice(lines)

    def uploadImage(self):
        try:
            filename = filedialog.askopenfilename(initialdir=os.getcwd())
            pic =  Image.open(filename)
            if not filename:
                return

            # resize (if necessary)
            global wid, hei
            wid, hei = pic.size
            for i in range(10, 1, -1):
                if(hei > i*int(self.canvas["height"])):
                    wid /= i
                    hei /= i
                    break
                if(wid > i*int(self.canvas["width"])/2):
                    wid /= i
                    hei /= i
                    break

            # display image
            load = customtkinter.CTkImage(Image.open(filename), size = (wid, hei))

            if self.image is None:            
                self.image = customtkinter.CTkButton(self.canvas, image=load, text = "", fg_color = "transparent", hover="False")
                self.image.place(relx = 0.25, rely = 0.5, anchor="center")

            else:
                if self.image2 is None:
                    self.image.configure(image="")
                else:
                    self.image2.configure(image="")

                self.image2 = customtkinter.CTkButton(self.canvas, image=load, text = "", fg_color = "transparent", hover="False")
                self.image2.place(relx = 0.25, rely = 0.5, anchor="center")

            # processing of the application
            Caffe_net.getLayer(Caffe_net.getLayerId("class8_ab")).blobs = [numpy_file.astype(np.float32)]
            Caffe_net.getLayer(Caffe_net.getLayerId("conv8_313_rh")).blobs = [np.full([1, 313], 2.606, np.float32)]

            input_width = 224
            input_height = 224

            frame = cv.imread(filename)
            rgb_img = (frame[:,:,[2, 1, 0]] * 1.0 / 255).astype(np.float32)
            lab_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2Lab)
            l_channel = lab_img[:,:,0] 

            l_channel_resize = cv.resize(l_channel, (input_width, input_height)) 
            l_channel_resize -= 50 

            Caffe_net.setInput(cv.dnn.blobFromImage(l_channel_resize))
            ab_channel = Caffe_net.forward()[0,:,:,:].transpose((1,2,0)) 

            (original_height,original_width) = rgb_img.shape[:2] 
            ab_channel_us = cv.resize(ab_channel, (original_width, original_height))
            lab_output = np.concatenate((l_channel[:,:,np.newaxis],ab_channel_us),axis=2)
            bgr_output = np.clip(cv.cvtColor(lab_output, cv.COLOR_Lab2BGR), 0, 1)

            global output_addr
            output_addr = self.address.get("0.0", "end")[:-1]+"/result.png"
            cv.imwrite(output_addr, (bgr_output*255).astype(np.uint8))

        except AttributeError:
            tkinter.messagebox.showwarning("Warning", "Please import an image before continuing")

    def color(self):
        try:
            new_pic = Image.open(output_addr)
            new_w, new_h = new_pic.size

            for i in range(10, 1, -1):
                if(new_h > i*int(self.canvas["height"])):
                    new_w /= i
                    new_h /= i
                    break
                if(new_w > i*int(self.canvas["width"])/2):
                    new_w /= i
                    new_h /= i
                    break
            
            new_load = customtkinter.CTkImage(Image.open(output_addr), size = (new_w, new_h))
            
            if self.image3 is None:            
                self.image3 = customtkinter.CTkButton(self.canvas, image=new_load, text = "", fg_color = "transparent", hover="False")
                self.image3.place(relx = 0.75, rely = 0.5, anchor="center")

            else:
                if self.image4 is None:
                    self.image3.configure(image="")

                else:
                    self.image4.configure(image="")

                self.image4 = customtkinter.CTkButton(self.canvas, image=new_load, text = "", fg_color = "transparent", hover="False")
                self.image4.place(relx = 0.75, rely = 0.5, anchor="center")

        except NameError:
            tkinter.messagebox.showerror("Error", "Please import a file before continuing")


    def open_output(self):
        try:
            os.system("start " + output_addr)
        except NameError:
            tkinter.messagebox.showerror("Error", "No file imported")

app = App()
file_path = "E:/Project/color/icons/logo.ico"
app.iconbitmap(file_path)
app.mainloop()

