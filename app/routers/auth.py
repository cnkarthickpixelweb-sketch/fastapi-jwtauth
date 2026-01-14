from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,status,Request
from app.core.security import verify_access_token,get_current_user,verify_password,generate_hash_password
from app.models.user import User
from sqlalchemy.orm import Session
from app.schema.user import UpdateSchema,ChangepasswordSchema
from app.db.database import get_db
import os
import shutil
from typing import Annotated


router = APIRouter()


IMAGEDIR = "profile_images/"
os.makedirs(IMAGEDIR, exist_ok=True)

## UPDATE USER
@router.post('/update-user')
def updateUser(user:UpdateSchema = Depends(),db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    check_user = db.query(User).filter(User.id == current_user['id']).first()
    if not check_user:
        raise HTTPException(
                status_code=422,
                detail= {
                    "success" : False,
                    "message" : "User Not Found"
                }
            )
       
    check_user.firstname = user.firstname
    check_user.lastname = user.lastname

    db.add(check_user)
    db.commit()
    db.refresh(check_user)

    return  {
        "success" : True,
        "message" : "User Details Update Successfully",
        "data": {
            "id": check_user.id,
            "firstname": check_user.firstname,
            "lastname": check_user.lastname,
            "email": check_user.email
        }
    }


## CHANGE PASSWORD
@router.post('/change-password')
def changePassoword(password:ChangepasswordSchema,db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    check_user = db.query(User).filter(User.id == current_user['id']).first()
    if not check_user:
        raise HTTPException(
                status_code=422,
                detail= {
                    "success" : False,
                    "message" : "User Not Found"
                }
            )

    if  verify_password(password.password,check_user.password):
        raise HTTPException(
                status_code=422,
                detail= {
                    "success" : False,
                    "message" : "New password cannot be the same as the old password"
                }
            )
    
    hashed_password = generate_hash_password(password.password)
    check_user.password = hashed_password
    db.add(check_user)
    db.commit()
    
    return {
        'success' : True,
        "message" : 'Your Password update successfully'
    }
                    

## TOKEN BASE CEHCK
@router.post('/token_base_check')
def tokenBasedCheck(token:str):
    return verify_access_token(token)


## DASHBOARD
@router.get("/dashboard")
def dashboard(current_user: dict = Depends(get_current_user)):
     return {
        "success": True,
        "message": "Welcome to dashboard",
        "user": current_user
    }


@router.post("/upload-profile-image/")
async def upload_profile_image( request: Request,file: Annotated[UploadFile, File(...)],db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    
    user = db.query(User).filter(User.id == current_user['id']).first()
    if not user:
        raise HTTPException(
                status_code=422,
                detail= {
                    "success" : False,
                    "message" : "User Not Found"
                }
            )
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "message": f"Invalid file type: {file.content_type}"
            }
        )
    
    filename = os.path.basename(file.filename)
    file_path = os.path.join(IMAGEDIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        if user.profile_image and os.path.exists(user.profile_image):
            os.remove(user.profile_image)

        user.profile_image = f"profile_images/{filename}"
        db.add(user)
        db.commit()
        db.refresh(user)
            
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                    "success" : False, 
                    "message" : "There was an error uploading the file: {e}"
                }
        )
    finally:      
        await file.close()
    
    return {
        "success": True,
        "filename": user.profile_image,
        "image_url": f"{request.base_url}{user.profile_image}"
    }

