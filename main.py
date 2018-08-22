from owslib.wmts import WebMapTileService
from pathlib import Path
from flask import Flask, render_template, send_file, abort
app = Flask(__name__)


wmts_service_url = "https://julkinen.liikennevirasto.fi/rasteripalvelu/wmts"
system = 'WGS84_Pseudo-Mercator'

wmts = WebMapTileService(wmts_service_url)

def row_and_col_range(limits):
    return (range(limits.mintilerow, limits.maxtilerow+1), range(limits.mintilecol, limits.maxtilecol+1))

def find_layer(z, x, y):
    for _z in range(z, 16)++range(5, z+1):
        for layer_name, layer in list(wmts.contents.items()):
            limits = layer.tilematrixsetlinks.get(system).tilematrixlimits.get(system+":"+str(_z))
            row_range, col_range = row_and_col_range(limits)
            if y in row_range and x in col_range:
                return (_z, layer_name)

    return "asd"

def save_tile(path, z, x, y):
    z, layer_name = find_layer(int(z), x, y)
    tilematrix = system+":"+z

    if not layer_name:
        print("\n",z,x,y,"\n")
        print("\n"+find_layer(int(z), x, y)+"\n")
        abort(404)

    tile = wmts.gettile(
        layer="liikennevirasto:Merikarttasarja B",
        tilematrixset=system,
        tilematrix=tilematrix,
        column=x,
        row=y,
        format="image/png"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    out = open(path, 'wb')
    out.write(tile.read())
    out.close()

def format_path(z, x, y):
    return Path('tiledata/{z}/{x}/{y}.png'.format(z=z, x=x, y=y))

@app.route('/get/<z>/<x>/<y>')
def get_tile(z, x, y):
    path = format_path(z, x, y)

    if not path.exists():
        save_tile(path, z, x, y)

    return send_file(open(path, 'rb'), mimetype='image/png')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0')
