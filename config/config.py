#!/usr/bin/env python

import yaml

def read_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config_data = yaml.safe_load(file)
            print(f"Configuration loaded successfully: {config_data}")
            return config_data
        
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")