from flask import Flask, render_template
import os

drive_sites = []
sites = [
    "antagning", "bth", "chalmers", "du", "esh", "extern", "fhs", "gih", "gu",
    "hb", "hh", "hhs", "hig", "his", "hj", "hkr", "hv", "irf", "kau", "kb",
    "ki", "kkh", "kmh", "konstfack", "kth", "kva", "liu", "lnu", "ltu", "lu",
    "mau", "mdu", "miun", "nordunet", "nrm", "oru", "rkh", "scilifelab", "shh",
    "sics", "slu", "smhi", "sp", "su", "sunet", "suni", "swamid", "ths", "uhr",
    "umu", "uniarts", "uu", "vinnova", "vr"
]

for site in sorted(sites):
    caption = f"{site}"
    href = f"https://{caption}.drive.test.sunet.se/"
    drive_sites.append({"href": href, "caption": caption})

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", drive_sites=drive_sites)
