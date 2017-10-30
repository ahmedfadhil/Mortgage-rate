import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

# Not necessary, I just do this so I do not show my API key.
api_key = open('quandlapikey.txt', 'r').read()


def mortgage_30y():
    df = quandl.get('FMAC/MORTG', trim_start="1975-01-01", authtoken=api_key)
    df['Value'] = (df['Value'] - df['Value'][0]) / df['Value'][0] * 100.0
    df = df.resample('D')
    df = df.resample('M')
    df.column = ['M30']
    return df


def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][0][1:]


def grab_initial_state_data():
    states = state_list()

    main_df = pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_" + str(abbv)
        df = quandl.get(query, authtoken=api_key)
        print(query)
        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][0] * 100.0
        print(df.head())
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    pickle_out = open('fiddy_states3.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()


def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df["United States"] = (df["United States"] - df["United States"][0]) / df["United States"][0] * 100.0
    return df


M30 = mortgage_30y()
HPI_data = pd.read_pickle('friddy_state.pickle')
HPI_bench = HPI_Benchmark()

state_HPI_M30 = HPI_data.join(M30)
print(state_HPI_M30.corr()['M30'].describe())
# def mortgage_30y():
#     df = Quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken=api_key)
#     df["Value"] = (df["Value"] - df["Value"][0]) / df["Value"][0] * 100.0
#     df = df.resample('1D')
#     df = df.resample('M')
#     return df
