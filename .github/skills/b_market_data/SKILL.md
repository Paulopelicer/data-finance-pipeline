---
name: b_market_data
description: 'Use when ingesting, normalizing, or validating B3 market data such as tickers, OHLCV prices, or historical series. Trigger phrases: B3, ticker, prices, Yahoo Finance, BRAPI, OHLCV, market data ingestion.'
---

# B - Market Data

## When to Use
- Adding or adjusting ingestion of B3 tickers or prices
- Normalizing columns, timestamps, or timezones
- Validating a new market data source

## Procedure
1. Identify ticker universe, source, and periodicity.
2. Validate schema, column names, and timestamps.
3. Normalize fields following existing conventions.
4. Document assumptions and data limitations.

## Standards
- Keep financial data real and traceable to its source.
- No hardcoded tokens or credentials.
