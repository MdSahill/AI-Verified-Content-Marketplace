from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List
import datetime

from ..ai_verification.verification import ContentVerifier
from ..nft.minting import NFTMinter
from ..database.models import Content, NFTMetadata
from ..config import config

router = APIRouter()

# Dependency injections (would be properly set up in main.py)
verifier = ContentVerifier(config.MODEL_PATH, config.CIRCUITS_PATH)
# nft_minter would be initialized with contract

class ContentSubmission(BaseModel):
    content: str
    content_type: str = "text"
    creator_address: str

class VerificationResponse(BaseModel):
    content_hash: str
    is_verified: bool
    verification_data: Dict[str, Any]
    zk_proof: Dict[str, Any]

class MintingRequest(BaseModel):
    content_hash: str
    creator_address: str

class MintingResponse(BaseModel):
    token_id: int
    transaction_hash: str
    metadata_uri: str
    blockchain_address: str

@router.post("/verify", response_model=VerificationResponse)
async def verify_content(submission: ContentSubmission):
    """Verify content and generate ZK proof"""
    try:
        verification_record, content_hash = verifier.verify_content(
            submission.content,
            submission.creator_address
        )
        
        # Save to database (simplified)
        # In production, use proper database session
        content_record = {
            'content_hash': content_hash,
            'original_content': submission.content,
            'content_type': submission.content_type,
            'creator_address': submission.creator_address,
            'ai_model_hash': verification_record['model_hash'],
            'verification_proof': json.dumps(verification_record['verification_data']),
            'zk_proof': json.dumps(verification_record['zk_proof']),
            'verified_at': datetime.datetime.utcnow(),
            'is_verified': verification_record['is_verified']
        }
        
        return VerificationResponse(
            content_hash=content_hash,
            is_verified=verification_record['is_verified'],
            verification_data=verification_record['verification_data'],
            zk_proof=verification_record['zk_proof']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@router.post("/mint", response_model=MintingResponse)
async def mint_content(request: MintingRequest):
    """Mint verified content as NFT"""
    try:
        # In production, fetch content record from database
        # For now, use mock data
        content_data = {
            'content_hash': request.content_hash,
            'creator_address': request.creator_address,
            'content_type': 'text'
        }
        
        verification_record = {
            'content_hash': request.content_hash,
            'model_hash': 'mock_model_hash',
            'verification_data': {'is_ai_assisted': True},
            'zk_proof': {'proof': 'mock_proof'},
            'timestamp': datetime.datetime.utcnow()
        }
        
        # Mock minting - in production, use actual NFT minter
        mock_result = {
            'token_id': 12345,
            'transaction_hash': '0x' + 'mock_tx_hash'.zfill(64),
            'metadata_uri': 'https://ipfs.io/ipfs/Qmmockmetadata',
            'blockchain_address': '0xmockContractAddress'
        }
        
        return MintingResponse(**mock_result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Minting failed: {str(e)}")

@router.get("/content/{content_hash}")
async def get_content(content_hash: str):
    """Get content verification status"""
    # In production, fetch from database
    return {"content_hash": content_hash, "status": "verified"}

@router.get("/nft/{token_id}")
async def get_nft(token_id: int):
    """Get NFT information"""
    # In production, fetch from database and blockchain
    return {"token_id": token_id, "metadata_uri": "https://ipfs.io/ipfs/Qmmock"}