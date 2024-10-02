'''

This script contains the functions to be called from streamlit.py

'''
import numpy as np
import locale as lc
import datetime as dt

import matplotlib.pyplot as plt


lc.setlocale(lc.LC_ALL,'es_ES.UTF-8')

month = dt.datetime.now().strftime("%B %Y").capitalize()
year = month.split(' ')[-1]

def grapher(country,df):

    row = df.loc[df.index==country]

    row['TOTAL'] = row[['SOLAR','WIND','BESS']].sum(axis = 1)

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    val = row[['SOLAR','WIND','BESS']].iloc[0].index.values + ' ' + row[['SOLAR','WIND','BESS']].astype(str) + ' MW'
    total = 'TOTAL ' + round(row['TOTAL'],2).astype(str) + ' MW'

    wedges, texts = ax.pie(row[['SOLAR','WIND','BESS']].iloc[0].values, wedgeprops=dict(width=0.5), startangle=-40, colors = ['yellow','lightsteelblue','honeydew'])

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(val.iloc[0][i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)

    ax.set_title(f"{country}\n{total[0]}")

    return fig

