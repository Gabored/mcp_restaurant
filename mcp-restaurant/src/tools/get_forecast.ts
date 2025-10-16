import { getForecast } from '../services/sevenTimerClient';
import { logger } from '../infra/logger';

export async function getForecastTool(lat: number, lon: number) {
  try {
    const forecast = await getForecast(lat, lon);
    logger.info({ lat, lon }, 'Forecast retrieved');
    return forecast;
  } catch (err) {
    logger.error({ err }, 'Error fetching forecast');
    throw new Error('Forecast retrieval failed');
  }
}
