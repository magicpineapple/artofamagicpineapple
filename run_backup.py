# Import weird hover stuff
import json
from textwrap import dedent as d
import csv

# Import viz stuff
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Import ML stuff
import os
import math
import glob
import colorsys
import numpy as np
from matplotlib import pyplot as plt

from PIL import Image
from collections import Counter
from sklearn.cluster import KMeans

# Guess I don't need this...
# %matplotlib inline

print('Sup')

# Important variables
imageList = []
# Number of cols to display (CHANGE)
size = 10
# Display bar width
barWidth=1

# CLASS: images
class ImageObject:
  def __init__(self, filepath, color, hue, hueScore, width, height):
    self.filepath = filepath
    self.color = color
    self.hue = hue
    self.hueScore = hueScore
    self.width = width
    self.height = height

# FUNCTION: rgb to hex
def rgb2hex(rgb):
    hex = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    return hex

# FUNCTION: get hue from hex color
def getHue(rgb):
    hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    # Just need hue value
    return hsv[0]

# FUNCTION: get hue score using size var
def getHueScore(hue):
    hueScore = math.ceil(hue*size)
    return hueScore


# FUNCTION: prep all images objects for grpah
def getImageListData(imageList):
    graphData = []
    for image in imageList:
        position = image.hueScore
        # Scale size for graph
        scaledSize = getScaledSize(image.width, image.height, barWidth)
        scaledHeight = scaledSize[1]
        # Set up tempY
        tempY = []
        for i in sizeArray:
            if i == position:
                tempY.append(scaledHeight)
            else:
                tempY.append(0)

        tempData = go.Bar(name=image.filepath, width=barWidth, x=sizeArray, y=tempY, marker_color=image.color, text = image.color, hoverinfo="name + y + text")
        graphData.append(tempData)
    return graphData

# FUNCTION: scale image fof graph
def getScaledSize(width, height, barWidth):
    scaledHeight = (height / width) * barWidth
    scaledSize = [barWidth, scaledHeight]
    return scaledSize

# Loop through all images
for filepath in glob.iglob('images/*.jpg'):
    # Importatn variables
    PATH = filepath
    WIDTH = 128
    HEIGHT = 128
    # Number colors to extract (CHANGE)
    CLUSTERS = 1

    # Open image with Pillow
    image = Image.open(PATH)

    # FUNCTION: make image smaller so ML faster
    def calculate_new_size(image):
        if image.width >= image.height:
            wpercent = (WIDTH / float(image.width))
            hsize = int((float(image.height) * float(wpercent)))
            new_width, new_height = WIDTH, hsize
        else:
            hpercent = (HEIGHT / float(image.height))
            wsize = int((float(image.width) * float(hpercent)))
            new_width, new_height = wsize, HEIGHT
        return new_width, new_height

    calculate_new_size(image)
    new_width, new_height = calculate_new_size(image)
    image.resize((new_width, new_height), Image.ANTIALIAS)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Create numpy arrays
    img_array = np.array(image)
    img_vector = img_array.reshape((img_array.shape[0] * img_array.shape[1], 3))

    # Create and train ML model
    model = KMeans(n_clusters=CLUSTERS)
    labels = model.fit_predict(img_vector)
    label_counts = Counter(labels)
    total_count = sum(label_counts.values())

    hex_colors = [
        rgb2hex(center) for center in model.cluster_centers_
    ]

    list(zip(hex_colors, list(label_counts.values())))

    # Just need first hex color
    hex_color = hex_colors[0]
    rgb_color = model.cluster_centers_[0]
    hue = getHue(rgb_color)
    hueScore = getHueScore(hue)

    # Create image object, add to list
    tempImageObject = ImageObject(filepath, hex_color, hue, hueScore, new_width, new_height)
    imageList.append(tempImageObject)

    # Visualize results
    # plt.figure(figsize=(14, 8))
    # plt.subplot(221)
    # plt.imshow(image)
    # plt.axis('off')

    # plt.subplot(222)
    # plt.pie(label_counts.values(), labels=hex_colors, colors=[color / 255 for color in model.cluster_centers_], startangle=90)
    # plt.axis('equal')
    # plt.show()

# Print imageList
for image in imageList:
    print(image.filepath)
    print(image.color)
    print(image.hue)
    print(image.hueScore)
    print(image.width)
    print(image.height)

################################################ CREATE GRAPH

# Array size based on size var
sizeArray = []
for i in range(size):
    sizeArray.append(i+1)

fig = go.Figure(data=getImageListData(imageList))
fig.update_xaxes(dtick=barWidth, showticklabels=False, gridcolor="white")
fig.update_yaxes(dtick=barWidth, showticklabels=False, gridcolor="white")
fig.update_layout(
    showlegend = False,
    barmode='stack', 
    bargap = 0, 
    plot_bgcolor = '#f2f2f2',
    # Keep tick distance same to maintain image ratio
    yaxis = dict(
      scaleanchor = "x",
      scaleratio = 1,
    )
)

# Hover

# Google Fonts
external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Crimson+Text|Lato:300|Montserrat&display=swap'
]

# Display results
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    # Graph here
    html.Div(
        id="col1",
        className = "col",
        children=[
            html.Div(
                className = "colContent",
                children=[
                    html.H1('art of a magic pineapple'),
                    html.H2('storytelling through digital art'),

                    dcc.Graph(
                        id='graph',
                        figure=fig
                    )
                
                ]
            )
        ]
    ),

    html.Div(
        id="col2",
        className="col",
        children=[

            html.Div(
                className = "colContent",
            
                children=[
                    
                ]
            )
        ]
    )
])

if __name__ == '__main__':
    app.run_server()