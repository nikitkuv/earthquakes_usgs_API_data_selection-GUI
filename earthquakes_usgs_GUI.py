import requests
import pandas as pd
from tkinter import *
from tkinter import ttk

# url to use
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'


def parse_earthquakes(*args):

    # getting data in json format
    data_json = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?',
                             headers={
                                 'Accept': 'application/json'
                             },
                             params={
                                 'format': 'geojson',
                                 'starttime': start_time.get(),
                                 'endtime': end_time.get(),
                                 'latitude': float(lat.get()),
                                 'longitude': float(long.get()),
                                 'maxradiuskm': float(radius_km.get()),
                             }
                             ).json()

    # sorting by magnintude and taking desired number of entities
    data_json_top_n_by_magnitude = list(
        sorted(
            data_json['features'],
            key=lambda x: x['properties']['mag'],
            reverse=True
        )
    )[:int(number_of_features_to_show.get())]

    # None values in place name handling
    for eq in data_json_top_n_by_magnitude:
        if eq['properties']['place'] == None:
            eq['properties']['place'] = 'Unknown'

    results = []
    for num, eq in enumerate(data_json_top_n_by_magnitude):
        ttk.Label(mainframe, text='Location:').grid(column=1, row=11+2*num, sticky=(W, E))
        ttk.Label(mainframe, text=eq['properties']['place'].split(' ')[-1]).grid(column=2, row=11+2*num, sticky=(W, E))
        ttk.Label(mainframe, text='Magnitude:').grid(column=1, row=12+2*num, sticky=(W, E))
        ttk.Label(mainframe, text=eq['properties']['mag']).grid(column=2, row=12+2*num, sticky=(W, E))

# Setting up a root
root = Tk()
root.title('Earthquake data from USGS database')

# Setting up a mainframe
mainframe = ttk.Frame(root,
                      padding='75 20 75 20'
                      )
mainframe.grid()
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text='Input data:').grid(column=1, row=2, sticky=(W, E))

# Creating input variables and corresponding labels
start_time = StringVar()
start_time_entry = ttk.Entry(mainframe, width=7, textvariable=start_time)
start_time_entry.grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, text='Start time (YYYY-MM-DD):').grid(column=1, row=3, sticky=(W, E))

end_time = StringVar()
end_time_entry = ttk.Entry(mainframe, width=7, textvariable=end_time)
end_time_entry.grid(column=2, row=4, sticky=(W, E))
ttk.Label(mainframe, text='End time (YYYY-MM-DD):').grid(column=1, row=4, sticky=(W, E))

lat = StringVar()
lat_entry = ttk.Entry(mainframe, width=7, textvariable=lat)
lat_entry.grid(column=2, row=5, sticky=(W, E))
ttk.Label(mainframe, text='Latitude:').grid(column=1, row=5, sticky=(W, E))

long = StringVar()
long_entry = ttk.Entry(mainframe, width=7, textvariable=long)
long_entry.grid(column=2, row=6, sticky=(W, E))
ttk.Label(mainframe, text='Longitude:').grid(column=1, row=6, sticky=(W, E))

radius_km = StringVar()
radius_km_entry = ttk.Entry(mainframe, width=7, textvariable=radius_km)
radius_km_entry.grid(column=2, row=7, sticky=(W, E))
ttk.Label(mainframe, text='Radius in km:').grid(column=1, row=7, sticky=(W, E))

number_of_features_to_show = StringVar()
number_of_features_to_show_entry = ttk.Entry(mainframe, width=7, textvariable=number_of_features_to_show)
number_of_features_to_show_entry.grid(column=2, row=8, sticky=(W, E))
ttk.Label(mainframe, text='№ of earthquakes to display: ').grid(column=1, row=8, sticky=(W, E))

# Setting up results
ttk.Label(mainframe, text='Results:').grid(column=1, row=10, sticky=(W, E))

# Setting up a button and its label
ttk.Button(mainframe, text='Search', command=parse_earthquakes).grid(column=2, row=9, sticky=W)

root.mainloop()