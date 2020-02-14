from collections import OrderedDict

import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

from weighted_average_weather import get_weather_at_all_points


def create_rain_radar(weather_at_all_points):
    img = mpimg.imread("uk_map.png")
    height = img.shape[0]
    width = img.shape[1]

    sorted_items = sorted(weather_at_all_points.items(), key=lambda x: x[1])
    ordered_weather_at_all_points = OrderedDict({k: v for (k, v) in sorted_items})
    ordered_weather_list = list(ordered_weather_at_all_points.values())
    colour_values = 100 * (np.array(ordered_weather_list) / max(ordered_weather_list))

    boxes = []
    colours = []
    for idx, (point, weather_value) in enumerate(ordered_weather_at_all_points.items()):
        x, y = width * (point[0] - 0.1), height * (point[1] - 0.1)
        rect = Rectangle(xy=(x, y), width=0.1 * width, height=0.1 * height)
        boxes.append(rect)

    # PLOTTING
    fig, ax = plt.subplots()
    ax.imshow(np.flip(img, axis=0), origin='lower')

    pc = PatchCollection(boxes, alpha=0.7, cmap=matplotlib.cm.GnBu)
    pc.set_array(colour_values)

    # Add collection to axes
    ax.add_collection(pc)
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    plt.savefig('./rain_radar.png')


if __name__ == '__main__':

    df_weather = pd.read_excel(r'C:\Users\fergg\PycharmProjects\Weather.App\combined_df.xlsx')
    df_coord = pd.read_excel(r'C:\Users\fergg\PycharmProjects\Weather.App\coordinates.xlsx')
    weather_at_all_points = get_weather_at_all_points(df_weather, df_coord, weather_type='rain', year=2000, month=2)
    create_rain_radar(weather_at_all_points)

