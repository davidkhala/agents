/**
 * Testing utilities for Moltbook authentication
 * Use these to test and debug your implementation
 */

const http = require('http');
const https = require('https');

/**
 * Test if Moltbook API endpoint is reachable
 */
async function testMoltbookConnectivity() {
  console.log('Testing Moltbook API connectivity...');
  
  try {
    const response = await fetch('https://moltbook.com/api/v1/agents/verify-identity', {
      method: 'OPTIONS',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    console.log('✓ Moltbook API is reachable');
    return true;
  } catch (error) {
    console.error('✗ Cannot reach Moltbook API:', error.message);
    return false;
  }
}

/**
 * Test if environment variables are properly configured
 */
function testEnvironmentConfig() {
  console.log('\nTesting environment configuration...');
  
  const appKey = process.env.MOLTBOOK_APP_KEY;
  const audience = process.env.MOLTBOOK_AUDIENCE;
  
  if (!appKey) {
    console.error('✗ MOLTBOOK_APP_KEY not set');
    return false;
  }
  
  if (!appKey.startsWith('moltdev_')) {
    console.warn('⚠ MOLTBOOK_APP_KEY does not start with "moltdev_"');
  } else {
    console.log('✓ MOLTBOOK_APP_KEY is configured');
  }
  
  if (!audience) {
    console.warn('⚠ MOLTBOOK_AUDIENCE not set (optional)');
  } else {
    console.log('✓ MOLTBOOK_AUDIENCE is configured:', audience);
  }
  
  return true;
}

/**
 * Test middleware with a mock request/response
 */
async function testMiddlewareWithMockToken(mockToken) {
  console.log('\nTesting middleware with mock token...');
  
  const { verifyMoltbookIdentity } = require('./middleware/moltbook-auth');
  
  // Create mock objects
  const req = {
    headers: {
      'x-moltbook-identity': mockToken
    }
  };
  
  const res = {
    status: function(code) {
      this.statusCode = code;
      return this;
    },
    json: function(data) {
      this.jsonData = data;
      return this;
    }
  };
  
  let nextCalled = false;
  const next = () => { nextCalled = true; };
  
  // Call middleware
  await verifyMoltbookIdentity(req, res, next);
  
  if (nextCalled) {
    console.log('✓ Middleware succeeded');
    if (req.moltbookAgent) {
      console.log('  Agent:', {
        name: req.moltbookAgent.name,
        karma: req.moltbookAgent.karma,
        owner: req.moltbookAgent.owner.x_handle
      });
    }
    return true;
  } else {
    console.error('✗ Middleware failed');
    if (res.jsonData) {
      console.error('  Error:', res.jsonData.error);
      console.error('  Hint:', res.jsonData.hint);
    }
    return false;
  }
}

/**
 * Test missing identity token
 */
async function testMissingToken() {
  console.log('\nTesting missing identity token...');
  
  const { verifyMoltbookIdentity } = require('./middleware/moltbook-auth');
  
  const req = { headers: {} };
  const res = {
    status: function(code) {
      this.statusCode = code;
      return this;
    },
    json: function(data) {
      this.jsonData = data;
      return this;
    }
  };
  const next = () => {};
  
  await verifyMoltbookIdentity(req, res, next);
  
  if (res.statusCode === 401) {
    console.log('✓ Correctly returns 401 for missing token');
    console.log('  Error:', res.jsonData.error);
    return true;
  } else {
    console.error('✗ Did not return 401 for missing token');
    return false;
  }
}

/**
 * Test invalid API key
 */
async function testInvalidApiKey() {
  console.log('\nTesting invalid API key...');
  
  const originalKey = process.env.MOLTBOOK_APP_KEY;
  
  // Temporarily set invalid key
  process.env.MOLTBOOK_APP_KEY = 'invalid_key';
  
  const { verifyIdentityToken } = require('./middleware/moltbook-auth');
  
  try {
    const result = await verifyIdentityToken('mock_token');
    
    if (!result.valid || result.error === 'invalid_app_key') {
      console.log('✓ Correctly handles invalid API key');
      return true;
    }
  } catch (error) {
    console.log('⚠ Error testing invalid key:', error.message);
  }
  
  // Restore original key
  process.env.MOLTBOOK_APP_KEY = originalKey;
  
  return false;
}

/**
 * Full diagnostic test
 */
async function runFullDiagnostics() {
  console.log('='.repeat(50));
  console.log('Moltbook Authentication Diagnostics');
  console.log('='.repeat(50));
  
  const results = {
    connectivity: await testMoltbookConnectivity(),
    config: testEnvironmentConfig(),
    missingToken: await testMissingToken()
  };
  
  console.log('\n' + '='.repeat(50));
  console.log('Diagnostic Results');
  console.log('='.repeat(50));
  
  Object.entries(results).forEach(([test, passed]) => {
    const icon = passed ? '✓' : '✗';
    console.log(`${icon} ${test}`);
  });
  
  const allPassed = Object.values(results).every(r => r);
  
  if (allPassed) {
    console.log('\n✓ All diagnostics passed!');
  } else {
    console.log('\n✗ Some diagnostics failed. Check the output above.');
  }
  
  return allPassed;
}

/**
 * Create a test Express app for manual testing
 */
function createTestApp() {
  const express = require('express');
  const { verifyMoltbookIdentity } = require('./middleware/moltbook-auth');
  
  const app = express();
  app.use(express.json());
  
  // Health check (no auth required)
  app.get('/health', (req, res) => {
    res.json({ status: 'ok' });
  });
  
  // Protected endpoint
  app.post('/api/test-action', verifyMoltbookIdentity, (req, res) => {
    const agent = req.moltbookAgent;
    
    res.json({
      success: true,
      message: 'Authentication successful',
      agent: {
        name: agent.name,
        karma: agent.karma,
        id: agent.id,
        owner: {
          handle: agent.owner.x_handle,
          verified: agent.owner.x_verified
        }
      }
    });
  });
  
  return app;
}

module.exports = {
  testMoltbookConnectivity,
  testEnvironmentConfig,
  testMiddlewareWithMockToken,
  testMissingToken,
  testInvalidApiKey,
  runFullDiagnostics,
  createTestApp
};
