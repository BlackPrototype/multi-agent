import os
from dotenv import load_dotenv
from github import Github, GithubException
from utils.github_repo import GitHubRepo
from utils.database import Database
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_environment_variables():
    load_dotenv()
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

def extract_github_owner_repo(url):
    if url.startswith("https://github.com/"):
        parts = url[len("https://github.com/"):].strip('/').split('/')
        if len(parts) >= 2:
            owner = parts[0]
            repo = parts[1]
            return owner, repo
    return None, None

def vectorize_codebase(req):
    load_environment_variables()

    ACCESS_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')

    owner, repo_name = extract_github_owner_repo(req['github_url'])

    ghr = GitHubRepo(owner, repo_name, ACCESS_TOKEN)
    files = ghr.get_file_structure()

    db = Database('projects')
    record = {
        "name": req["name"],
        "github_url": req["github_url"],
        "owner": owner,
        "repo_name": repo_name,
        "auth0_id": req["auth0_id"],
        "files_processed": len(files)
    }
    project_id = db.write_one(record)

    db = Database('vectors')

    for file in files:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        file_content = ghr.get_file_content(file)
        if isinstance(file_content, list):
            file_content = ''.join(file_content)
        documents = text_splitter.split_text(file_content)

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vectors = [embeddings.embed_query(text) for text in documents]

        for vector in vectors:
            vector_record = {
                "project_id": project_id,
                "file_path": file,
                "vector": vector
            }
            db.write_one(vector_record)

    return {"message": "Vectorization completed and record saved to the database"}
