from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import database, models, routes

app = FastAPI()

# CORS: allow frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

# Include routes
app.include_router(routes.router, prefix="/api")
