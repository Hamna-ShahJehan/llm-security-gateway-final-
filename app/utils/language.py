import re
def detect_language(text):
    if not text or len(text.strip()) == 0:
        return "EN" # Default fallback
        
    detected_languages = []
    text_lower = text.lower()
    
    # 1. Check for Urdu characters
    if re.search(r'[\u0600-\u06FF]', text_lower):
        detected_languages.append("UR")
        
    # 2. Check for Korean Hangul characters
    if re.search(r'[\uac00-\ud7af]', text_lower):
        detected_languages.append("KO")
        
    # 3. Check for English/Latin characters
    # We look for standard English words or longer character strings so standalone punctuation doesn't trip it
    if re.search(r'[a-z]{2,}', text_lower):
        detected_languages.append("EN")
        
    # ─── Decision Logic Matrix ───
    if len(detected_languages) > 1:
        # If multiple languages are found, return MIXED along with the breakdown (e.g., "MIXED (EN + UR)")
        return f"MIXED ({" + ".join(detected_languages)})"
    elif len(detected_languages) == 1:
        return detected_languages[0]
    
    return "EN" # Default if nothing else matches

def normalize_text(text: str) -> str:
    """Handles spacing, casing, and partial leetspeak variations."""
    text = text.lower()
    # Normalize leetspeak variations
    # replacements = {'0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '!': 'i'}
    
    replacements = {
        '0': 'o', '1': 'i', '2': 'z', '3': 'e', '4': 'a', 
        '5': 's', '6': 'g', '7': 't', '8': 'b', '9': 'g',
        '!': 'i', '@': 'a', '$': 's', '+': 't', '|': 'i',
        '€': 'e', '£': 'l', '¥': 'y',
        '(': 'c', '[': 'c', '{': 'c', '<': 'c',
        ')': '', ']': '', '}': '', '>': '', '*': ''  # Safely drop closing brackets
    }
    text = re.sub(r'[^a-zA-Z0-9\u0600-\u06FF\uac00-\ud7af\s]', '', text)
    for leet, normal in replacements.items():
        text = text.replace(leet, normal)
    # Clear spaces between split words (e.g., "j a i l b r e a k" -> "jailbreak")
    if len(re.findall(r'\b\w\s(?=\w\b)', text)) > 2:
        text = re.sub(r'\s+', '', text)
    return text
