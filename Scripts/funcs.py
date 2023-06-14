import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def data_is_empty (table, column, engine):
    with engine.connect() as connection:
        result = connection.execute(f"SELECT COUNT(*) FROM {table} WHERE {column} IS NOT NULL")
        count = result.scalar()
    return count == 0

def total_hours (start_date, end_date):
    delta = end_date - start_date
    return int((delta.days*24) + (delta.seconds/3600))

def time_period (start_date, end_date, limit_hours= 743):
    result = []
    hours = total_hours(start_date, end_date)
    periods = int(np.ceil(hours / limit_hours))
    time_range = pd.to_timedelta(limit_hours, "hr")
    first_date = start_date
    for period in range(periods):
        date_range = [first_date]
        second_date = first_date + time_range
        if second_date > end_date:
            second_date = end_date
        date_range.append(second_date)
        first_date = second_date
        result.append(date_range)
    return result

def plot_show(df, plot_type, orientation= "vertical"):
    fig = plt.figure(figsize=(10,7))
    plt.xticks(rotation= 45);

    if plot_type == "bar":
        if orientation == "vertical":
            plt.bar(df['datetime'], df['value'], width=0.1)
            plt.show()
        elif orientation == "horizontal":
            plt.barh(df['datetime'], df['value'], height=0.1)
            plt.show()
        else:
            return "Something went wrong, please check your inputs"

    elif plot_type == "line":
        if orientation == "vertical":
            plt.plot(df['datetime'], df['value'])
            plt.show()
        elif orientation == "horizontal":
            plt.plot(df['value'], df['datetime'])
            plt.show()
        else:
            return "Something went wrong, please check your inputs"


