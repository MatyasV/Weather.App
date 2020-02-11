
import pandas as pd


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


if __name__ == '__main__':
    df = pd.read_excel(r'C:\Users\fergg\PycharmProjects\Weather.App\combined_df.xlsx')
    year = 2005
    month = 'june'
    new_df = get_all_weather_at_time(df=df, year=year, month=month)
    print('stop here')


