'''Used to process .csv files to a structured time series pandas DataFrame and store 
in a pickle file for use.'''


import pandas as pd
import numpy as np
import cPickle as pickle
import datetime as dt

def pickle_new_data(filename, pickle_name):
    """Takes .csv file of orders and reformats them into pandas DataFraim in time series format.
    
    filename - the name and path to the .csv file
    picklename - path and name of the pickle file to be made"""
    

    df = pd.read_csv(filename, parse_dates=['Calendar day'], thousands=',')
    #Save full dataframe to pickle file
    #Rows are dates (by day) and columns are quantity of Material ordered for day
    df.to_pickle(pickle_name)

    pass

def add_new_data(filename, pickle_name):
    """Takes given .csv file of orders and reformats them into pandas DataFraim in time series format and addes it to the existing pandas file. 
    
    
    filename - the name and path to the .csv file
    picklename - path and name of the pickle file to appended"""
    dfp = pd.read_pickle(pickle_name)
    df = pd.read_csv(filename, parse_dates=['Calendar day'], thousands=',')
    
    df = df.append(dfp, ignore_index=True)
    #Save full dataframe to pickle file
    #Rows are dates (by day) and columns are quantity of Material ordered for day
    df.to_pickle(pickle_name)

    pass

def make_graph_pickles(df_pickle, materal_pickle, cust_pickle):
    
    df = pd.read_pickle(df_pickle)

    df_m = group_by_materal(df)
    df_c = gorup_by_customer(df)

    df_c.to_pickle(cust_pickle)
    df_m.to_pickle(materal_pickle)
    
    pass

def group_by_materal(df):
    df = df[['Calendar day','Material','Order Qty']]
    df = df.groupby(by = ['Calendar day','Material'])['Order Qty'].sum()
    df = pd.DataFrame(df)
    df = df.unstack()
    df.fillna(0, inplace=True)
    df.columns = df.columns.droplevel()
    
    return df

def group_by_customer(df):
    df = df[['Customer Price Group','Calendar day','Material','Order Qty']]
    df = df.groupby(by = ['Customer Price Group','Calendar day','Material'])['Order Qty'].sum()
    df = pd.DataFrame(df)
    df = df.unstack()
    df.fillna(0, inplace=True)
    df.columns = df.columns.droplevel()
    
    return df

def remove_columns(df):
    sums = df.sum(axis=0)
    sums_drop = sums[sums < 8000]
    d = list(sums_drop.index)
    df1 = df.drop(d, axis=1)
    
    return df1