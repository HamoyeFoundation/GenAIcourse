from fastapi import FastAPI
from routes.conversation import conversation_router
from routes.document import document_router
import uvicorn


app = FastAPI()

app.include_router(conversation_router, prefix="/conversation")
app.include_router(document_router,prefix="/document")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)