import urllib.request
from owslib.wmts import WebMapTileService
from pathlib import Path
import time

wmts_service_url = "https://julkinen.liikennevirasto.fi/rasteripalvelu/wmts"
system = 'WGS84_Pseudo-Mercator'

wmts = WebMapTileService(wmts_service_url)

empty = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x00\x00\x00\x01\x00\x08\x06\x00\x00\x00\\r\xa8f\x00\x00\x02]IDATx\xda\xed\xd41\x01\x00\x00\x0c\xc20\xfc\x9bf\x06p\xb0\x1c1\xd0\xa3i\x1b\xe0'\x11\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x000\x00\x11\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x000\x00\x11\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x000\x00\x11\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00\xc0\x00\x00\x03\x00\x0c\x000\x00`:C|,\xd4~-z\xb5\x00\x00\x00\x00IEND\xaeB`\x82"

def get_tile(layer_name, tilematrix, z, row, col):
    filename = 'tiledata/{z}/{col}/{row}.png'.format(z=z, row=row, col=col)
    path = Path(filename)
    if path.exists():
        return path

    tile = wmts.gettile(
        layer=layer_name,
        tilematrixset=system,
        tilematrix=tilematrix,
        row=row,
        column=col,
        format="image/png"
    )

    tiledata = tile.read()
    if tiledata == empty:
        print("Empty")
        return None

    path.parent.mkdir(parents=True, exist_ok=True)
    out = open(path, 'wb')
    out.write(tile.read())
    out.close()

    return filename

def save_layer(layer_name, z, tilematrixsetlinks):
    name = system+":"+str(z)
    limits = tilematrixsetlinks.get(system).tilematrixlimits.get(name)
    row_range, col_range = row_and_col_range(limits)
    for row in row_range:
        for col in col_range:
            get_tile(layer_name, name, z, row, col)

def row_and_col_range(limits):
    return (range(limits.mintilerow, limits.maxtilerow+1), range(limits.mintilecol, limits.maxtilecol+1))

def find_layer(z, x, y):
    for _z in range(z, 16):
        for layer_name, layer in list(wmts.contents.items()):
            limits = layer.tilematrixsetlinks.get(system).tilematrixlimits.get(system+":"+str(_z))
            row_range, col_range = row_and_col_range(limits)
            if y in row_range and x in col_range:
                return layer_name

    print("\n",z,x,y,"\n")

#print(find_layer(tz, tx, ty))

"""
for layer_name, layer in list(wmts.contents.items()):
    limits = layer.tilematrixsetlinks.get(system).tilematrixlimits.get(system+":15")
    row_range, col_range = row_and_col_range(limits)
    print(layer_name)
    print(len(row_range), len(col_range))
    print("\n")
    #if y in row_range and x in col_range:
    #    return layer_name

"""
w = 256
h = 256
from PIL import Image

n = 10

#new_im = Image.new('RGB', (w*n, h*n))
c = 0
for layer_name, layer in list(wmts.contents.items())[:1]:
    limits = layer.tilematrixsetlinks.get(system).tilematrixlimits.get(system+":15")
    row_range, col_range = row_and_col_range(limits)
    print(len(row_range), len(col_range))
    """
    for x, row in enumerate(row_range):
        for y, col in enumerate(col_range):
            filename = get_tile(layer_name, system+":15", 15, row, col)
            if filename:
                print(filename)
                c+=1
            #img = Image.open(filename)
            #new_im.paste(img, (y*w, x*h))
    """
    #if y in row_range and x in col_range:
    #    return layer_name

print(c)
#new_im.save('test.png')