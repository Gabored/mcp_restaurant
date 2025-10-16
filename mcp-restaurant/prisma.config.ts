import { defineConfig } from '@prisma/config';
import dotenv from 'dotenv';

// Load env for any Prisma CLI that runs during build
dotenv.config({ path: '.env' });

export default defineConfig({
  schema: 'src/infra/db/schema.prisma',
});
