import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import track_record.postprocess.stat_gen as stat_gen


def plot_polar(stat_entry):
    data_length = len(stat_entry['data'])
    theta = np.linspace(0.0, 2 * np.pi, data_length, endpoint=False)
    radii = stat_entry['data']
    width = 2 * np.pi / data_length
    ax = plt.subplot(111, projection='polar')
    labels = ["{}:00 - {}:00".format(x, x+1) for x in range(0, 24, 3)]
    ax.set_xticklabels(labels)
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi/2)
    # bars = ax.bar(theta, radii, width=width, bottom=0.0)
    ax.bar(theta, radii, width=width, bottom=0.0)
    plt.show()


def plot_stat(stat_entry):
    if stat_entry['graph_type'] == 'polar_bar':
        plot_polar(stat_entry)


def cool_stat_print(stat_dict):
    for key in stat_dict.keys():
        if not stat_dict[key]['graph']:
            print(
                "{}: {}".format(stat_dict[key]['stat_title'],
                                stat_dict[key]['flavour_text'])
                )
        else:
            plot_stat(stat_dict[key])

def static_out():
        print("total listens: " + str(stat_gen.count_total_listens()))
        print("total tracks: " + str(stat_gen.count_total_tracks()))
        print("total albums: " + str(stat_gen.count_total_albums()))
        print("total artists: " + str(stat_gen.count_total_artists()))