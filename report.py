import json

class Report:
    def __init__(self, base_url, commit_sha, dockerfile_path, base_image_name):
        self.base_url = base_url
        self.commit_sha = commit_sha
        self.dockerfile_path = dockerfile_path
        self.base_image_name = base_image_name
    
    def build_report(self):
        report = {
            "data": {
                f"{self.base_url}:{self.commit_sha}": {
                    f"{self.dockerfile_path}": [
                        f"{self.base_image_name}"
                    ]
                }
            }
        }

        return report

    def write_report(self, report):
        with open('data.json', 'w') as outfile:
            json.dump(report, outfile)
