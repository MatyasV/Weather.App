from sklearn.metrics import pairwise_distances
import pandas as pd
import numpy as np


def get_all_weather_at_time(df, year, month):
    """
    this function takes in a pandas df containing all weather data and returns a subdf containing only the data for the
    given yr and month.
    Parameters
    ----------
    df: pandas.core.frame.DataFrame
    year: int
    month: int

    Returns
    -------
    sub_df:  pandas.core.frame.DataFrame
    """
    assert 1 <= month <= 12

    sub_df = df[(df['year'] == year) &(df['month'] == month)]

    return sub_df


def get_dist_from_point_to_each_location(df_coords, point):
    """

    Parameters
    ----------
    df_coords:  pandas.core.frame.DataFrame
    point: tuple
        (x, y)
    Returns
    -------
    output_dict: dict
    """
    coords_array = df_coords[['x', 'y']].values
    point_array = np.array(point)
    point_array = np.expand_dims(point_array, axis=0)
    new_coords_array = np.concatenate([point_array, coords_array])
    dist_matrix = pairwise_distances(new_coords_array)
    dist_list = list(dist_matrix[0, 1:])

    name_df = df_coords['Name']
    name_list = list(name_df)

    output_dict = {}
    for dist, name in zip(dist_list, name_list):
        output_dict[name] = dist

    return output_dict


def get_weather_at_point(weather_df, df_coords, point, weather_type):
    """

    Parameters
    ----------
    weather_df: pandas.core.frame.DataFrame
    point: tuple
        (x, y)
    weather_type: str
    df_coords: pandas.core.frame.DataFrame

    Returns
    -------
    weather_at_point:
    """
    assert weather_type in ['temp_max', 'temp_min', 'rain']

    # get dict mapping name of location to its distance to point onn image
    name_to_dist_dict = get_dist_from_point_to_each_location(df_coords, point)
    name_to_recipricol_of_distance = {k: 1/v for k, v in name_to_dist_dict.items()}
    sum_of_recipricols = np.sum(list(name_to_recipricol_of_distance.values()))
    name_to_normalised_reciprical = {k: v/sum_of_recipricols for k, v in name_to_recipricol_of_distance.items()}
    print('stop')

    return True



if __name__ == '__main__':
    df_weather = pd.read_excel(r'C:\Users\fergg\PycharmProjects\Weather.App\combined_df.xlsx')
    # year = 2005
    # month = 8
    # new_df = get_all_weather_at_time(df=df, year=year, month=month)

    df_coord = pd.read_excel(r'C:\Users\fergg\PycharmProjects\Weather.App\coordinates.xlsx')
    _point = (0.5, 0.5)
    # get_dist_from_point_to_each_location(df_coords=df_coord, point=_point)

    get_weather_at_point(df_weather, df_coord, _point, weather_type='rain')
    print('stop')



