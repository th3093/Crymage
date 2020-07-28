import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from script import crymage as cry

LARGEFONT = ("Verdana", 24)
SMALLFONT = ("Verdana", 12)
image_ft = [('image files', '.png')]


class App(tk.Tk):

    # __init__ function for class App
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
        for F in (StartPage, EncPage, DecPage):
            frame = F(container, self)
            # initializing frame of that object from
            # StartPage, EncPage, DecPage respectively with for loop
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    # display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# StartPage class as Frame
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button_enc = ttk.Button(self, text="Encrypt", width=40, command=lambda: controller.show_frame(EncPage))
        button_enc.pack(side='left', fill='y')

        button_dec = ttk.Button(self, text="Decrypt", width=40, command=lambda: controller.show_frame(DecPage))
        button_dec.pack(side='right', fill='y')


# EncPage class as Frame
class EncPage(tk.Frame):
    # intern variables
    __org_file_path = ''
    __output_path = ''
    __message_path = ''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Encrypt", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        label_input_file = ttk.Label(self, text='Input Image in *.PNG Format', font=SMALLFONT)
        label_input_file.grid(row=1, column=1, padx=10, pady=10)

        button_browse_image = ttk.Button(self, text='Browse', command=self.get_image_input)
        button_browse_image.grid(row=2, column=1, padx=10, pady=10)

        output_path_label = ttk.Label(self, text='Output directory and filename (without extension)', font=SMALLFONT)
        output_path_label.grid(row=3, column=1, padx=10, pady=10)

        button_browse_output = ttk.Button(self, text='Set Output', command=self.set_output)
        button_browse_output.grid(row=4, column=1, padx=10, pady=10)

        label_entry_message = ttk.Label(self, text='Message to Encrypt in *.txt Format', font=SMALLFONT)
        label_entry_message.grid(row=5, column=1, padx=10, pady=10)

        button_browse_message = ttk.Button(self, text='Browse', command=self.get_message_input)
        button_browse_message.grid(row=6, column=1, padx=10, pady=10)

        button_do_enc = ttk.Button(self, text='Encrypt image', command=self.encrypt)
        button_do_enc.grid(row=7, column=1, padx=10, pady=10)

        button_start = ttk.Button(self, text=" < StartPage", command=lambda: controller.show_frame(StartPage))
        button_start.grid(row=0, column=0)

    # input dialog image
    def get_image_input(self):
        self.__org_file_path = filedialog.askopenfilename(filetypes=image_ft)

    # input dialog message
    def get_message_input(self):
        self.__message_path = filedialog.askopenfilename(filetypes=[('text files', '.txt')])

    # output dialog location and name
    def set_output(self):
        self.__output_path = filedialog.asksaveasfilename(filetypes=image_ft)
        if self.__output_path[-4:] not in ['.png', '.jpg']:
            self.__output_path += '.png'

    # start encryption
    def encrypt(self):
        cry.encrypt_picture(self.__message_path, self.__org_file_path, self.__output_path)


# DecPage class as Frame
class DecPage(tk.Frame):
    # intern variables
    _encrypt_file_path = ''
    _org_file_path = ''
    _message = ''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Decrypt", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        label_input_file = ttk.Label(self, text='Input original Image in *.PNG Format', font=SMALLFONT)
        label_input_file.grid(row=1, column=1, padx=10, pady=10)

        button_browse_image = ttk.Button(self, text='Browse', command=self.get_image_input)
        button_browse_image.grid(row=2, column=1, padx=10, pady=10)

        label_input_enc_file = ttk.Label(self, text='Input enc Image in *.PNG Format', font=SMALLFONT)
        label_input_enc_file.grid(row=3, column=1, padx=10, pady=10)

        button_browse_output = ttk.Button(self, text='Browse', command=self.get_enc_image_input)
        button_browse_output.grid(row=4, column=1, padx=10, pady=10)

        button_do_dec = ttk.Button(self, text='Decrypt image', command=self.decrypt)
        button_do_dec.grid(row=5, column=1, padx=10, pady=10)

        button_start = ttk.Button(self, text=" < StartPage", command=lambda: controller.show_frame(StartPage))
        button_start.grid(row=0, column=0)

    # input dialog original img
    def get_image_input(self):
        self._org_file_path = filedialog.askopenfilename(filetypes=image_ft)

    # input dialog encrypted img
    def get_enc_image_input(self):
        self._encrypt_file_path = filedialog.askopenfilename(filetypes=image_ft)

    # start decryption
    def decrypt(self):
        self._message = cry.decrypt_picture(self._org_file_path, self._encrypt_file_path)
        tk.messagebox.showinfo(title='Message', message=self._message)


# main loop
app = App()
app.title('Crymage - Encrypt and Decrypt Images')
app.geometry('800x400')
app.mainloop()
