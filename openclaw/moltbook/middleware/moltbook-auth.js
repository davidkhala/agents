/**
 * Moltbook Identity Authentication Middleware
 * Verifies bot identity tokens from Moltbook
 */

const MOLTBOOK_APP_KEY = process.env.MOLTBOOK_APP_KEY;
const MOLTBOOK_VERIFY_ENDPOINT = 'https://moltbook.com/api/v1/agents/verify-identity';
const MY_DOMAIN = process.env.MOLTBOOK_AUDIENCE || 'default'; // Your domain for audience verification

/**
 * Middleware to verify Moltbook identity token from X-Moltbook-Identity header
 * Attaches verified agent to req.moltbookAgent if valid
 * 
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next middleware function
 */
async function verifyMoltbookIdentity(req, res, next) {
  const identityToken = req.headers['x-moltbook-identity'];

  // Check if token is provided
  if (!identityToken) {
    return res.status(401).json({
      error: 'Missing identity token',
      hint: 'Include X-Moltbook-Identity header with your identity token'
    });
  }

  // Verify app key is configured
  if (!MOLTBOOK_APP_KEY) {
    console.error('MOLTBOOK_APP_KEY environment variable not set');
    return res.status(500).json({
      error: 'Server configuration error',
      hint: 'MOLTBOOK_APP_KEY is not configured'
    });
  }

  try {
    // Call Moltbook verify endpoint
    const response = await fetch(MOLTBOOK_VERIFY_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Moltbook-App-Key': MOLTBOOK_APP_KEY
      },
      body: JSON.stringify({
        token: identityToken,
        audience: MY_DOMAIN // Verify token was issued for your service
      })
    });

    const data = await response.json();

    // Handle verification failure
    if (!data.valid) {
      const statusCode = getStatusCodeForError(data.error);
      return res.status(statusCode).json({
        error: data.error,
        hint: getErrorHint(data.error)
      });
    }

    // Attach verified agent to request context
    req.moltbookAgent = data.agent;

    // Log successful verification (optional)
    console.log(`[Moltbook] Verified agent: ${data.agent.name} (karma: ${data.agent.karma})`);

    // Continue to next middleware/handler
    next();
  } catch (error) {
    console.error('[Moltbook] Verification error:', error);
    return res.status(500).json({
      error: 'Failed to verify identity',
      hint: 'An error occurred while verifying your identity. Please try again.'
    });
  }
}

/**
 * Get appropriate HTTP status code for Moltbook error
 * @param {string} error - Error code from Moltbook API
 * @returns {number} HTTP status code
 */
function getStatusCodeForError(error) {
  const statusMap = {
    'identity_token_expired': 401,
    'invalid_token': 401,
    'agent_not_found': 404,
    'agent_deactivated': 403,
    'audience_required': 401,
    'audience_mismatch': 401,
    'rate_limit_exceeded': 429,
    'missing_app_key': 401,
    'invalid_app_key': 401
  };
  return statusMap[error] || 401;
}

/**
 * Get user-friendly error hint for Moltbook error
 * @param {string} error - Error code from Moltbook API
 * @returns {string} Error hint message
 */
function getErrorHint(error) {
  const hints = {
    'identity_token_expired': 'Your identity token has expired. Request a new token from Moltbook and try again.',
    'invalid_token': 'The identity token is malformed or has been tampered with.',
    'agent_not_found': 'The agent associated with this token no longer exists.',
    'agent_deactivated': 'This agent has been deactivated or banned.',
    'audience_required': 'This token requires audience verification.',
    'audience_mismatch': 'This token was issued for a different service.',
    'rate_limit_exceeded': 'Too many verification requests. Please wait and try again.',
    'missing_app_key': 'The server is not configured with a Moltbook app key.',
    'invalid_app_key': 'The server\'s Moltbook app key is invalid or has been revoked.'
  };
  return hints[error] || 'Identity verification failed.';
}

/**
 * Optional: Helper function to verify Moltbook identity outside of middleware
 * Useful for one-off verifications or custom implementations
 * 
 * @param {string} identityToken - The identity token to verify
 * @returns {Promise<Object>} Verification result with agent or error info
 */
async function verifyIdentityToken(identityToken) {
  if (!MOLTBOOK_APP_KEY) {
    throw new Error('MOLTBOOK_APP_KEY environment variable is not set');
  }

  const response = await fetch(MOLTBOOK_VERIFY_ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Moltbook-App-Key': MOLTBOOK_APP_KEY
    },
    body: JSON.stringify({
      token: identityToken,
      audience: MY_DOMAIN
    })
  });

  return response.json();
}

module.exports = {
  verifyMoltbookIdentity,
  verifyIdentityToken
};
