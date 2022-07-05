"""
Plotting template for a bowling pitch map with overlaid 2D density, which utilises the front view of the plot_wicket_3d
function.

"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.font_manager as fm
from pitch_views.wicket_3d import plot_wicket_3d
from utilities.plotting_utils import add_title_axis


# Helper function to get gaussian kde for plotting - returns X,Y grid and Z density
def get_density(data):
    xmin = min(data[:, 0])
    xmax = max(data[:, 0])
    ymin = min(data[:, 1])
    ymax = max(data[:, 1])

    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])

    kernel = gaussian_kde(data.T, bw_method=0.30)
    Z = np.reshape(kernel(positions).T, X.shape)
    return X, Y, Z


def pitch_densitymap(xy, title='', subtitle_1='', subtitle_2=''):

    """ Plots a heatmap overlaid on wicket_3d front view, using a specified values array for square shading

    ----------
    xy: A 2d array
        The x and y coordinates of the delivery pitching locations
    title: A string
        The plot title
    subtitle_1: A string
        The plot's 1st subtitle
    subtitle_2: A string
        The plot's 2nd subtitle

    Returns
    -------
    matplotlib.axes.Axes"""

    # Define some styling
    pitch_colour = 'white'
    wicket_colour = '#f5f6fa'
    marking_colour = 'cornflowerblue'
    stump_colour = 'slategray'
    outline_colour = 'lightsteelblue'
    title_colour = '#080a2e'
    subtitle_colour = '#9e9fa3'
    fname = 'fonts/AlumniSans-SemiBold.ttf'
    fp = fm.FontProperties(fname=fname)

    X, Y, Z = get_density(xy)

    # Plot a 2D KDE plot of the delivery pitch locations on a 3D pitch

    fig = plt.figure()
    fig.set_size_inches(8, 5)
    fig.subplots_adjust(left=0,
                        right=1,
                        bottom=-0.2,
                        top=2)  # Get rid of some excess whitespace - adjust to taste

    ax = plt.gca(projection='3d')  # We'll plot on a 3D axis

    # We have data for a 3D surface plot, but we want to plot a 2D surface on the xy plane, so we'll set the Z axis
    # to zeros
    z_axis = np.zeros(X.shape)

    # We will manually set the colours of the surface based on the actual Z data using facecolors argument of
    # ax.plot_surface
    colours = plt.cm.PuRd(Z)

    # A trick to apply gradual alpha shading to the surface plot for cleaner looking visual

    for i in range(len(colours)):
        plane = colours[i]
        for j in range(len(plane)):
            row = plane[j]
            if (row[0:3].mean() >= 0.87) & (row[0:3].mean() < 0.92):
                row[3] = 0.25
            elif row[0:3].mean() >= 0.92:
                row[3] = 0

    # Plot the surfaces
    ax.plot_surface(X,
                    Y,
                    z_axis,
                    cmap='Purples',
                    facecolors=colours,
                    linewidth=1,
                    antialiased=False)

    # Plot the pitch points as a scatter overlaid
    # ax.scatter(xy[:, 0], xy[:, 1], c='blue', edgecolor='black', alpha=0.5, zorder=9)


    # Add titles and subtitles
    add_title_axis(fig,
                   title,
                   subtitle_1,
                   subtitle_2,
                   fp=fp,
                   title_colour=title_colour,
                   subtitle_colour=subtitle_colour)

    # Generate a cricket pitch on the axis we created
    plot_wicket_3d(ax,
                   view='front',
                   pitch_colour=pitch_colour,
                   marking_colour=marking_colour,
                   outline_colour=outline_colour,
                   stump_colour=stump_colour,
                   wicket_colour=wicket_colour)
