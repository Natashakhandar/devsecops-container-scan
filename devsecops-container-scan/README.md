# DevSecOps Container Vulnerability Scanning Project

## 🔒 Project Overview
This DevSecOps mini project demonstrates automated container vulnerability scanning using Trivy integrated with GitHub Actions CI/CD pipeline. The project scans Docker images for security vulnerabilities and generates automated alerts when critical issues are detected.

## 🚀 Features
- ✅ Automated Docker image vulnerability scanning using Trivy
- ✅ CI/CD pipeline integration with GitHub Actions
- ✅ Severity-based scanning (CRITICAL, HIGH, MEDIUM, LOW)
- ✅ Automated scan reports generation
- ✅ Build failure on critical vulnerabilities
- ✅ JSON and SARIF report formats
- ✅ GitHub Security tab integration
- ✅ Sample Python Flask application

## 🛠️ Technologies Used
- **Trivy**: Open-source vulnerability scanner by Aqua Security
- **GitHub Actions**: CI/CD automation
- **Docker**: Container platform
- **Python Flask**: Sample application
- **SARIF**: Security report format

## 📁 Project Structure
```
devsecops-container-scan/
├── .github/
│   └── workflows/
│       └── container-scan.yml       # CI/CD pipeline configuration
├── app/
│   ├── Dockerfile                   # Docker image definition
│   ├── app.py                       # Sample Flask application
│   └── requirements.txt             # Python dependencies
├── docs/
│   ├── PROJECT_EXPLANATION.md       # Detailed project documentation
│   ├── SETUP_GUIDE.md              # Step-by-step setup instructions
│   └── ARCHITECTURE.md             # Architecture and workflow
├── reports/                         # Scan reports directory
├── .trivyignore                     # Trivy ignore file (optional)
└── README.md                        # This file
```

## 🎯 Quick Start

### Prerequisites
- GitHub account
- Git installed
- Docker installed (for local testing)
- Basic understanding of CI/CD pipelines

### Setup Steps
1. Fork/Clone this repository
2. Navigate to repository Settings → Secrets and variables → Actions
3. The GitHub Actions workflow will run automatically on push/pull requests
4. Check the Actions tab to see scan results

For detailed setup instructions, see [SETUP_GUIDE.md](docs/SETUP_GUIDE.md)

## 📊 How It Works
1. Developer pushes code or creates a pull request
2. GitHub Actions workflow triggers automatically
3. Docker image is built from the application code
4. Trivy scans the image for known vulnerabilities
5. Results are analyzed and reports are generated
6. If CRITICAL or HIGH vulnerabilities are found, the build fails
7. Reports are uploaded to GitHub Security tab

## 📈 Scan Reports
- Scan results are available in the GitHub Actions logs
- SARIF reports are uploaded to GitHub Security tab
- JSON reports are stored as workflow artifacts

## 🔧 Customization
- Modify `.github/workflows/container-scan.yml` to adjust scan severity levels
- Update `Dockerfile` to change the base image
- Add ignored vulnerabilities to `.trivyignore` file

## 📚 Learn More
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [DevSecOps Best Practices](https://owasp.org/www-project-devsecops-guideline/)

## 👨‍💻 Author
Created as a DevSecOps learning project

## 📝 License
MIT License - feel free to use for learning and portfolio purposes
