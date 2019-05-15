import pathlib
import io
import re
import requests
import os

github_token = os.getenv('GITHUB_TOKEN')
if not github_token:
    print("No GITHUB_TOKEN defined!")
    os.exit(1)

version_re = re.compile(r'^version\s+(\S+)$')
homepage_re = re.compile(r'^homepage\s+(\S+)$')
name_re = re.compile(r'^name\s+(\S+)$')
github_url_re = re.compile(r'^https://github.com/([^/]+)/([^/]+)/?$')

def get_latest_release(url, token):
    header = {
        'Authorization': f'token {token}',
    }
    mo = github_url_re.match(url)
    owner = mo.group(1)
    name = mo.group(2)
    data = {
        'query' : '''
        {
            repository(owner: "%s", name: "%s") {
              releases(last: 1) {
                nodes {
                  tag { name }
                }
              }
            }
        }''' % (owner, name),
    }
    releases = requests.post(url='https://api.github.com/graphql', json=data, headers=header).json()
    return releases['data']['repository']['releases']['nodes'][0]['tag']['name']

portfiles = pathlib.Path('..').glob('**/Portfile')
for portfile in portfiles:
    with io.open(portfile, encoding='utf-8') as fp:
        version = None
        name = None
        url = None
        for line in fp:
            l = line.strip()

            mo = version_re.match(l)
            if mo:
                version = mo.group(1)
            mo = homepage_re.match(l)
            if mo:
                url = mo.group(1)
            mo = name_re.match(l)
            if mo:
                name = mo.group(1)

        if not name or not url or not version:
            print('Not all required fields found. Skipping.')
            continue
        if 'github.com' in url:
            latest_release = get_latest_release(url, github_token).lstrip('v')
            if latest_release != version:
                print(f'{name}@{version} is OLD. New version available: {latest_release}')
            else:
                print(f'{name}@{version} up to date')
            
