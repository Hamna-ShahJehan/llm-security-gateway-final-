# import yaml

# def make_decision(rule_score: float, semantic_score: float, pii_entities: list, reason_codes: list, composite: bool) -> tuple[float, str]:
#     with open("config/gateway_config.yaml", "r") as f:
#         config = yaml.safe_load(f)
        
#     cfg_p = config["policy"]
#     cfg_s = config["scoring"]
    
#     # Calculate base composite risk
#     base_risk = (rule_score * cfg_s["rule_weight"]) + (semantic_score * cfg_s["semantic_weight"])
    
#     # Add adjustments based on findings
#     if len(pii_entities) > 0:
#         base_risk += cfg_s["pii_weight"]
#     if composite:
#         base_risk += cfg_s["composite_weight"]
#     if "DATA_EXFILTRATION" in reason_codes:
#         base_risk += cfg_s["secret_weight"]
        
#     final_risk = min(float(base_risk), 1.0)
    
#     # Clear routing rules
#     if final_risk >= cfg_p["block_threshold"] or "PROMPT_INJECTION" in reason_codes or "JAILBREAK" in reason_codes or "SEMANTIC_INJECTION" in reason_codes or semantic_score >= 0.75 or "DATA_EXFILTRATION" in reason_codes:
#         decision = "BLOCK"
#     elif len(pii_entities) > 0:
#         # FIXED: Only mask if PII is actually present
#         decision = "MASK"
#     else:
#         decision = "ALLOW"
        
#     return final_risk, decision



# def make_decision(rule_score: float, semantic_score: float, pii_entities: list, reason_codes: list, composite: bool) -> tuple[float, str]:
#     """
#     Super Simplified Security Gateway.
#     Blocks immediately if ANY attack type is found in the reason codes, 
#     or if the ML semantic engine reports a high attack probability.
#     """
    
#     # 1. Define our absolute high-confidence ML threshold
#     ML_ATTACK_THRESHOLD = 0.70 
    
#     # 2. Check if the ML model says it's a semantic attack
#     is_semantic_attack = semantic_score >= ML_ATTACK_THRESHOLD

#     # 3. Simplify risk tracking: 1.0 means an attack was caught, 0.0 means safe
#     if len(reason_codes) > 0 or is_semantic_attack:
#         final_risk = 1.0
#         decision = "BLOCK"
        
#     # 4. If no attacks are found, check if we need to clean up sensitive PII
#     elif len(pii_entities) > 0:
#         final_risk = 0.0
#         decision = "MASK"
        
#     # 5. If it's completely clean ground, let it pass
#     else:
#         final_risk = 0.0
#         decision = "ALLOW"
        
#     return final_risk, decision



# def make_decision(rule_score: float, semantic_score: float, pii_entities: list, reason_codes: list, composite: bool) -> tuple[float, str]:
#     # 🛡️ CRASH PROTECTION: If reason_codes or pii_entities are None, turn them into clean empty lists
#     if reason_codes is None:
#         reason_codes = []
#     if pii_entities is None:
#         pii_entities = []

#     # 1. High-confidence ML Threshold
#     ML_ATTACK_THRESHOLD = 0.70 
#     is_semantic_attack = semantic_score >= ML_ATTACK_THRESHOLD

#     # 2. Define real attack tags explicitly
#     attack_categories = ["PROMPT_INJECTION", "JAILBREAK", "DATA_EXFILTRATION", "SEMANTIC_INJECTION"]
#     has_active_attack_code = any(attack in reason_codes for attack in attack_categories)

#     # 3. Secure Routing Gate
#     if has_active_attack_code or is_semantic_attack:
#         final_risk = 1.0
#         decision = "BLOCK"
        
#     elif len(pii_entities) > 0:
#         final_risk = 0.0
#         decision = "MASK"  # Now your phone number and CNIC will hit here perfectly!
        
#     else:
#         final_risk = 0.0
#         decision = "ALLOW"
        
#     return final_risk, decision




# def make_decision(rule_score, semantic_score,
#                   pii_entities, reason_codes):

#     ATTACK_THRESHOLD = 0.70

#     # attack detection
#     attack_detected = (
#         rule_score >= ATTACK_THRESHOLD or
#         semantic_score >= ATTACK_THRESHOLD or
#         len(reason_codes) > 0
#     )

#     # BLOCK
#     if attack_detected:
#         return 1.0, "BLOCK"

#     # MASK
#     elif len(pii_entities) > 0:
#         return 0.3, "MASK"

#     # ALLOW
#     else:
#         return 0.0, "ALLOW"


import yaml

def make_decision(rule_score, semantic_score,
                  pii_entities, reason_codes,
                  composite):

    # Optional config loading
    with open("config/gateway_config.yaml", "r") as f:
        config = yaml.safe_load(f)

    ATTACK_CODES = [
        "PROMPT_INJECTION",
        "JAILBREAK",
        "DATA_EXFILTRATION",
        "SEMANTIC_INJECTION"
    ]

    # Check for attacks
    attack_detected = any(
        code in ATTACK_CODES
        for code in reason_codes
    )

    # ML threshold
    if semantic_score >= 0.75:
        attack_detected = True

    # BLOCK
    if attack_detected:
        return 1.0, "BLOCK"

    # MASK
    elif len(pii_entities) > 0:
        return 0.3, "MASK"

    # ALLOW
    else:
        return 0.0, "ALLOW"