from flask import Flask, render_template, request
import os
import yaml

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



@app.route('/', methods=['GET', 'POST'])
def index():
    user_info = {}
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json' and request.method == 'POST'):
        json = request.get_json()
        # {
        #   "user_id": ...
        #   "displayname": ...
        #   "timestamp": ...
        #   "issuer": ...
        #   "service": ...
        # }
        user_info['displayname'] = json['displayname']
        user_info['domain'] = json['user_id'].split('@')[1]
        user_info['site'] = json['service'].lstrip('https://').rstrip('/index.php/apps/user_saml/saml/metadata')
    return render_template("index.html", drive_sites=drive_sites, domain=domain, user_info=user_info)
