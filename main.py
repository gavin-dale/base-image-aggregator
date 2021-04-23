import requests
from repository import Repository
from report import Report
import sys

def get_sources(source_url):
    sources = requests.get(source_url)
    return sources.text.split('\n')

#sources = requests.get('https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt')

source_dict = {}
def build_dict(sources_list):
    for source in sources_list:
        if source:
            key_value = source.split(' ')
            source_dict[key_value[0]] = key_value[1]
    return source_dict

sources_list = get_sources(sys.argv[1])
sources_dict = build_dict(sources_list)
print(sources_dict)

for repo_link,commit_sha in sources_dict.items():
    repo = Repository(repo_link,commit_sha)
    url = repo.build_tree_url()
    dockerfile_paths = repo.get_dockerfile_paths(url)
    dockerfile_base_image = repo.get_base_image(dockerfile_paths)
    report = Report(repo.repo_url, repo.commit_sha, dockerfile_paths, repo.base_images)
    report_data = report.build_report()
    report.write_report(report_data)


#qontract_repo = Repository('https://github.com/app-sre/qontract-reconcile.git', '30af65af14a2dce962df923446afff24dd8f123e')
#url = qontract_repo.build_tree_url()
#q_dockerfile_paths = qontract_repo.get_dockerfile_paths(url)
#print(q_dockerfile_paths)
#
#container_images_repo = Repository('https://github.com/app-sre/container-images.git', 'c260deaf135fc0efaab365ea234a5b86b3ead404')
#url = container_images_repo.build_tree_url()
#
#ci_dockerfile_paths = container_images_repo.get_dockerfile_paths(url)
#print(ci_dockerfile_paths)
#
#q_dockerfile_base_image = qontract_repo.get_base_image(q_dockerfile_paths)
#print(q_dockerfile_base_image)
#
#ci_dockerfile_base_image = container_images_repo.get_base_image(ci_dockerfile_paths)
#print(ci_dockerfile_base_image)
#
#qontract_report = Report(qontract_repo.repo_url, qontract_repo.commit_sha, q_dockerfile_paths, qontract_repo.base_images)
#data = qontract_report.build_report()
#qontract_report.write_report(data)
#
#ci_report = Report(container_images_repo.repo_url, container_images_repo.commit_sha, ci_dockerfile_paths, container_images_repo.base_images)
#ci_data = ci_report.build_report()
#ci_report.write_report(ci_data)
#