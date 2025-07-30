#!/usr/bin/env python3
"""
Calculate opportunity cost: bits storable vs bits transmittable for $1.
Shows the economic argument for local storage over interstellar transmission.
"""

import argparse
import math

def calculate_opportunity_cost():
    """Calculate opportunity cost comparison"""
    
    # Constants for transmission costs (from probe_cost.py analysis)
    mars_cost_per_bit = 3.25e-8  # USD per bit to Mars
    proxima_cost_per_bit = 1.56e-6  # USD per bit to Proxima
    
    # Storage cost model: halves every 2 years from 2025
    storage_2025_USD_per_bit = 2e-12  # From storage analysis
    
    years = [2025, 2075, 2125, 2217]
    results = []
    
    for year in years:
        years_from_2025 = year - 2025
        halvings = years_from_2025 / 2
        
        # Storage cost decreases exponentially  
        storage_cost_per_bit = storage_2025_USD_per_bit * (0.5 ** halvings)
        
        # For $1, how many bits can you store vs transmit?
        bits_storable = 1.0 / storage_cost_per_bit
        bits_to_mars = 1.0 / mars_cost_per_bit
        bits_to_proxima = 1.0 / proxima_cost_per_bit
        
        # Ratios
        ratio_store_mars = bits_storable / bits_to_mars
        ratio_store_proxima = bits_storable / bits_to_proxima
        
        results.append({
            'year': year,
            'bits_storable': bits_storable,
            'bits_mars': bits_to_mars,
            'bits_proxima': bits_to_proxima,
            'ratio_mars': ratio_store_mars,
            'ratio_proxima': ratio_store_proxima
        })
    
    return results

def format_large_number(num):
    """Format very large numbers appropriately"""
    if num >= 1e30:
        return f"{num:.1e}"
    elif num >= 1e15:
        return f"{num:.0e}"
    elif num >= 1e9:
        return f"{num:.1e}"
    else:
        return f"{num:.2g}"

def main():
    parser = argparse.ArgumentParser(description='Generate opportunity cost analysis')
    parser.add_argument('--csv', action='store_true', help='Output CSV format')
    args = parser.parse_args()
    
    results = calculate_opportunity_cost()
    
    if args.csv:
        print("Year,BitsStorable/$,BitsToMars/$,BitsToProxima/$,RatioStore/Mars,RatioStore/Proxima")
        for r in results:
            print(f"{r['year']},{format_large_number(r['bits_storable'])},{format_large_number(r['bits_mars'])},{format_large_number(r['bits_proxima'])},{format_large_number(r['ratio_mars'])},{format_large_number(r['ratio_proxima'])}")
    else:
        print("| Year | Bits Storable for $1 | Bits to Mars for $1 | Bits to Proxima for $1 | Storage Advantage |")
        print("|------|---------------------|---------------------|------------------------|------------------|")
        for r in results:
            advantage = f"Store {format_large_number(r['ratio_mars'])}x more than Mars, {format_large_number(r['ratio_proxima'])}x more than Proxima"
            print(f"| {r['year']} | {format_large_number(r['bits_storable'])} | {format_large_number(r['bits_mars'])} | {format_large_number(r['bits_proxima'])} | {advantage} |")

if __name__ == "__main__":
    main()