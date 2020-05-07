#!/usr/bin/python3

import os
import sys
import xml.etree.ElementTree as ET

def parse_manifest():
    tree = ET.parse(".repo/manifests/default.xml")
    root = tree.getroot()

    repos = []

    for item in root.findall('./project'):
        if item.attrib['name'].startswith("platform") and "clone-depth" not in item.attrib.keys():
            repos.append({
                'name': item.attrib['name'],
                'path': item.attrib['path'],
            })

    return repos

def find_diff(repos, old_tag, new_tag):
    for repo in repos:
        print("\n\n" + repo['path'] + "\n\n")
        os.system("""
        cd {0} &&
        git fetch https://source.codeaurora.org/quic/la/{1} tag {2} --no-tags && 
        git fetch https://source.codeaurora.org/quic/la/{1} tag {3} --no-tags && 
        git log {2}..{3} --oneline --no-merges && 
        git diff {2}..{3} --stat && 
        git tag -d {2} && git tag -d {3}
        """.format(repo['path'], repo['name'], old_tag, new_tag))


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 compare-tags.py <old tag> <new tag>")
        sys.exit()
    else:
        old_tag = sys.argv[1]
        new_tag = sys.argv[2]
        repos = parse_manifest()
        find_diff(repos, old_tag, new_tag)

if __name__ == '__main__':
    main()
