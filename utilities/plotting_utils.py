""" Module containing extra cricket wicket plotting functions"""

from matplotlib.patches import PathPatch
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib.font_manager as fm


def text3d(ax, xyz, s, zdir="z", size=None, angle=0, usetex=False, facecolor='black', edgecolor='black', **kwargs):
    """
    https://matplotlib.org/stable/gallery/mplot3d/pathpatch3d.html

    Plots the string *s* on the axes *ax*, with position *xyz*, size *size*,
    and rotation angle *angle*. *zdir* gives the axis which is to be treated as
    the third dimension. *usetex* is a boolean indicating whether the string
    should be run through a LaTeX subprocess or not.  Any additional keyword
    arguments are forwarded to `.transform_path`.

    Note: zdir affects the interpretation of xyz.
    """

    x, y, z = xyz
    if zdir == "y":
        xy1, z1 = (x, z), y
    elif zdir == "x":
        xy1, z1 = (y, z), x
    else:
        xy1, z1 = (x, y), z

    # Load font
    # fname = 'fonts/FiraSans-ThinItalic.ttf'
    # fp = fm.FontProperties(fname=fname)

    text_path = TextPath((0, 0), s, size=size, usetex=usetex) # prop=fp if required
    trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])

    p1 = PathPatch(trans.transform_path(text_path), facecolor=facecolor, edgecolor=edgecolor, fill=True)
    p1.set_alpha(None)  # Very important - needed so alpha is respected
    ax.add_patch(p1)
    art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)


def add_title_axis(fig, title, subtitle_1, subtitle_2, fp, title_colour='black', subtitle_colour='grey'):
    # Add an inset axis for the plot title for nicer (to me at least) behaviour on the 3D axis
    rect = [0, 0.85, 1, 0.15]
    ax_title = fig.add_axes(rect, anchor='NW', facecolor=None)

    # Remove axis markings
    ax_title.set_axis_off()

    # Add titles and subtitles
    # Main title
    ax_title.text(0.18,
                  0.42,
                  title,
                  horizontalalignment='left',
                  fontproperties=fp,
                  size=36,
                  c=title_colour)

    # 1st Subtitle
    ax_title.text(0.18,
                  0.18,
                  subtitle_1,
                  horizontalalignment='left',
                  fontproperties=fp,
                  size=16,
                  c=title_colour)

    # 2nd Subtitle
    ax_title.text(0.18,
                  -0.05,
                  subtitle_2,
                  horizontalalignment='left',
                  fontproperties=fp,
                  size=14,
                  c=subtitle_colour)






