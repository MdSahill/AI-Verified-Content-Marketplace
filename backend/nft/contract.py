from web3 import Web3
import json
import os
from typing import Dict, Any, Optional

class ContentNFTContract:
    def __init__(self, web3_provider: str, contract_address: str, private_key: str):
        self.w3 = Web3(Web3.HTTPProvider(web3_provider))
        self.contract_address = contract_address
        self.private_key = private_key
        self.account = self.w3.eth.account.from_key(private_key)
        
        # Load contract ABI (simplified - would load from compiled contract)
        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=self._get_contract_abi()
        )
    
    def _get_contract_abi(self) -> list:
        """Get contract ABI (simplified)"""
        return [
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "string", "name": "tokenURI", "type": "string"},
                    {"internalType": "bytes32", "name": "contentHash", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "modelHash", "type": "bytes32"},
                    {"internalType": "bytes", "name": "zkProof", "type": "bytes"}
                ],
                "name": "mintVerifiedContent",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
                "name": "getVerificationData",
                "outputs": [
                    {"internalType": "bytes32", "name": "", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "", "type": "bytes32"},
                    {"internalType": "bool", "name": "", "type": "bool"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
    def mint_nft(self, 
                 to_address: str,
                 token_uri: str,
                 content_hash: str,
                 model_hash: str,
                 zk_proof: Dict[str, Any]) -> Dict[str, Any]:
        """Mint NFT for verified content"""
        
        # Prepare proof data
        proof_bytes = json.dumps(zk_proof).encode()
        
        # Build transaction
        transaction = self.contract.functions.mintVerifiedContent(
            to_address,
            token_uri,
            Web3.to_bytes(hexstr=content_hash),
            Web3.to_bytes(hexstr=model_hash),
            proof_bytes
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 2000000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign and send transaction
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            'transaction_hash': tx_hash.hex(),
            'token_id': self._get_token_id_from_receipt(receipt),
            'block_number': receipt['blockNumber']
        }
    
    def _get_token_id_from_receipt(self, receipt) -> int:
        """Extract token ID from transaction receipt (simplified)"""
        # In production, parse logs to get token ID
        return receipt['blockNumber'] * 1000 + receipt['transactionIndex']