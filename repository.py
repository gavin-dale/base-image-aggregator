import re
import requests

class Repository:
    """"Models metadata for a single git repo"""
    def __init__(self, repo_url, commit_sha):
        self.repo_url = repo_url
        self.commit_sha = commit_sha
        self.api_base_url = 'https://api.github.com/repos'
        self.raw_content_url = 'https://raw.githubusercontent.com'
        self.base_images = []
        self.dockerfile_paths = []
        self.repo_details = ""
        self.project = ""
        self.repo = ""

    def build_tree_url(self):
        """builds url that links to the recursive tree of a git repo"""
        self.repo_details = self.repo_url.split('/')
        self.project = self.repo_details[3]
        self.repo = self.repo_details[4][:-4]
        tree_url = f'{self.api_base_url}/{self.project}/{self.repo}/git/trees/{self.commit_sha}?recursive=true'

        return tree_url

    def get_dockerfile_paths(self, url):
        """requests git repo tree and parses out Dockerfile locations.
        Returns one or more Dockerfile paths"""
        dockerfile_paths = []
        request = requests.get(f'{url}')
        json = request.json()
        tree = json['tree']
        for obj in tree:
            if re.search(r"(.)Dockerfile$", obj['path']):
                dockerfile_paths.append(obj['path'])

        return dockerfile_paths

    def get_base_image(self, dockerfile_paths):
        """Parses Dockerfile and returns the name of the base images it uses.
        It's gross and needs to be refactored I know"""
        for path in dockerfile_paths:
            raw_dockerfile = requests.get(f'{self.raw_content_url}/{self.project}/{self.repo}/{self.commit_sha}/{path}')
            raw_dockerfile_split = raw_dockerfile.text.split('\n')
            for line in raw_dockerfile_split:
                if re.search(r"(\A)FROM", line):
                    split_line = line.split(' ')
                    base_image = split_line[1]
                    self.base_images.append(base_image)
        return self.base_images
