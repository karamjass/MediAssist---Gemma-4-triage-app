import os
import base64
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not set in .env file")

# Available Gemma 4 models via Gemini API:
#   gemma-4-26b-a4b-it  (26B MoE — faster)
#   gemma-4-31b-it      (31B Dense — more accurate)
MODEL_NAME = os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it")

client = genai.Client(api_key=GOOGLE_API_KEY)

SYSTEM_PROMPT = """You are MediAssist, an expert medical triage AI for rural clinics in India with limited resources.
Analyze the patient symptoms and optionally the wound/condition image provided.

Respond ONLY in this exact JSON format (no markdown, no extra text):
{
  "urgency": "CRITICAL|MODERATE|MINOR",
  "condition": "Likely condition in 1 sentence",
  "first_aid": ["Step 1", "Step 2", "Step 3", "Step 4"],
  "refer_to_hospital": true or false,
  "referral_reason": "Reason to refer (empty string if false)",
  "vitals_to_monitor": ["Vital 1", "Vital 2"],
  "do_not": ["Thing to avoid 1", "Thing to avoid 2"],
  "notes": "Any important additional clinical note"
}

Rules:
- CRITICAL: life-threatening, needs immediate emergency care
- MODERATE: needs medical attention within hours
- MINOR: can be managed at clinic or home
- Be practical for low-resource rural settings
- If image shows wound/injury, factor that into assessment
- Keep all text concise and action-oriented"""


def parse_json_response(text):
    text = text.strip()
    for fence in ["```json", "```"]:
        if fence in text:
            text = text.split(fence)[1].split("```")[0].strip()
            break
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end != 0:
        text = text[start:end]
    return json.loads(text)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/triage", methods=["POST"])
def triage():
    data = request.json
    symptoms = data.get("symptoms", "").strip()
    language = data.get("language", "English")
    age = data.get("age", "").strip()
    image_data = data.get("image")

    if not symptoms:
        return jsonify({"error": "Please describe the symptoms."}), 400

    patient_info = f"Patient symptoms: {symptoms}"
    if age:
        patient_info = f"Patient age: {age}\n" + patient_info
    

    contents = []

    if image_data:
        try:
            if "," in image_data:
                header, b64 = image_data.split(",", 1)
                mime_type = header.split(":")[1].split(";")[0] if ":" in header else "image/jpeg"
            else:
                b64, mime_type = image_data, "image/jpeg"
            image_bytes = base64.b64decode(b64)
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
        except Exception as e:
            return jsonify({"error": f"Image processing failed: {str(e)}"}), 400

    contents.append(patient_info)

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
                max_output_tokens=1024,
            )
        )
        result = parse_json_response(response.text)
        return jsonify(result)

    except json.JSONDecodeError:
        return jsonify({"error": "Could not parse model response.", "raw": response.text[:500]}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "model": MODEL_NAME})


if __name__ == "__main__":
    print(f"✅ MediAssist running → http://localhost:5000")
    print(f"✅ Using model: {MODEL_NAME}")
    app.run(debug=True, port=5000)