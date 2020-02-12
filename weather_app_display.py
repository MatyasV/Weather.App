from tkinter import *

from weighted_average_weather import get_weather_at_all_points


class WeatherAppDisplay:

    def __init__(self, width=600, height=800, colour='steel blue'):
        self.width = width
        self.height = height
        self.colour = colour

        self.gui = Tk()
        #self.gui.configure(background=colour)
        self.gui.geometry("{}x{}".format(self.width, self.height))
        self.gui.title('weatherapp')

        self.go_button = None
        self.year_entry = None
        self.month_entry = None
        self.weather_entry = None
        self.photo = None
        self.image_label = None
        self.build_display()

    def build_display(self):
        self.go_button = Button(master=self.gui, text='go!', fg='black', bg='green', font="Calibri 20", command=self.press_go)
        self.go_button.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.1)

        self.year_entry = Entry(master=self.gui, font="Calibri 20")
        self.year_entry.place(relx=0.0, rely=0, relwidth=0.25, relheight=0.1)

        self.month_entry = Entry(master=self.gui, font="Calibri 20")
        self.month_entry.place(relx=0.25, rely=0, relwidth=0.25, relheight=0.1)

        self.weather_entry = Entry(master=self.gui, font="Calibri 20")
        self.weather_entry.place(relx=0.5, rely=0, relwidth=0.25, relheight=0.1)

        self.photo = PhotoImage(file="uk_map.png", )
        self.image_label = Label(self.gui, image=self.photo)
        self.image_label.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def start_display(self):
        self.gui.mainloop()

    def press_go(self):
        print('Go has been pressed')
        print('year is {}'.format(self.year_entry.get()))
        print('month is {}'.format(self.month_entry.get()))
        print('weather type is {}'.format(self.weather_entry.get()))

if __name__ == '__main__':

    display = WeatherAppDisplay()
    display.start_display()


