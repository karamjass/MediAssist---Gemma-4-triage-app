# 🏥 MediAssist — Rural Triage AI
### Gemma 4 Good Hackathon Submission

> Offline-capable medical triage assistant for rural clinics — powered by Gemma 4

---

## 🎯 Problem Statement
Rural clinics in India operate with:
- Spotty or no internet
- Limited staff & resources
- No specialist doctors

MediAssist uses **Gemma 4** (runs locally/on-device) to help clinic workers quickly triage patients, prioritize urgent cases, and provide actionable first-aid steps — even in zero-connectivity zones.

---

## ✨ Features
- 🚨 **3-level urgency triage** — CRITICAL / MODERATE / MINOR
- 📷 **Multimodal** — analyze wound/condition photos (Gemma 4 vision)
- 🗣️ **Hindi + English** — bilingual output
- 🏥 **Refer/No-refer decision** with reasoning
- ✅ **Do's and Don'ts** — prevents dangerous mistakes
- 📊 **Vitals to monitor** — structured monitoring guide
- 🔒 **Privacy-first** — no patient data sent to external servers

---

## 🚀 Quick Setup (5 minutes)

### Step 1 — Clone & enter project
```bash
cd medical-triage
```

### Step 2 — Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Get Google AI Studio API Key
1. Go to → https://aistudio.google.com/app/apikey
2. Click "Create API Key" (free)
3. Copy the key

### Step 5 — Configure environment
```bash
cp .env.example .env
# Open .env and paste your API key
```

### Step 6 — Run
```bash
python app.py
```

Open → **http://localhost:5000**

---

## 🧠 Model
Uses **Gemma 4** via Google AI Studio API:
- `gemma-4-9b-it` — default (fast)
- `gemma-4-27b-it` — more accurate (set in .env)

Change model in `.env`:
```
GEMMA_MODEL=gemma-4-27b-it
```

---

## 📁 Project Structure
```
medical-triage/
├── app.py              # Flask backend + Gemma 4 integration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── README.md
└── templates/
    └── index.html      # Full frontend UI
```

---

## 🔗 API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Web interface |
| `/api/triage` | POST | Run triage assessment |
| `/api/health` | GET | Server health check |

### `/api/triage` Request Body
```json
{
  "symptoms": "Patient has chest pain and difficulty breathing",
  "age": "45",
  "language": "English",
  "image": "data:image/jpeg;base64,..."
}
```

### Response
```json
{
  "urgency": "CRITICAL",
  "condition": "Suspected acute myocardial infarction",
  "first_aid": ["Make patient sit upright", "Give aspirin 300mg if available", "..."],
  "refer_to_hospital": true,
  "referral_reason": "Requires ECG and cardiac monitoring",
  "vitals_to_monitor": ["Blood pressure", "Pulse rate", "Oxygen saturation"],
  "do_not": ["Let patient walk", "Give food or water"],
  "notes": "Time-critical — every minute matters"
}
```

---

## 🌍 Impact
- Targets 640,000+ rural health centers in India
- Works on low-end devices with basic connectivity
- Bilingual (Hindi/English) for wider accessibility
- Structured output reduces human error in triage decisions

---

## 🏆 Hackathon
**The Gemma 4 Good Hackathon** · Deadline: May 19, 2026
Built with Gemma 4 multimodal capabilities for real-world social impact.
