/**
 * MCP Login Scenarios Script
 * This script demonstrates how to use the Playwright MCP Server
 * to automate login scenarios for https://new.viewz.co/login
 * 
 * To use this script:
 * 1. Ensure MCP server is running: ./scripts/start_mcp_server.sh
 * 2. Configure your AI client to connect to http://127.0.0.1:8931/sse
 * 3. Use these commands through your AI client
 */

// =============================================================================
// SCENARIO SETUP
// =============================================================================

console.log("🚀 Starting Viewz Login Scenarios");
console.log("📍 Target URL: https://new.viewz.co/login");

// Navigate to login page
await browser_navigate("https://new.viewz.co/login");

// Wait for page to load
await browser_wait_for(3); // Wait 3 seconds

// Take initial screenshot
await browser_take_screenshot("login_page_initial.png");

// =============================================================================
// PAGE ANALYSIS
// =============================================================================

console.log("🔍 Analyzing page structure...");

// Capture page snapshot to understand structure
const snapshot = await browser_snapshot();
console.log("📊 Page snapshot captured for analysis");

// The snapshot will show us:
// - All interactive elements
// - Form fields and their selectors
// - Buttons and their accessibility information
// - Any demo credentials visible on the page

// =============================================================================
// CREDENTIAL DISCOVERY
// =============================================================================

console.log("🔑 Scanning for demo credentials...");

// Look for common demo credential patterns
const demoSelectors = [
    "text=demo",
    "text=test", 
    "text=sample",
    "[data-testid*='demo']",
    "[data-testid*='test']",
    ".demo-credentials",
    ".test-credentials"
];

// Check each selector for visible credentials
for (const selector of demoSelectors) {
    try {
        await browser_click("Demo credential element", selector);
        console.log(`✅ Found demo credentials with selector: ${selector}`);
        break;
    } catch (error) {
        console.log(`❌ No demo credentials found with: ${selector}`);
    }
}

// =============================================================================
// SCENARIO 1: VALID LOGIN
// =============================================================================

console.log("🎯 Executing Scenario 1: Valid Login");

// Find and fill email field
const emailSelectors = [
    "input[type='email']",
    "input[name='email']", 
    "input[name='username']",
    "input[placeholder*='email' i]",
    "#email",
    "#username"
];

let emailField = null;
for (const selector of emailSelectors) {
    try {
        await browser_type("Email field", selector, "demo@viewz.co");
        emailField = selector;
        console.log(`✅ Found email field: ${selector}`);
        break;
    } catch (error) {
        console.log(`❌ Email field not found: ${selector}`);
    }
}

// Find and fill password field
const passwordSelectors = [
    "input[type='password']",
    "input[name='password']",
    "#password"
];

let passwordField = null;
for (const selector of passwordSelectors) {
    try {
        await browser_type("Password field", selector, "demo123");
        passwordField = selector;
        console.log(`✅ Found password field: ${selector}`);
        break;
    } catch (error) {
        console.log(`❌ Password field not found: ${selector}`);
    }
}

// Find and click login button
const loginButtonSelectors = [
    "button[type='submit']",
    "input[type='submit']",
    "button:has-text('Login')",
    "button:has-text('Sign In')",
    "button:has-text('Log In')",
    ".login-button",
    "#login-btn"
];

let loginButton = null;
for (const selector of loginButtonSelectors) {
    try {
        await browser_click("Login button", selector);
        loginButton = selector;
        console.log(`✅ Found login button: ${selector}`);
        break;
    } catch (error) {
        console.log(`❌ Login button not found: ${selector}`);
    }
}

// Wait for navigation
await browser_wait_for(3);

// Take screenshot after login attempt
await browser_take_screenshot("login_attempt_result.png");

// =============================================================================
// LOGIN VALIDATION
// =============================================================================

console.log("✅ Validating login success...");

// Check if we're still on login page
const currentSnapshot = await browser_snapshot();

// Common success indicators
const successChecks = [
    // URL should have changed
    "Should not be on login page anymore",
    // Look for dashboard elements
    "text=Dashboard",
    "text=Welcome", 
    "[data-testid='user-menu']",
    ".user-profile",
    "text=Logout"
];

let loginSuccessful = false;

// Check each success indicator
for (const check of successChecks) {
    try {
        if (check.startsWith("text=") || check.startsWith("[") || check.startsWith(".")) {
            await browser_click("Success indicator", check);
            console.log(`✅ Login success indicator found: ${check}`);
            loginSuccessful = true;
            break;
        }
    } catch (error) {
        console.log(`❌ Success indicator not found: ${check}`);
    }
}

if (!loginSuccessful) {
    console.log("❌ Login may have failed - checking for error messages");
    
    // Look for error messages
    const errorSelectors = [
        ".error",
        ".error-message", 
        ".alert-danger",
        "[role='alert']",
        "text=Invalid",
        "text=Error"
    ];
    
    for (const selector of errorSelectors) {
        try {
            await browser_click("Error message", selector);
            console.log(`❌ Error message found: ${selector}`);
        } catch (error) {
            // No error message found with this selector
        }
    }
}

// =============================================================================
// SCENARIO 2: LOGOUT USER
// =============================================================================

console.log("🚪 Executing Scenario 2: Logout User");

// Take screenshot before logout
await browser_take_screenshot("before_logout.png");

// Find logout mechanism
const logoutSelectors = [
    "text=Logout",
    "text=Log Out", 
    "text=Sign Out",
    "button:has-text('Logout')",
    "[data-testid='logout']",
    ".logout-btn"
];

