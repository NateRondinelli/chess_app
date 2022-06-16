# https://stackoverflow.com/questions/55943631/putting-svg-images-into-tkinter-frame
# User erentknn on Oct 7, 2021 at 20:53

from pylunasvg import Document
import numpy as np
from urllib import request
from PIL import Image

contents = request.urlopen("https://betacssjs.chesscomfiles.com/bundles/web/favicons/safari-pinned-tab.f387b3f2.svg").read()

document = Document.loadFromData(contents)
bitmap = document.renderToBitmap()

svgArray = np.array(bitmap, copy=False)
img = Image.fromarray(svgArray)

# Insert tkinter code here