# 🐳 Containerized Playwright Framework Setup

This guide will help you set up the Playwright testing framework to run in containers and automatically execute on every developer push.

## 🚀 Quick Start

### 1. **Initial Setup**
```bash
# Clone the repository
git clone <your-repo-url>
cd playwright_python_framework

# Run the setup script
./scripts/docker-setup.sh
```

### 2. **Configure Environment**
Edit the `.env` file with your credentials:
```env
TEST_USERNAME=your_username
TEST_PASSWORD=your_password
TEST_TOTP_SECRET=your_totp_secret
TESTRAIL_URL=https://your-instance.testrail.io
TESTRAIL_USERNAME=your_testrail_username
TESTRAIL_PASSWORD=your_testrail_password
TESTRAIL_PROJECT_ID=1
```

### 3. **Run Tests**
```bash
# Development mode (with live code mounting)
docker-compose up playwright-dev

# Production mode
docker-compose up playwright-test

# Specific test suites
docker-compose up upload-tests
docker-compose up parallel-tests
```

## 🏗️ Architecture

### **Docker Images**
- **Base Image**: `python:3.12-slim` with Playwright dependencies
- **Production Stage**: Optimized for CI/CD
- **Development Stage**: Includes debugging tools

### **Components**
```
playwright_python_framework/
├── Dockerfile                     # Multi-stage container definition
├── docker-compose.yml             # Local development orchestration
├── .github/workflows/             # CI/CD automation
│   └── playwright-tests.yml       # GitHub Actions workflow
├── scripts/docker-setup.sh        # Setup automation
└── .dockerignore                  # Build optimization
```

## 🔄 CI/CD Pipeline

### **Triggers**
- ✅ **Every push** to `main`, `develop`, `feature/*`
- ✅ **Pull requests** to `main`, `develop`  
- ✅ **Daily scheduled** runs at 6 AM UTC
- ✅ **Manual dispatch** with test suite selection

### **Pipeline Stages**

#### 1. **Build Stage**
- Builds Docker image with Playwright dependencies
- Caches layers for faster subsequent builds
- Publishes to GitHub Container Registry

#### 2. **Test Stage (Parallel)**
- **Upload Tests**: Invoice file upload/delete functionality
- **Login Tests**: Authentication and 2FA
- **Navigation Tests**: UI navigation and tabs
- **Ledger Tests**: General ledger operations
- **API Tests**: Backend API validation

#### 3. **Full Suite** (Scheduled/Manual)
- Comprehensive test execution
- Performance testing
- Load testing with parallel execution

#### 4. **Artifacts**
- HTML test reports
- JSON test data
- Screenshots on failures
- Performance metrics

## 🔧 Local Development

### **Development Workflow**
```bash
# Start development environment
docker-compose up playwright-dev

# Run specific tests
docker-compose run --rm playwright-dev python -m pytest tests/e2e/payables/ -v

# Debug with screenshots
docker-compose run --rm playwright-dev python -m pytest tests/ -v --headed

# Performance testing
docker-compose up parallel-tests
```

### **File Mounting**
- Source code: Live mounted for development
- Reports: `./reports/` → Container `/app/reports/`
- Screenshots: `./screenshots/` → Container `/app/screenshots/`

## 🔐 GitHub Secrets Setup

### **Required Secrets**
Add these in GitHub Settings → Secrets and variables → Actions:

```env
TEST_USERNAME          # Application login username
TEST_PASSWORD          # Application login password  
TEST_TOTP_SECRET       # 2FA TOTP secret key
TESTRAIL_URL           # TestRail instance URL
TESTRAIL_USERNAME      # TestRail username
TESTRAIL_PASSWORD      # TestRail password/API key
TESTRAIL_PROJECT_ID    # TestRail project ID
```

### **Setting Up Secrets**
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret with exact names above

## 🎯 Test File Management

### **CI/CD Strategy**
- **Local Development**: Uses your real test files from `uploaded_test_files/`
- **CI/CD Environment**: Auto-generates fallback test content
- **Security**: Real files are `.gitignored` and never committed

### **Fallback System**
```python
# Automatic fallback content for CI/CD
fallback_hebrew_invoice.txt    # Hebrew invoice content
fallback_english_invoice.txt   # English invoice content
```

## 📊 Monitoring & Reports

### **GitHub Actions**
- ✅ Real-time test status in Pull Requests
- 📊 Downloadable HTML reports
- 📸 Failure screenshots
- 📈 Performance metrics

### **TestRail Integration**
- ✅ Automatic test case updates
- 📝 Run tracking with GitHub links
- 🏷️ Test case mapping

### **Notifications**
- ✅ Success/failure notifications
- 📧 Email alerts (configurable)
- 💬 Slack integration (optional)

## 🛠️ Troubleshooting

### **Common Issues**

#### Docker Build Fails
```bash
# Clear Docker cache
docker builder prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### Tests Fail in Container
```bash
# Run with debug output
docker-compose run --rm playwright-dev python -m pytest tests/ -v -s

# Check container logs
docker-compose logs playwright-dev
```

#### Missing Test Files
```bash
# Verify fallback system
docker-compose run --rm playwright-dev ls -la uploaded_test_files/

# Check environment detection
docker-compose run --rm playwright-dev python -c "import os; print(f'CI: {os.getenv(\"CI\")}')"
```

### **Performance Optimization**

#### Parallel Execution
```bash
# Run tests in parallel
docker-compose up parallel-tests

# Custom parallel configuration  
docker-compose run --rm playwright-dev python -m pytest tests/ -n 4
```

#### Resource Limits
```yaml
# In docker-compose.yml
services:
  playwright-test:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

## 🚀 Production Deployment

### **Scaling**
- Horizontal scaling with multiple containers
- Load balancing for parallel test execution
- Resource optimization for cost efficiency

### **Monitoring**
- Container health checks
- Performance metrics collection
- Alerting on test failures

### **Maintenance**
- Automated Docker image updates
- Regular cleanup of old artifacts
- Security scanning

## 🔄 Developer Workflow

### **Feature Development**
1. Create feature branch: `feature/new-test-suite`
2. Develop locally with: `docker-compose up playwright-dev`
3. Push to GitHub → Automatic CI/CD runs
4. Review results in Pull Request
5. Merge → Full test suite runs

### **Best Practices**
- ✅ Test locally before pushing
- ✅ Use descriptive commit messages
- ✅ Add test files to `uploaded_test_files/` for local testing
- ✅ Monitor CI/CD results
- ✅ Fix failing tests promptly

## 🆘 Support

### **Getting Help**
- Check GitHub Actions logs for detailed error messages
- Review Docker logs: `docker-compose logs`
- Verify environment variables: Check `.env` file
- Test fallback system: Ensure CI/CD fallback files work

### **Contributing**
- Follow existing patterns for new tests
- Update documentation for new features
- Test in both local and CI/CD environments
- Ensure backward compatibility

---

**🎉 Your framework is now production-ready with containerized CI/CD!** 