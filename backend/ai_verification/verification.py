from typing import Dict, Any, Tuple
from .model import ContentProcessor
from .zk_circuits import ZKProofGenerator
import hashlib
import json

class ContentVerifier:
    def __init__(self, model_path: str, circuits_path: str):
        self.processor = ContentProcessor(model_path)
        self.zk_generator = ZKProofGenerator(circuits_path)
    
    def verify_content(self, content: str, creator_address: str) -> Tuple[Dict[str, Any], str]:
        """Verify content and generate ZK proof"""
        # Process content with AI model
        verification_data = self.processor.process_content(content)
        
        # Generate ZK proof
        zk_proof = self.zk_generator.generate_verification_proof(
            verification_data['content_hash'],
            verification_data['model_hash'],
            verification_data
        )
        
        # Create verification record
        verification_record = {
            'content_hash': verification_data['content_hash'],
            'creator_address': creator_address,
            'model_hash': verification_data['model_hash'],
            'verification_data': verification_data,
            'zk_proof': zk_proof,
            'is_verified': verification_data['is_ai_assisted'],
            'timestamp': None  # Will be set when saved to DB
        }
        
        return verification_record, verification_data['content_hash']
    
    def validate_proof(self, proof_data: Dict[str, Any]) -> bool:
        """Validate ZK proof (simplified)"""
        # In production, this would verify the proof on-chain or off-chain
        try:
            # Mock validation - replace with actual proof verification
            public_signals = proof_data.get('public_signals', [])
            if len(public_signals) >= 2:
                return int(public_signals[1]) == 1  # is_verified flag
            return False
        except:
            return False