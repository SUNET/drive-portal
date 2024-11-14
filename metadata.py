#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import sys
import yaml
import os


class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


drive_scopes = ["antagning.se",
                "bth.se",
                "chalmers.se",
                "du.se",
                "esh.se",
                "fhs.se",
                "gih.se",
                "gu.se",
                "hb.se",
                "hh.se",
                "hhs.se",
                "hig.se",
                "his.se",
                "hj.se",
                "hkr.se",
                "hv.se",
                "irf.se",
                "kau.se",
                "kb.se",
                "ki.se",
                "kkh.se",
                "kmh.se",
                "konstfack.se",
                "kth.se",
                "kva.se",
                "liu.se",
                "lnu.se",
                "ltu.se",
                "lu.se",
                "mau.se",
                "mdu.se",
                "miun.se",
                "nordunet.se",
                "nrm.se",
                "oru.se",
                "rkh.se",
                "scilifelab.se",
                "shh.se",
                "sics.se",
                "slu.se",
                "smhi.se",
                "sp.se",
                "su.se",
                "sunet.se",
                "suni.se",
                "swamid.se",
                "ths.se",
                "uhr.se",
                "umu.se",
                "uniarts.se",
                "uu.se",
                "vinnova.se",
                "vr.se"]


def validate(idps):
    seen = []
    problem = False
    for key in idps:
        idp = idps[key]
        for entityID in idp['entityIDs']:
            if entityID not in seen:
                seen.append(entityID)
            else:
                problem = True
                print(f"Duplicate entityID: {entityID}")
    if problem:
        sys.exit(1)


def output(idps):
    transformed = {"domain": os.environ.get("DRIVE_DOMAIN"), "idps": []}

    for key in idps:
        idp = idps[key]
        transformed["idps"].append(
            {"id": key, "entityIDs": idp['entityIDs']})
    yaml.dump(transformed, sys.stdout, Dumper=MyDumper, sort_keys=False)


def main():
    idps = {}
    # idps["extern"] = {"name": "Extern", 'entityIDs': []}
    r = requests.get("https://mds.swamid.se/md/swamid-transitive-ds.json")
    metadata = r.json()
    for entity in metadata:
        if 'scope' in entity and 'type' in entity and entity['type'] == 'idp':
            scopes = entity['scope'].split(',')
            for scope in scopes:
                if scope in drive_scopes:
                    index = scope.replace('.se', "")
                    if index not in idps:
                        idps[index] = {'entityIDs': []}
                    idps[index]['entityIDs'].append(entity['entityID'])
    validate(idps)
    output(idps)


if __name__ == '__main__':
    main()
