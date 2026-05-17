import os
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Custom precise regex patterns
analyzer.registry.add_recognizer(PatternRecognizer(
    supported_entity="CNIC", 
    patterns=[Pattern("cnic", r"\b\d{5}-\d{7}-\d{1}\b", 0.95)]
))
analyzer.registry.add_recognizer(PatternRecognizer(
    supported_entity="STUDENT_ID", 
    patterns=[Pattern("sid", r"\b[A-Z0-9]{2,4}-[A-Z0-9]{3,4}-\d{3,4}\b", 0.95)]
))
analyzer.registry.add_recognizer(PatternRecognizer(
    supported_entity="API_KEY", 
    patterns=[Pattern("api", r"\b(sk-[a-zA-Z0-9]{32,48})\b", 0.95)]
))
analyzer.registry.add_recognizer(PatternRecognizer(
    supported_entity="DATE_OF_BIRTH", 
    patterns=[Pattern("dob", r"\b\d{2}-\d{2}-\d{4}\b", 0.95)]
))

CONTEXT_WORDS = ["cnic", "student id", "phone", "email", "api key","dob","date of birth", "ssn", "social security", "credit card", "card number", "person"]

def process_pii(text):
    raw_res = analyzer.analyze(text=text, language="en")   #raw results
    text_lower = text.lower()
    
    filtered_res = []
    has_context = any(w in text_lower for w in CONTEXT_WORDS)
    
    for r in raw_res:
        # Only boost if context words are explicitly near
        if has_context:
            r.score = min(r.score + 0.05, 1.0)
        # Higher confidence filter threshold to ignore weak matches
        if r.score >= 0.65:
            filtered_res.append(r)
            
    unique_types = set(r.entity_type for r in filtered_res)
    composite_detected = len(unique_types) > 1
    
    # Explicit replacement mappings matching your requirements
    operators = {
        "CNIC": OperatorConfig("replace", {"value": "<CNIC>"}),
        "STUDENT_ID": OperatorConfig("replace", {"value": "<STUDENT_ID>"}),
        "API_KEY": OperatorConfig("replace", {"value": "<API_KEY>"}),
        "PHONE_NUMBER": OperatorConfig("replace", {"value": "<PHONE>"}),
        "EMAIL_ADDRESS": OperatorConfig("replace", {"value": "<EMAIL>"}),
        "PERSON": OperatorConfig("replace", {"value": "<PERSON>"})
    }
    
    masked_text = text
    if len(filtered_res) > 0:
        anonymized_item = anonymizer.anonymize(text=text, analyzer_results=filtered_res, operators=operators)
        masked_text = anonymized_item.text
    
    entities_list = [{
        "type": r.entity_type, 
        "text": text[r.start:r.end], 
        "score": round(r.score, 2)
    } for r in filtered_res]
    
    return {
        "masked_text": masked_text,
        "pii_entities": entities_list,
        "composite": composite_detected
    }