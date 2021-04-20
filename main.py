# TODO:
# handle non-200 responses
# write to log file
# refactor into classes
# run as k8s job
# unit testing
# dockerfile class that imports a request class has project name, repo name, sha
# request class has base url, url structure, dockerfile paths
# report class base image name, url, sha, path to dockerfile

import requests
import json
from repository import Repository

def get_sources():
    sources = requests.get('https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt')
    return sources.text.split('\n')

# steps:
# retrieve sources
# build dictionary
# get tree
# get dockerfile locations
# get dockerfile contents
# get base image
# write report 

qontract_repo = Repository('https://github.com/app-sre/qontract-reconcile.git', '30af65af14a2dce962df923446afff24dd8f123e')
url = qontract_repo.build_tree_url()
q_dockerfile_paths = qontract_repo.get_dockerfile_paths(url)
print(q_dockerfile_paths)

container_images_repo = Repository('https://github.com/app-sre/container-images.git', 'c260deaf135fc0efaab365ea234a5b86b3ead404')
url = container_images_repo.build_tree_url()
ci_dockerfile_paths = container_images_repo.get_dockerfile_paths(url)
print(ci_dockerfile_paths)

q_dockerfile_base_image = qontract_repo.get_dockerfile(q_dockerfile_paths)
print(q_dockerfile_base_image)

ci_dockerfile_base_image = container_images_repo.get_dockerfile(ci_dockerfile_paths)
print(ci_dockerfile_base_image)

