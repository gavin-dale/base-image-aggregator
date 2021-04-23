import json

class Report:
    """Models the report generated from data provided by Repository class"""
    def __init__(self, base_url, commit_sha, dockerfile_path, base_image_name):
        self.base_url = base_url
        self.commit_sha = commit_sha
        self.dockerfile_path = dockerfile_path
        self.base_image_name = base_image_name

    def build_report(self):
        """Builds out the data structure of the report"""
        report = [] 
        for path in self.dockerfile_path:
            report.append({
                "data": {
                    f"{self.base_url}:{self.commit_sha}": {
                        f"{path}": [
                            f"{self.base_image_name}"
                        ]
                    }
                }
            })

        return report

    def write_report(self, report):
        """Writes the report to a file"""
        with open('data.json', 'w') as outfile:
            json.dump(report, outfile)
