import numpy as np
import matplotlib.pyplot as plt

from flexitext import flexitext

from matplotlib import lines
from matplotlib import patches
from matplotlib.patheffects import withStroke

BROWN = "#AD8C97"
BROWN_DARKER = "#7d3a46"
GREEN = "#2FC1D3"
BLUE = "#076FA1"
GREY = "#C7C9CB"
GREY_DARKER = "#5C5B5D"
RED = "#E3120B"

year = [2008, 2012, 2016, 2020]

latin_america = [10, 9, 7.5, 5.8]
asia_and_pacific = [13.5, 9.5, 7.5, 5.5]
sub_saharan_africa = [25.5, 21, 22.2, 24]
percentages = [sub_saharan_africa, asia_and_pacific, latin_america]

COLORS = [BLUE, GREEN, BROWN]

# Initialize plot ------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_facecolor('white')

# Add lines with dots
# Note the zorder to have dots be on top of the lines
for percentage, color in zip(percentages, COLORS):
    ax.plot(year, percentage, color=color, lw=5)
    ax.scatter(year, percentage, fc=color, s=100, lw=1.5, ec="white", zorder=12)
    
    # Customize axis -------------------------------------------
# Customize y-axis ticks
ax.yaxis.set_ticks([i * 5 for i in range(0, 7)])
ax.yaxis.set_ticklabels([i * 5 for i in range(0, 7)])
ax.yaxis.set_tick_params(labelleft=False, length=0)

# Customize y-axis ticks
ax.xaxis.set_ticks([2008, 2012, 2016, 2020])
ax.xaxis.set_ticklabels([2008, 12, 16, 20], fontsize=16, fontfamily="Econ Sans Cnd", fontweight=100)
ax.xaxis.set_tick_params(length=6, width=1.2)

# Make gridlines be below most artists.
ax.set_axisbelow(True)

# Add grid lines
ax.grid(axis = "y", color="#A8BAC4", lw=1.2)

# Remove all spines but the one in the bottom
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
# ax.spines["left"].set_visible(True)

# # Customize bottom spine
# ax.spines["bottom"].set_visible(True)

# Set custom limits
ax.set_ylim(0, 35)
ax.set_xlim(2007.5, 2021.5)

fig

# Add labels for vertical grid lines -----------------------
# The pad is equal to 1% of the vertical range (35 - 0)
PAD = 35 * 0.01
for label in [i * 5 for i in range(0, 7)]:
    ax.text(
        2021.5, label + PAD, label, 
        ha="right", va="baseline", fontsize=18,
        fontfamily="Econ Sans Cnd", fontweight=100
    )

# Annotate labels for regions ------------------------------

# Note the path effect must be a list
path_effects = [withStroke(linewidth=10, foreground="white")]

# We create a function to avoid repeating 'ax.text' many times
def add_region_label(x, y, text, color, path_effects, ax):
    ax.text(
        x, y, text, color=color,
        fontfamily="Econ Sans Cnd", fontsize=18, 
        va="center", ha="left", path_effects=path_effects
    ) 
region_labels = [
    {
        "x": 2007.9, "y": 5.8, "text": "Latin America and\nthe Caribbean", 
        "color": BROWN_DARKER, "path_effects": path_effects},
    {
        "x": 2010, "y": 13, "text": "Asia and the Pacific", 
        "color": GREEN, "path_effects": []
    },
    {
        "x": 2007.9, "y": 27, "text": "Sub-Saharan Africa", 
        "color": BLUE, "path_effects": []
    },
]    

for label in region_labels:
    add_region_label(**label, ax=ax)

fig

# Add title ------------------------------------------------

# Use flexitext instead of `ax.text()`
text = "<name:Econ Sans Cnd, size:18><weight:bold>Selected regions,</> % of child population</>"
flexitext(0, 0.975, text, va="top", ax=ax)

# This is the small line on top of the title
# Note the 'solid_capstyle' and the 'transform', these are very important.
ax.add_artist(
    lines.Line2D(
        [0, 0.05], [1, 1], lw=2, color="black",
        solid_capstyle="butt", transform=ax.transAxes
    )
)
fig

# stacked area chart

COLORS += [GREY]
counts = [
    [65, 55, 67, 85],
    [130, 85, 65, 50],
    [10, 10, 10, 8],
    [60, 20, 10, 16]
    
]

# Initialize plot ------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))

# Add stacked area
ax.stackplot(year, counts, colors=COLORS, lw=1.5, edgecolor='white');

# Customize y-axis ticks
ax.yaxis.set_ticks([i * 50 for i in range(0, 7)])
ax.yaxis.set_ticklabels([i * 50 for i in range(0, 7)])
ax.yaxis.set_tick_params(labelleft=False, length=0)

