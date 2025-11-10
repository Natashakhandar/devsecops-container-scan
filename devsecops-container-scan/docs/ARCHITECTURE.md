# DevSecOps Container Scanning - Architecture Documentation

## 🏛️ System Architecture

This document provides a comprehensive overview of the system architecture, components, data flow, and technical implementation details.

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Developer Workstation                    │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Code      │→ │ Dockerfile   │→ │  Git Push/PR     │   │
│  │  (Python)   │  │              │  │                  │   │
│  └─────────────┘  └──────────────┘  └──────────┬───────┘   │
└──────────────────────────────────────────────────┼──────────┘
                                                   │
                                                   ↓
┌─────────────────────────────────────────────────────────────┐
│                       GitHub Repository                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Source Code, Dockerfile, Workflow YAML             │   │
│  └────────────────────────┬────────────────────────────┘   │
└────────────────────────────┼───────────────────────────────┘
                             │ Trigger on Push/PR
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Actions (CI/CD)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Workflow Execution                       │  │
│  │  1. Checkout Code                                     │  │
│  │  2. Setup Docker                                      │  │
│  │  3. Build Image     ──→  Docker Image (myapp:latest) │  │
│  │  4. Scan Image      ──→  Trivy Scanner               │  │
│  │  5. Generate Reports                                  │  │
│  │  6. Upload Results                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬──────────────────────┬─────────────────────────┘
             │                      │
             ↓                      ↓
┌────────────────────┐   ┌──────────────────────────┐
│  GitHub Security   │   │  Workflow Artifacts      │
│      Tab           │   │  (JSON Reports)          │
│  - SARIF Reports   │   │  - Scan Results          │
│  - CVE Details     │   │  - Retention: 30 days    │
│  - Trend Analysis  │   └──────────────────────────┘
└────────────────────┘

Optional: Notifications
     ↓
┌────────────────────┐
│  Slack/Email       │
│  Alerts on         │
│  Vulnerabilities   │
└────────────────────┘
```

## 🧩 Component Details

### 1. Source Code Repository (GitHub)

**Purpose**: Central version control and workflow orchestration

**Components**:
- Application source code (`app/app.py`)
- Dockerfile for containerization
- GitHub Actions workflow (`.github/workflows/container-scan.yml`)
- Documentation files

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` branch
- Manual workflow dispatch

**Technology**: Git, GitHub

---

### 2. CI/CD Pipeline (GitHub Actions)

**Purpose**: Automate build, test, and security scanning

**Runner Environment**:
- OS: Ubuntu Latest (Linux)
- Pre-installed: Docker, Git, Node.js
- Ephemeral: Created per workflow run

**Workflow Jobs**:
```yaml
jobs:
  build-and-scan:
    runs-on: ubuntu-latest
    steps: [8 steps total]
```

**Permissions Required**:
- `contents: read` - Read repository files
- `security-events: write` - Upload to Security tab
- `actions: read` - Access workflow artifacts

---

### 3. Docker Build System

**Purpose**: Create containerized application artifact

**Build Process**:
```bash
docker build -t myapp:${{ github.sha }} ./app
```

**Image Layers**:
1. Base Image: `python:3.9-slim`
2. Dependency Layer: Python packages
3. Application Layer: Flask app code
4. Security Layer: Non-root user configuration

**Image Tags**:
- `myapp:latest` - Latest build
- `myapp:${COMMIT_SHA}` - Commit-specific tag

**Best Practices Applied**:
- Minimal base image (slim variant)
- Multi-stage potential (can be enhanced)
- Layer caching optimization
- Non-root user execution

---

### 4. Trivy Vulnerability Scanner

**Purpose**: Detect security vulnerabilities in container images

**Technology**: Aqua Security Trivy (Open Source)

**Scan Types**:
1. **Image Scan**: Analyzes Docker images
2. **Filesystem Scan**: Scans project files
3. **Repository Scan**: Scans Git repositories

