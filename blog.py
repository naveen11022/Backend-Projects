from fastapi import APIRouter,Depends,Response
from data_validate import blogger
from DB import Blogger,user
from Auth import session,get_current_user

router = APIRouter()

@router.post("/create_blog")
def create_blog(blog:blogger,current_user:user=Depends(get_current_user)):
    new_blog = blogger(title=blog.title,content=blog.content,category=blog.category,tags=blog.tags,uid=current_user)
    session.add(new_blog)
    session.close()
    return({"messages":"blog created successfully!!!"})

@router.get("/get_blog")
def get_blog(current_user:user=Depends(get_current_user)):
    blogger_details = session.query(blogger).filter(uid=current_user)
    if blogger_details:
        return Response({"details":blogger_details})
    return Response({"messages":"No details found!!!"})

@router.delete("/delete/{id}")
def delete_blog(current_user:user=Depends(get_current_user)):
    delete_blog = session.query(Blogger).filter(id=id,uid=current_user)
    if delete_blog:
        delete_blog.delete()
        return Response({"messages":"Blogger deleted successfully!!!"})
    return Response({"messages":"no data found!!!"})

