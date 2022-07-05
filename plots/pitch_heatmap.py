"""Plotting template for a bowling pitch map with overlaid 2D heatmap based on a specified values array,
which utilises the front view of the plot_wicket_3d function.

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.font_manager as fm
import mpl_toolkits.mplot3d.art3d as art3d
from pitch_views.wicket_3d import plot_wicket_3d
from utilities.plotting_utils import add_title_axis


def pitch_heatmap(xy,
                  values,
                  title='',
                  subtitle_1='',
                  subtitle_2='',
                  legend_title='',
                  min_balls=12,
                  cmap='cool',
                  measure=None):

    """ Plots a heatmap overlaid on wicket_3d front view, using a specified values array for square shading

    ----------
    xy: A 2d array
        The x and y coordinates of the delivery pitching locations
    values: A 1d array
        The values which will determine the heatmap zone shading
    title: A string
        The plot title
    subtitle_1: A string
        The plot's 1st subtitle
    subtitle_2: A string
        The plot's 2nd subtitle
    legend_title: A string
        The title of the value legend
    min_balls: An integer
        The minimum number of balls used for each heatmap zone. If not met the zone is not displayed
    cmap: Any valid matplotlib named colormap string
        The colour map used for the heatmap shading
    measure: string
        The measurement type used for the values. Can be:
        "strike_rate" - Strike Rate, value multiplied by 100
        "economy" - Economy, value multiplied by 6
        Any other value - No transformation applied

    Returns
    -------
    matplotlib.axes.Axes"""

    # Define some styling
    pitch_colour = 'white'
    wicket_colour = '#f5f6fa'
    marking_colour = '#595959'
    stump_colour = 'slategray'
    outline_colour = '#595959'
    title_colour = '#080a2e'
    subtitle_colour = '#9e9fa3'
    fname = 'fonts/AlumniSans-SemiBold.ttf'
    fp = fm.FontProperties(fname=fname)

    # Bin edges
    XMIN = -1.2
    XMAX = 1.2
    XBIN = 0.2

    YMIN = 0
    YMAX = 15
    YBIN = 1

    x_edges = np.arange(XMIN, XMAX, XBIN)
    y_edges = np.arange(YMIN, YMAX, YBIN)

    df = pd.DataFrame(np.column_stack([xy, values]),
                      columns=['pitchX', 'pitchY', 'values'])

    df['x_binned'] = pd.cut(df.pitchX, x_edges)
    df['y_binned'] = pd.cut(df.pitchY, y_edges)

    grouped = df.groupby(['x_binned', 'y_binned']).agg(['mean', 'count'])['values'].reset_index()
    grouped = grouped[grouped['count'] >= min_balls]

    mean_norm = (grouped['mean'] - grouped['mean'].min()) / (grouped['mean'].max() - grouped['mean'].min())

    colours = plt.get_cmap(cmap)(mean_norm)

    grouped['colours'] = [tuple(x) for x in colours.tolist()]

    fig = plt.figure()
    fig.set_size_inches(8, 5)
    fig.subplots_adjust(left=0,
                        right=1,
                        bottom=-0.2,
                        top=2)  # Get rid of some excess whitespace - adjust to taste

    ax = plt.gca(projection='3d')

    plot_wicket_3d(ax,
                   view='front',
                   pitch_colour=pitch_colour,
                   marking_colour=marking_colour,
                   outline_colour=outline_colour,
                   stump_colour=stump_colour,
                   wicket_colour=wicket_colour)

    for row in grouped.itertuples():
        x = [row.x_binned.left,
             row.x_binned.right,
             row.x_binned.right,
             row.x_binned.left]
        y = [row.y_binned.left,
             row.y_binned.left,
             row.y_binned.right,
             row.y_binned.right]
        z = [0, 0, 0, 0]
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(art3d.Poly3DCollection(verts,
                                                   edgecolors=outline_colour,
                                                   facecolors=row.colours,
                                                   alpha=0.9,
                                                   linewidths=0.5,
                                                   zorder=0))

    legend_ypos = np.linspace(10,0,6)

    legend_labels = np.linspace(grouped['mean'].max(), grouped['mean'].min(), 6)
    if measure == 'strike_rate':
        legend_labels = legend_labels*100
    elif measure == 'economy':
        legend_labels = legend_labels*6

    legend_colours = plt.get_cmap(cmap)([y/10 for y in legend_ypos])
    colour_tuples = [tuple(x) for x in legend_colours.tolist()]
    for ypos in legend_ypos:
        x = [-2.3,-2.6,-2.6,-2.3]
        y = [ypos, ypos, ypos+2, ypos+2]
        z = [0,0,0,0]
        count = int(ypos/2)
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(art3d.Poly3DCollection(verts,
                                                   edgecolors=outline_colour,
                                                   facecolors=colour_tuples[count],
                                                   alpha=0.9,
                                                   linewidths=0.5,
                                                   zorder=0))

        if measure == 'strike_rate':
            ax.text(x[0]+0.20, y[0]+1, z[0], f'{legend_labels[count]*1:.0f}', fontproperties=fp, size=12, c=outline_colour, ha='center', va='center')
        else:
            ax.text(x[0]+0.20, y[0]+1, z[0], f'{legend_labels[count]*1:.1f}', fontproperties=fp, size=12, c=outline_colour, ha='center', va='center')

    ax.text(-2.4,-1,0,legend_title, fontproperties=fp, size=17, c=outline_colour, ha='center', va='center')

    add_title_axis(fig,
                   title,
                   subtitle_1,
                   subtitle_2,
                   fp=fp,
                   title_colour=title_colour,
                   subtitle_colour=subtitle_colour)
