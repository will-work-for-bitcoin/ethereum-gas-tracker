# Ethereum Gas Tracker

Monitor gas prices and find optimal times to transact on Ethereum.
Fetches real-time gas data from Ethereum API endpoints.

## Features
- Real-time gas price monitoring
- Base fee and priority fee breakdown
- Transaction cost estimation in USD
- Historical context and recommendations
- Clear, actionable output

## Usage
```bash
python3 gas.py
```

## Example Output
```
============================================================
ETHEREUM GAS TRACKER
Updated: 2026-05-24 13:15:01
============================================================

Base Fee: 12.4567 Gwei

  Slow        12.5567 Gwei  $ 2.15  🟢
  Standard    12.9567 Gwei  $ 2.23  🟢
  Fast        13.4567 Gwei  $ 2.33  🟢
  Instant     14.4567 Gwei  $ 2.52  🟡

ETH price: $2,101.35

BTC Tips: 1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9
```

## How to Use
1. Check the Base Fee (minimum required to get transaction processed)
2. Choose your speed preference based on current network conditions
3. See estimated transaction cost in USD
4. Green = good time to transact, Yellow = moderate, Red = expensive

## API Sources
- Ethereum RPC via LlamaRpc for base fee
- CoinGecko for ETH price
- Blocknative API for additional data (when available)

## Support
If this tool helps you, feel free to donate:
**BTC:** `1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9`

## License
MIT
