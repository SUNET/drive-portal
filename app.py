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
domain = os.environ.get('DRIVE_DOMAIN')
if domain is None:
    raise Exception("DRIVE_DOMAIN environment variable not set")
if not os.path.exists("/app/config.yaml"):
    raise Exception("/app/config.yaml file not found")
with open("/app/config.yaml", 'r') as fh:
    yml = yaml.safe_load(fh)


def map_entity(entityID):
    for idp in yml['idps']:
        if entityID in idp['entityIDs']:
            mid = idp['id']
            # Map customers with different scope than name
            if mid == 'mdh':
                mid = "mdu"
            if mid == 'nordu':
                mid = 'nordunet'
            if mid == 'ri':
                mid = 'sics'

            drive = f"https://{mid}.{domain}/index.php/apps/user_saml"
            return f"{drive}/saml/login?idp_hint={entityID}"
    drive = f"https://extern.{domain}/index.php/apps/user_saml"
    return f"{drive}/saml/login?idp_hint={entityID}"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/status.php')
def status():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'status.json',
                               mimetype='application/json')


@app.route('/', methods=['GET'])
def index():
    disco_url = "https://service.seamlessaccess.org/ds/"
    disco_url += f"?entityID=https%3A%2F%2Fidp-proxy.{domain}%2Fsp&return="
    disco_url += f"https%3A%2F%2Fportal.{domain}"

    entityID = request.args.get('entityID')
    if not entityID:
        return redirect(disco_url)
    else:
        return redirect(map_entity(entityID))


@app.errorhandler(404)
def page_not_found(error):
    return redirect('/')
