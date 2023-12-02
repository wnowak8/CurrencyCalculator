CREATE TABLE public."exchange_rates" (
	"date" date NOT NULL,
    "currency" char(3) NOT NULL,
   	"bid" float8 NOT NULL,
	"ask" float8 NOT NULL,
	CONSTRAINT "exchange_rates_pkey" PRIMARY KEY ("date","currency")
);