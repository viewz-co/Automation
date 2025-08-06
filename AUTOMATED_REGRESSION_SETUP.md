# 🤖 Automated Regression Testing Setup

This guide explains how to set up automated regression testing that runs on every developer push.

## 🎯 **Overview**

The automated regression testing system provides:
- **Smart Test Selection**: Different test suites based on branch type
- **Comprehensive Coverage**: Full regression tests for main/develop branches  
- **Fast Feedback**: Smoke tests for feature branches
- **Team Notifications**: Automatic alerts on failures
- **Detailed Reporting**: Test results, artifacts, and summaries

---

## 🔧 **Configuration**

### **1. GitHub Secrets Setup**

Add these secrets in your repository settings (`Settings > Secrets and variables > Actions`):

#### **Required Secrets:**
```bash
TEST_USERNAME=your_test_username
TEST_PASSWORD=your_test_password  
TEST_TOTP_SECRET=your_2fa_secret_key
TESTRAIL_URL=https://your-instance.testrail.io
TESTRAIL_USERNAME=your_testrail_email
TESTRAIL_PASSWORD=your_testrail_password
TESTRAIL_PROJECT_ID=1
```

#### **Optional Secrets (for team notifications):**
```bash
TEAM_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
# OR
TEAM_WEBHOOK_URL=https://your-company.webhook.office.com/YOUR/TEAMS/WEBHOOK
```

### **2. Branch Protection Rules**

Set up branch protection in `Settings > Branches` for `main` and `develop`:

✅ **Require status checks to pass before merging**
✅ **Require branches to be up to date before merging**  
✅ **Required status checks:**
   - `Playwright Regression Tests / test (Authentication & Login)`
   - `Playwright Regression Tests / test (Critical Path)`
   - `Playwright Regression Tests / test (Navigation & Menu)`

---

## 🚀 **How It Works**

### **Automatic Trigger Rules**

| **Branch Type** | **Test Suite** | **Triggered On** | **Tests Run** |
|-----------------|----------------|------------------|---------------|
| `main` | Full Regression | Every push | All test categories |
| `develop` | Full Regression | Every push | All test categories |
| `feature/*` | Smoke Tests | Every push | Critical path only |
| `bugfix/*` | Smoke Tests | Every push | Critical path only |
| `hotfix/*` | Critical Path | Every push | Essential tests only |

### **Test Categories**

#### **🚀 Smoke Tests** (Feature branches)
- Authentication & Login
- Critical navigation paths
- ⏱️ **Duration**: ~5-10 minutes

#### **🔍 Full Regression** (Main/Develop branches)  
- Authentication & Login
- Navigation & Menu
- File Upload & Payables
- Reconciliation Operations
- Ledger & Financial
- API Integration
- Security & Compatibility
- Performance & Load
- Snapshot & Regression
- ⏱️ **Duration**: ~30-45 minutes

#### **⚡ Critical Path** (Hotfix branches)
- Essential login functionality
- Core file upload
- ⏱️ **Duration**: ~3-5 minutes

---

## 📊 **Developer Workflow**

### **1. Feature Development**
```bash
# Create feature branch
git checkout -b feature/new-functionality

# Make your changes
git add .
git commit -m "Add new functionality"
git push origin feature/new-functionality
```

**Result**: 🔄 Smoke tests run automatically (5-10 min)

### **2. Pull Request**
```bash
# Create PR to main/develop
gh pr create --title "Add new functionality" --body "Description"
```

**Result**: 
- 🔄 Full regression tests run automatically
- 🤖 Automated comment posted with results
- ✅ Branch protection prevents merge if tests fail

### **3. Main Branch Push**
```bash
# Merge to main
git checkout main
git merge feature/new-functionality
git push origin main
```

**Result**: 
- 🔄 Complete regression suite runs
- 📢 Team notifications on failure
- 📋 Automatic issue creation for repeated failures

---

## 🎛️ **Manual Controls**

### **Run Specific Test Suite**
Go to `Actions > Playwright Regression Tests > Run workflow`:

- **Test Suite**: Choose from dropdown
  - `full-regression`: Complete test suite
  - `smoke-tests`: Fast critical path
  - `critical-path`: Essential tests only
  - Individual categories (login, navigation, etc.)

