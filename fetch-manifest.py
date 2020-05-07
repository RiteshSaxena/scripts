#!/usr/bin/python3

import requests
import sys
from xml.etree import ElementTree


def get_manifest(tag):
    url = "https://source.codeaurora.org/quic/la/platform/manifest/plain/default_{0}.xml?h={0}".format(tag)
    res = requests.get(url)

    with open('{0}.xml'.format(tag), 'wb') as f:
        f.write(res.content)


def parse_manifest(tag):
    tree = ElementTree.parse("{0}.xml".format(tag))
    root = tree.getroot()

    for item in root.findall('./project'):
        if 'revision' in item.attrib.keys():
            item.attrib.pop('revision')
        if 'groups' in item.attrib.keys():
            item.attrib.pop('groups')

    tree.write("{0}.xml".format(tag))


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch-manifest.py <tag>")
        sys.exit()
    else:
        tag = sys.argv[1]
        get_manifest(tag)
        parse_manifest(tag)

if __name__ == '__main__':
    main()
