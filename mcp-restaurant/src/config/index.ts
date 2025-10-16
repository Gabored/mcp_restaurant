import dotenv from 'dotenv';
import { z } from 'zod';
dotenv.config();

// treat empty strings as undefined
const emptyToUndefined = z
  .string()
  .transform((s) => (s?.trim() === '' ? undefined : s.trim()))
  .optional();

const schema = z.object({
  MCP_HOST: z.string().default('127.0.0.1'),
  MCP_PORT: z.coerce.number().default(8080),
  LOG_LEVEL: z.string().default('info'),

  SEVEN_TIMER_BASE_URL: z.string().url(),
  DEFAULT_PRODUCT: z.string().default('civillight'),
  DEFAULT_OUTPUT: z.string().default('json'),

  DATABASE_URL: z.string(),

  OAUTH_ISSUER_URL: emptyToUndefined,
  OAUTH_AUDIENCE: emptyToUndefined,

  DEV_BYPASS_OAUTH: z.string().optional(), // 'true' enables bypass
});

const raw = schema.parse(process.env);

export const DEV_BYPASS = raw.DEV_BYPASS_OAUTH === 'true';
export const OAUTH_ENABLED =
  !DEV_BYPASS && !!raw.OAUTH_ISSUER_URL && !!raw.OAUTH_AUDIENCE;

type AppConfig = z.infer<typeof schema> & { OAUTH_ENABLED: boolean };

export const Config: AppConfig = {
  ...raw,
  OAUTH_ENABLED,
};
