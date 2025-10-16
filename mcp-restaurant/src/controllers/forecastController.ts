import { Router, Request, Response } from 'express';
import { getOrCreateForecast } from '../services/forecastService';

export const forecastRouter = Router();

forecastRouter.get('/forecast', async (req: Request, res: Response) => {
  const lat = Number(req.query.lat);
  const lon = Number(req.query.lon);
  if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
    return res.status(400).json({ error: 'Invalid coordinates' });
  }

  const row = await getOrCreateForecast(lat, lon);
  res.json(row);
});
