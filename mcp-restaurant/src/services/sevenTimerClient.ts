import axios from 'axios';
import { Config } from '../config';
import { CivillightSchema, Civillight } from '../domain/forecast';
import { forecastCache } from '../infra/cache';

export async function fetchCivillight(lat: number, lon: number, product = Config.DEFAULT_PRODUCT): Promise<Civillight> {
  const key = `${lat}|${lon}|${product}`;
  const cached = forecastCache.get(key);
  if (cached) return cached;

  const url = `${Config.SEVEN_TIMER_BASE_URL}/bin/api.pl`;
  const params = { lat, lon, product, output: 'json' };

  const { data } = await axios.get(url, { params, timeout: 10_000 });
  const parsed = CivillightSchema.parse(data);
  forecastCache.set(key, parsed);
  return parsed;
}
