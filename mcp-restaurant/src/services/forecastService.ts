import { prisma } from '../infra/db/prisma';
import { fetchCivillight } from './sevenTimerClient';

const FRESH_MS = 3 * 60 * 60 * 1000; // 3h

export async function getOrCreateForecast(lat: number, lon: number) {
  const recent = await prisma.forecast.findFirst({
    where: { lat, lon },
    orderBy: { dateUtc: 'desc' },
  });

  if (recent && recent.dateUtc.getTime() > Date.now() - FRESH_MS) {
    return recent;
  }

  const civillight = await fetchCivillight(lat, lon);
  const day0 = civillight.dataseries[0];
  if (!day0) {
  // You can choose to throw, or return the last DB row if present.
  throw new Error('7Timer returned no forecast data (dataseries was empty).');
}
  const created = await prisma.forecast.upsert({
    where: {
      lat_lon_product_dateUtc: {
        lat,
        lon,
        product: civillight.product,
        dateUtc: new Date(new Date().toDateString()),
      },
    },
    update: {
      weatherCode: day0.weather,
      tempMin: day0.temp2m.min,
      tempMax: day0.temp2m.max,
      windMax: day0.wind10m_max ?? null,
      source: '7timer',
    },
    create: {
      lat,
      lon,
      product: civillight.product,
      dateUtc: new Date(new Date().toDateString()),
      weatherCode: day0.weather,
      tempMin: day0.temp2m.min,
      tempMax: day0.temp2m.max,
      windMax: day0.wind10m_max ?? null,
      source: '7timer',
    },
  });

  return created;
}
