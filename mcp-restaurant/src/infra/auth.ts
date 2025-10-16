import { Request, Response, NextFunction } from 'express';
import { Config, DEV_BYPASS } from '../config';
import { createRemoteJWKSet, jwtVerify, type JWTVerifyOptions } from 'jose';

let JWKS: ReturnType<typeof createRemoteJWKSet> | null = null;

export async function verifyJWT(req: Request, res: Response, next: NextFunction) {
  // Allow when bypass enabled or OAuth not configured/enabled
  if (DEV_BYPASS || !Config.OAUTH_ENABLED) return next();

  const header = req.header('authorization');
  if (!header) return res.status(401).json({ error: 'Missing Authorization header' });

  const [scheme, token] = header.split(' ');
  if (scheme !== 'Bearer' || !token) {
    return res.status(401).json({ error: 'Invalid Authorization header (expect Bearer token)' });
  }

  if (!Config.OAUTH_ISSUER_URL || !Config.OAUTH_AUDIENCE) {
    return res.status(500).json({ error: 'OAuth not configured' });
  }

  try {
    if (!JWKS) {
      JWKS = createRemoteJWKSet(new URL(`${Config.OAUTH_ISSUER_URL}/.well-known/jwks.json`));
    }

    const options: JWTVerifyOptions = {
      issuer: Config.OAUTH_ISSUER_URL,
      audience: Config.OAUTH_AUDIENCE,
    };

    // token is now definitely a string
    await jwtVerify(token, JWKS, options);
    return next();
  } catch {
    return res.status(403).json({ error: 'Invalid or expired token' });
  }
}
