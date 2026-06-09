import pandas as pd
import numpy as np
from scipy import signal
import importlib.util
import os
import sys
from pathlib import Path

file_path = Path(os.getcwd()).parent / "src" / "drawing_function.py"

print(f"Attempting to load from: {file_path}")

spec = importlib.util.spec_from_file_location("drawing_function", str(file_path))
drawing_module = importlib.util.module_from_spec(spec)
sys.modules["drawing_function"] = drawing_module

try:
    spec.loader.exec_module(drawing_module)
    _draw_spectrum_plots = drawing_module._draw_spectrum_plots
    print("SUCCESS: Function loaded directly from file!")
except Exception as e:
    print(f"Still encountering an error: {e}")


def plot_fourier_universal(file_path, months_to_analyze=1, freq_minutes=6, time_col='Date + Time', water_col='Verified (m)', delimiter=';'):

    file_name = os.path.basename(file_path)
    print(f"\n--- DYNAMIC FFT | Range: {months_to_analyze} months | Step: {freq_minutes} min | File: {file_name} ---")
    
    try:
        # Load data
        df = pd.read_csv(file_path, delimiter=delimiter)
    except FileNotFoundError:
        print(f"!!! ERROR: File not found: {file_path}")
        return
        
    df[time_col] = pd.to_datetime(df[time_col], dayfirst=True, format='mixed')
    
    # Limit time based on the months_to_analyze argument
    start_date = df[time_col].min()
    end_date = start_date + pd.DateOffset(months=months_to_analyze)
    df = df[(df[time_col] >= start_date) & (df[time_col] < end_date)].copy()
    
    # Sort and remove time duplicates
    df = df.sort_values(by=time_col).drop_duplicates(subset=[time_col])
    
    # --- DATA AUDIT AND PATH SELECTION ---
    missing_count = df[water_col].isna().sum()
    
    if missing_count > 0:
        print(f"   Missing values detected ({missing_count}). Applied 3rd-order spline interpolation.")
        mode_title = "WITH INTERPOLATION"
        
        # Create a strict time grid and patch missing data
        df = df.set_index(time_col)
        full_time_grid = pd.date_range(start=df.index.min(), end=df.index.max(), freq=f'{freq_minutes}min')
        df = df.reindex(full_time_grid)
        
        df[water_col] = df[water_col].interpolate(method='spline', order=3, limit=100) 
        df[water_col] = df[water_col].interpolate(method='linear').fillna(0) 
        df = df.reset_index().rename(columns={'index': time_col})
        
        # Forced, ideal time step (e.g., exactly 6 minutes as a fraction of a day)
        dt_days = freq_minutes / 1440.0
        
    else:
        print("   Data 100% complete. Utilizing raw measurements.")
        mode_title = "No interpolation"
        
        # Clean and prepare from the original time axis
        df = df.dropna(subset=[water_col]).reset_index(drop=True)
        # Calculate the actual time step from the data
        dt_days = df[time_col].diff().dt.total_seconds().median() / 86400

    # --- FFT CALCULATIONS (Common for both paths) ---
    y = df[water_col].values
    y_det = signal.detrend(y)
    n = len(y_det)
    
    yf = np.fft.fft(y_det)
    freq = np.fft.fftfreq(n, d=dt_days)
    
    amplitudes = np.abs(yf) / (n / 2)
    pos_mask = freq > 0
    freq_pos = freq[pos_mask]
    amp_pos = amplitudes[pos_mask]

    # Draw plots
    _draw_spectrum_plots(freq_pos, amp_pos, file_name, mode_title, months_to_analyze)
