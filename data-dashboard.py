import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from speedmon import read_speedLog

logP = read_speedLog('speedtest.log')

fig, ax = plt.subplots(3, 1)

sns.distplot(logP['Ping'], kde=False, hist_kws={"range": [0,200]}, ax=ax[0])
sns.distplot(logP['Download'], kde=False, hist_kws={"range": [0,150]}, ax=ax[1])
sns.distplot(logP['Upload'], kde=False, hist_kws={"range": [0,15]}, ax=ax[2])

ax[0].set_ylabel(r'Frequency')
ax[1].set_ylabel(r'Frequency')
ax[2].set_ylabel(r'Frequency')
ax[0].set_xlabel(r'Ping ($ms$)')
ax[1].set_xlabel(r'Download ($Mbit/s$)')
ax[2].set_xlabel(r'Upload ($Mbit/s$)')

sns.despine(fig)
# fig.set_size_inches(4, (4 / 1.618) * 3)
# fig.subplots_adjust(hspace=0.4)

# Plot!
st.plotly_chart(fig, use_container_width=True)

