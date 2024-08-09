# app/moderation.py
from google.cloud import language_v1

def analyze_content(text: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    
    # Check for negative content
    if response.document_sentiment.score < -0.25:
        return True
    return False
