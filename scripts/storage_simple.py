#!/usr/bin/env python3
"""
Simplified storage/deletion crossover calculation for Information Economics section.
Generates table showing when storage becomes cheaper than deletion.
"""

import argparse
import math

def calculate_storage_simple():
    """Calculate simplified storage vs deletion costs"""
    
    # Constants
    k_B = 1.380649e-23  # Boltzmann constant
    T = 300  # Room temperature (K)
    landauer_cost_J = k_B * T * math.log(2)  # Minimum energy per bit deletion
    landauer_cost_USD = landauer_cost_J * 2.78e-8  # At $0.10/kWh
    
    # Storage cost model: halves every 2 years from 2025 baseline
    storage_2025_USD_per_GB = 0.16  # Current SSD cost
    bits_per_GB = 8e9
    storage_2025_USD_per_bit = storage_2025_USD_per_GB / bits_per_GB
    
    years = [2025, 2075, 2125, 2217]
    results = []
    
    for year in years:
        years_from_2025 = year - 2025
        halvings = years_from_2025 / 2
        
        # Storage cost decreases exponentially
        storage_cost_per_bit = storage_2025_USD_per_bit * (0.5 ** halvings)
        storage_cost_per_GB = storage_cost_per_bit * bits_per_GB
        
        # Deletion cost stays constant (Landauer limit)
        delete_cost_per_bit = landauer_cost_USD
        delete_cost_per_GB = delete_cost_per_bit * bits_per_GB
        
        # Which is cheaper and by how much?
        if storage_cost_per_GB < delete_cost_per_GB:
            cheaper = "Store"
            factor = delete_cost_per_GB / storage_cost_per_GB
        else:
            cheaper = "Delete" 
            factor = storage_cost_per_GB / delete_cost_per_GB
            
        results.append({
            'year': year,
            'store_usd_gb': storage_cost_per_GB,
            'delete_usd_gb': delete_cost_per_GB,
            'cheaper': cheaper,
            'factor': factor
        })
    
    return results

def format_number(num):
    """Format number for maximum readability"""
    if num >= 1e15:
        # Use scientific notation for very large numbers
        return f"{num:.1e}"
    elif num >= 1:
        return f"{num:.2f}"
    elif num >= 1e-6:
        # Use decimal notation for readable numbers (down to micro scale)
        formatted = f"{num:.12f}".rstrip('0').rstrip('.')
        return formatted
    elif num >= 1e-15:
        # Use scientific notation but cleaner format
        return f"{num:.1e}"
    else:
        return f"~{num:.0e}"

def main():
    parser = argparse.ArgumentParser(description='Generate simplified storage crossover table')
    parser.add_argument('--csv', action='store_true', help='Output CSV format')
    args = parser.parse_args()
    
    results = calculate_storage_simple()
    
    if args.csv:
        print("Year,StoreUSD/GB,DeleteUSD/GB,Cheaper,Factor")
        for r in results:
            print(f"{r['year']},{format_number(r['store_usd_gb'])},{format_number(r['delete_usd_gb'])},{r['cheaper']},{format_number(r['factor'])}")
    else:
        print("| Year | StoreUSD/GB | DeleteUSD/GB | Cheaper | Factor |")
        print("|------|-------------|--------------|---------|--------|")
        for r in results:
            print(f"| {r['year']} | {format_number(r['store_usd_gb'])} | {format_number(r['delete_usd_gb'])} | {r['cheaper']} | {format_number(r['factor'])} |")

if __name__ == "__main__":
    main()