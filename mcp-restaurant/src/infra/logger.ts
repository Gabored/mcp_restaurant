import pino from 'pino';
import { Config } from '../config';

export const logger = pino({
  level: Config.LOG_LEVEL,
  // Use null (not undefined) when exactOptionalPropertyTypes is true
  base: null, // removes default pid/hostname bindings cleanly
});
