from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.subscription.router import router as subscription_router
from app.sme.router import router as sme_router
from app.users.router import router as users_router
from app.database import Base, engine

app = FastAPI()

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(subscription_router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(sme_router, prefix="/smes", tags=["SMEs"])
app.include_router(users_router, prefix="/users", tags=["Users"])

# Create the database tables
Base.metadata.create_all(bind=engine)
