import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./content_marketplace.db")
    
    # Blockchain
    WEB3_PROVIDER: str = os.getenv("WEB3_PROVIDER", "http://localhost:8545")
    CONTRACT_ADDRESS: Optional[str] = os.getenv("CONTRACT_ADDRESS")
    PRIVATE_KEY: Optional[str] = os.getenv("PRIVATE_KEY")
    
    # AI Model
    MODEL_PATH: str = os.getenv("MODEL_PATH", "./models/content_verifier.pth")
    
    # ZK Settings
    CIRCUITS_PATH: str = os.getenv("CIRCUITS_PATH", "./circuits")
    
    # API
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000"))

config = Config()