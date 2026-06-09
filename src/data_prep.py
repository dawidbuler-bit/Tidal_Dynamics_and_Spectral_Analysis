import pandas as pd
import os
import sys
from pathlib import Path

def prepare_tide_data(input_path, output_path, water_col='Verified (m)'):

    file_name = os.path.basename(input_path)
    
    try:
        df = pd.read_csv(input_path, sep=None, engine='python', na_values='-')
        
        missing_count = df[water_col].isna().sum()
        total_rows = len(df)
        missing_percent = (missing_count / total_rows) * 100
        
        print(f"🔍 REPORT FOR: {file_name}")
        print(f"   - Total records: {total_rows}")
        print(f"   - Missing values in '{water_col}': {missing_count}")
        print(f"   - Missing percentage: {missing_percent:.2f}%")
        
        if missing_count > 0:
            print(f"   WARNING: Interpolation required for this file.")
        else:
            print(f"   DATA COMPLETE: Interpolation will not change the results.")
        print("-" * 50)
        # ----------------------------

        time_col = 'Time (GMT)' if 'Time (GMT)' in df.columns else 'Time'
        df['Date + Time'] = pd.to_datetime(df['Date'] + ' ' + df[time_col])
        
        df = df.sort_values('Date + Time')
        df.to_csv(output_path, sep=';', index=False)
        
    except Exception as e:
        print(f"ERROR processing file {file_name}: {e}")