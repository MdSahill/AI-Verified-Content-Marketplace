import json
import requests
from typing import Dict, Any
from .contract import ContentNFTContract

class NFTMinter:
    def __init__(self, contract: ContentNFTContract, ipfs_gateway: str = "https://ipfs.io/ipfs/"):
        self.contract = contract
        self.ipfs_gateway = ipfs_gateway
    
    def create_metadata(self, 
                       content_data: Dict[str, Any],
                       verification_record: Dict[str, Any]) -> Dict[str, Any]:
        """Create NFT metadata for content"""
        
        metadata = {
            "name": f"AI-Verified Content #{content_data['content_hash'][:16]}",
            "description": "Content verified and authenticated through AI verification system",
            "image": "https://example.com/placeholder-image.png",  # Would be actual content or generated image
            "attributes": [
                {
                    "trait_type": "Content Type",
                    "value": content_data.get('content_type', 'text')
                },
                {
                    "trait_type": "AI Verification Score",
                    "value": verification_record['verification_data']['verification_scores'][0][1]
                },
                {
                    "trait_type": "Content Hash",
                    "value": content_data['content_hash']
                },
                {
                    "trait_type": "Model Hash",
                    "value": verification_record['model_hash']
                },
                {
                    "trait_type": "ZK Proof Verified",
                    "value": True
                }
            ],
            "properties": {
                "content_hash": content_data['content_hash'],
                "model_hash": verification_record['model_hash'],
                "verification_timestamp": verification_record.get('timestamp'),
                "creator": content_data['creator_address']
            }
        }
        
        return metadata
    
    def upload_to_ipfs(self, metadata: Dict[str, Any]) -> str:
        """Upload metadata to IPFS (simplified - would use actual IPFS client)"""
        # In production, use ipfshttpclient or similar
        # For now, return mock IPFS hash
        mock_hash = f"Qm{json.dumps(metadata).encode().hex()[:44]}"
        return f"{self.ipfs_gateway}{mock_hash}"
    
    def mint_verified_content(self, 
                            content_data: Dict[str, Any],
                            verification_record: Dict[str, Any]) -> Dict[str, Any]:
        """Mint NFT for verified content"""
        
        # Create metadata
        metadata = self.create_metadata(content_data, verification_record)
        
        # Upload to IPFS
        metadata_uri = self.upload_to_ipfs(metadata)
        
        # Mint NFT
        mint_result = self.contract.mint_nft(
            to_address=content_data['creator_address'],
            token_uri=metadata_uri,
            content_hash=verification_record['content_hash'],
            model_hash=verification_record['model_hash'],
            zk_proof=verification_record['zk_proof']
        )
        
        return {
            **mint_result,
            'metadata_uri': metadata_uri,
            'metadata': metadata
        }