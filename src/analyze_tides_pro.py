import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from pathlib import Path

def analyze_tides_pro(file_path, station_name, first_phase="Full Moon"):
    """
    Reads the data, searches for a syzygy pair (offset ~14.7d),
    and generates the validation plot.
    """
    file_path = Path(file_path)
    try:
        data = pd.read_csv(file_path, sep=';', na_values='-')
        data['Date + Time'] = pd.to_datetime(data['Date + Time'], format='mixed')

        time_diff = (data['Date + Time'].iloc[1] - data['Date + Time'].iloc[0]).total_seconds() / 60
        rows_per_day = int(1440 / time_diff)

        peaks, _ = find_peaks(data['Verified (m)'], distance=rows_per_day * 10)
        pot_dates = data.iloc[peaks]['Date + Time'].tolist()
        pot_vals = data.iloc[peaks]['Verified (m)'].tolist()
        pot_idx = peaks.tolist()

        best_pair = None
        max_sum = -999.0

        for i in range(len(pot_dates)):
            for j in range(i + 1, len(pot_dates)):
                t1, t2 = pot_dates[i], pot_dates[j]
                v1, v2 = pot_vals[i], pot_vals[j]
                diff = abs((t2 - t1).total_seconds() / (3600 * 24))
                
                if 13.5 <= diff <= 16.5:
                    if (v1 + v2) > max_sum:
                        max_sum = v1 + v2
                        best_pair = (pot_idx[i], pot_idx[j])

        plt.figure(figsize=(15, 7))
        plt.plot(data['Date + Time'], data['Predicted (m)'], color='blue', alpha=0.15, label='Predicted')
        plt.plot(data['Date + Time'], data['Verified (m)'], color='green', label='Verified', linewidth=1.2)

        if best_pair:
            idx1, idx2 = best_pair
            d1, d2 = data.loc[idx1, 'Date + Time'], data.loc[idx2, 'Date + Time']
            v1, v2 = data.loc[idx1, 'Verified (m)'], data.loc[idx2, 'Verified (m)']
            
            second_phase = "New Moon" if first_phase == "Full Moon" else "Full Moon"
            
            plt.scatter(d1, v1, color='white' if first_phase == "Full Moon" else 'black', 
                        edgecolors='black', s=180, zorder=5, label=first_phase)
            plt.scatter(d2, v2, color='black' if first_phase == "Full Moon" else 'white', 
                        edgecolors='black', s=180, zorder=5, label=second_phase)
            
            print(f"[{station_name}] Determined: {first_phase} ({d1.date()}) and {second_phase} ({d2.date()})")
        else:
            print(f"[{station_name}] ERROR: Valid interval pair not found!")

        # Plot aesthetics
        plt.title(f"Sea Level and Moon Phase Analysis - {station_name}")
        plt.ylabel("Height (m)")
        plt.xticks(data['Date + Time'][::rows_per_day * 2], rotation=45)
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print(f"ERROR: Data file not found at path: {file_path}")