import os

import pandas as pd
from tqdm import tqdm

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


if __name__ == '__main__':

    column_names = ['year', 'month', 'temp_max', 'temp_min', 'air_frost', 'rain', 'sun']
    dir = r"C:\Users\fergg\PycharmProjects\Weather.App\historical_weather_data"
    output_path = r"C:\Users\fergg\PycharmProjects\Weather.App\combined_df.xlsx"
    filenames = os.listdir(dir)

    df_list = []
    for filename in tqdm(filenames):
        filepath = os.path.join(dir, filename)
        location = filename.strip('.txt')
        df = pd.read_csv(
            filepath_or_buffer=filepath, skiprows=7,
            names=column_names, sep=None,
            usecols=[0, 1, 2, 3, 4, 5, 6], engine='python', false_values='---', skipinitialspace=True)
        df['location'] = location
        df_list.append(df)

    concat_df = pd.concat(df_list, ignore_index=True)
    concat_df.to_excel(output_path)