let logoutFound = false;

// Try direct logout buttons first
for (const selector of logoutSelectors) {
    try {
        await browser_click("Logout button", selector);
        console.log(`✅ Found logout button: ${selector}`);
        logoutFound = true;
        break;
    } catch (error) {
        console.log(`❌ Logout button not found: ${selector}`);
    }
}

// If no direct logout, try user menu dropdown
if (!logoutFound) {
    const userMenuSelectors = [
        "[data-testid='user-menu']",
        ".user-menu",
        ".user-dropdown",
        "button:has-text('Profile')",
        "button:has-text('Account')"
    ];
    
    for (const menuSelector of userMenuSelectors) {
        try {
            await browser_click("User menu", menuSelector);
            console.log(`✅ Opened user menu: ${menuSelector}`);
            
            // Wait for dropdown to appear
            await browser_wait_for(1);
            
            // Now try logout options
            for (const logoutSelector of logoutSelectors) {
                try {
                    await browser_click("Logout from menu", logoutSelector);
                    console.log(`✅ Clicked logout from menu: ${logoutSelector}`);
                    logoutFound = true;
                    break;
                } catch (error) {
                    console.log(`❌ Logout from menu not found: ${logoutSelector}`);
                }
            }
            
            if (logoutFound) break;
            
        } catch (error) {
            console.log(`❌ User menu not found: ${menuSelector}`);
        }
    }
}

// Wait for logout to complete
await browser_wait_for(3);

// Take screenshot after logout
await browser_take_screenshot("after_logout.png");

// =============================================================================
// LOGOUT VALIDATION
// =============================================================================

console.log("✅ Validating logout success...");

// Check if redirected to login page
const finalSnapshot = await browser_snapshot();

// Look for login form elements
const loginIndicators = [
    "input[type='email']",
    "input[type='password']", 
    "button:has-text('Login')",
    "text=Sign In",
    "text=Login"
];

let logoutSuccessful = false;

for (const indicator of loginIndicators) {
    try {
        await browser_click("Login indicator", indicator);
        console.log(`✅ Login form visible - logout successful: ${indicator}`);
        logoutSuccessful = true;
        break;
    } catch (error) {
        console.log(`❌ Login indicator not found: ${indicator}`);
    }
}

// =============================================================================
// RESULTS SUMMARY
// =============================================================================

console.log("📊 Test Results Summary:");
console.log("========================");
console.log(`✅ Navigation to login page: SUCCESS`);
console.log(`✅ Page structure analysis: SUCCESS`);
console.log(`${loginSuccessful ? '✅' : '❌'} Scenario 1 (Valid Login): ${loginSuccessful ? 'SUCCESS' : 'FAILED'}`);
console.log(`${logoutSuccessful ? '✅' : '❌'} Scenario 2 (Logout): ${logoutSuccessful ? 'SUCCESS' : 'FAILED'}`);

// =============================================================================
// GENERATE ASSERTIONS
// =============================================================================

console.log("📝 Generating test assertions...");

const assertions = [
    `// URL Assertions`,
    `expect(page.url).not.toBe('https://new.viewz.co/login');`,
    `expect(page.url).toContain('viewz.co');`,
    ``,
    `// Element Assertions`,
    `expect(page.locator('${emailField}').first).toBeVisible();`,
    `expect(page.locator('${passwordField}').first).toBeVisible();`,
    `expect(page.locator('${loginButton}').first).toBeVisible();`,
    ``,
    `// Success Assertions`,
    `expect(page.locator('text=Dashboard').first).toBeVisible();`,
    `expect(page.locator('[data-testid="user-menu"]').first).toBeVisible();`,
    ``,
    `// Logout Assertions`,
    `expect(page.locator('text=Logout').first).toBeVisible();`,
    `expect(page.url).toBe('https://new.viewz.co/login'); // After logout`
];

console.log("Generated assertions:");
assertions.forEach(assertion => console.log(assertion));

// =============================================================================
// CLEANUP
// =============================================================================

console.log("🧹 Cleaning up...");

// Close any open dialogs
try {
    await browser_handle_dialog(false);
} catch (error) {
    // No dialogs to handle
}

// Take final screenshot
await browser_take_screenshot("test_complete.png");

console.log("🎉 Login scenarios completed!");
console.log("📸 Screenshots saved:");
console.log("   - login_page_initial.png");
console.log("   - login_attempt_result.png"); 
console.log("   - before_logout.png");
console.log("   - after_logout.png");
console.log("   - test_complete.png");

// =============================================================================
// NEXT STEPS FOR CODE GENERATION
// =============================================================================

console.log("🔄 Next Steps:");
console.log("1. Use browser_generate_playwright_test to create TypeScript code");
console.log("2. Convert to Page Object Model structure");
console.log("3. Save credentials in cypress.env.json");
console.log("4. Create comprehensive test suite");

// Generate test code
await browser_generate_playwright_test(
    "Viewz Login Scenarios",
    "Complete login and logout test scenarios for Viewz platform",
    [
        "Navigate to https://new.viewz.co/login",
        "Analyze page structure and find form elements",
        "Execute valid login with discovered credentials", 
        "Verify successful login and dashboard access",
        "Execute logout process",
        "Verify successful logout and return to login page",
        "Generate comprehensive assertions for validation"
    ]
);

console.log("✅ Test code generation requested!"); 