# Customize x-axis ticks
ax.xaxis.set_ticks([2008, 2012, 2016, 2020])
ax.xaxis.set_ticklabels([2008, 12, 16, 20], fontsize=16, fontfamily="Econ Sans Cnd", fontweight=100)
ax.xaxis.set_tick_params(length=6, width=1.2)

# Make gridlines be below most artists.
ax.set_axisbelow(True)

# Add grid lines
ax.grid(axis = "y", color="#A8BAC4", lw=1.2)

# Remove all spines but the one in the bottom
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)

# Customize bottom spine
ax.spines["bottom"].set_lw(1.2)
ax.spines["bottom"].set_capstyle("butt")

# Specify both horizontal and vertical limits
ax.set_ylim(0, 350)
ax.set_xlim(2007.5, 2021.5)

fig

# Add labels for vertical grid lines -----------------------
# The pad is equal to 1% of the vertical range (350 - 0)
PAD = 350 * 0.01
for label in [i * 50 for i in range(0, 7)]:
    ax.text(
        2021.5, label + PAD, label, 
        ha="right", va="baseline", fontsize=18,
        fontfamily="Econ Sans Cnd", fontweight=100
    )
    
# Annotate labels for regions ------------------------------
# We use the 'add_region_labels()' function from above
region_labels = [
    {"x": 2013, "y": 225, "text": "Latin America and\nthe Caribbean", "color": BROWN_DARKER, "path_effects":[]},
    {"x": 2013, "y": 100, "text": "Asia and the Pacific", "color": "white", "path_effects":[]},
    {"x": 2013, "y": 25, "text": "Sub-Saharan Africa", "color": "white", "path_effects":[]},
    {"x": 2008.05, "y": 225, "text": "Rest\nof world", "color": GREY_DARKER, "path_effects":[]},
]    

for label in region_labels:
    add_region_label(**label, ax=ax)


# Add custom arrow-like line -------------------------------
# It's not possible to use a dot as an arrowhead.
# So we add an arrow without a head, but we then add a point
# using `ax.scatter()` as shown below
ax.add_artist(
    patches.FancyArrowPatch(
        (2016.25, 214), (2018.5, 137),
        arrowstyle = "Simple", 
        connectionstyle="arc3, rad=-0.45",
        color="k"
    )
)

ax.scatter(2018.5, 138, s=10, color="k")    
    
    
fig

# Add title ------------------------------------------------

# Use flexitext instead of `ax.text()`
text = "<name:Econ Sans Cnd, size:18><weight:bold>Number of children,</> m</>"
flexitext(0, 0.975, text, va="top", ax=ax)

# Same line on top of title
ax.add_artist(
    lines.Line2D(
        [0, 0.05], [1, 1], lw=2, color="black",
        solid_capstyle="butt", transform=ax.transAxes
    )
)

fig

# full chart

fig, axes = plt.subplots(1, 2, figsize=(12, 7.2))
fig.subplots_adjust(left=0, right=1)

# Set background to white. Useful when saving a .png
fig.set_facecolor("white")

def customize_axis(ax):
   # Make gridlines be below most artists.
    ax.set_axisbelow(True)
    ax.set_facecolor("white")
    # Add grid lines
    ax.grid(axis = "y", color="#A8BAC4", lw=1.2)

    # Customize x-axis ticks
    ax.xaxis.set_ticks([2008, 2012, 2016, 2020])
    ax.xaxis.set_ticklabels([2008, 12, 16, 20], fontsize=16, fontfamily="Econ Sans Cnd", fontweight=100)
    ax.xaxis.set_tick_params(length=6, width=1.2)
    
    # Remove all spines but the one in the bottom
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Customize bottom spine
    ax.spines["bottom"].set_lw(1.2)
    ax.spines["bottom"].set_capstyle("butt") 

# Add lines with dots
for percentage, color in zip(percentages, COLORS):
    axes[0].plot(year, percentage, color=color, lw=5)
    axes[0].scatter(year, percentage, fc=color, s=100, lw=1.5, ec="white", zorder=12)

# Customize axis -------------------------------------------
axes[0].yaxis.set_ticks([i * 5 for i in range(0, 7)])
axes[0].yaxis.set_ticklabels([i * 5 for i in range(0, 7)])
axes[0].yaxis.set_tick_params(labelleft=False, length=0)

customize_axis(axes[0])

axes[0].set_ylim(0, 35)
axes[0].set_xlim(2007.5, 2021.5)

# Add labels for vertical grid lines -----------------------
PAD = 35 * 0.01
for label in [i * 5 for i in range(0, 7)]:
    axes[0].text(
        2021.5, label + PAD, label, 
        ha="right", va="baseline", fontsize=18,
        fontfamily="Econ Sans Cnd", fontweight=100
    )

