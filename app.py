from flask import Flask, render_template, request
from urllib.parse import unquote
import os
import glob
import yaml
import json
import base64

app = Flask(__name__)

if not os.path.exists("/app/config.yaml"):
    raise Exception("/app/config.yaml file not found")
with open("/app/config.yaml", 'r') as fh:
    yml = yaml.safe_load(fh)
    domain = yml["domain"]

# get languages from files
language_files = glob.glob("i18n/*.json")
languages = {}
for lang in language_files:
    filename = lang.split('/')
    lang_code = filename[1].split('.')[0]
    with open(lang, 'r', encoding='utf8') as file:
        languages[lang_code] = json.loads(file.read())
supported_languages = list(languages.keys())


@app.route('/', methods=['GET'])
def index():
    user_lang = request.accept_languages.best_match(
        supported_languages) or 'sv_SE'
    i18n = languages[user_lang]
    drive_sites = []
    for site_dict in i18n["sites"]:
        site = site_dict['short_name']
        caption = site_dict['full_name']
        external_url = site_dict['domain']
        href = f"https://{site}.{domain}/"
        drive_sites.append({
            "href": href,
            "caption": caption,
            "site": site,
            "external_url": external_url
        })
    user_info = {}
    url_encoded = request.args.get('context')
    relay_state = request.args.get('RelayState')
    if url_encoded:
        user_info['direction'] = 'login'
        base64_decoded = base64.b64decode(unquote(url_encoded))
        obj = json.loads(base64_decoded)
        user_info['displayname'] = obj['displayname']
        user_info['domain'] = obj['user_id'].split('@')[1]
        user_info['site'] = obj['service'].removeprefix(
            'https://').removesuffix('/index.php/apps/user_saml/saml/metadata')
    elif relay_state:
        user_info['direction'] = 'logout'
        user_info['site'] = relay_state.removeprefix('https://').removesuffix(
            '/index.php/apps/user_saml/saml/sls')
    return render_template("index.html",
                           drive_sites=drive_sites,
                           domain=domain,
                           i18n=i18n,
                           user_info=user_info)
