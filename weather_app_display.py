from tkinter import *
from tkinter import messagebox
import pandas as pd
import logging

from weighted_average_weather import get_weather_at_all_points
from utils.common import month_number_to_string


class WeatherAppDisplay:

    def __init__(self, width=600, height=800, colour='steel blue'):
        self.width = width
        self.height = height
        self.colour = colour

        self.weather_df = pd.read_excel(r'C:\Users\fergg\PycharmProjects\Weather.App\combined_df.xlsx')
        self.coord_df = pd.read_excel(r'C:\Users\fergg\PycharmProjects\Weather.App\coordinates.xlsx')

        self.gui = Tk()
        # self.gui.configure(background=colour)
        self.gui.geometry("{}x{}".format(self.width, self.height))
        self.gui.title('weatherapp')

        self.year_var = StringVar()
        self.month_var = StringVar()
        self.weather_type_var = StringVar()


        # These are widgets
        self.go_button = None
        self.year_entry = None
        self.month_entry = None
        self.weather_dropdown = None
        self.photo = None
        self.image_label = None
        self.year_month_error_label = None

        self.build_display()

    def build_display(self):
        self.go_button = Button(master=self.gui, text='go!', fg='black', bg='green', font="Calibri 20",
                                command=self.press_go, anchor=CENTER, justify=CENTER)
        self.go_button.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.1)

        self.year_var.set('YYYY')
        self.year_entry = Entry(master=self.gui, font="Calibri 20", justify=CENTER, bg='sky blue',
                                textvariable=self.year_var)
        self.year_entry.place(relx=0.0, rely=0, relwidth=0.25, relheight=0.1)
        self.year_entry.bind('<Button-1>', self.click_year_entry)

        self.month_var.set('MM')
        self.month_entry = Entry(master=self.gui, font="Calibri 20", justify=CENTER, bg='sky blue',
                                 textvariable=self.month_var)
        self.month_entry.bind('<Button-1>', self.click_month_entry)
        self.month_entry.place(relx=0.25, rely=0, relwidth=0.25, relheight=0.1)

        options = {'rain', 'temp_max', 'temp_min'}
        frame = Frame(master=self.gui)
        frame.place(relx=0.5, rely=0, relwidth=0.25, relheight=0.1)
        weather_type_label = Label(master=frame, text='Select Weather Type', bg='sky blue')
        weather_type_label.place(relx=0, rely=0, relwidth=1, relheight=0.5)
        self.weather_dropdown = OptionMenu(frame, self.weather_type_var, *options)
        self.weather_dropdown.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

        self.photo = PhotoImage(file="uk_map.png", )
        self.image_label = Label(self.gui, image=self.photo)
        self.image_label.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)


    def click_year_entry(self, event):
        self.year_var.set('')

    def click_month_entry(self, event):
        self.month_var.set('')

    def start_display(self):
        self.gui.mainloop()

    def press_go(self):
        print('Go has been pressed')

        check_passed = self.check_year_month_input()
        if not check_passed:
            return

        entered_year = int(self.year_entry.get())
        entered_month = int(self.month_entry.get())
        entered_weather_type = self.weather_type_var.get()

        weather_at_points = get_weather_at_all_points(weather_df=self.weather_df,
                                                      df_coords=self.coord_df,
                                                      year=entered_year,
                                                      month=entered_month,
                                                      weather_type=entered_weather_type)
        if weather_at_points == {}:
            error_message = 'No weather data for {} {}'.format(month_number_to_string[entered_month], entered_year)
            messagebox.showinfo('Error', error_message)
        print('')

    def check_year_month_input(self):

        if self.year_month_error_label is not None:
            self.year_month_error_label.destroy()
            self.year_month_error_label = None

        check_passed = True
        error_message = ''

        entered_year = self.year_entry.get()
        if (len(entered_year) != 4) or not entered_year.isnumeric():
            check_passed = False
            error_message = '\n'.join([error_message, 'Invalid Year'])

        entered_month = self.month_entry.get()
        if (len(entered_month) != 2) or not entered_year.isnumeric():
            check_passed = False
            error_message = '\n'.join([error_message, 'Invalid Month'])

        if not check_passed:
            messagebox.showinfo('Error', error_message)

        return check_passed


if __name__ == '__main__':
    display = WeatherAppDisplay()
    display.start_display()
