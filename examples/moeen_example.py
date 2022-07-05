"""
A quick example that calls the 3D wicket function to plot Moeen Ali's pitch map using the Hawkeye data from
the Men's ICC Cricket World Cup 2015 vs Australia on 14-02-2015
"""

import numpy as np
import pandas as pd
from plots.pitch_densitymap import pitch_densitymap

# Import Moeen Ali data
df = pd.read_csv('data/moeen.csv')

# Hawkeye Data has Y co-ord as meters from stumps towards bowler, so need to flip pitchX and stumpsX for plotting
df['pitchX'] = -df['pitchX']
df['stumpsX'] = -df['stumpsX']

# Filter to balls with tracking enabled
balls = df[df['pitchY'] > 0]

# Split balls for RHB and LHB and select pitch co-ords
xy_rh = np.array(balls[balls.rightHandedBat == True][['pitchX', 'pitchY']])

title = 'Moeen Ali'
subtitle_1 = 'Deliveries to Right-handers'
subtitle_2 = 'ICC Cricket World Cup 2015 | vs Australia | 14-02-2015'

pitch_densitymap(xy_rh, title=title, subtitle_1=subtitle_1, subtitle_2=subtitle_2)
