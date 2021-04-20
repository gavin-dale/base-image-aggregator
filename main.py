# TODO:
# handle non-200 responses/error handling in general
# write to log file
# run as k8s job
# unit testing

import requests
import json
from repository import Repository
from report import Report

def get_sources():
    sources = requests.get('https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt')
    return sources.text.split('\n')

qontract_repo = Repository('https://github.com/app-sre/qontract-reconcile.git', '30af65af14a2dce962df923446afff24dd8f123e')
url = qontract_repo.build_tree_url()
q_dockerfile_paths = qontract_repo.get_dockerfile_paths(url)
print(q_dockerfile_paths)

container_images_repo = Repository('https://github.com/app-sre/container-images.git', 'c260deaf135fc0efaab365ea234a5b86b3ead404')
url = container_images_repo.build_tree_url()

ci_dockerfile_paths = container_images_repo.get_dockerfile_paths(url)
print(ci_dockerfile_paths)

q_dockerfile_base_image = qontract_repo.get_base_image(q_dockerfile_paths)
print(q_dockerfile_base_image)

ci_dockerfile_base_image = container_images_repo.get_base_image(ci_dockerfile_paths)
print(ci_dockerfile_base_image)

qontract_report = Report(qontract_repo.repo_url, qontract_repo.commit_sha, q_dockerfile_paths, qontract_repo.base_images) 
data = qontract_report.build_report()
qontract_report.write_report(data)

ci_report = Report(container_images_repo.repo_url, container_images_repo.commit_sha, ci_dockerfile_paths, container_images_repo.base_images) 
ci_data = ci_report.build_report()
ci_report.write_report(ci_data)