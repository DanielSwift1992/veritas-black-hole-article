#!/usr/bin/env python3
"""
Substitute calculated values into the article using markdown tags.
Tags format: {{VALUE_NAME}} or {{VALUE_NAME:format}}
"""

import json
import re
import argparse
import pathlib

def load_values():
    """Load calculated values from JSON"""
    values_file = pathlib.Path('build/artifacts/calculated_values.json')
    if not values_file.exists():
        raise FileNotFoundError("calculated_values.json not found. Run calculate_all_values.py first.")
    
    with open(values_file, 'r') as f:
        return json.load(f)

def format_value(value, format_type=None):
    """Format value according to specified format"""
    if format_type is None:
        return str(value)
    
    if isinstance(value, str):
        return value
    
    if format_type == "int":
        return str(int(value))
    elif format_type == "year":
        return str(int(value))
    elif format_type == "float2":
        return f"{value:.2f}"
    elif format_type == "float3":
        return f"{value:.3f}"
    elif format_type == "sci":
        return f"{value:.1e}"
    elif format_type == "currency":
        if value >= 1:
            return f"{value:.2f}"
        elif value >= 1e-9:
            return f"{value:.10f}".rstrip('0').rstrip('.')
        else:
            return f"~{value:.0e}"
    elif format_type == "big":
        if value >= 1e15:
            return f"{value:.1e}"
        else:
            return f"{value:,.0f}"
    else:
        return str(value)

def substitute_values_in_text(text, values):
    """Substitute all {{VALUE}} tags in text"""
    
    def replace_tag(match):
        full_tag = match.group(0)
        tag_content = match.group(1)
        
        # Parse format if specified
        if ':' in tag_content:
            value_name, format_type = tag_content.split(':', 1)
        else:
            value_name = tag_content
            format_type = None
        
        # Get value
        if value_name not in values:
            print(f"Warning: Value '{value_name}' not found in calculated values")
            return full_tag  # Return original tag if not found
        
        value = values[value_name]
        formatted_value = format_value(value, format_type)
        
        return formatted_value
    
    # Replace all {{VALUE}} or {{VALUE:format}} tags
    pattern = r'\{\{([^}]+)\}\}'
    result = re.sub(pattern, replace_tag, text)
    
    return result

def main():
    parser = argparse.ArgumentParser(description='Substitute calculated values into article')
    parser.add_argument('--input', default='article_blackhole_inevitable_en.md', 
                       help='Input markdown file')
    parser.add_argument('--output', help='Output file (default: overwrite input)')
    args = parser.parse_args()
    
    # Load values
    values = load_values()
    
    # Read input file
    input_file = pathlib.Path(args.input)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file {args.input} not found")
    
    text = input_file.read_text(encoding='utf-8')
    
    # Substitute values
    result = substitute_values_in_text(text, values)
    
    # Write output
    output_file = pathlib.Path(args.output) if args.output else input_file
    output_file.write_text(result, encoding='utf-8')
    
    print(f"Values substituted in {output_file}")

if __name__ == "__main__":
    main()