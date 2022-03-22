# Make sure you pip install fastapi[all] in order for this code to work
# ****You can copy this command in your terminal ----> pip install fastapi[all]****

# Here we import all the packages we need
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, users, auth, votes

# To create all models (this was copy paste from the FastAPI website.
# It is commented out due to the implementation of Alembic
# models.Base.metadata.create_all(bind=engine)

# Create an instance for Fast API. Lines 9-13 are always needed.
app = FastAPI()

# Here we will be given a list of allowed origins to talk to our API
origins = ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Here we are going to use the routers to send any requests to our routers file
app.include_router(post.router)  # <--This one sends the request to the posts file

app.include_router(users.router)  # <--This one send the request to the users file

app.include_router(auth.router)  # <---This one is the authentication and token generator

app.include_router(votes.router)  # <---This one is the votes router to keep track of votes
