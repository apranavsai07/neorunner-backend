from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "NeoRunner Behavioral Biometric API"
    }

@router.get("/")
def root():
    return {
        "message": "NeoRunner Behavioral Biometric Continuous Authentication API",
        "version": "1.0.0",
        "docs": "/docs"
    }
