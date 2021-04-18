# TODO: find Dockerfile by crawling file tree
# TODO: handle non-200 responses
# TODO: write to log file and error file
# TODO: read values from file
# TODO: curl file from external location first, put in __init__.py?
# TODO: refactor into classes?
import requests

repo_url = 'https://github.com/app-sre/qontract-reconcile.git'
repo_url = repo_url.split('/')

commit_sha = '30af65af14a2dce962df923446afff24dd8f123e'
api_base_url = 'https://api.github.com/repos'
project = repo_url[3]
repo = repo_url[4][:-4]

#target = f'{api_base_url}/{project}/{repo}/contents/dockerfiles?ref={commit_sha}'
target = f'{api_base_url}/{project}/{repo}/contents/dockerfiles'

r = requests.get(target, params=commit_sha)
print(r.url)
print(r.json())