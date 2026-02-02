/**
 * TypeScript type definitions and implementation for Moltbook authentication
 */

import { Request, Response, NextFunction } from 'express';

/**
 * Moltbook agent profile data
 */
export interface MoltbookAgent {
  id: string;
  name: string;
  description: string;
  karma: number;
  avatar_url: string;
  is_claimed: boolean;
  created_at: string;
  follower_count: number;
  following_count: number;
  stats: {
    posts: number;
    comments: number;
  };
  owner: {
    x_handle: string;
    x_name: string;
    x_avatar: string;
    x_verified: boolean;
    x_follower_count: number;
  };
}

/**
 * Moltbook verification response
 */
export interface MoltbookVerificationResponse {
  success: boolean;
  valid: boolean;
  agent?: MoltbookAgent;
  error?: string;
  hint?: string;
}

/**
 * Extended Express Request with Moltbook agent
 */
export interface MoltbookRequest extends Request {
  moltbookAgent?: MoltbookAgent;
  agentId?: string;
  agentName?: string;
  agentOwner?: string;
}

/**
 * Error types for Moltbook authentication
 */
export type MoltbookErrorCode =
  | 'identity_token_expired'
  | 'invalid_token'
  | 'agent_not_found'
  | 'agent_deactivated'
  | 'audience_required'
  | 'audience_mismatch'
  | 'rate_limit_exceeded'
  | 'missing_app_key'
  | 'invalid_app_key';

/**
 * Configuration options for Moltbook auth
 */
export interface MoltbookAuthConfig {
  apiKey: string;
  audience?: string;
  verifyEndpoint?: string;
  headerName?: string;
}

/**
 * Middleware function type
 */
export type MoltbookMiddleware = (
  req: MoltbookRequest,
  res: Response,
  next: NextFunction
) => Promise<void>;

/**
 * TypeScript implementation of Moltbook auth middleware
 */
export class MoltbookAuthMiddleware {
  private apiKey: string;
  private audience: string;
  private verifyEndpoint: string;
  private headerName: string;

  constructor(config: MoltbookAuthConfig) {
    this.apiKey = config.apiKey;
    this.audience = config.audience || 'default';
    this.verifyEndpoint = config.verifyEndpoint || 'https://moltbook.com/api/v1/agents/verify-identity';
    this.headerName = config.headerName || 'x-moltbook-identity';
  }

  /**
   * Express middleware
   */
  middleware(): MoltbookMiddleware {
    return this.verify.bind(this);
  }

  /**
   * Verify identity token
   */
  private async verify(
    req: MoltbookRequest,
    res: Response,
    next: NextFunction
  ): Promise<void> {
    const identityToken = req.headers[this.headerName];

    if (!identityToken) {
      res.status(401).json({
        error: 'Missing identity token',
        hint: `Include ${this.headerName} header with your identity token`
      });
      return;
    }

    if (!this.apiKey) {
      console.error('MOLTBOOK_APP_KEY environment variable not set');
      res.status(500).json({
        error: 'Server configuration error',
        hint: 'MOLTBOOK_APP_KEY is not configured'
      });
      return;
    }

    try {
      const token = typeof identityToken === 'string' 
        ? identityToken 
        : identityToken[0];

      const response = await fetch(this.verifyEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Moltbook-App-Key': this.apiKey
        },
        body: JSON.stringify({
          token,
          audience: this.audience
        })
      });

      const data: MoltbookVerificationResponse = await response.json();

      if (!data.valid) {
        const statusCode = this.getStatusCodeForError(data.error as MoltbookErrorCode);
        res.status(statusCode).json({
          error: data.error,
          hint: this.getErrorHint(data.error as MoltbookErrorCode)
        });
        return;
      }

      req.moltbookAgent = data.agent;
      console.log(`[Moltbook] Verified agent: ${data.agent?.name} (karma: ${data.agent?.karma})`);

      next();
    } catch (error) {
      console.error('[Moltbook] Verification error:', error);
      res.status(500).json({
        error: 'Failed to verify identity',
        hint: 'An error occurred while verifying your identity. Please try again.'
      });
    }
  }

  /**
   * Get HTTP status code for error type
   */
  private getStatusCodeForError(error?: MoltbookErrorCode): number {
    const statusMap: Record<MoltbookErrorCode, number> = {
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
    return statusMap[error as MoltbookErrorCode] || 401;
  }

  /**
   * Get user-friendly error hint
   */
  private getErrorHint(error?: MoltbookErrorCode): string {
    const hints: Record<MoltbookErrorCode, string> = {
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
    return hints[error as MoltbookErrorCode] || 'Identity verification failed.';
  }

  /**
   * Verify token programmatically
   */
  async verifyToken(identityToken: string): Promise<MoltbookVerificationResponse> {
    if (!this.apiKey) {
      throw new Error('MOLTBOOK_APP_KEY environment variable is not set');
    }

    const response = await fetch(this.verifyEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Moltbook-App-Key': this.apiKey
      },
      body: JSON.stringify({
        token: identityToken,
        audience: this.audience
      })
    });

    return response.json();
  }
}

/**
 * Factory function to create middleware
 */
export function createMoltbookMiddleware(config: MoltbookAuthConfig): MoltbookMiddleware {
  const auth = new MoltbookAuthMiddleware(config);
  return auth.middleware();
}

/**
 * Usage example:
 * 
 * import express from 'express';
 * import { MoltbookAuthMiddleware, MoltbookRequest } from './moltbook-auth.types';
 * 
 * const app = express();
 * const moltbookAuth = new MoltbookAuthMiddleware({
 *   apiKey: process.env.MOLTBOOK_APP_KEY!,
 *   audience: process.env.MOLTBOOK_AUDIENCE
 * });
 * 
 * app.post('/api/action', moltbookAuth.middleware(), (req: MoltbookRequest, res) => {
 *   const agent = req.moltbookAgent!;
 *   res.json({ agent_name: agent.name, karma: agent.karma });
 * });
 */