**Vulnerability Databases**:
- CVE (Common Vulnerabilities and Exposures)
- NVD (National Vulnerability Database)
- Vendor-specific advisories
- GitHub Security Advisories

**Detection Capabilities**:
- OS package vulnerabilities
- Application dependency vulnerabilities
- Misconfigurations
- Exposed secrets (if configured)

**Scan Modes in Pipeline**:

#### Mode 1: Comprehensive Scan
```yaml
severity: 'UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL'
exit-code: '0'  # Never fail
format: 'table'
```
- **Purpose**: Full visibility
- **Output**: Console table
- **Action**: Informational only

#### Mode 2: Enforcement Scan
```yaml
severity: 'CRITICAL,HIGH'
exit-code: '1'  # Fail on findings
format: 'sarif'
```
- **Purpose**: Security gate
- **Output**: SARIF for GitHub
- **Action**: Fail build if issues found

#### Mode 3: Report Generation
```yaml
format: 'json'
output: 'trivy-report.json'
```
- **Purpose**: Detailed reporting
- **Output**: JSON artifact
- **Action**: Archive for analysis

---

### 5. Report Generation System

**Purpose**: Create actionable security reports

**Report Formats**:

#### SARIF (Static Analysis Results Interchange Format)
- **Purpose**: GitHub Security tab integration
- **Benefits**: 
  - Native GitHub integration
  - Visual vulnerability tracking
  - Historical trend analysis
- **Location**: GitHub Security → Code scanning

#### JSON (JavaScript Object Notation)
- **Purpose**: Machine-readable detailed report
- **Benefits**:
  - Parseable by other tools
  - Custom analysis and dashboards
  - Integration with SIEM systems
- **Location**: Workflow artifacts (30-day retention)

#### Table (Console Output)
- **Purpose**: Human-readable quick view
- **Benefits**:
  - Immediate feedback in logs
  - Easy troubleshooting
- **Location**: GitHub Actions logs

---

### 6. GitHub Security Integration

**Purpose**: Centralized security dashboard

**Features**:
- **Code Scanning Alerts**: All detected vulnerabilities
- **Severity Filtering**: Filter by CRITICAL, HIGH, etc.
- **CVE Details**: Links to CVE databases
- **Fix Suggestions**: Recommended versions
- **Trend Analysis**: Track security posture over time
- **Branch Comparison**: Compare vulnerability counts

**Access**: Repository → Security tab → Code scanning alerts

---

## 🔄 Data Flow Diagram

### Build and Scan Process

```
┌─────────────┐
│   Trigger   │ (Push/PR)
└──────┬──────┘
       │
       ↓
┌─────────────────────┐
│  Checkout Code      │
│  actions/checkout   │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│  Build Docker Image │
│  docker build       │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│  Trivy Scan #1      │
│  (All Severities)   │
│  Format: Table      │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│  Trivy Scan #2      │
│  (CRITICAL/HIGH)    │
│  Format: SARIF      │
└──────┬──────────────┘
       │
       ├──→ Vulnerabilities Found? ──→ EXIT CODE 1 (Fail Build)
       │
       ↓
┌─────────────────────┐
│  Upload SARIF       │
│  → Security Tab     │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│  Generate JSON      │
│  Trivy Scan #3      │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│  Upload Artifact    │
│  → Workflow Storage │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│  Pipeline Complete  │
│  (Success/Failure)  │
└─────────────────────┘
```

---

## 🔐 Security Architecture

### Security Layers

#### Layer 1: Source Code Security
- **Control**: Code review process
- **Tools**: Git, Branch protection
- **Threat**: Malicious code injection

#### Layer 2: Build Security
- **Control**: Isolated build environment
- **Tools**: GitHub Actions runners
- **Threat**: Build tampering

#### Layer 3: Image Security
- **Control**: Vulnerability scanning
- **Tools**: Trivy scanner
- **Threat**: Vulnerable dependencies

