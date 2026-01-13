from fastapi import FastAPI
from app.db.database import DATABASE_URL
from fastapi.staticfiles import StaticFiles
from app.routers import auth, user

app = FastAPI()

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



