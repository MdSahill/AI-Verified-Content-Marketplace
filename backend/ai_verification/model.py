import torch
import torch.nn as nn
import hashlib
import json
from typing import Dict, Tuple, Any

class ContentVerificationModel(nn.Module):
    def __init__(self, input_size: int = 768, hidden_size: int = 512, output_size: int = 256):
        super(ContentVerificationModel, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, output_size)
        )
        
        self.verification_head = nn.Sequential(
            nn.Linear(output_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 2)  # [original_prob, ai_assisted_prob]
        )
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        encoded = self.encoder(x)
        verification = self.verification_head(encoded)
        return encoded, verification
    
    def get_model_hash(self) -> str:
        """Generate hash of model architecture and parameters"""
        model_info = {
            'architecture': str(self),
            'parameters_hash': hashlib.sha256(
                str([p.data for p in self.parameters()]).encode()
            ).hexdigest()
        }
        return hashlib.sha256(json.dumps(model_info).encode()).hexdigest()

class ContentProcessor:
    def __init__(self, model_path: str = None):
        self.model = ContentVerificationModel()
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
    
    def process_content(self, content: str) -> Dict[str, Any]:
        """Process content and generate verification features"""
        # Convert content to feature vector (simplified)
        content_features = self._text_to_features(content)
        
        with torch.no_grad():
            encoded, verification = self.model(content_features)
            
        # Convert to probabilities
        probs = torch.softmax(verification, dim=-1)
        
        return {
            'content_hash': self._hash_content(content),
            'feature_vector': encoded.numpy().tolist(),
            'verification_scores': probs.numpy().tolist(),
            'model_hash': self.model.get_model_hash(),
            'is_ai_assisted': probs[0][1] > 0.5  # Threshold for AI-assisted detection
        }
    
    def _text_to_features(self, text: str) -> torch.Tensor:
        """Convert text to feature vector (simplified - use proper embeddings in production)"""
        # In production, use sentence transformers or similar
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        # Convert hash to numerical features (simplified approach)
        features = [int(text_hash[i:i+8], 16) for i in range(0, min(len(text_hash), 192), 8)]
        # Pad or truncate to 768 features
        features = features[:768] + [0] * (768 - len(features))
        return torch.tensor(features, dtype=torch.float32).unsqueeze(0)
    
    def _hash_content(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()