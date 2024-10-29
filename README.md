## Prerequisites
- Python 3.11 (for local setup)
- GitHub account
- PostgreSQL

## Setup

### 0. Setup the PostgreSQL database for vector storing:
Execute the following script to setup the database:
  ```
  ./setup_pgvector.sh
  ```
### 1. Environment Variables:
Copy the sample environment file and edit it with your API keys:
   ```
   cp .env.sample .env
   ```
Edit the `.env` file and add your required variables:
   ```
   OPENAI_API_KEY=your_openai_key
   LANGCHAIN_API_KEY=your-langchain-key
   GITHUB_PERSONAL_ACCESS_TOKEN=your-github-token 
   ```
Export your `.env` variables to the system:
   **Linux / Bash**
   ```
   export $(grep -v '^#' .env | xargs)
   ```
### Local Setup:
1. Ensure you have Python 3.11+ installed.
2. Set up a virtual environment:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the main script:
   ```
   python server.py
   ```

### Vectorize codebase:
  Change the values in the vectorize.example file and execute.
