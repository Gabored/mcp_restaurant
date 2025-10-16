import { z } from 'zod';

export const CivillightSchema = z.object({
  product: z.string(),
  init: z.string().optional(),
  dataseries: z.array(
    z.object({
      date: z.number(),
      weather: z.string(),
      temp2m: z.object({
        min: z.number(),
        max: z.number(),
      }),
      wind10m_max: z.number().optional(),
    })
  ).min(1, 'dataseries is empty'),
});
