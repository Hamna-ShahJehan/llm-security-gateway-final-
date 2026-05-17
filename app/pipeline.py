import time
import os
import sys

# Ensure module pathing stays linked
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils import language
from utils.language import detect_language, normalize_text
from detectors.rule_detector import rule_detect
from detectors.semantic_detector import semantic_score
from pii.presidio_custom import process_pii
from policy.policy_engine import make_decision
from utils.logging import write_log

def run_pipeline(text: str, input_id: str = "case_default") -> dict:
    start_total = time.time()
    
    # 0. Language Processing
    language = detect_language(text)
    clean_text = normalize_text(text)
    
    # 1. Rule Evaluation + Latency
    start_rule = time.time()
    rule_res = rule_detect(clean_text)
    rule_score = rule_res["rule_score"]
    rule_latency = int((time.time() - start_rule) * 1000)
    
    reason_codes = []
    if rule_res["prompt_injection"]: reason_codes.append("PROMPT_INJECTION")
    if rule_res["jailbreak"]: reason_codes.append("JAILBREAK")
    if rule_res["data_exfiltration"]: reason_codes.append("DATA_EXFILTRATION")
    
    # 2. Semantic Evaluation + Latency
    start_sem = time.time()
    sem_score = semantic_score(clean_text)
    if sem_score > 0.75:
        reason_codes.append("SEMANTIC_INJECTION")
    sem_latency = int((time.time() - start_sem) * 1000)
        
    # 3. Presidio PII Parsing Layer + Latency
    start_pii = time.time()
    pii_res = process_pii(text)
    pii_latency = int((time.time() - start_pii) * 1000)
    if len(pii_res["pii_entities"]) > 0:
        reason_codes.append("PII_DETECTED")

    # 4. Policy Verification Matrix + Latency
    start_pol = time.time()
    final_risk, decision = make_decision(
        rule_score, 
        sem_score, 
        pii_res["pii_entities"], 
        reason_codes, 
        pii_res["composite"]
    )
    policy_latency = int((time.time() - start_pol) * 1000)
    
    # 5. Output Text Determination
    if decision == "BLOCK":
        final_output = "Input Blocked due to policy violations."
    elif decision == "MASK":
        final_output = pii_res["masked_text"]
    else:
        final_output = text
        
    total_latency = int((time.time() - start_total) * 1000)
    
    # Format return dictionary to match your exact HTML rendering variables
    result = {
        "input_text": text,
        "language": language.upper(),
        "rule_score": round(rule_score, 2),
        "semantic_score": round(sem_score, 2),
        "pii_score": len(pii_res["pii_entities"]),
        "composite": "YES" if pii_res["composite"] else "NO",
        "final_risk": round(final_risk, 2),
        "decision": decision,
        "final_output": final_output,
        "reason_codes": ", ".join(reason_codes) if reason_codes else "None",
        "rule_latency": max(rule_latency, 1),
        "semantic_latency": max(sem_latency, 1),
        "presidio_latency": max(pii_latency, 1),
        "policy_latency": max(policy_latency, 1),
        "total_latency": max(total_latency, 1)
    }

    # # 1. Transform your raw Presidio entities to match the required format
    # formatted_pii_entities = []
    # for entity in pii_res.get("pii_entities", []):
    #     formatted_pii_entities.append({
    #         "type": entity.get("entity_type"),  # Checks for the tag type (e.g., EMAIL_ADDRESS)
    #         "text": text[entity.get("start"):entity.get("end")],  # Extracts the raw text string
    #         "score": round(entity.get("score", 0.0), 2)  # Extracted match confidence
    # })

    # # 2. Build the exact required JSON response object
    # result = {
    #     "input_id": "case_041",  # Replace with your dynamic ID generation variable if available
    #     "language": language.upper(),  # target uses lowercase format (e.g., 'ur')
    #     "rule_score": round(rule_score, 2),
    #     "semantic_score": round(sem_score, 2),
    #     "pii_entities": formatted_pii_entities,  # Replaced with the clean list structure
    #     "final_risk": round(final_risk, 2),
    #     "decision": decision,
    #     "safe_text": final_output if decision == "MASK" else None,  # null if blocked, masked string if active
    #     "reason_codes": reason_codes if reason_codes else [],  # Keeps it as a clean Python list array
    #     "latency_ms": max(total_latency, 1)  # Maps total latency execution to target key
    # }
    
    write_log(result)
    return result