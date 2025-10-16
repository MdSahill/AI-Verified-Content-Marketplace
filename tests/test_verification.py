
def test_verify_stub():
    from backend.ai_verification.verification import verify_content
    r = verify_content("hello")
    assert "model" in r
