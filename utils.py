import streamlit as st
import json
import pandas as pd
import re
import datetime
from typing import Dict, Any, Optional
import os

# Try to import Gemini libraries (with fallback if not installed)
try:
    import google.generativeai as genai
except ImportError:
    genai = None

def load_data(file_path):
    """Load and preprocess data from Excel file"""
    try:
        df = pd.read_excel(file_path)
        
        # Rename columns to match expected format
        column_mapping = {
            'Timestamp': 'date',
            'Device ID': 'device_id',
            'Location': 'location',
            'Total Output': 'total_units',
            'Good Output': 'good_units',
            'Downtime (min)': 'downtime_minutes',
            'Operating Time (min)': 'uptime_minutes',
            'Ideal Cycle Time (s)': 'ideal_cycle_time'
        }
        
        # Rename columns if they exist
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df[new_col] = df[old_col]
        
        # Calculate additional required columns
        if 'uptime_minutes' in df.columns:
            # Planned production time is operating time + downtime
            df['planned_production_minutes'] = df['uptime_minutes'] + df.get('downtime_minutes', 0)
        
        # Calculate theoretical output based on uptime and ideal cycle time
        if 'uptime_minutes' in df.columns and 'ideal_cycle_time' in df.columns:
            # Convert ideal cycle time from seconds to minutes and calculate theoretical output
            df['theoretical_output'] = df['uptime_minutes'] / (df['ideal_cycle_time'] / 60)
        
        # Set actual output equal to total units
        if 'total_units' in df.columns:
            df['actual_output'] = df['total_units']
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def filter_data(data, device_id=None, location=None, month=None):
    """Filter the data based on device_id, location, and month"""
    df = data.copy()
    
    if device_id and 'device_id' in df.columns:
        df = df[df['device_id'] == device_id]
    
    if location and 'location' in df.columns:
        df = df[df['location'] == location]
    
    if month and 'date' in df.columns:
        # Convert month string (e.g. "January 2025") to date range
        try:
            month_year = datetime.datetime.strptime(month, "%B %Y")
            next_month = month_year.replace(month=month_year.month % 12 + 1)
            if next_month.month == 1:
                next_month = next_month.replace(year=next_month.year + 1)
            
            start_date = month_year.strftime("%Y-%m-%d")
            end_date = next_month.strftime("%Y-%m-%d")
            
            # Convert date column to datetime if it's not already
            if not pd.api.types.is_datetime64_any_dtype(df['date']):
                df['date'] = pd.to_datetime(df['date'])
                
            df = df[(df['date'] >= start_date) & (df['date'] < end_date)]
        except Exception as e:
            st.warning(f"Error filtering by month: {e}")
    
    return df

def calculate_oee(data):
    """Calculate OEE metrics from filtered data"""
    if data.empty:
        return None
    
    # Check if required columns exist
    required_columns = ['uptime_minutes', 'planned_production_minutes', 
                        'actual_output', 'theoretical_output',
                        'good_units', 'total_units']
    
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return None
    
    # Calculate metrics (example implementation)
    try:
        availability = round((data['uptime_minutes'].sum() / data['planned_production_minutes'].sum()) * 100, 1)
        performance = round((data['actual_output'].sum() / data['theoretical_output'].sum()) * 100, 1)
        quality = round((data['good_units'].sum() / data['total_units'].sum()) * 100, 1)
        
        # Calculate overall OEE
        oee = round((availability / 100) * (performance / 100) * (quality / 100) * 100, 1)
        
        return {
            'OEE': oee,
            'Availability': availability,
            'Performance': performance,
            'Quality': quality
        }
    except Exception as e:
        st.error(f"Error calculating OEE: {e}")
        return None

def parse_query_with_gemini(query: str) -> Dict[str, Optional[str]]:
    """
    Parse a natural language query to extract device_id, location, and month information.
    Uses regex parsing.
    
    Args:
        query: The natural language query from the user
        
    Returns:
        Dictionary with extracted device_id, location, and month values
    """
    # Use regex parsing as the default approach
    device = re.search(r"(PKG-\d{3})", query)
    location = next((loc for loc in ['Mumbai', 'Chennai', 'Delhi', 'Kolkata', 'Hyderabad']
                    if loc.lower() in query.lower()), None)
    month_pattern = r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}"
    month = re.search(month_pattern, query, re.IGNORECASE)
    
    # Also look for "last month", "last year" phrases
    if not month and "last july" in query.lower():
        # If we're currently in 2025, last July would be July 2024
        month = "July 2024"
    
    parsed = {
        "device_id": device.group(0) if device else None,
        "location": location,
        "month": month.group(0).title() if isinstance(month, re.Match) else month
    }
    
    return parsed