#### Layer 4: Deployment Gate
- **Control**: Security gate (exit-code: 1)
- **Tools**: Pipeline automation
- **Threat**: Deploying vulnerable images

#### Layer 5: Runtime Security (Future)
- **Control**: Runtime monitoring
- **Tools**: Falco, Sysdig (not implemented)
- **Threat**: Runtime exploits

### Security Principles Applied

1. **Shift Left**: Security early in SDLC
2. **Automation**: No manual security checks
3. **Defense in Depth**: Multiple security layers
4. **Least Privilege**: Non-root container user
5. **Fail Secure**: Pipeline fails on critical issues

---

## ⚙️ Technical Specifications

### Supported Platforms
- **Git Hosting**: GitHub
- **CI/CD**: GitHub Actions
- **Container Runtime**: Docker
- **Scanner**: Trivy 0.28.0+

### Resource Requirements

#### GitHub Actions Runner:
- **CPU**: 2 cores
- **RAM**: 7 GB
- **Storage**: 14 GB SSD
- **Network**: Required for image pull/scan

#### Build Time Estimates:
- **Checkout**: ~5 seconds
- **Docker Build**: ~30-60 seconds
- **Trivy Scan**: ~20-40 seconds
- **Report Upload**: ~10 seconds
- **Total**: ~1-2 minutes per run

### Network Requirements:
- GitHub.com access
- Docker Hub access (for base images)
- Trivy vulnerability database access

---

## 🔧 Configuration Options

### Workflow Customization

#### Change Trigger Events:
```yaml
on:
  push:
    branches: [ main, staging, production ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly Sunday scan
```

#### Adjust Scan Severity:
```yaml
severity: 'CRITICAL'              # Most strict
severity: 'CRITICAL,HIGH'         # Default
severity: 'CRITICAL,HIGH,MEDIUM'  # More strict
```

#### Configure Timeouts:
```yaml
timeout-minutes: 10  # Prevent hanging
```

#### Enable/Disable Scans:
```yaml
if: github.event_name != 'pull_request'  # Skip on PRs
```

---

## 📊 Monitoring and Observability

### Metrics Tracked:
- Pipeline execution time
- Vulnerability counts by severity
- Build success/failure rate
- Time to remediate vulnerabilities

### Logs Available:
- GitHub Actions execution logs
- Trivy scan output
- Docker build logs

### Reports Generated:
- SARIF reports (Security tab)
- JSON reports (Artifacts)
- Console output (Logs)

---

## 🚀 Scalability Considerations

### Horizontal Scaling:
- **Multiple Repositories**: Same workflow reusable
- **Multiple Services**: Separate workflows per service
- **Matrix Builds**: Scan multiple images in parallel

### Vertical Scaling:
- **Self-Hosted Runners**: More resources if needed
- **Caching**: Docker layer caching for speed
- **Parallelization**: Run scans concurrently

### Future Enhancements:
- Container registry integration
- Kubernetes manifest scanning
- Runtime security monitoring
- Secrets detection
- SAST/DAST integration

---

## 🔗 Integration Points

### Current Integrations:
- ✅ GitHub Actions
- ✅ Docker
- ✅ Trivy
- ✅ GitHub Security Tab

### Potential Future Integrations:
- 🔜 Slack notifications
- 🔜 Email alerts
- 🔜 JIRA ticket creation
- 🔜 Docker Hub / ECR / ACR
- 🔜 Kubernetes clusters
- 🔜 Prometheus metrics
- 🔜 Grafana dashboards

---

## 📚 Technical References

- **GitHub Actions**: [docs.github.com/actions](https://docs.github.com/actions)
- **Trivy**: [aquasecurity.github.io/trivy](https://aquasecurity.github.io/trivy)
- **SARIF**: [sarifweb.azurewebsites.net](https://sarifweb.azurewebsites.net)
- **CVE**: [cve.mitre.org](https://cve.mitre.org)
- **Docker**: [docs.docker.com](https://docs.docker.com)

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**Maintained By**: DevSecOps Team
