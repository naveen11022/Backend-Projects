from DB import user,Notes
from Auth import get_current_user,session
from fastapi import APIRouter,Response,Depends
from data_validate import Notes
router = APIRouter()

@router.post("/create_notes")
def create_notes(notes:Notes,current_user:user=Depends(get_current_user)):
    new_notes = Notes(title=notes.title,description=notes.description,uid=current_user)
    session.add(new_notes)
    session.close()
    return Response({"messages":"Notes created successfully!!!"})


@router.get("/get_notes")
def get_notes(current_user:user=Depends(get_current_user)):
    note_exists = session.query(Notes).filter_by(uid=current_user)
    if note_exists:
        return Response("message":note_exists)
    return Response({"messages":"No Data found!!!"})

@router.delete("/delete")
def delete_notes(uid:int,current_user:user=Depends(get_current_user)):
    notes_exists = session.query(Notes).filter(id=uid,uid=current_user)
    if notes_exists:
        notes_exists.delete()
        return Response({"messages":"Notes deleted successfully!!!"})
    return Response({"messages":"No data found!!!"})