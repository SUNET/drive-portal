from flask import Flask, render_template, request, redirect
from urllib.parse import unquote
import os
import yaml
import json
import base64

app = Flask(__name__)
drive_sites = []
if not os.path.exists("/app/config.yaml"):
    raise Exception("/app/config.yaml file not found")
with open("/app/config.yaml", 'r') as fh:
    yml = yaml.safe_load(fh)
    sites = yml["sites"]
    domain = yml["domain"]

    for site in sorted(sites):
        caption = f"{site}"
        href = f"https://{caption}.{domain}/"
        drive_sites.append({"href": href, "caption": caption})


@app.route('/', methods=['GET'])
def index():
    user_info = {}
    url_encoded = request.args.get('context')
    relay_state = request.args.get('RelayState')
    if url_encoded:
        base64_decoded = base64.b64decode(unquote(url_encoded))
        obj = json.loads(base64_decoded)
        site = obj['service'].removesuffix(
            '/index.php/apps/user_saml/saml/metadata')
        return redirect(site, code=302)
    elif relay_state:
        user_info['site'] = relay_state.removeprefix('https://').removesuffix('/index.php/apps/user_saml/saml/sls')
    return render_template("index.html",
                           drive_sites=drive_sites,
                           domain=domain,
                           user_info=user_info)
