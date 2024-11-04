from flask import Flask, render_template, request, send_from_directory, redirect
import os
import yaml

app = Flask(__name__)

# Load config
yml = {}
domain = ""
if not os.path.exists("/app/config.yaml"):
    raise Exception("/app/config.yaml file not found")
with open("/app/config.yaml", 'r') as fh:
    yml = yaml.safe_load(fh)
    domain = yml["domain"]

def map_entity(entityId):
    for idp in yml['idps']:
        if idp['entityId'] == entityId:
            return idp['drive']
    return f"https://extern.{domain}"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET'])
def index():
    disco_url = f'https://service.seamlessaccess.org/ds/?entityID=https%3A%2F%2Fidp-proxy.{domain}%2Fsp&return=https%3A%2F%2Fportal.{domain}'

    entityId = request.args.get('entityID')
    if not entityId:
        return redirect(disco_url)
    else:
        return redirect(map_entity(entityId))

