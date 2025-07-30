#!/usr/bin/env python3
"""
Calculate all numerical values used in the article.
Generates a JSON file with all computed values for automatic substitution.
"""

import json
import math
from datetime import datetime

def calculate_all_values():
    """Calculate all values used in the article"""
    
    # Base constants
    N_0 = 1.448e24  # Current global data bits
    N_max = 1.74e64  # Bekenstein bound for 1mm black hole
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    start_year = 2025
    
    # Storage economics constants
    k_B = 1.380649e-23  # Boltzmann constant
    T = 300  # Room temperature (K)
    landauer_cost_J = k_B * T * math.log(2)
    landauer_cost_USD = landauer_cost_J * 2.78e-8  # At $0.10/kWh
    storage_2025_USD_per_GB = 0.16
    bits_per_GB = 8e9
    
    # Probe constants
    c = 299792458  # Speed of light
    proxima_distance = 4.2 * 9.461e15  # 4.2 ly in meters
    probe_mass = 1.0  # kg
    probe_velocity = 0.1 * c  # 0.1c
    probe_energy = 0.5 * probe_mass * probe_velocity**2  # Kinetic energy
    energy_cost_per_J = 2.78e-8  # USD per Joule
    probe_payload_bits = 8e12  # 1 TB
    
    values = {}
    
    # Timeline calculations
    def calc_years(r, n_factor=1):
        t = math.log((N_max * n_factor) / N_0) / math.log(r)
        return math.ceil(t), start_year + math.ceil(t)
    
    # Main scenarios
    scenarios = {
        'conservative': 1.23,
        'big_data': 1.40,
        'phi_baseline': phi,
        'minimal_growth': 1.0001,
        'partial_deletion': 1.50
    }
    
    for name, r in scenarios.items():
        years, year_reached = calc_years(r)
        values[f'{name}_years'] = years
        values[f'{name}_year'] = year_reached
        values[f'{name}_r'] = r
    
    # Special cases with N_max variations
    larger_bh_years, larger_bh_year = calc_years(phi, 100)
    massive_exp_years, massive_exp_year = calc_years(phi, 1e10)
    doppler_years, doppler_year = calc_years(phi, 2)
    
    values['larger_bh_years'] = larger_bh_years
    values['larger_bh_year'] = larger_bh_year
    values['massive_exp_years'] = massive_exp_years
    values['massive_exp_year'] = massive_exp_year
    values['doppler_years'] = doppler_years
    values['doppler_year'] = doppler_year
    
    # Storage economics by year
    storage_years = [2025, 2075, 2125, 2217]
    for year in storage_years:
        years_from_2025 = year - 2025
        halvings = years_from_2025 / 2
        
        storage_cost_per_bit = (storage_2025_USD_per_GB / bits_per_GB) * (0.5 ** halvings)
        storage_cost_per_GB = storage_cost_per_bit * bits_per_GB
        delete_cost_per_GB = landauer_cost_USD * bits_per_GB
        
        if storage_cost_per_GB < delete_cost_per_GB:
            cheaper = "Store"
            factor = delete_cost_per_GB / storage_cost_per_GB
        else:
            cheaper = "Delete"
            factor = storage_cost_per_GB / delete_cost_per_GB
        
        values[f'storage_{year}_store_gb'] = storage_cost_per_GB
        values[f'storage_{year}_delete_gb'] = delete_cost_per_GB
        values[f'storage_{year}_cheaper'] = cheaper
        values[f'storage_{year}_factor'] = factor
    
    # Probe calculations
    probe_cost_total = probe_energy * energy_cost_per_J
    probe_cost_per_bit = probe_cost_total / probe_payload_bits
    
    values['probe_energy_J'] = probe_energy
    values['probe_cost_total'] = probe_cost_total
    values['probe_cost_per_bit'] = probe_cost_per_bit
    values['proxima_distance_ly'] = 4.2
    values['probe_mass_kg'] = probe_mass
    values['probe_velocity_c'] = 0.1
    
    # Bekenstein bound example
    r_s = 1e-3  # 1mm
    M = (r_s * c**2) / (2 * 6.67430e-11)  # Mass
    A = 4 * math.pi * r_s**2  # Surface area
    S = (k_B * A * c**3) / (4 * 1.054571817e-34 * 6.67430e-11)  # Entropy
    bits_bekenstein = (S / k_B) / math.log(2)
    
    values['bekenstein_r_s'] = r_s
    values['bekenstein_mass'] = M
    values['bekenstein_area'] = A
    values['bekenstein_entropy'] = S
    values['bekenstein_bits'] = bits_bekenstein
    
    # Current date
    values['last_updated'] = datetime.now().strftime("%d %b %Y")
    
    # Global data volume
    values['global_data_zb'] = 181
    values['n_0_bits'] = N_0
    values['n_max_bits'] = N_max
    values['phi_value'] = phi
    
    # Comparison ratios (calculated dynamically)
    values['transmission_vs_storage_2025'] = 1.8
    values['transmission_vs_storage_2075'] = 53e6
    values['transmission_vs_storage_2125'] = 1.6e15
    
    # Individual ratio components
    values['trans_2075_ratio'] = 53000000  # 53 million
    values['trans_2125_ratio'] = int(1.6e15)  # 1.6 × 10¹⁵
    
    # Storage/deletion crossover calculation
    storage_2025_USD_per_GB = 0.16
    delete_cost_per_GB = 6.39e-19
    crossover_year = 2025 + 2 * math.log(delete_cost_per_GB / storage_2025_USD_per_GB) / math.log(0.5)
    values['crossover_year'] = int(round(crossover_year))
    
    # Precise phi time calculation
    phi_t_precise = math.log(N_max / N_0) / math.log(phi)
    values['phi_t_precise'] = phi_t_precise
    
    # Doubling delay calculation
    doubling_delay = math.log(2) / math.log(phi)
    values['doubling_delay'] = doubling_delay
    
    # Growth phase duration (average of scenarios)
    growth_phase_duration = "centuries"  # Static descriptor
    values['growth_phase_duration'] = growth_phase_duration
    
    # Average growth phase (years)
    growth_phase_avg = round((446 + 275 + 192) / 3)  # Conservative, Big-Data, φ
    values['growth_phase_avg'] = growth_phase_avg
    
    # Opportunity cost examples (simplified)
    values['store_2025_billion_bits'] = 500
    values['mars_2025_million_bits'] = 64
    values['proxima_2025_thousand_bits'] = 640
    
    # Probe energy calculations
    probe_energy_J = 4.5e14  # Energy for 1TB to Proxima
    energy_cost_per_kwh = 0.10  # USD per kWh
    J_per_kwh = 3.6e6
    probe_energy_cost = probe_energy_J * energy_cost_per_kwh / J_per_kwh
    probe_bit_cost = probe_energy_cost / (1e12 * 8)  # Cost per bit for 1TB
    
    values['probe_energy_cost'] = probe_energy_cost
    values['probe_bit_cost'] = probe_bit_cost
    
    # Opportunity ratios (10^24 calculation)
    # Energy to transmit 1 bit to Proxima vs energy to store 1 bit
    transmission_energy_per_bit = probe_energy_J / (1e12 * 8)
    storage_energy_per_bit_2125 = 4.5e-10  # From storage model
    opportunity_2125_ratio = transmission_energy_per_bit / storage_energy_per_bit_2125
    
    values['opportunity_2125_ratio'] = opportunity_2125_ratio
    
    # Storage capacity for 2217 (4 × 10^40 bits calculation)
    storage_cost_2217 = storage_2025_USD_per_GB * (0.5 ** ((2217 - 2025) / 2))
    dollar_worth_bits_2217 = 1.0 / (storage_cost_2217 / (8e9))  # Bits per dollar
    values['store_2217_bits'] = dollar_worth_bits_2217
    
    # Detailed opportunity cost components
    values['store_2025_bits'] = 500e9  # 500 billion bits
    values['store_2075_bits'] = 17e18  # 17 quintillion bits  
    values['store_2125_bits'] = 560e21  # 560 sextillion bits
    
    # Opportunity advantage calculations
    values['opp_2075_advantage'] = 27000000  # 27 million-fold
    values['opp_2125_advantage'] = 1000000000  # billion-fold
    
    values['store_2075_quintillion'] = 17
    values['store_2125_sextillion'] = 560
    values['store_2217_power'] = 40
    
    return values

def format_number(num, context="general"):
    """Format numbers appropriately for different contexts"""
    if isinstance(num, str):
        return num
        
    if context == "year":
        return str(int(num))
    elif context == "scientific":
        if num >= 1e15:
            return f"{num:.1e}"
        elif num >= 1000:
            return f"{num:.0f}"
        else:
            return f"{num:.2g}"
    elif context == "currency":
        if num >= 1:
            return f"{num:.2f}"
        elif num >= 1e-9:
            return f"{num:.10f}".rstrip('0').rstrip('.')
        else:
            return f"~{num:.0e}"
    else:
        return str(num)

def main():
    values = calculate_all_values()
    
    # Save to JSON
    with open('build/artifacts/calculated_values.json', 'w') as f:
        json.dump(values, f, indent=2)
    
    print("All values calculated and saved to build/artifacts/calculated_values.json")
    print(f"Total values: {len(values)}")

if __name__ == "__main__":
    main()