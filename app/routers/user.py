from fastapi import APIRouter,HTTPException,status,Depends
from app.schema.user import LoginSchema,CreateUserSchema,UpdateSchema,ChangepasswordSchema
from app.models.user import User
from app.db.database import get_db
from app.core.security import create_access_token,generate_hash_password,verify_password,get_current_user
from sqlalchemy.orm import Session


router = APIRouter()


## SIGN-UP USER
@router.post('/sign-up')
def signUp(user:CreateUserSchema, db: Session = Depends(get_db)):
    check_exist = db.query(User).filter(User.email == user.email).first()

    if check_exist:
        raise HTTPException(
            status_code=422, 
            detail= {
                "success" : "false", 
                "message" : "Email Already Exits"
            }
        ) 
    
    hashed_password = generate_hash_password(user.password)
    
    new_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=hashed_password  
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success" : True,
        "message" : "Register Successfully",
        "data": {
            "id": new_user.id,
            "firstname": new_user.firstname,
            "lastname": new_user.lastname,
            "email": new_user.email
        }
    }


## LOGIN  USER
@router.post('/sign-in')
def signIn(user:LoginSchema,db: Session = Depends(get_db)):

    ## CHECK EXIT EMAIL 
    check_exist = db.query(User).filter(User.email == user.email).first()
    if not check_exist:
        raise HTTPException(
            status_code=422, 
            detail= {
                "success" : "false", 
                "message" : "This email is not registered with us"
            }
        ) 
    

    ## VERIFY PASSWORD
    if not verify_password(user.password, check_exist.password):
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "message": "Invalid password"
            }
        )
    

    ## TOKEN GENERATE
    data = {
            "id": check_exist.id,
            "firstname": check_exist.firstname,
            "lastname": check_exist.lastname,
            "email": check_exist.email
        }
    
    token = create_access_token(data)

    ## LOGIN SUCCESS 
    return {
        "Success" : True,
        "message" : "Login Successfully",
        "data" : {
            "accesstoken" : token,
            "id": check_exist.id,
            "firstname": check_exist.firstname,
            "lastname": check_exist.lastname,
            "email": check_exist.email
        }
    }


## LOGOUT 
@router.post('/logout')
def logout():
    return {
        "success": True,
        "message": "Logged out successfully"
    }