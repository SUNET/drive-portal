from flask import (
    Flask,
    request,
    send_from_directory,
    redirect
)
import os
import yaml

app = Flask(__name__)

# Load config
yml = {}
domain = ""
if not os.path.exists("/config/config.yaml"):
    raise Exception("/config/config.yaml file not found")
with open("/config/config.yaml", 'r') as fh:
    yml = yaml.safe_load(fh)
    domain = yml["domain"]


def map_entity(entityId):
    for idp in yml['idps']:
        if entityId in idp['entityIds']:
            drive = f"https://{idp['id']}.{domain}/index.php/apps/user_saml"
            return f"{drive}/saml/login?idp_hint={entityId}"
    drive = f"https://extern.{domain}/index.php/apps/user_saml"
    return f"{drive}/saml/login?idp_hint={entityId}"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET'])
def index():
    disco_url = "https://service.seamlessaccess.org/ds/"
    disco_url += f"?entityID=https%3A%2F%2Fidp-proxy.{domain}%2Fsp&return="
    disco_url += f"https%3A%2F%2Fportal.{domain}"

    entityId = request.args.get('entityID')
    if not entityId:
        return redirect(disco_url)
    else:
        return redirect(map_entity(entityId))
