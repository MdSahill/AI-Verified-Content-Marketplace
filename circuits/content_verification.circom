pragma circom 2.0.0;

include "node_modules/circomlib/circuits/comparators.circom";

template ContentVerification() {
    signal input contentHash;
    signal input modelHash;
    signal input verificationScore;
    signal input threshold;
    signal input isVerified;
    
    signal output verified;
    
    // Verify that verification score meets threshold
    component scoreCheck = GreaterEqThan(32);
    scoreCheck.in[0] <== verificationScore;
    scoreCheck.in[1] <== threshold;
    
    // Ensure content and model hashes are non-zero
    component contentNonZero = IsZero();
    contentNonZero.in <== contentHash;
    
    component modelNonZero = IsZero();
    modelNonZero.in <== modelHash;
    
    // Combined verification logic
    verified <== scoreCheck.out * (1 - contentNonZero.out) * (1 - modelNonZero.out) * isVerified;
}

component main = ContentVerification();