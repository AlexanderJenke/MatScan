import base64
import json
import uuid
from io import BytesIO

import numpy as np
from PIL import Image, ImageEnhance
from flask import Flask, send_from_directory, render_template, request

import decoder

app = Flask("MatScan", static_url_path='')
with open("PZN.csv", 'r') as PZNs:
    PZN_LUT = {pzn.split(';')[1].zfill(8): pzn.split(';')[0] for pzn in PZNs}


@app.route('/')
def page():
    """Returns the page body
    Sets the session cookie if not existent. (uuid4.hex)
    :return: return the Frontend according to the page controller
    """
    return render_template("scan.html")


@app.route('/auto')
def autoscan():
    """Returns the page body
    Sets the session cookie if not existent. (uuid4.hex)
    :return: return the Frontend according to the page controller
    """
    return render_template("scan.html", auto=True)


@app.route('/scan', methods=["POST"])
def scan():
    img = Image.open(BytesIO(base64.b64decode(request.get_data().split(b'base64,')[-1]))).convert('L')
    im = np.array(ImageEnhance.Contrast(img).enhance(2.0))
    codes = decoder.decode(im)
    if len(codes):
        print(codes[0])
        if codes[0]['dfi'] == 'UNKONWN':
            text = f"<b>Code ungültig!</b> {codes[0]['RAW']}"
            codes = []
        else:
            text = f"<b>{PZN_LUT[codes[0]['PZN']]}</b> Exp: 20{codes[0]['EXP'][:2]}-{codes[0]['EXP'][2:4]}"
    else:
        text = "<b>Kein Code erkannt!</b>"

    u = uuid.uuid4().hex

    return json.dumps({'content': render_template('alert_template.html',
                                                  content=text,
                                                  type='info' if len(codes) else 'danger',
                                                  uuid=u),
                       'uuid': u,
                       }), 200 if len(codes) else 404


@app.route('/img/<path:path>')
def images(path):
    """ Handles requests for image data.
    :param path: path to image
    :return: requested image
    """
    return send_from_directory('static/img', path)


@app.route('/webfonts/<path:path>')
def fonts(path):
    """ Handles requests for web font.
    :param path: path to web font
    :return: requested web font
    """
    return send_from_directory('static/webfonts', path)


@app.route("/css/<path:path>")
def css(path):
    """ Handles requests for css file.
    :param path: path to css file
    :return: requested css file
    """
    return send_from_directory("static/css", path)


@app.route("/js/<path:path>")
def javascript(path):
    """ Handles requests for javascript file.
    :param path: path to javascript file
    :return: requested javascript file
    """
    return send_from_directory("static/js", path)


if __name__ == '__main__':
    app.run(
        host="10.0.0.20",
        port=8080,
        ssl_context=('cert.pem', 'key.pem'))
