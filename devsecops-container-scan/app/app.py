from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to DevSecOps Container Security Demo!",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "devsecops-demo"
    }), 200

@app.route('/info')
def info():
    return jsonify({
        "app": "DevSecOps Demo Application",
        "description": "Sample app for container vulnerability scanning",
        "security": "Scanned with Trivy",
        "pipeline": "GitHub Actions"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
