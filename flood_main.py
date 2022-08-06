import tkinter as tk
from tkinter import *
from tkinter import ttk

import tkintermapview
from tkintermapview import TkinterMapView
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from flood import stations_near_auto, measures, reading
import tkinter.messagebox as mb


class flood_viewer:
    def __init__(self, root):
        self.root = root
        self.clear()
        data = stations_near_auto()
        # create map widget
        map_widget: TkinterMapView = tkintermapview.TkinterMapView(self.root, width=1000, height=900,
                                                                   corner_radius=0)
        map_widget.grid(row=0, column=0)

        # set current widget position and zoom
        map_widget.set_position(data[0]["lat"], data[0]["long"], marker=True)
        map_widget.set_zoom(11)
        map_widget.set_marker(data[0]["lat"], data[0]["long"], text=data[0]["label"])
        for i in range(len(data)):
            map_widget.set_marker(data[i]["lat"], data[i]["long"], text=data[i]["label"],
                                  command=self.get_measures_data,
                                  data=data[i]["id"])

    def get_measures_data(self, v):
        measures_data = measures(v.data)
        self.clear()
        self.measures_data_viewer(measures_data)

    def measures_data_viewer(self, data):
        home_button = tk.Button(self.root, text="HOME", command=lambda: flood_viewer(self.root))
        home_button.grid(row=0, column=0)
        if data:
            for i in range(len(data)):
                measures_cavase = tk.Canvas(self.root, width=200, height=500)
                measures_cavase.grid(row=i + 5, column=0, pady=10, padx=10)
                label = tk.Label(measures_cavase, text="Name = " + data[i]["label"])
                label.grid(row=3, column=0)
                label = tk.Label(measures_cavase, text="parameter = " + data[i]["parameter"])
                label.grid(row=4, column=0)
                label = tk.Label(measures_cavase, text="parameterName = " + data[i]["parameterName"])
                label.grid(row=5, column=0)
                label = tk.Label(measures_cavase, text="period = " + str(data[i]["period"]))
                label.grid(row=6, column=0)
                label = tk.Label(measures_cavase, text="qualifier = " + data[i]["qualifier"])
                label.grid(row=6, column=0)
                reading_button = tk.Button(measures_cavase, text="TO SEE 24H READING GRAPH",
                                           command=lambda: self.reading_graph(data[i]["@id"]))
                reading_button.grid(row=8, column=0)
        else:
            mb.showinfo(message="No Measures Value available for this station")

    def reading_graph(self, reading_url):
        reading_value = reading(reading_url)
        df = pd.DataFrame(reading_value)
        if not df.empty:
            df.set_index(pd.to_datetime(df['timestamp']), inplace=True)

            fig, ax = plt.subplots(figsize=(6, 6))
            ax.plot(df['elevation'], label="X = Time , Y = Measures Value")

            ax.set(xlabel='Time', ylabel='Measures Value', title='Line Plot of 24H Value')
            ax.grid()
            plt.xticks(rotation=45)
            plt.legend(loc="upper left")
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.get_tk_widget().grid(row=10, column=0, padx=30)
            canvas.draw()
        else:
            mb.showinfo(message="No Measures Value available for this station")

    def clear(self):
        for child in self.root.winfo_children():
            child.destroy()





class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # Create Frame for X Scrollbar

        frame_fit = Frame(self)

        frame_fit.pack(fill=X, side=BOTTOM)

        # Create A Canvas

        my_canvas = Canvas(self)

        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbars to Canvas

        x_scrollbar = ttk.Scrollbar(frame_fit, orient=HORIZONTAL, command=my_canvas.xview)

        x_scrollbar.pack(side=BOTTOM, fill=X)

        y_scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=my_canvas.yview)
        y_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure the canvas

        my_canvas.configure(xscrollcommand=x_scrollbar.set)

        my_canvas.configure(yscrollcommand=y_scrollbar.set)

        my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox(ALL)))

        # Create Another Frame INSIDE the Canvas

        main_frame = Frame(my_canvas)

        # Add that New Frame a Window In The Canvas

        my_canvas.create_window((0, 0), window=main_frame, anchor="nw")

        flood_viewer(main_frame)


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("900x700")
    root.mainloop()
