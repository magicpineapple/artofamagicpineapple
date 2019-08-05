# Import weird hover stuff
import json
from textwrap import dedent as d
import json
from dash.dependencies import Input, Output

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

print('Sup')

# Important variables
imageList = []
# Number of cols to display (CHANGE)
size = 10
# Display bar width
barWidth=1
# Image director path
imgDirectory = 'assets/images/'
imgType = '.jpg'

# CLASS: images
class ImageObject:
  def __init__(self, index, filepath, name, color, hue, hueScore, width, height):
    self.index = index
    self.filepath = filepath
    self.name = name
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
        tempData = go.Bar(
            name=image.name, 
            width=barWidth, 
            x=sizeArray, 
            y=tempY, 
            marker_color=image.color, 
            text = image.name + " " + image.color, 
            hoverinfo="text",
        )
        graphData.append(tempData)
    return graphData

# FUNCTION: scale image fof graph
def getScaledSize(width, height, barWidth):
    scaledHeight = (height / width) * barWidth
    scaledSize = [barWidth, scaledHeight]
    return scaledSize

# FUNCTION: store data as JSON
def storeAsJson(dataList):
    jsonData = {}
    jsonData['imageData'] = []
    for data in dataList:
        jsonData['imageData'].append({
            'index': data.index,
            'filepath': data.filepath,
            'name': data.name,
            'color': data.color,
            'hue': data.hue,
            'hueScore': data.hueScore,
            'width': data.width,
            'height': data.height
        })
    with open('assets/data.json', 'w') as outfile:
        json.dump(jsonData, outfile)

# FUNCTION: replace \ in PATH with /
def getNewFilepath(oldfilepath):
    return oldfilepath.replace("\\", "/")

# FUNCTION: generate string name from filepath
def getImgName(filepath):
    # Remove director path
    name = filepath.replace(imgDirectory, "")
    # Remove file extension
    name = name.replace(imgType, "")
    # Replace - with " "
    name = name.replace("-", " ")
    # Capitalize first letters
    nameList = list(name)
    for i in range(len(nameList)):
        if i == 0:
            letter = nameList[i].capitalize()
            nameList[i] = letter
        elif nameList[i - 1] == " ": # Space before letter
            letter = nameList[i].capitalize()
            nameList[i] = letter
    return "".join(nameList)

# Assign index var to each image, use to match Dash block to image
index = -1

# Loop through all images
for filepath in glob.iglob(imgDirectory+'*' + imgType):
    # Importatn variables
    WIDTH = 128
    HEIGHT = 128
    index = index + 1
    # Number colors to extract (CHANGE)
    CLUSTERS = 1

    # Open image with Pillow, use orig PATH var
    image = Image.open(filepath)

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
    tempImageObject = ImageObject(index, getNewFilepath(filepath), getImgName(getNewFilepath(filepath)), hex_color, hue, hueScore, new_width, new_height)
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

# Create, store data in JSON file
storeAsJson(imageList)

# Print imageList
for image in imageList:
    print(image.index)
    print(image.filepath)
    print(image.name)
    print(image.color)
    print(image.hue)
    print(image.hueScore)
    print(image.width)
    print(image.height)
    print()

################################################ CREATE GRAPH

# Array size based on size var
sizeArray = []
for i in range(size):
    sizeArray.append(i+1)

graphData = getImageListData(imageList)

fig = go.Figure(data=graphData)
fig.update_xaxes(dtick=barWidth, showticklabels=False, gridcolor="white")
fig.update_yaxes(dtick=barWidth, showticklabels=False, gridcolor="white")
fig.update_layout(
    showlegend = False,
    barmode='stack', 
    bargap = 0, 
    plot_bgcolor = '#f2f2f2',
    margin=go.layout.Margin(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0
    ),
    # Keep tick distance same to maintain image ratio
    yaxis = dict(
      scaleanchor = "x",
      scaleratio = 1,
    )
)

# External CSS
external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Crimson+Text|Lato:300|Montserrat&display=swap'
]

# External JS
external_scripts = [
    'https://cdn.plot.ly/plotly-latest.min.js',
    'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'
]

# Display results
app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)
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
                    html.Img(
                        id="imgDisplay",
                    ),
                    html.H3(
                        id="imgCaption"
                    )
                ]
            )
        ]
    )
])

###################### Hover gallery stuff 

# Update image
@app.callback(dash.dependencies.Output('imgDisplay', 'src'), # CHANGE THIS
              [dash.dependencies.Input('graph', 'hoverData')])
def updateImg(hoverData):
    index = hoverData['points'][0]['curveNumber']
    image = imageList[index]
    filepath = image.filepath
    print(filepath)
    return filepath

# Update background color
@app.callback(dash.dependencies.Output('col2', 'style'), # CHANGE THIS
              [dash.dependencies.Input('graph', 'hoverData')])
def updateImgBackground(hoverData):
    index = hoverData['points'][0]['curveNumber']
    image = imageList[index]
    color = image.color
    return {
        'background-color': color
    }

if __name__ == '__main__':
    app.run_server()  