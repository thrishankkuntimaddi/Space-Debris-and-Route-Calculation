import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

class TimestampSelector:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Select Timestamp")

        # Add calendar widget for date selection
        self.cal = Calendar(self.root, selectmode="day", date_pattern="yyyy-mm-dd")
        self.cal.pack(pady=20)

        # Add dropdowns for time selection (HH, MM, SS)
        self.time_frame = ttk.Frame(self.root)
        self.time_frame.pack(pady=10)

        self.hour_var = tk.StringVar(value="12")
        hour_options = [f"{i:02d}" for i in range(24)]
        self.hour_menu = ttk.OptionMenu(self.time_frame, self.hour_var, *hour_options)
        self.hour_menu.pack(side=tk.LEFT)

        self.minute_var = tk.StringVar(value="00")
        minute_options = [f"{i:02d}" for i in range(60)]
        self.minute_menu = ttk.OptionMenu(self.time_frame, self.minute_var, *minute_options)
        self.minute_menu.pack(side=tk.LEFT)

        self.second_var = tk.StringVar(value="00")
        second_options = [f"{i:02d}" for i in range(60)]
        self.second_menu = ttk.OptionMenu(self.time_frame, self.second_var, *second_options)
        self.second_menu.pack(side=tk.LEFT)

        # Add a button to confirm the selection
        self.submit_button = ttk.Button(self.root, text="Select", command=self.get_datetime)
        self.submit_button.pack(pady=10)

        # Variable to store the selected timestamp
        self.selected_timestamp = None

    def get_datetime(self):
        # Get the selected date and time
        selected_date = self.cal.get_date()
        selected_time = f"{self.hour_var.get()}:{self.minute_var.get()}:{self.second_var.get()}"
        timestamp_str = f"{selected_date}T{selected_time}"
        self.selected_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
        print("Selected timestamp:", self.selected_timestamp)
        self.root.destroy()  # Close the window after selection

    def select_timestamp(self):
        # Run the tkinter main loop
        self.root.mainloop()
        return self.selected_timestamp

# Usage
if __name__ == "__main__":
    selector = TimestampSelector()
    launch_timestamp = selector.select_timestamp()
