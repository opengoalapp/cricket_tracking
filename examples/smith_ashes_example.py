"""A quick example that calls the 3D wicket function to plot Steve Smiths's strike rate per pitch zone using the
Hawkeye data from the Ashes Series in England in 2019 """

import numpy as np
import pandas as pd
from plots.pitch_heatmap import pitch_heatmap

# Import Steve Smith data
df = pd.read_csv('data/ssmith_ashes_2019.csv')

# Hawkeye Data has Y co-ord as meters from stumps towards bowler, so need to flip pitchX and stumpsX for plotting
df['pitchX'] = -df['pitchX']
df['stumpsX'] = -df['stumpsX']

xy = np.array(df[['pitchX', 'pitchY']])
runs = df.batterRuns

title = 'Steve Smith'
subtitle_1 = 'Series Batting Strike Rate Zones | Ashes 2019 | England'
subtitle_2 = 'From {0} balls faced with tracking enabled | Minimum 12 balls per zone'.format(len(xy))
legend_title = 'Strike Rate'

pitch_heatmap(xy, runs, title, subtitle_1, subtitle_2, legend_title, measure='strike_rate')
