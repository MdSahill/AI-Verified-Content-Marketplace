import React, { useState } from 'react';
import axios from 'axios';

const ContentUpload = () => {
    const [content, setContent] = useState('');
    const [creatorAddress, setCreatorAddress] = useState('');
    const [isVerifying, setIsVerifying] = useState(false);
    const [verificationResult, setVerificationResult] = useState(null);

    const verifyContent = async () => {
        setIsVerifying(true);
        try {
            const response = await axios.post('http://localhost:8000/api/v1/verify', {
                content,
                content_type: 'text',
                creator_address: creatorAddress
            });
            setVerificationResult(response.data);
        } catch (error) {
            console.error('Verification failed:', error);
            alert('Verification failed');
        } finally {
            setIsVerifying(false);
        }
    };

    const mintNFT = async () => {
        if (!verificationResult) return;
        
        try {
            const response = await axios.post('http://localhost:8000/api/v1/mint', {
                content_hash: verificationResult.content_hash,
                creator_address: creatorAddress
            });
            alert(`NFT minted! Token ID: ${response.data.token_id}`);
        } catch (error) {
            console.error('Minting failed:', error);
            alert('Minting failed');
        }
    };

    return (
        <div className="content-upload">
            <h2>Upload Content for AI Verification</h2>
            
            <div>
                <label>Creator Address:</label>
                <input
                    type="text"
                    value={creatorAddress}
                    onChange={(e) => setCreatorAddress(e.target.value)}
                    placeholder="0x..."
                />
            </div>
            
            <div>
                <label>Content:</label>
                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    rows="10"
                    placeholder="Enter your content here..."
                />
            </div>
            
            <button onClick={verifyContent} disabled={isVerifying || !content}>
                {isVerifying ? 'Verifying...' : 'Verify Content'}
            </button>
            
            {verificationResult && (
                <div className="verification-result">
                    <h3>Verification Result</h3>
                    <p>Content Hash: {verificationResult.content_hash}</p>
                    <p>Status: {verificationResult.is_verified ? 'Verified' : 'Not Verified'}</p>
                    <p>AI Assistance: {verificationResult.verification_data.is_ai_assisted ? 'Detected' : 'Not Detected'}</p>
                    
                    <button onClick={mintNFT} disabled={!verificationResult.is_verified}>
                        Mint as NFT
                    </button>
                </div>
            )}
        </div>
    );
};

export default ContentUpload;