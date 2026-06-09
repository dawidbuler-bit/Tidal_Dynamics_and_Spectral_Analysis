import pandas as pd
import numpy as np
from scipy import signal
import importlib.util
import sys
from pathlib import Path

if (Path.cwd() / "src").exists():
    ROOT_DIR = Path.cwd()
else:
    ROOT_DIR = Path.cwd().parent

sys.path.append(str(ROOT_DIR))

drawing_script_path = ROOT_DIR / "src" / "drawing_function.py"
_draw_spectrum_plots = None

if drawing_script_path.exists():
    try:
        spec = importlib.util.spec_from_file_location("drawing_function", str(drawing_script_path))
        drawing_module = importlib.util.module_from_spec(spec)
        sys.modules["drawing_function"] = drawing_module
        spec.loader.exec_module(drawing_module)
        _draw_spectrum_plots = drawing_module._draw_spectrum_plots
        print("SUCCESS: Visualization script loaded successfully.")
    except Exception as e:
        print(f"WARNING: Visualization script import failed: {e}")

def plot_fourier_universal_Hann(file_path, months_to_analyze=1, freq_minutes=6, time_col='Date + Time', water_col='Verified (m)', delimiter=';'):
    file_path = Path(file_path)
    file_name = file_path.name
    print(f"\n--- DYNAMIC FFT | Range: {months_to_analyze} months | Step: {freq_minutes} min | File: {file_name} ---")
    
    try:
        df = pd.read_csv(file_path, delimiter=delimiter)
        df[time_col] = pd.to_datetime(df[time_col], dayfirst=True, format='mixed')
        
        start_date = df[time_col].min()
        end_date = start_date + pd.DateOffset(months=months_to_analyze)
        df = df[(df[time_col] >= start_date) & (df[time_col] < end_date)].copy()
        df = df.sort_values(by=time_col).drop_duplicates(subset=[time_col])
        
        missing_count = df[water_col].isna().sum()
        
        if missing_count > 0:
            print(f"   Missing values detected ({missing_count}). Applied 3rd-order spline interpolation.")
            mode_title = "WITH INTERPOLATION"
            df = df.set_index(time_col)
            full_time_grid = pd.date_range(start=df.index.min(), end=df.index.max(), freq=f"{freq_minutes}min")
            df = df.reindex(full_time_grid)
            df[water_col] = df[water_col].interpolate(method='spline', order=3, limit_direction='both')
            df[water_col] = df[water_col].interpolate(method='linear').fillna(0)
            df = df.reset_index().rename(columns={'index': time_col})
            dt_days = freq_minutes / 1440.0
        else:
            print("   Data 100% complete. Utilizing raw measurements.")
            mode_title = "RAW DATA"
            df = df.dropna(subset=[water_col]).reset_index(drop=True)
            dt_days = df[time_col].diff().dt.total_seconds().median() / 86400.0
            
        # --- FFT CALCULATION WITH WINDOWING ---
        y = df[water_col].values
        y_det = signal.detrend(y)
        n = len(y_det)
        
        # Applying the Hann window to eliminate spectral leakage
        window = np.hanning(n)
        yf = np.fft.fft(y_det * window)
        
        freq = np.fft.fftfreq(n, d=dt_days)
        
        # The amplitude must be scaled by the Hann window correction factor (~2.0)
        amplitudes = (np.abs(yf) * 2.0) / (n / 2) 
        
        pos_mask = freq > 0
        freq_pos = freq[pos_mask]
        amp_pos = amplitudes[pos_mask]
        
        if _draw_spectrum_plots is not None:
            _draw_spectrum_plots(freq_pos, amp_pos, file_name, mode_title, months_to_analyze)
            
    except FileNotFoundError:
        print(f"!!! ERROR: Expected data file not found: {file_path}")
