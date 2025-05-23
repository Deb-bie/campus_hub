from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from .api.v1.api_router import router as api_router
from .config import settings
from .models.user import Base
from .db.base import engine


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # will replace in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Include API router
app.include_router(api_router, prefix=settings.API_V1)

@app.get("/")
def root():
    return {
        "message": "Campus Hub User Service"
    }

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn # type: ignore
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.PORT
    )

