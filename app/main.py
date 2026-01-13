from fastapi import FastAPI
from app.db.database import DATABASE_URL
from fastapi.staticfiles import StaticFiles
from app.routers import auth, user
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "profile_images")
os.makedirs("profile_images", exist_ok=True)

## INCLUDE ROUTERS
app.include_router(user.router)
app.include_router(auth.router)
app.mount(
    "/profile_images",
    StaticFiles(directory="profile_images"),
    name="profile_images"
)


## CEHCK EXIT FAST API WORK
@app.get('/')
def root():
    return { 'status' : DATABASE_URL, 'message' : 'Test Succesfully' }