# Annotate labels for regions ------------------------------
path_effects = [withStroke(linewidth=10, foreground="white")]
region_labels = [
    {
        "x": 2007.9, "y": 5.8, "text": "Latin America and\nthe Caribbean", 
        "color": BROWN_DARKER, "path_effects": path_effects},
    {
        "x": 2010, "y": 13, "text": "Asia and the Pacific", 
        "color": GREEN, "path_effects": []
    },
    {
        "x": 2007.9, "y": 27, "text": "Sub-Saharan Africa", 
        "color": BLUE, "path_effects": []
    },
]    

for label in region_labels:
    add_region_label(**label, ax=axes[0])

# Add title ------------------------------------------------
# Use flexitext instead of `ax.text()`
text = "<name:Econ Sans Cnd, size:18><weight:bold>Selected regions,</> % of child population</>"
flexitext(0, 0.975, text, va="top", ax=axes[0])
axes[0].add_artist(
    lines.Line2D(
        [0, 0.05], [1, 1], lw=2, color="black",
        solid_capstyle="butt", transform=axes[0].transAxes
    )
)
fig

# Add stacked area
axes[1].stackplot(year, counts, colors=COLORS, lw=1.5, edgecolor='white');

# Customize axis -------------------------------------------
axes[1].yaxis.set_ticks([i * 50 for i in range(0, 7)])
axes[1].yaxis.set_ticklabels([i * 50 for i in range(0, 7)])
axes[1].yaxis.set_tick_params(labelleft=False, length=0)

customize_axis(axes[1])

axes[1].set_ylim(0, 350)
axes[1].set_xlim(2007.5, 2021.5)

# Add labels for vertical grid lines -----------------------
PAD = 350 * 0.01
for label in [i * 50 for i in range(0, 7)]:
    axes[1].text(
        2021.5, label + PAD, label, 
        ha="right", va="baseline", fontsize=18,
        fontfamily="Econ Sans Cnd", fontweight=100
    )
    

# Annotate labels for regions ------------------------------
region_labels = [
    {"x": 2013, "y": 225, "text": "Latin America and\nthe Caribbean", "color": BROWN_DARKER, "path_effects":[]},
    {"x": 2013, "y": 100, "text": "Asia and the Pacific", "color": "white", "path_effects":[]},
    {"x": 2013, "y": 25, "text": "Sub-Saharan Africa", "color": "white", "path_effects":[]},
    {"x": 2008.05, "y": 225, "text": "Rest\nof world", "color": GREY_DARKER, "path_effects":[]},
]  

for label in region_labels:
    add_region_label(**label, ax=axes[1])


# Add custom arrow-like line -------------------------------
axes[1].add_artist(
    patches.FancyArrowPatch(
        (2016.8, 215), (2019.4, 137),
        arrowstyle = "Simple", 
        connectionstyle="arc3, rad=-0.45",
        color="k"
    )
)

axes[1].scatter(2019.4, 138, s=10, color="k")

# Add title ------------------------------------------------
text = "<name:Econ Sans Cnd, size:18><weight:bold>Number of children,</> m</>"
flexitext(0, 0.975, text, va="top", ax=axes[1])

axes[1].add_artist(
    lines.Line2D(
        [0, 0.05], [1, 1], lw=2, color="black",
        solid_capstyle="butt", transform=axes[1].transAxes
    )
)

fig

# Make room below on top and bottom
fig.subplots_adjust(top=0.825, bottom=0.15)

# Add title
fig.text(
    0, 0.92, "All work, no play", 
    fontsize=22,
    fontweight="bold", 
    fontfamily="Econ Sans Cnd"
)
# Add subtitle
fig.text(
    0, 0.875, "Children in child labour*", 
    fontsize=20, 
    fontfamily="Econ Sans Cnd"
)

# Add caption
source = 'Source: "Child Labour: Global estimates 2020, trends and the road forward", ILO and UNICEF'
fig.text(
    0, 0.06, source, color="#a2a2a2", 
    fontsize=8, fontfamily="Econ Sans Cnd"
)
fig.text(
    1, 0.06, "*5- to 17- year-olds", color="#a2a2a2", ha="right",
    fontsize=14, fontfamily="Econ Sans Cnd"
)
# Add authorship
fig.text(
    0, 0.005, "The Economist", color="#a2a2a2",
    fontsize=16, fontfamily="Milo TE W01"
)

# Add line and rectangle on top.
fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color=RED, solid_capstyle="butt"))
fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color=RED))
fig

# If you want to save the plot to see it in better quality
#fig.savefig("plot.png", dpi=300)





