from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox, layout, gridplot
from bokeh.plotting import ColumnDataSource, Figure
from bokeh.models.widgets import Select, TextInput, Slider, DataTable, DateFormatter, TableColumn, IntEditor


#from scipy.cluster.hierarchy import fcluster
import scipy.cluster.hierarchy as hac
import numpy as np
import pandas as pd


sample_peorid = 'W'
smoothing_window = 5

#Load Data
df = pd.read_pickle('/home/ubuntu/data/jacksonville_2014_2017.pkl')
df = df.remove_columns(df)
resample_df = df.resample(sample_peorid).sum()
materals = get_materal_cluster(resample_df)


slider_smoothing = Slider(start=2, end=9, step=1, value=smoothing_window, title="Smoothing Window")

p = Figure(title="Clustered Materals", plot_height=500, plot_width=650)
df_source = ColumnDataSource(data= dict(x=resample_df[materals[0]],y=resample_df.index))

p.line(x='x', y='y', source=df_source)

df_source.data = dict(x=resample_df[materals[0]],y=resample_df.index)


grid = girdplot()







def get_materal_cluster(df):
    rolling_df = df.rolling(window=smoothing_window, center=True)
    rolling_df = rolling_df.mean()

    rm = round(smoothing_window/2)
    rolling_df = c.iloc[rm:-rm]

    clusters = hac.linkage(rolling_df.T, 'complete', 'correlation')
    clusters = hac.fcluster(cluster, .5, criterion='distance')

    clst = pd.value_counts(clusters).index[0]
    
    return rolling_df.columns[clusters==clst]



def remove_columns(df):
    sums = df.sum(axis=0)
    sums_drop = sums[sums < 8000]
    sums_drop = list(sums_drop.index)
    df = df.drop(sums_drop, axis=1)
    
    return df