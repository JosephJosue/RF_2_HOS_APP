from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from i01_interface import call_i01_gui
from i53_interface import call_i53_gui
from i34_interface import call_i34_gui
from i38_interface import call_i38_gui
from i52_interface import call_i52_gui
from i51_interface import call_i51_gui
from utils import relative_to_assets


class SelectionScreen(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("401x546")
        self.configure(bg="#FFFFFF")
        self.title("RF 2 HOS")

        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=546,
            width=401,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("frame0", "image_1.png"))
        self.image_1 = self.canvas.create_image(
            200.0,
            24.0,
            image=self.image_image_1
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("frame0", "button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: call_i01_gui(self),
            relief="flat"
        )

        self.button_1.place(
            x=24.5,
            y=175.5,
            width=100.0,
            height=100.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("frame0", "button_2.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: call_i53_gui(self),
            relief="flat"
        )

        self.button_2.place(
            x=150.5,
            y=175.5,
            width=100.0,
            height=100.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("frame0", "button_3.png"))
        self.button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: call_i34_gui(self),
            relief="flat"
        )

        self.button_3.place(
            x=276.5,
            y=174.0,
            width=100.0,
            height=100.0
        )

        self.button_image_4 = PhotoImage(
            file=relative_to_assets("frame0", "button_4.png"))
        self.button_4 = Button(
            self,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )

        self.button_4.place(
            x=24.5,
            y=414.0,
            width=100.0,
            height=100.0
        )

        self.button_image_5 = PhotoImage(
            file=relative_to_assets("frame0", "button_5.png"))
        self.button_5 = Button(
            self,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )

        self.button_5.place(
            x=150.5,
            y=414.0,
            width=100.0,
            height=100.0
        )

        self.button_image_6 = PhotoImage(
            file=relative_to_assets("frame0", "button_6.png"))
        self.button_6 = Button(
            self,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat"
        )

        self.button_6.place(
            x=276.5,
            y=412.5,
            width=100.0,
            height=100.0
        )

        self.button_image_7 = PhotoImage(
            file=relative_to_assets("frame0", "button_7.png"))
        self.button_7 = Button(
            self,
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: call_i51_gui(self),
            relief="flat"
        )

        self.button_7.place(
            x=24.5,
            y=294.0,
            width=100.0,
            height=100.0
        )

        self.button_image_8 = PhotoImage(
            file=relative_to_assets("frame0", "button_8.png"))
        self.button_8 = Button(
            self,
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: call_i52_gui(self),
            relief="flat"
        )

        self.button_8.place(
            x=150.5,
            y=294.0,
            width=100.0,
            height=100.0
        )

        self.button_image_9 = PhotoImage(
            file=relative_to_assets("frame0", "button_9.png"))
        self.button_9 = Button(
            self,
            image=self.button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: call_i38_gui(self),
            relief="flat"
        )

        self.button_9.place(
            x=276.5,
            y=292.5,
            width=100.0,
            height=100.0
        )

        self.canvas.create_text(
            50.0,
            93.0,
            anchor="nw",
            text="SELECT THE TYPE OF FILE",
            fill="#000000",
            font=("Arial", 18)
        )


if __name__ == "__main__":
    app = SelectionScreen()
    app.resizable(False, False)
    app.mainloop()