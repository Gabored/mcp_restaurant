import express from 'express';
import { Config } from './config';
import { logger } from './infra/logger';
import { adminRouter } from './controllers/adminController';
import { forecastRouter } from './controllers/forecastController';

const app = express();
app.use(express.json());

// Mount routes
app.use('/', adminRouter);
app.use('/', forecastRouter);

app.listen(Config.MCP_PORT, Config.MCP_HOST, () => {
  logger.info(`Admin API running at http://${Config.MCP_HOST}:${Config.MCP_PORT}`);
});
