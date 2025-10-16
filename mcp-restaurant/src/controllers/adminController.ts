import { Router, Request, Response } from 'express';
import { verifyJWT } from '../infra/auth';
import { Config } from '../config';
import client from 'prom-client';
import { forecastCache } from '../infra/cache';

const register = new client.Registry();
client.collectDefaultMetrics({ register });

export const adminRouter = Router();

// Public
adminRouter.get('/healthz', (_req: Request, res: Response) => {
  res.json({ status: 'ok', uptime: process.uptime(), time: new Date().toISOString() });
});

// Protected
adminRouter.get('/config', verifyJWT, (_req, res) => {
  // redacted config surface
  res.json({
    host: Config.MCP_HOST,
    port: Config.MCP_PORT,
    product: Config.DEFAULT_PRODUCT,
    output: Config.DEFAULT_OUTPUT,
    sevenTimerBaseUrl: Config.SEVEN_TIMER_BASE_URL,
  });
});

adminRouter.get('/metrics', verifyJWT, async (_req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

adminRouter.get('/cache/keys', verifyJWT, (_req, res) => {
  res.json({ keys: forecastCache.keys() });
});
