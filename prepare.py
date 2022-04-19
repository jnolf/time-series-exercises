import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

import warnings
warnings.filterwarnings("ignore")


def prep_store(df):
    '''
    
    '''
    df.sale_date = df.sale_date.apply(lambda date: date[:-13])
    df['sale_date'] = pd.to_datetime(df.sale_date)
    df = df.set_index('sale_date').sort_index()
    df['month'] = df.index.strftime('%m-%b')
    df['day_of_week'] = df.index.strftime('%A')
    df['sales_total'] = df.sale_amount * df.item_price
    return df


def prep_opsd(df):
    '''
    
    '''
    df.columns = [column.replace('+','_').lower() for column in df]
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').sort_index()
    df['month'] = df.index.month_name()
    df['year'] = df.index.year
    df = df.fillna(0)
    return df


def split_store(df):
    # Human-Based
    train = store.loc[:'2016'] # includes 2016
    test = store.loc['2017']
    return df


def split_ospd(df):
    # Percentage-Based
    train_size = .70
    n = opsd.shape[0]
    test_start_index = round(train_size * n)

    train = opsd[:test_start_index]
    test = opsd[test_start_index:]
    return df