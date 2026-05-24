#!/usr/bin/env python3
"""
Ethereum Gas Tracker - Monitor gas prices and find optimal times to transact
Fetches real-time gas data from Ethereum API endpoints

BTC Tips: 1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9
"""
import json
import urllib.request
import sys
from datetime import datetime

def get_gas_prices():
    """Get current gas prices from multiple sources"""
    prices = {}
    
    # EIP-1559 fees
    try:
        url = "https://api.blocknative.com/api/v1/gasnow/eth-mainnet"
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
        prices['blocknative'] = data
    except:
        pass
    
    # Fallback: simple estimation from Ethereum RPC
    try:
        payload = json.dumps({"jsonrpc": "2.0", "method": "eth_gasPrice", "params": [], "id": 1})
        req = urllib.request.Request(
            "https://eth.llamarpc.com",
            data=payload.encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            gas_wei = int(data['result'], 16)
            prices['current_gwei'] = gas_wei / 1e9
    except:
        pass
    
    return prices

def get_base_fee():
    """Get current base fee from latest block"""
    try:
        payload = json.dumps({"jsonrpc": "2.0", "method": "eth_getBlockByNumber", "params": ["latest", False], "id": 1})
        req = urllib.request.Request(
            "https://eth.llamarpc.com",
            data=payload.encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            base_fee_wei = int(data['result']['baseFeePerGas'], 16)
            return base_fee_wei / 1e9
    except:
        return None

def estimate_transaction_cost(gas_gwei, gas_units=21000):
    """Estimate transaction cost in USD"""
    # Get ETH price
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        with urllib.request.urlopen(url, timeout=10) as response:
            eth_price = json.loads(response.read())['ethereum']['usd']
        cost = (gas_gwei * 1e9 * gas_units) / 1e18 * eth_price
        return cost, eth_price
    except:
        return None, None

def main():
    print("=" * 60)
    print("ETHEREUM GAS TRACKER")
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    base_fee = get_base_fee()
    if base_fee:
        print(f"\nBase Fee: {base_fee:.4f} Gwei")
        
        # Estimates for different priority fees
        for name, tip in [("Slow", 0.1), ("Standard", 0.5), ("Fast", 1.0), ("Instant", 2.0)]:
            total = base_fee + tip
            cost, eth_price = estimate_transaction_cost(total)
            if cost:
                status = "🟢" if total < 20 else "🟡" if total < 50 else "🔴"
                print(f"  {name:<10} {total:>8.4f} Gwei  ${cost:>8.2f}  {status}")
    
    print(f"\nETH price: ${estimate_transaction_cost(1, 1)[1]:,.2f}" if estimate_transaction_cost(1, 1)[1] else "\nETH price: unavailable")
    print(f"\nBTC Tips: 1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9")

if __name__ == "__main__":
    main()
