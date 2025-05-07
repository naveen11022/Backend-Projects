from fastapi import APIRouter,Response,Depends
from fastapi.responses import JSONResponse
from Db import todo,session,user
from Auth import get_current_user
from data_validate import todo
router = APIRouter()

@router.post("/create_todo")
def create_todo(todo:todo,current_user:user=Depends(get_current_user)):
    new_todo = todo(title=todo.title,description=todo.description,uid=current_user)
    session.add(new_todo)
    session.close()
    return Response({"messages":"Todo created sucessfully!!!"})

@router.get("/get")
def get_todo(current_user:user=Depends(get_current_user)):
    todo = session.query(todo).filter_by(current_user)
    if todo:
        return JSONResponse({todo})
    return Response({"messages":"No data found"})

@router.delete("/delete_todo{id}")
def delete_todo(current_user:user=Depends(get_current_user)):
    todo_exists = session.query(todo).filter(id=id,uid=current_user)
    if todo_exists:
        todo_exists.delete()
    return Response({"messages":"todo deleted sucessfully!!!"})