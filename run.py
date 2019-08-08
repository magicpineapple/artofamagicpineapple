# Import weird hover stuff
import json
from textwrap import dedent as d
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

# Important variables
imageList = []
# Number of graph cols to display (CHANGE)
size = 10
# Num colors to display (CHANGE)
numColors = 4
# Display bar width
barWidth = 1
# Image director path
imgDirectory = 'assets/images/'
imgType = '.jpg'
# Font colors
lightFontColor = '#ffffff'
darkFontColor = '#000000'

# CLASS: images
class ImageObject:
  def __init__(self, index, filepath, name, colors, hue, hueScore, width, height):
    self.index = index
    self.filepath = filepath
    self.name = name
    self.colors = colors
    self.hue = hue
    self.hueScore = hueScore
    self.width = width
    self.height = height

# FUNCTION: rgb array to hex string
def rgb2hex(rgb):
    hex = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    return hex

# FUNCTION: hex string to rgb array
def hex2rgb(hex):
    value = hex.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) / 255 for i in range(0, lv, lv // 3))

# FUNCTION: get value from rgb array
def getLightness(rgb):
    hls = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    print("HLS: " + str(hls[0]) + " " + str(hls[1]) + " " + str(hls[2]))
    # Just need lightness
    return hls[1]

# FUNCTION: get hue from rgb array
def getHue(rgb):
    hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    # Just need hue 
    return hsv[0]

# FUNCTION: get hue score using size var
def getHueScore(hue):
    hueScore = math.ceil(hue*size) # Min score is 1, max is size
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
            marker_color=image.colors[0], 
            text = image.name + " " + image.colors[0], 
            hoverinfo="text",
        )
        graphData.append(tempData)
    return graphData

# FUNCTION: scale image fof graph
def getScaledSize(width, height, barWidth):
    scaledHeight = (height / width) * barWidth
    scaledSize = [barWidth, scaledHeight]
    return scaledSize

# FUNCTION: replace \ in PATH with /
def getNewFilepath(oldfilepath):
    return oldfilepath.replace("\\", "/")

# FUNCTION: return true if word does not need capitalized first letter
def keepLowercase(word):
    lowercaseList = ["a", "the", "for", "with", "from", "an"]
    for lowercaseWord in lowercaseList:
        if lowercaseWord == word:
            return True
    return False

# FUNCTION: generate string name from filepath
def getImgName(filepath):
    # Remove director path
    name = filepath.replace(imgDirectory, "")
    # Remove file extension
    name = name.replace(imgType, "")
    # Replace - with " "
    name = name.replace("-", " ")
    # Convert to list
    wordsList = name.split()
    # Capitalize first letters except for articles, short words
    for i in range(len(wordsList)):
        if (i == 0) or (keepLowercase(wordsList[i]) == False):
            lettersList = list(wordsList[i])
            capitalLetter = lettersList[0].capitalize()
            lettersList[0] = capitalLetter
            newWord = "".join(lettersList)
            wordsList[i] = newWord
    return " ".join(wordsList)

# FUNCTION: get font color by color background
def getFontColor(backgroundColor):
    rgbArray = hex2rgb(backgroundColor)
    l = getLightness(rgbArray)
    print("COLORS: " + backgroundColor + " " + str(l))
    if l >= 0.5: # Light background color
        print("Dark font color for " + backgroundColor)
        return darkFontColor
    else: # Dark background
        return lightFontColor

# FUNCTION: create Dash div array for palette 
def createPaletteDivs(colorsList):
    divs = []
    for i in range(len(colorsList)):
        colorDiv = html.Div(
            className = "colorDiv",
            style = {
                'background-color' : colorsList[i], 
                'color' : getFontColor(colorsList[i]),
                'width' : 'calc(100% / ' + str(len(colorsList)) + ')',
                'height' : '100%',
                'display' : 'inline-flex',
                'text-align': 'center'
            },

            children = [
                html.H3(colorsList[i])
            ]   
        )
        divs.append(colorDiv)
    return divs

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

# FUNCTION: print imageLis (for testing)
def printImageList(imageList):
    for image in imageList:
        print(image.index)
        print(image.filepath)
        print(image.name)
        print(image.colors)
        print(image.hue)
        print(image.hueScore)
        print(image.width)
        print(image.height)
        print()

# FUNCTION: return image by matching curve number to imageList
def getImageOnClick(clickData):
    index = int(clickData['points'][0]['curveNumber'])
    image = imageList[index]
    return image

# FUNCTION: return image and caption for col2Content div
def createCol2Content(image):
    col2Content = [
        # Color palette bar
        html.Div(
            id="paletteDiv",
            # Show palette of first image
            children=createPaletteDivs(image.colors)
        ), 
        # Image display 
        html.Div(
            className = "colContent",
            style = {
                'color' : getFontColor(image.colors[0])
            },
            children=[
                html.Img(
                    id="imgDisplay",
                    src=image.filepath
                ),
                       html.H3(image.name)       
            ]
        )
    ]
    return col2Content

