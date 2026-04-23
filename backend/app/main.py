from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import auth

app = FastAPI(
    title="Finance AI",
    description="AI Financial Decision System API",
    version="1.0.0",
)

# CORS — allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routes import auth, profile, transactions, analysis, query, stocks

# Include routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(transactions.router)
app.include_router(analysis.router)
app.include_router(query.router)
app.include_router(stocks.router)


@app.on_event("startup")
def on_startup():
    """Initialize database tables on server start."""
    init_db()


@app.get("/")
def root():
    return {"message": "Finance AI API is running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}
