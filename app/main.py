import os
import sys
from flask import Flask, request, jsonify, render_template
# Setup base routing fallback configurations
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)
from app.pipeline import run_pipeline
app = Flask(__name__, 
            template_folder=os.path.join(base_dir, 'app', 'templates'),
            static_folder=os.path.join(base_dir, 'app', 'static'))

@app.route("/")
def home():
    return render_template("template1.html")

@app.route("/check", methods=["POST"])
def check():
    if request.is_json:
        data = request.get_json()
        text = data.get("text", "")
        return jsonify(run_pipeline(text))
        
    # Standard HTML text input capture
    text = request.form.get("text", "")
    if not text.strip():
        return render_template("template1.html")
        
    result = run_pipeline(text)
    return render_template("template1.html", **result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)