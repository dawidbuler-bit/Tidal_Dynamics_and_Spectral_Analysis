from pathlib import Path
import pandas as pd 
import matplotlib.pyplot as plt

def analyze_tides(file_path, station_name):
    """
    Function implementing the baseline algorithm:
    Divides the data in half and finds the highest point in each segment.
    """
    file_path = Path(file_path)
    try:
        data = pd.read_csv(file_path, sep=';', na_values='-')
        data['Date + Time'] = pd.to_datetime(data['Date + Time'], format='mixed')

        half_point = len(data) // 2
        part_1 = data.iloc[:half_point]
        part_2 = data.iloc[half_point:]

        idx1 = part_1['Verified (m)'].idxmax()
        idx2 = part_2['Verified (m)'].idxmax()

        val1 = data.loc[idx1, 'Verified (m)']
        val2 = data.loc[idx2, 'Verified (m)']
        date1 = data.loc[idx1, 'Date + Time']
        date2 = data.loc[idx2, 'Date + Time']

        # Assuming the higher maximum is always the New Moon
        if val1 > val2:
            label1, label2 = "New Moon", "Full Moon"
        else:
            label1, label2 = "Full Moon", "New Moon"

        plt.figure(figsize=(15, 7))

        plt.plot(data['Date + Time'], data['Predicted (m)'], color='blue', alpha=0.3, label='Predicted')
        plt.plot(data['Date + Time'], data['Verified (m)'], color='green', label='Verified', linewidth=1.5)

        if label1 == "New Moon":
            plt.scatter(date1, val1, color='black', s=150, zorder=5, label='New Moon')
            plt.scatter(date2, val2, color='white', edgecolors='black', s=150, linewidth=2, zorder=5, label='Full Moon')
        else:
            plt.scatter(date1, val1, color='white', edgecolors='black', s=150, linewidth=2, zorder=5, label='Full Moon')
            plt.scatter(date2, val2, color='black', s=150, zorder=5, label='New Moon')

        plt.xticks(data['Date + Time'][::200], rotation=45)
        plt.title(f"Water Level - {station_name} - Basic Analysis (idxmax)")
        plt.ylabel("Height (m)")
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.tight_layout()
        plt.show()

        print(f"[{station_name}] Detected: {date1} ({label1}) and {date2} ({label2})")

    except FileNotFoundError:
        print(f"ERROR: Data file not found at path: {file_path}")
