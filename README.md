# AI-Verified Content Marketplace

A decentralized platform where AI tools verify original content creation and mint it as NFTs with proof of AI-assisted authenticity, using zero-knowledge proofs to protect proprietary models.

## Features

- **AI Content Verification**: Uses PyTorch models to verify content authenticity
- **Zero-Knowledge Proofs**: Protects proprietary AI models using zk-SNARKs
- **NFT Minting**: Converts verified content into tradable NFTs
- **Transparent Verification**: On-chain proof of AI verification without revealing model details
- **Content Authenticity**: Cryptographic proof of content origin and AI assistance

## Architecture

### Components

1. **AI Verification Engine** (Python/PyTorch)
   - Content processing and feature extraction
   - AI-assisted content detection
   - Model integrity hashing

2. **ZK Proof System** (Circom)
   - Generates proofs of verification without revealing model details
   - Circuit-based verification logic
   - Proof generation and validation

3. **Blockchain Layer** (Solidity)
   - NFT minting and management
   - Verification data storage
   - On-chain proof validation

4. **API Layer** (FastAPI)
   - RESTful API for content submission
   - Verification and minting endpoints
   - Database integration

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Ethereum client (Ganache/Hardhat)
- Circom compiler

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/ai-content-marketplace.git
   cd ai-content-marketplace
2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
3. **Blockchain Setup**
   ```bash
   # Using Hardhat or Ganache
   npx hardhat node
   npx hardhat run scripts/deploy.js --network localhost
4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
### Usage
1. **Content Verification**
   ```bash
   curl -X POST http://localhost:8000/api/v1/verify \
   -H "Content-Type: application/json" \
   -d '{
    "content": "Your original content here",
    "content_type": "text",
    "creator_address": "0xYourEthereumAddress"
   }'
2. **NFT Minting**
   ```bash
   curl -X POST http://localhost:8000/api/v1/mint \
   -H "Content-Type: application/json" \
   -d '{
    "content_hash": "verified_content_hash",
    "creator_address": "0xYourEthereumAddress"
   }'
