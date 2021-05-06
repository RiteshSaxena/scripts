#!/usr/bin/python3

import requests
import sys
from xml.etree import ElementTree

tag = {
    'system': 'LA.QSSI.11.0.r1-11600-qssi.0',
    'vendor': 'LA.UM.9.14.r1-16100-LAHAINA.0'
}

clone_depth = [
    'device/amlogic/yukawa-kernel',
    'platform/cts',
    'platform/external/autotest',
    'platform/external/dokka',
    'platform/external/icu',
    'platform/frameworks/layoutlib',
    'platform/test/mlts/models',
    'kernel/msm-5.4'
]

def get_manifest(type):
    url = "https://source.codeaurora.org/quic/la/la/{0}/manifest/plain/default_{1}.xml?h={1}".format(type, tag[type])
    res = requests.get(url)
        
    with open('{0}_{1}.xml'.format(type, tag[type]), 'wb') as f:
        f.write(res.content)

def parse_manifest(type):
    tree = ElementTree.parse("{0}_{1}.xml".format(type, tag[type]))
    root = tree.getroot()

    for item in root.findall('./project'):
        if 'revision' in item.attrib.keys():
            item.attrib.pop('revision')
        if 'groups' in item.attrib.keys():
            item.attrib.pop('groups')

        item.attrib['remote'] = type

        if 'clone-depth' in item.attrib.keys():
            item.attrib.pop('clone-depth')
            item.attrib['clone-depth'] = '1'

        if item.attrib['name'] in clone_depth:
            item.attrib['clone-depth'] = '1'

    for item in root.findall('./remote'):
        root.remove(item)

    for item in root.findall('./default'):
        root.remove(item);

    for item in root.findall('./refs'):
        root.remove(item);

    tree.write("{0}_{1}.xml".format(type, tag[type]), encoding='utf-8', xml_declaration=True)


def main():
    get_manifest('system')
    parse_manifest('system')
    get_manifest('vendor')
    parse_manifest('vendor')

if __name__ == '__main__':
    main()