# FUNCTION: return ticktext array by size
def getTicktextArray(size):
    ticktextArray = []
    for i in range(size):
        if i == 0:
            ticktextArray.append('RED')
        elif i == (size - 1):
            ticktextArray.append('VIOLET')
        else:
            ticktextArray.append('')
    return ticktextArray

####################################### Run code

# Assign index var to each image, use to match Dash block to image
index = -1

# Loop through all images
for filepath in glob.iglob(imgDirectory+'*' + imgType):
    # Important variables
    WIDTH = 128
    HEIGHT = 128
    index = index + 1

    # Open image with Pillow, use orig PATH var
    image = Image.open(filepath)

    calculate_new_size(image)
    new_width, new_height = calculate_new_size(image)
    image.resize((new_width, new_height), Image.ANTIALIAS)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Create numpy arrays
    img_array = np.array(image)
    img_vector = img_array.reshape((img_array.shape[0] * img_array.shape[1], 3))

    # Create and train ML model
    model = KMeans(n_clusters=numColors)
    labels = model.fit_predict(img_vector)
    label_counts = Counter(labels)
    total_count = sum(label_counts.values())

    # All hex colors
    hex_colors = [
        rgb2hex(center) for center in model.cluster_centers_
    ]

    rgb_color = model.cluster_centers_[0]
    hue = getHue(rgb_color)
    hueScore = getHueScore(hue)
    newFilepath = getNewFilepath(filepath)
    imgName = getImgName(getNewFilepath(filepath))

    # Create image object, add to list
    tempImageObject = ImageObject(index, newFilepath, imgName, hex_colors, hue, hueScore, new_width, new_height)
    imageList.append(tempImageObject)

################################################ CREATE GRAPH

# Array size based on size var 
sizeArray = []
for i in range(size):
    sizeArray.append(i+1)

graphData = getImageListData(imageList)

fig = go.Figure(
    data=graphData
)

fig.update_layout(
    height = 300,
    showlegend = False,
    barmode='stack', 
    bargap = 0, 
    plot_bgcolor = '#f2f2f2',
    margin=go.layout.Margin(
        l=0,
        r=0,
        b=0,
        t=0
    ),
    # Keep tick distance same to maintain image ratio
    yaxis = dict(
      scaleanchor = "x",
      scaleratio = 1,
    ),
    # Label x axis
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="VISIBLE SPECTRUM HUES",
            font=dict(
                family="Arial",
                size=18,
                # color="#a4a4a4"
            )
        ),
        tickmode = 'array',
        tickvals = sizeArray, # red = 1...
        ticktext = getTicktextArray(size)
    )
)

fig.update_xaxes(
    dtick=barWidth, 
    gridcolor="white",
    tick0 = 0,
)

fig.update_yaxes(
    dtick=barWidth, 
    showticklabels=False, 
    gridcolor="white", 
    tick0 = 0
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
                    
                    html.Div(
                        id="col1Header",
                        children=[
                            html.H1('colors of a magic pineapple'),
                    
                            html.H2('click on colored tiles to explore art | works best on desktop | color palettes extracted with python machine learning'),
                        ]
                    ), 

                    html.Div(
                        id="graphDiv",
                        children=[
                            dcc.Graph(
                                id='graph',
                                figure=fig
                            ) 
                        ]
                    )
                
                ]
            )
        ]
    ),

    html.Div(
        id="col2",
        className="col",
        style = {
            'background-color' : imageList[0].colors[0]
        },

        children=createCol2Content(imageList[0])
    )
])

###################### GRAPH INTERACTION
# Update image
@app.callback(dash.dependencies.Output('col2', 'children'), # CHANGE THIS
              [dash.dependencies.Input('graph', 'clickData')])
def updateCol2Content(clickData):
    image = getImageOnClick(clickData)
    return createCol2Content(image)

""" @app.callback(dash.dependencies.Output('imgDisplay', 'src'), # CHANGE THIS
              [dash.dependencies.Input('graph', 'clickData')])
def updateImg(clickData):
    image = getImageOnClick(clickData)
    filepath = image.filepath
    print(filepath)
    return filepath """

# Update background color
@app.callback(dash.dependencies.Output('col2', 'style'), # CHANGE THIS
              [dash.dependencies.Input('graph', 'clickData')])
def updateImgBackground(clickData):
    image = getImageOnClick(clickData)
    mainColor = image.colors[0]
    return {
        'background-color': mainColor
    } 

""" # Update paletteDiv colors
@app.callback(dash.dependencies.Output('paletteDiv', 'children'), # CHANGE THIS
              [dash.dependencies.Input('graph', 'clickData')])
def updatePaletteDiv(clickData):
    image = getImageOnClick(clickData)
    colors = image.colors
    return createPaletteDivs(colors) """

if __name__ == '__main__':
    app.run_server()  