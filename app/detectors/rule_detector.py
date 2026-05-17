import re

def rule_detect(text: str) -> dict:
    # Your exact dictionary kept completely as it is
    keywords = {
        "prompt_injection": [
            "ignore", "forget", "disregard", "override", "bypass instructions",
            "new instructions", "instead follow", "do not follow", "change rules",
            "system prompt", "hidden instructions", "developer message", "پرامپٹ",
            "نظر انداز کریں", "بھول جائیں", "ترمیم کریں", "ہدایات کو بائی پاس کریں", 
            "نئی ہدایات", "سسٹم پرامپٹ", "خفیہ ہدایات",
            "무시하십시오", "잊어버리세요", "기존 지침 무시", "새로운 지침", "시스템 프롬프트"
        ],
        "jailbreak": [
            "act as", "act like", "pretend", "roleplay", "simulate", "you are now",
            "no restrictions", "without restrictions", "bypass", "break rules",
            # Urdu translations
            "کے طور پر کام کریں", "ڈرامہ کریں", "نقالی کریں", "کوئی پابندی نہیں", "اصول توڑیں",
            # Korean translations
            "역할을 하십시오", "흉내내세요", "역할 놀이", "제한 없음", "규칙 위반", "우회"
        ],
        "data_exfiltration": [
            "api key", "password", "secret", "token", "credentials",
            "private", "confidential", "sensitive", "internal", "leak", "expose",
            # Urdu translations
            "پاس ورڈ", "خفیہ کوڈ", "ٹوکن", "خفیہ ڈیٹا", "لیک کریں", "ظاہر کریں",
            # Korean translations
            "비밀번호", "시크릿 토큰", "기밀 정보", "민감한 데이터", "유출", "폭로"
        ]
    }
    
    # Squash spaces from the input text for matching
    text_squashed = text.lower().replace(" ", "")
    
    # Match using your concise design: squash the keyword space inside the loop at runtime!
    p = any(k.replace(" ", "") in text_squashed for k in keywords["prompt_injection"])
    j = any(k.replace(" ", "") in text_squashed for k in keywords["jailbreak"])
    d = any(k.replace(" ", "") in text_squashed for k in keywords["data_exfiltration"])
    
    
    score = 0.0
    if p or j or d:
        score = 0.70
        
    return {
        "rule_score": score,
        "prompt_injection": p,
        "jailbreak": j,
        "data_exfiltration": d
    }