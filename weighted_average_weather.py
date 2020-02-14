from sklearn.metrics import pairwise_distances
import pandas as pd
import numpy as np
from tqdm import tqdm


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


def get_weather_at_point(weather_df, df_coords, point, weather_type, year, month):
    """

    Parameters
    ----------
    weather_df: pandas.core.frame.DataFrame
    point: tuple
        (x, y)
    weather_type: str
    df_coords: pandas.core.frame.DataFrame
    year: int
    month: int

    Returns
    -------
    weather_at_point:
    """
    assert weather_type in ['temp_max', 'temp_min', 'rain']
    assert 0 <= point[0] <= 1  # check x coord is valid
    assert 0 <= point[1] <= 1  # check y coord is valid

    # get dict mapping name of location to its normalised reciprocal of it's distance from point
    name_to_dist_dict = get_dist_from_point_to_each_location(df_coords, point)
    name_to_reciprocal_of_distance = {k: 1/v for k, v in name_to_dist_dict.items()}
    sum_of_reciprocals = np.sum(list(name_to_reciprocal_of_distance.values()))
    name_to_normalised_reciprocal = {k: v/sum_of_reciprocals for k, v in name_to_reciprocal_of_distance.items()}

    # Get dict mapping loaction to weather
    weather_sub_df_at_time = get_all_weather_at_time(df=weather_df, year=year, month=month)
    if weather_sub_df_at_time.empty:
        return None

    weather_sub_df = weather_sub_df_at_time[['location', weather_type]].dropna()
    list_of_locations = list(weather_sub_df['location'])
    list_of_weather_values = list(weather_sub_df[weather_type])
    final_list_of_weather_values = []
    for val in list_of_weather_values:
        if isinstance(val, float):
            final_list_of_weather_values.append(val)
        elif isinstance(val, str):

            cleaned_val = float(''.join([char for char in list(val) if char.isnumeric() or char == '.']))
            final_list_of_weather_values.append(cleaned_val)
        elif isinstance(val, int):
            final_list_of_weather_values.append(float(val))

    location_to_weather_dict = {}
    location: object
    for location, weather in zip(list_of_locations, final_list_of_weather_values):
        location_to_weather_dict[location] = weather

    weather_at_point = 0
    for location in location_to_weather_dict:
        weather_at_location = location_to_weather_dict[location]
        normalised_reciprocal_at_location = name_to_normalised_reciprocal[location]
        weather_at_point += (normalised_reciprocal_at_location * weather_at_location)

    return weather_at_point


def get_weather_at_all_points(weather_df, df_coords, weather_type, year, month):
    """

    Parameters
    ----------
    weather_df: pandas.core.frame.DataFrame
    weather_type: str
    df_coords: pandas.core.frame.DataFrame
    year: int
    month: int

    Returns
    -------
    point_to_weather: dict
        dict mapping an (x, y) tuple to the weather at that point
        e.g. {(0.1, 0.4): 40,...}
    """
    point_to_weather = {}
    for x in tqdm(np.linspace(0.1, 1, 10)):
        for y in np.linspace(0.1, 1, 10):
            weather_at_point = get_weather_at_point(weather_df=weather_df,
                                                    df_coords=df_coords,
                                                    point=(x, y),
                                                    weather_type=weather_type,
                                                    year=year,
                                                    month=month)
            if weather_at_point is not None:
                point_to_weather[(x, y)] = weather_at_point

    return point_to_weather


if __name__ == '__main__':
    df_weather = pd.read_excel(r'C:\Users\fergg\PycharmProjects\Weather.App\combined_df.xlsx')
    df_coord = pd.read_excel(r'C:\Users\fergg\PycharmProjects\Weather.App\coordinates.xlsx')
    weather_at_all_points = get_weather_at_all_points(df_weather, df_coord, weather_type='rain', year=2000, month=2)

    print('stop')



