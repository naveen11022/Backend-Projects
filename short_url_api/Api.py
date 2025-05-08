from DB import shorturl,user,session
from fastapi import APIRouter,Depends,Response,HTTPException
from fastapi.responses import  JSONResponse
from  data_validate import shorturl,update_url
from Auth import get_current_user
import datetime
router = APIRouter()

@router.post("/create_url")
def create_url(create:shorturl,current_user:user=Depends(get_current_user)):
    shorturl(url=create.url,shortend=create.shortend,uid=current_user)
    session.add(shorturl)
    session.close()
    return Response({"messages":"url created successfully!!!"})

@router.get("/get_utl/{uid}")
def get_url(current_user:user=Depends(get_current_user)):
    url_exists = session.query(shorturl).filter(uid=current_user)
    if url_exists:
        return JSONResponse({"details":url_exists})
    return Response({"messages":"No data found!!!"})

@router.delete("/delete/{id}")
def delete_url(current_user:user=Depends(get_current_user)):
    url_exists = session.query(shorturl).filter(uid=current_user,id=id)
    if url_exists:
        url_exists.delete()
        return JSONResponse({"details":"url deleted successfully!!!"})
    return Response({"messages":"No data found!!!"})

@router.patch("/update_url{id}")
def update_url(update:update_url,current_user:user=Depends(get_current_user)):
    url_exists = session.query(shorturl).filter(id=id,uid=current_user)
    if url_exists:
        url_exists.update(url=update.url,shorturl=update.shortend,updated_at=datetime.datetime.now())
        return Response({"messages":"url updated successfully!!!"})
    return Response({"messages":"No data found"})


