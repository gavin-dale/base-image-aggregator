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

def get_sources():
    sources = requests.get('https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt')
    return sources.text.split('\n')

source_dict = {}
def build_dict(sources_list):
    for source in sources_list:
        if source:
            key_value = source.split(' ')
            source_dict[key_value[0]] = key_value[1]
    return source_dict

def extract_url_data(source_dict):
    urls = []
    for source, sha in source_dict.items(): 
        repo_url = source.split('/')
        commit_sha = sha

        api_base_url = 'https://api.github.com/repos'
        project = repo_url[3]
        repo = repo_url[4][:-4]

        urls.append(f'{api_base_url}/{project}/{repo}/git/trees/{commit_sha}?recursive=true')
    return urls

def get_trees(urls):
    trees = []
    for url in urls:
        trees.append(requests.get(f'{url}').json())
    with open('trees.json', 'w') as outfile:
        json.dump(trees, outfile)
    return trees

def get_paths(trees):
    paths = []
    for tree in trees:
        print(tree)
    return(paths)

def get_base_image(url):
    raw = requests.get(url)
    base_image = raw.text.split('\n')
    base_image = base_image[0].replace('FROM', '')

# steps:
# retrieve sources
# build dictionary
# get tree
# get dockerfile locations
# get dockerfile contents
# get base image
# write report 

sources_list = get_sources()

sources_dict = build_dict(sources_list)

urls = extract_url_data(sources_dict)

trees = get_trees(urls)

paths = get_paths(trees)