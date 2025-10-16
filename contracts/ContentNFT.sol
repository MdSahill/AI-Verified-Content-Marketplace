// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ContentNFT is ERC721, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    struct VerificationData {
        bytes32 contentHash;
        bytes32 modelHash;
        bytes zkProof;
        bool isVerified;
        uint256 timestamp;
    }

    mapping(uint256 => VerificationData) public verificationData;
    mapping(bytes32 => bool) public contentHashes;

    event ContentMinted(
        uint256 indexed tokenId,
        address indexed creator,
        bytes32 contentHash,
        bytes32 modelHash,
        string tokenURI
    );

    constructor() ERC721("AIVerifiedContent", "AIVC") {}

    function mintVerifiedContent(
        address to,
        string memory tokenURI,
        bytes32 contentHash,
        bytes32 modelHash,
        bytes memory zkProof
    ) external returns (uint256) {
        require(!contentHashes[contentHash], "Content already minted");
        
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();

        _mint(to, newTokenId);
        _setTokenURI(newTokenId, tokenURI);

        verificationData[newTokenId] = VerificationData({
            contentHash: contentHash,
            modelHash: modelHash,
            zkProof: zkProof,
            isVerified: true,
            timestamp: block.timestamp
        });

        contentHashes[contentHash] = true;

        emit ContentMinted(newTokenId, to, contentHash, modelHash, tokenURI);

        return newTokenId;
    }

    function getVerificationData(uint256 tokenId) 
        external 
        view 
        returns (bytes32, bytes32, bool) 
    {
        require(_exists(tokenId), "Token does not exist");
        VerificationData memory data = verificationData[tokenId];
        return (data.contentHash, data.modelHash, data.isVerified);
    }

    function _setTokenURI(uint256 tokenId, string memory tokenURI) internal {
        // In production, you might want to store this differently
        // This is a simplified implementation
    }

    function tokenURI(uint256 tokenId) 
        public 
        view 
        virtual 
        override 
        returns (string memory) 
    {
        require(_exists(tokenId), "URI query for nonexistent token");
        // In production, return actual stored URI
        return "https://ipfs.io/ipfs/example";
    }
}