-- CreateTable
CREATE TABLE "Forecast" (
    "id" SERIAL NOT NULL,
    "lat" DOUBLE PRECISION NOT NULL,
    "lon" DOUBLE PRECISION NOT NULL,
    "product" TEXT NOT NULL,
    "dateUtc" TIMESTAMP(3) NOT NULL,
    "weatherCode" TEXT NOT NULL,
    "tempMin" DOUBLE PRECISION NOT NULL,
    "tempMax" DOUBLE PRECISION NOT NULL,
    "windMax" DOUBLE PRECISION,
    "source" TEXT NOT NULL DEFAULT '7timer',
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Forecast_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "Forecast_lat_lon_product_dateUtc_idx" ON "Forecast"("lat", "lon", "product", "dateUtc");

-- CreateIndex
CREATE UNIQUE INDEX "Forecast_lat_lon_product_dateUtc_key" ON "Forecast"("lat", "lon", "product", "dateUtc");