- **Environment**: Choose target environment
  - `production`: https://app.viewz.co
  - `staging`: https://staging.viewz.co  
  - `development`: https://dev.viewz.co

- **Notify Teams**: Enable/disable team notifications

### **Emergency Override**
```bash
# Skip CI checks (use sparingly!)
git push origin main --push-option=ci.skip
```

---

## 📈 **Monitoring & Notifications**

### **GitHub Interface**
- ✅ **Pull Request Comments**: Automated test results
- 📊 **Workflow Summaries**: Detailed test reports
- 🔍 **Artifacts**: Screenshots, logs, and reports

### **Team Notifications**
- 🚨 **Slack/Teams**: Failure alerts for main/develop
- 📋 **Auto Issues**: Created for repeated failures
- 📧 **Email**: GitHub's built-in notifications

### **TestRail Integration**
- 📊 **Automatic Updates**: Test results synced to TestRail
- 🎯 **Run Tracking**: Each CI run creates TestRail run
- 📈 **Reporting**: Historical test trends

---

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **Tests Not Running**
1. Check GitHub Secrets are configured
2. Verify branch naming follows convention
3. Check workflow file syntax

#### **Authentication Failures**
```bash
# Update credentials in GitHub Secrets
TEST_USERNAME=new_username
TEST_PASSWORD=new_password
TEST_TOTP_SECRET=new_secret
```

#### **Environment Issues**
```bash
# Check centralized config
python scripts/validate_environment_config.py

# Test specific environment  
ENVIRONMENT=staging python scripts/validate_environment_config.py
```

#### **Webhook Notifications Not Working**
1. Verify `TEAM_WEBHOOK_URL` secret is set
2. Test webhook URL manually
3. Check webhook format (Slack vs Teams)

### **Debug Mode**
```bash
# Run tests locally with same configuration
docker-compose up playwright-test

# Validate environment configuration
python scripts/validate_environment_config.py

# Test specific component
python -m pytest tests/e2e/login/ -v --headless
```

---

## 🔧 **Customization**

### **Add New Test Category**
1. Update `.github/workflows/playwright-tests.yml`
2. Add new matrix entry:
```yaml
- name: "Your New Category"
  path: "tests/your-category/"
  container: "your-category-tests"
  condition: "full-regression"
```

### **Modify Test Selection Logic**
Edit the "Determine test suite" step in the workflow:
```bash
elif [[ "${{ github.ref }}" == refs/heads/your-branch/* ]]; then
  TEST_SUITE="your-custom-suite"
```

### **Custom Notifications**
Update the notification job with your team's specific needs:
- Custom webhook formats
- Additional notification channels  
- Specific failure thresholds

---

## 📚 **Best Practices**

### **For Developers**
1. **Run tests locally** before pushing
2. **Keep feature branches small** for faster feedback
3. **Fix failing tests promptly** to avoid blocking others
4. **Use descriptive commit messages** for better tracking

### **For Team Leads**
1. **Monitor test trends** in TestRail dashboard
2. **Review failure patterns** weekly
3. **Update test priorities** based on business needs
4. **Ensure team has proper credentials** configured

### **For DevOps**
1. **Monitor CI/CD costs** and optimize where needed
2. **Keep secrets updated** and rotated regularly
3. **Review workflow performance** monthly
4. **Update dependencies** in Docker images

---

## 📞 **Support**

### **Quick Links**
- 🔗 **GitHub Actions**: [View Workflows](../../actions)
- 📊 **TestRail**: [Test Dashboard](https://your-instance.testrail.io)  
- 📚 **Framework Docs**: [README.md](./README.md)
- 🛠️ **Environment Config**: [configs/environment.py](./configs/environment.py)

### **Getting Help**
1. Check the [troubleshooting section](#troubleshooting)
2. Review workflow logs in GitHub Actions
3. Contact the QA/DevOps team
4. Create issue with `regression-testing` label

---

## ✅ **Success Metrics**

With this setup, you should see:
- **🚀 Faster feedback**: Sub-10 minute smoke tests
- **🛡️ Better quality**: Automated regression coverage
- **📈 Improved confidence**: Comprehensive test reporting
- **🤝 Team collaboration**: Clear failure notifications
- **📊 Data-driven decisions**: TestRail integration and metrics

This automated regression testing system ensures **every developer push is validated** while providing **fast feedback** and **comprehensive coverage**! 🎉 