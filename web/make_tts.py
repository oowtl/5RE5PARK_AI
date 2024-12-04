from fastapi import APIRouter

router = APIRouter(prefix="/tts")

@router.get("/")
def root():
    return "top explorer"