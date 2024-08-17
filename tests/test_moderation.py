import pytest
from app import moderation

class MockSentiment:
    def __init__(self, score):
        self.score = score

class MockAnalyzeSentimentResponse:
    def __init__(self, score):
        self.document_sentiment = MockSentiment(score=score)

@pytest.fixture
def mock_language_service_client(monkeypatch):
    class MockLanguageServiceClient:
        def analyze_sentiment(self, request):
            # Extract document content from the request dictionary
            text = request["document"].content
            if "great" in text:
                return MockAnalyzeSentimentResponse(score=0.5)
            elif "terrible" in text:
                return MockAnalyzeSentimentResponse(score=-0.5)
            else:
                return MockAnalyzeSentimentResponse(score=0.0)
    
    monkeypatch.setattr(
        "app.moderation.language_v1.LanguageServiceClient",
        MockLanguageServiceClient
    )

def test_analyze_content_positive_sentiment(mock_language_service_client):
    text = "This is a great post!"
    is_blocked = moderation.analyze_content(text)
    assert not is_blocked

def test_analyze_content_negative_sentiment(mock_language_service_client):
    text = "This is a terrible post!"
    is_blocked = moderation.analyze_content(text)
    assert is_blocked
