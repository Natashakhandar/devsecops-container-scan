# DevSecOps Container Scanning - Complete Setup Guide

This guide provides step-by-step instructions to set up and run the DevSecOps container vulnerability scanning project from scratch.

## 📋 Prerequisites

Before starting, ensure you have:

### Required:
- ✅ **GitHub Account**: Free account at [github.com](https://github.com)
- ✅ **Git Installed**: Download from [git-scm.com](https://git-scm.com)
- ✅ **Basic Command Line Knowledge**: Familiarity with terminal/command prompt

### Optional (for local testing):
- 🔧 **Docker Desktop**: For building and testing images locally
  - Windows/Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Linux: Docker Engine
- 🔧 **Trivy CLI**: For local scans (optional)
- 🔧 **VS Code or any code editor**: For editing files

---

## 🚀 Step-by-Step Setup

### Step 1: Create GitHub Repository

1. **Log in to GitHub**
   - Navigate to [github.com](https://github.com)
   - Sign in with your credentials

2. **Create New Repository**
   - Click the `+` icon in top-right corner
   - Select **"New repository"**

3. **Configure Repository**
   ```
   Repository name: devsecops-container-scan
   Description: DevSecOps mini project with automated container vulnerability scanning
   Visibility: Public (or Private)
   ✓ Add a README file
   .gitignore template: None
   License: MIT (optional)
   ```

4. **Create Repository**
   - Click **"Create repository"** button

### Step 2: Clone Repository to Local Machine

Open your terminal/command prompt and run:

```bash
# Navigate to your projects directory
cd ~/projects  # On Windows: cd C:\Users\YourName\projects

# Clone the repository
git clone https://github.com/YOUR_USERNAME/devsecops-container-scan.git

# Navigate into the project directory
cd devsecops-container-scan
```

**Replace `YOUR_USERNAME`** with your actual GitHub username.

### Step 3: Create Project Structure

Create the following directory structure:

```bash
# Create directories
mkdir -p .github/workflows
mkdir -p app
mkdir -p docs
mkdir -p reports

# Verify structure
ls -la  # On Windows: dir
```

Your structure should look like:
```
devsecops-container-scan/
├── .github/
│   └── workflows/
├── app/
├── docs/
├── reports/
└── README.md
```

### Step 4: Create Application Files

#### 4.1 Create Flask Application

Create `app/app.py`:

```bash
# On Linux/Mac
cat > app/app.py << 'EOF'
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
EOF
```

**On Windows**, use a text editor to create the file with the above content.

#### 4.2 Create Requirements File

Create `app/requirements.txt`:

```bash
cat > app/requirements.txt << 'EOF'
Flask==2.3.3
Werkzeug==2.3.7
requests==2.31.0
EOF
```

#### 4.3 Create Dockerfile

Create `app/Dockerfile`:

```bash
cat > app/Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/health')"

CMD ["python", "app.py"]
EOF
```

### Step 5: Create GitHub Actions Workflow

Create `.github/workflows/container-scan.yml`:

**Note**: See the full workflow file content in the project repository or copy from the README.

The workflow includes:
- Docker image build
- Trivy vulnerability scanning
- Report generation
- GitHub Security tab integration

### Step 6: Create Documentation Files

Create the following documentation files in the `docs/` directory:

1. `docs/PROJECT_EXPLANATION.md` - Detailed project explanation
2. `docs/SETUP_GUIDE.md` - This setup guide
3. `docs/ARCHITECTURE.md` - Architecture documentation

### Step 7: Create .trivyignore File (Optional)

Create `.trivyignore` in the root directory:

```bash
cat > .trivyignore << 'EOF'
# Trivy ignore file
# Add CVE IDs here to ignore specific vulnerabilities
# Example:
# CVE-2021-12345

# Use with caution and document why vulnerabilities are ignored
EOF
```

### Step 8: Update Main README.md

Update the root `README.md` with project information (see the README template in the repository).

### Step 9: Commit and Push to GitHub

```bash
# Stage all files
git add .

# Commit changes
git commit -m "Initial commit: DevSecOps container scanning project"

# Push to GitHub
git push origin main
```

**Note**: If your default branch is named `master` instead of `main`, use:
```bash
git push origin master
```

### Step 10: Verify GitHub Actions Setup

1. **Navigate to Your Repository on GitHub**
   - Go to `https://github.com/YOUR_USERNAME/devsecops-container-scan`

2. **Check Actions Tab**
   - Click on the **"Actions"** tab
   - You should see your workflow running or completed
   - Click on the workflow run to see detailed logs

3. **View Workflow Execution**
   - Expand each step to see execution details
   - Look for Trivy scan results in the logs
   - Check for any vulnerabilities detected

### Step 11: Check Security Tab

1. **Navigate to Security Tab**
   - Click on **"Security"** tab in your repository
   - Select **"Code scanning alerts"** (if available)

2. **View Vulnerability Findings**
   - See all detected vulnerabilities
   - Filter by severity level
   - View detailed information for each CVE

---

## 🧪 Testing the Project

### Test 1: Trigger Pipeline Manually

1. Go to **Actions** tab
2. Select your workflow
3. Click **"Run workflow"** button
4. Select branch and click **"Run workflow"**

### Test 2: Make a Code Change

1. Edit `app/app.py` locally
2. Add a new route:
   ```python
   @app.route('/test')
   def test():
       return jsonify({"test": "success"})
   ```
3. Commit and push:
   ```bash
   git add app/app.py
   git commit -m "Add test endpoint"
   git push origin main
   ```
4. Watch the pipeline execute automatically

### Test 3: Local Docker Build (Optional)

If you have Docker installed:

```bash
# Navigate to app directory
cd app

# Build image
docker build -t myapp:local .

# Run container
docker run -p 5000:5000 myapp:local

# Test in browser
# Visit: http://localhost:5000
```

### Test 4: Local Trivy Scan (Optional)

If you have Trivy installed locally:

```bash
# Scan the local image
trivy image myapp:local

# Scan with specific severity
trivy image --severity HIGH,CRITICAL myapp:local

# Generate JSON report
trivy image --format json --output report.json myapp:local
```

---

## 🔧 Troubleshooting

### Issue 1: Workflow Not Triggering

**Problem**: Pipeline doesn't run after pushing code

**Solutions**:
- Check that workflow file is in `.github/workflows/` directory
- Verify YAML syntax is correct
- Ensure branch name matches workflow configuration
- Check repository settings → Actions → Allow all actions

### Issue 2: Docker Build Fails

**Problem**: "Error building Docker image"

**Solutions**:
- Verify Dockerfile syntax
- Check that all required files exist in `app/` directory
- Review build logs for specific error messages
- Ensure requirements.txt has correct package versions

### Issue 3: Trivy Scan Takes Too Long

**Problem**: Scan step times out

**Solutions**:
- Add timeout parameter to workflow:
  ```yaml
  timeout-minutes: 10
  ```
- Use `--timeout` flag in Trivy command
- Check GitHub Actions runner status

### Issue 4: SARIF Upload Fails

**Problem**: Cannot upload to Security tab

**Solutions**:
- Verify repository has Security features enabled
- Check workflow permissions in YAML
- Ensure SARIF file is generated correctly
- Use `if: always()` to upload even on failure

### Issue 5: Build Fails Due to Vulnerabilities

**Problem**: Pipeline fails with "Vulnerabilities detected"

**Solutions**:
- **Short-term**: Lower severity threshold or use `.trivyignore`
- **Long-term**: Update base image and dependencies
  ```dockerfile
  FROM python:3.11-slim  # Use newer version
  ```
- Review and update `requirements.txt` versions

---

## 📊 Understanding Scan Results

### Reading Trivy Output

```
Total: 45 (UNKNOWN: 0, LOW: 20, MEDIUM: 15, HIGH: 8, CRITICAL: 2)
```

- **Total**: Total number of vulnerabilities found
- **UNKNOWN**: Vulnerabilities without CVSS scores
- **LOW**: Minor risks (CVSS 0.1-3.9)
- **MEDIUM**: Moderate risks (CVSS 4.0-6.9)
- **HIGH**: Significant risks (CVSS 7.0-8.9)
- **CRITICAL**: Severe risks (CVSS 9.0-10.0)

### Vulnerability Report Format

```
CVE-2021-12345 (HIGH)
Package: libssl1.1
Installed Version: 1.1.1f
Fixed Version: 1.1.1k
```

**Action**: Update base image or package to fixed version

---

## 🎯 Next Steps After Setup

### 1. Customize for Your Needs
- Modify the Flask app for your use case
- Adjust vulnerability severity thresholds
- Add more security scanning tools (SAST, secrets scanning)

### 2. Add Notifications
- Configure Slack webhooks for alerts
- Set up email notifications
- Integrate with incident management tools

### 3. Extend the Pipeline
- Add unit tests
- Implement code coverage
- Add deployment stages
- Integrate with container registries

### 4. Document Your Work
- Add screenshots to README
- Document findings and resolutions
- Create a project presentation

### 5. Practice for Interviews
- Explain the pipeline flow
- Discuss security best practices
- Demonstrate live in interviews

---

## ✅ Verification Checklist

Before considering setup complete, verify:

- [ ] Repository created on GitHub
- [ ] All files and directories in place
- [ ] Workflow file has correct YAML syntax
- [ ] First pipeline run completed successfully
- [ ] Scan results visible in Actions logs
- [ ] Security tab shows vulnerabilities (if any)
- [ ] Reports downloadable as artifacts
- [ ] README.md is comprehensive
- [ ] Documentation is complete
- [ ] Project ready for portfolio/interviews

---

## 📞 Getting Help

If you encounter issues:

1. **Check GitHub Actions Logs**: Detailed error messages
2. **Review Trivy Documentation**: [aquasecurity.github.io/trivy](https://aquasecurity.github.io/trivy)
3. **GitHub Actions Docs**: [docs.github.com/actions](https://docs.github.com/actions)
4. **Stack Overflow**: Search for specific error messages
5. **GitHub Issues**: Check Trivy and GitHub Actions issues

---

## 🎓 Learning Resources

- **DevSecOps Fundamentals**: [OWASP DevSecOps Guidelines](https://owasp.org/www-project-devsecops-guideline/)
- **Container Security**: [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- **Trivy Tutorial**: [Trivy Getting Started](https://aquasecurity.github.io/trivy/)
- **GitHub Actions Tutorial**: [GitHub Skills](https://skills.github.com/)

---

**Congratulations!** 🎉 You've successfully set up a DevSecOps container vulnerability scanning pipeline. This project demonstrates your understanding of security automation and modern DevOps practices.
