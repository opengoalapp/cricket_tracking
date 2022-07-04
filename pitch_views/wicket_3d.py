from matplotlib import colors
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib.font_manager as fm


def plot_wicket_3d(ax,
                   stumps_guide=True,
                   view='front',
                   pitch_colour='white',
                   wicket_colour='#f5f6fa',
                   wicket_alpha=0.1,
                   outline_colour='silver',
                   marking_colour='navy',
                   stump_colour='slategray',
                   guide_colour='royalblue'):

    """ Plots a standard cricket wicket to regulation dimensions in metres - centre of the middle stump is (0,0)

    ----------
    ax: A matplotlib axis where ax = plt.gca(projection='3d')
        The 3D axes to plot on.
    view: Camera angle for plot - either "front", "back", "top"
    stumps_guide: Boolean - stumps line guide overlay will be added if True
    pitch_colour: A matplotlib named colour string OR an RGBA (0-1) tuple
        The colour of the outfield pitch floor.
    wicket_colour: Any valid matplotlib colour
        The colour of the wicket pitch
    wicket_alpha: Float
        The alpha value (transparency) of the wicket colour
    outlineline_colour: Any valid matplotlib colour
        The colour of the wicket outline.
    marking_colour: Any valid matplotlib colour
        The colour of the pitch line markings.
    stump_colour: Any valid matplotlib colour
        The colour of the stumps.
    guide_colour: Any valid matplotlib colour
        The colour of shaded stumps line overlay.

    Returns
    -------
    matplotlib.axes.Axes"""

    fname = 'fonts/AlumniSans-SemiBold.ttf'
    fp = fm.FontProperties(fname=fname)

    if view == 'front':
        PITCH_X_BOUND = 0.5
        PITCH_Y_BOUND = 5
        STUMP_LINEWIDTH = 3
        BEHIND_STUMPS_Y_LIMIT = -2

        ax.view_init(elev=9, azim=90)

    elif view == 'back':
        PITCH_X_BOUND = -0.9
        PITCH_Y_BOUND = -1
        STUMP_LINEWIDTH = 5
        BEHIND_STUMPS_Y_LIMIT = -2

        ax.view_init(elev=2, azim=-90)

    elif view == 'top':
        PITCH_X_BOUND = 1
        PITCH_Y_BOUND = 10
        STUMP_LINEWIDTH = 2
        BEHIND_STUMPS_Y_LIMIT = -10

        ax.view_init(elev=90, azim=90)

    PITCH_Z_BOUND = 3

    WICKET_LENGTH = 22.56
    WICKET_WIDTH = 3.66

    BATTING_CREASE_LENGTH = 1.22
    BOWLING_CREASE_WIDTH = 2.64

    STUMP_HEIGHT = 0.7112
    STUMP_WIDTH = 0.03943
    STUMP_GAP = 0.08893

    min_h = 0  # Z height to plot court lines - 99% use cases will be ground level i.e. 0

    ax.set_xlim3d([-PITCH_X_BOUND, PITCH_X_BOUND])
    ax.set_ylim3d([BEHIND_STUMPS_Y_LIMIT, PITCH_Y_BOUND])
    ax.set_zlim3d([0, PITCH_Z_BOUND])

    # Plot wicket side lines
    ax.plot([-WICKET_WIDTH / 2, -WICKET_WIDTH / 2], [-BATTING_CREASE_LENGTH, WICKET_LENGTH - BATTING_CREASE_LENGTH],
            min_h, c=outline_colour, lw=0.5, zorder=1)
    ax.plot([WICKET_WIDTH / 2, WICKET_WIDTH / 2], [-BATTING_CREASE_LENGTH, WICKET_LENGTH - BATTING_CREASE_LENGTH],
            min_h, c=outline_colour, lw=0.5, zorder=1)

    # Plot wicket end lines
    ax.plot([-WICKET_WIDTH / 2, WICKET_WIDTH / 2],
            [WICKET_LENGTH - BATTING_CREASE_LENGTH, WICKET_LENGTH - BATTING_CREASE_LENGTH],
            min_h, c=outline_colour, lw=0.5, zorder=1)
    ax.plot([-WICKET_WIDTH / 2, WICKET_WIDTH / 2], [-BATTING_CREASE_LENGTH, -BATTING_CREASE_LENGTH],
            min_h, c=outline_colour, lw=0.5, zorder=1)

    # Plot batting crease
    ax.plot([-WICKET_WIDTH / 2, WICKET_WIDTH / 2], [BATTING_CREASE_LENGTH, BATTING_CREASE_LENGTH],
            min_h, c=marking_colour, zorder=1)

    # Plot bowling crease
    ax.plot([-BOWLING_CREASE_WIDTH / 2, BOWLING_CREASE_WIDTH / 2], [0, 0],
            min_h, c=marking_colour, zorder=1)

    # Plot return creases
    ax.plot([-BOWLING_CREASE_WIDTH / 2, -BOWLING_CREASE_WIDTH / 2], [BATTING_CREASE_LENGTH, -BATTING_CREASE_LENGTH],
            min_h, c=marking_colour, zorder=1)
    ax.plot([BOWLING_CREASE_WIDTH / 2, BOWLING_CREASE_WIDTH / 2], [BATTING_CREASE_LENGTH, -BATTING_CREASE_LENGTH],
            min_h, c=marking_colour, zorder=1)

    # Draw stumps
    x = [0, 0]
    y = [0, 0]
    z = [0, STUMP_HEIGHT]
    ax.plot(x, y, z, color=stump_colour, linewidth=STUMP_LINEWIDTH, zorder=10)

    x = [STUMP_GAP, STUMP_GAP]
    y = [0, 0]
    z = [0, STUMP_HEIGHT]
    ax.plot(x, y, z, color=stump_colour, linewidth=STUMP_LINEWIDTH, zorder=10)

    x = [-STUMP_GAP, -STUMP_GAP]
    y = [0, 0]
    z = [0, STUMP_HEIGHT]
    ax.plot(x, y, z, color=stump_colour, linewidth=STUMP_LINEWIDTH, zorder=10)

    if stumps_guide == True:
        # Draw stumps line guide

        x = [STUMP_GAP + STUMP_WIDTH / 2, -STUMP_GAP - STUMP_WIDTH / 2, -STUMP_GAP - STUMP_WIDTH / 2,
             STUMP_GAP + STUMP_WIDTH / 2]
        y = [0, 0, WICKET_LENGTH - BATTING_CREASE_LENGTH, WICKET_LENGTH - BATTING_CREASE_LENGTH]
        z = [0, 0, 0, 0]
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(art3d.Poly3DCollection(verts,
                                                   facecolors=guide_colour,
                                                   alpha=0.1))

    # Draw a pitch surface
    x = [WICKET_WIDTH / 2,
         -WICKET_WIDTH / 2,
         -WICKET_WIDTH / 2,
         WICKET_WIDTH / 2]
    y = [WICKET_LENGTH - BATTING_CREASE_LENGTH,
         WICKET_LENGTH - BATTING_CREASE_LENGTH,
         -BATTING_CREASE_LENGTH,
         -BATTING_CREASE_LENGTH]
    z = [0, 0, 0, 0]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(art3d.Poly3DCollection(verts,
                                               facecolors=wicket_colour,
                                               alpha=wicket_alpha,
                                               zorder=0))

    # Get rid of colored axes planes
    # First remove fill
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = True

    # Now set color to white (or whatever is "invisible")
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')

    # We accept either RGBA (0,1) or matplotlib named colour string
    if isinstance(pitch_colour, str):
        ax.w_zaxis.set_pane_color(colors.to_rgba(pitch_colour, 1))
    else:
        ax.w_zaxis.set_pane_color(pitch_colour)

    # Remove grid
    ax.grid(False)
    #
    # Remove tick labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    # Transparent spines
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    # No ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    #
    ax.set_box_aspect(
        (2 * PITCH_X_BOUND, PITCH_Y_BOUND - BEHIND_STUMPS_Y_LIMIT, PITCH_Z_BOUND))  # max - min for each axis

    # Plot ruler on the surface of the pitch - text angle is in radians
    for dist in [2, 4, 6, 8, 10]:
        # Plot text labels on pitch surface
        # text3d(ax, (2.5, dist, 0),
        #        '{0}m'.format(dist),
        #        zdir="z", size=0.25, usetex=False, angle=np.pi,
        #        facecolor='black', edgecolor=outline_colour)

        # Plot text labels as a regular text label
        ax.plot([-2, 2], [dist, dist], 0, c=marking_colour, alpha=0.2, ls='--', lw=1)
        ax.text(2.1, dist, 0, '{0}m'.format(dist), color=outline_colour, fontproperties=fp, size=12)
