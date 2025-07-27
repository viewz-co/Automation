// Playwright configuration for snapshot testing
module.exports = {
  testDir: './tests',
  timeout: 30000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  
  use: {
    // Global test settings
    actionTimeout: 0,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    
    // Snapshot testing settings
    baseURL: process.env.BASE_URL || 'https://new.viewz.co',
    
    // Browser settings for consistent snapshots
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    
    // Screenshot settings for visual testing
    screenshotMode: 'only-on-failure',
    
    // Snapshot comparison settings
    expect: {
      // Global threshold for screenshot comparison
      threshold: 0.1,
      // Animation handling
      toHaveScreenshot: {
        threshold: 0.1,
        animations: 'disabled'
      },
      toMatchSnapshot: {
        threshold: 0.1
      }
    }
  },

  projects: [
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        // Disable animations for consistent snapshots
        reducedMotion: 'reduce',
        // Force specific color scheme for consistent snapshots
        colorScheme: 'light'
      },
    },
    
    // Optional: Add other browsers for cross-browser snapshot testing
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },

    // Mobile viewports for responsive snapshot testing
    {
      name: 'Mobile Chrome',
      use: { 
        ...devices['Pixel 5'],
        reducedMotion: 'reduce',
        colorScheme: 'light'
      },
    },
    {
      name: 'Mobile Safari',
      use: { 
        ...devices['iPhone 12'],
        reducedMotion: 'reduce',
        colorScheme: 'light'
      },
    },
  ],

  // Snapshot settings
  expect: {
    // Screenshot comparison settings
    toHaveScreenshot: {
      // Default threshold for all screenshots
      threshold: 0.1,
      // Handle animations
      animations: 'disabled',
      // Clip dynamic areas if needed
      // clip: { x: 0, y: 0, width: 1280, height: 600 }
    }
  },

  // Web server for local testing
  webServer: {
    command: 'npm start',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
}; 