from pydantic import ValidationError
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langserve import add_routes
from agents.psql import psql_chain
from agents.review import review_chain
from agents.generate import generate_chain
from utils.vectorize import vectorize_codebase
from github import GithubException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Define CORS origins
origins = [
    "http://localhost:5173",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# Adding routes
add_routes(app, psql_chain, enable_feedback_endpoint=True, path="/psql")
add_routes(app, review_chain, enable_feedback_endpoint=True, path="/review")
add_routes(app, generate_chain, enable_feedback_endpoint=True, path="/generate")

class CodeRequest(BaseModel):
    input: dict
    config: dict
    kwargs: dict

# Define the Pydantic model for the request body
class VectorizeRequest(BaseModel):
    name: str
    github_url: str
    branch: str
    auth0_id: str
    email: str
    first_name: str
    last_name: str

# Endpoint to vectorize codebase
@app.post("/vectorize")
async def vectorize(req: VectorizeRequest):
    try:
        logging.info(f"Received request: {req.json()}")

        # Call the vectorize_codebase function
        result = vectorize_codebase(req.dict())
        return {"message": "Vectorization completed successfully" if result else "Index already exists"}, 200
    except ValidationError as e:
        logging.error(f"Validation error: {e.json()}")
        raise HTTPException(status_code=422, detail=e.errors())
    except GithubException as e:
        logging.error(f"GitHub error: {e.data['message']}")
        raise HTTPException(status_code=400, detail=f"GitHub error: {e.data['message']}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
