from github import Github
from github.GithubException import GithubException

class GitHubRepo:
    def __init__(self, owner: str, repo_name: str, access_token: str):
        self.owner = owner
        self.repo_name = repo_name
        self.access_token = access_token
        self.github = Github(access_token)
        try:
            self.repo = self.github.get_repo(f"{owner}/{repo_name}")
        except GithubException as e:
            print(f"Failed to access repository: {e.data['message']}")
            raise e

    def get_file_structure(self, path=""):
        try:
            contents = self.repo.get_contents(path)
            file_structure = []
            for content in contents:
                if content.type == "file":
                    file_structure.append(content.path)
                elif content.type == "dir":
                    file_structure.extend(self.get_file_structure(content.path))
            return file_structure
        except GithubException as e:
            print(f"Failed to get file structure: {e.data['message']}")
            return []

    def get_file_content(self, file_path: str):
        try:
            file_content = self.repo.get_contents(file_path)
            if isinstance(file_content, list):
                print(f"Path {file_path} is a directory, not a file.")
                return None
            return file_content.decoded_content.decode()
        except GithubException as e:
            print(f"Failed to get file content: {e.data['message']}")
            return None
