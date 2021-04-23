import requests
from repository import Repository
from report import Report
import sys

def get_sources(source_url):
    """Fetches git URLs and commit SHAs from provided URL"""
    sources = requests.get(source_url)
    return sources.text.split('\n')

source_dict = {}
def build_dict(sources_list):
    """Builds a dictionary from the list we create from the source URL"""
    for source in sources_list:
        if source:
            key_value = source.split(' ')
            source_dict[key_value[0]] = key_value[1]
    return source_dict

sources_list = get_sources(sys.argv[1])
sources_dict = build_dict(sources_list)

"""Loop through the dictionary, creat a new Repository object for each key value pair in the dictionary
   build out the GitHub URL needed to fetch the recursive tree of directories and files in the repo,
   gather the Dockerfile paths found in that tree, retrieve the plaintext Dockerfile contents,
   parse out the name of the base images(s) found within, then write it all to a json file. """
report_data = []
for repo_link,commit_sha in sources_dict.items():
    repo = Repository(repo_link,commit_sha)
    url = repo.build_tree_url()
    dockerfile_paths = repo.get_dockerfile_paths(url)
    dockerfile_base_image = repo.get_base_image(dockerfile_paths)
    report = Report(repo.repo_url, repo.commit_sha, dockerfile_paths, repo.base_images)
    report_data.append(report.build_report())
report.write_report(report_data)