
A robust, modular pre-model security gateway that protects Large Language Model (LLM) applications **before** user input reaches the model. Detects and blocks prompt injections, jailbreaks, system-prompt extractions, sensitive data exfiltration, paraphrased attacks, multilingual attacks (English, Urdu, Korean), and obfuscated inputs.

---

## 🚀 Key Features

- **Hybrid Detection Engine** — Fast keyword rule-based filter combined with a TF-IDF + Logistic Regression semantic ML classifier
- **Multilingual Coverage** — English, Urdu (Arabic script), and Korean (Hangul) keyword lists with mixed-language detection
- **Custom Presidio PII Detection** — Four custom Pattern Recognizers for Pakistani CNIC, University Student IDs, API Keys, and Dates of Birth
- **Three-Outcome Policy Engine** — `ALLOW`, `MASK`, or `BLOCK` decisions based on combined risk signals
- **Obfuscation Normalisation** — Leetspeak mapping and character-space squashing (`i g n o r e` → `ignore`) before detection
- **Full Audit Logging** — Every request logged to `results/audit_log.json` with scores, reason codes, decision, masked output, and per-stage latency

---

## 🔁 Processing Pipeline

```
[User Input]
     │
     ▼
Stage 0 — Language Detection & Leetspeak Normalisation (EN / UR / KO / MIXED)
     │
     ▼
Stage 1 — Rule-Based Keyword Scanning (EN + UR + KO keyword lists)
     │
     ▼
Stage 2 — Semantic ML Classifier (TF-IDF + Logistic Regression)
     │
     ▼
Stage 3 — Presidio PII Analyser & Anonymiser (custom entity recognisers)
     │
     ▼
Stage 4 — Policy Engine (ALLOW / MASK / BLOCK resolution)
     │
     ▼
Stage 5 — Audit Log Write (results/audit_log.json)
     │
     ▼
[Safe Output] → Anonymised text, original text, or rejection message
```

---

## 📂 Repository Structure

```
llm-security-gateway-final/
├── app/
│   ├── main.py                    # Flask API entry point (GET / and POST /check)
│   ├── pipeline.py                # Full 7-stage pipeline logic
│   ├── detectors/
│   │   ├── rule_detector.py       # Multilingual keyword detection (EN/UR/KO)
│   │   └── semantic_detector.py   # TF-IDF + Logistic Regression classifier
│   ├── pii/
│   │   └── presidio_custom.py     # Custom CNIC, Student ID, API Key recognisers
│   ├── policy/
│   │   └── policy_engine.py       # Risk scoring and ALLOW/MASK/BLOCK logic
│   └── utils/
│       ├── language.py            # Language detection + leetspeak normalisation
│       └── logging.py             # JSON audit log writer
├── config/
│   └── gateway_config.yaml        # Configurable thresholds and weights
├── data/
│   └── final_eval.csv             # 150-row labeled evaluation dataset
├── results/
│   ├── evaluation_results.csv     # Output of run_evaluation.py
│   └── audit_log.json             # Runtime audit trace log
├── run_evaluation.py              # Full dataset evaluation script
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation & Setup

**1. Clone the repository**
```bash
git clone [repo link here]
cd llm-security-gateway-final
```

**2. Create and activate a virtual environment**
```bash
python -m venv env

# Windows
.\env\Scripts\activate

```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the application**
```bash
python app/main.py
```

Open your browser and go to `http://127.0.0.1:5000`

---

## 📊 Running Evaluation

To run the full 150-row evaluation dataset and regenerate results:

```bash
python run_evaluation.py
```

Output is saved to `results/evaluation_results.csv`.

---

## 📈 Example API Request & Response

**POST** `/check` with JSON:
```json
{ "text": "my cnic is 03032-7976543-6" }
```

**Response:**
```json
{
  "input_text": "my cnic is 03032-7976543-6",
  "language": "EN",
  "rule_score": 0.0,
  "semantic_score": 0.23,
  "pii_score": 1,
  "composite": "NO",
  "final_risk": 0.3,
  "decision": "MASK",
  "final_output": "my cnic is <CNIC>",
  "reason_codes": "PII_DETECTED",
  "rule_latency": 4,
  "semantic_latency": 336,
  "presidio_latency": 818,
  "total_latency": 1178
}
```

---

## 📉 Evaluation Results (150-row dataset)

| Metric | Rule-Only Baseline | Hybrid (Final) |
|---|---|---|
| Accuracy | 61.3% | **73.3%** |
| Precision | 89.7% | **89.7%** |
| Recall | 42.6% | **64.9%** |
| F1-Score | 57.9% | **75.3%** |
| False Negatives | 54 | **33** |

**Per-category recall highlights:**
- Benign prompts: 100% (no false positives on safe input)
- Direct injection: 91%
- Multilingual attacks: 77%
- Obfuscated attacks: 82%
- Paraphrased attacks: 28% ← primary gap (see Limitations)

---

## ⚠️ Limitations

- Paraphrase recall is only 28% — TF-IDF lacks semantic generalisation for novel phrasings
- Short API keys not matching the `sk-[32+]` regex pattern go undetected
- `gateway_config.yaml` thresholds are defined but currently hardcoded in the policy engine

---

## 🛠️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/llm-security-gateway-final.git
cd llm-security-gateway-final
```

**2. Create a virtual environment**
```bash
python -m venv env
```

**3. Activate the virtual environment**
```bash
# Windows
.\env\Scripts\activate

# macOS / Linux
source env/bin/activate
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Download the spaCy language model (required for Presidio)**
```bash
python -m spacy download en_core_web_lg
```

**6. Run the application**
```bash
python app/main.py
```

**7. Open in browser**
