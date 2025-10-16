from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import datetime

Base = declarative_base()

class Content(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    content_hash = Column(String(66), unique=True, index=True)
    original_content = Column(Text, nullable=False)
    content_type = Column(String(50), nullable=False)  # text, image, audio, etc.
    creator_address = Column(String(42), nullable=False)
    ai_model_hash = Column(String(66), nullable=False)
    verification_proof = Column(Text, nullable=False)
    zk_proof = Column(Text, nullable=False)
    nft_token_id = Column(Integer, unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    verified_at = Column(DateTime(timezone=True), nullable=True)
    is_verified = Column(Boolean, default=False)

class NFTMetadata(Base):
    __tablename__ = "nft_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, unique=True, index=True)
    content_id = Column(Integer, nullable=False)
    metadata_uri = Column(String(256), nullable=False)
    transaction_hash = Column(String(66), nullable=True)
    blockchain_address = Column(String(42), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())