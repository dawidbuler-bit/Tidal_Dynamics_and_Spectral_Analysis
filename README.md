# Tidal Dynamics & Spectral Analysis: A Comparative Study of Spring Tides

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Manipulation-150458.svg)
![SciPy](https://img.shields.io/badge/SciPy-Signal_Processing-8CAAE6.svg)

## 📊 Project Overview

This project investigates sea level variability across three distinct North American tidal regimes: **Alaska (Juneau)**, **Los Angeles**, and **Texas (Galveston)**. The primary objective is to develop and evaluate algorithms for the automatic identification of spring tide events from raw oceanographic time-series data. 

The study documents a comprehensive analytical evolution—from basic time-domain heuristic peak detection to advanced frequency-domain analysis using Digital Signal Processing (DSP). It definitively demonstrates that while oceanographic data can reliably isolate spring tide events in macro-tidal environments, it cannot uniquely distinguish between New Moon and Full Moon phases without external astronomical calibration.

## 🔬 Key Analytical Findings

1. **The Boundary of Time-Domain Heuristics:** Time-series algorithms successfully track astronomical alignments in high-energy, semi-diurnal settings (Alaska, LA). However, in micro-tidal, diurnal zones (Galveston), they fail structurally due to the fundamental multi-component nature of tidal forcing and meteorological dominance.

2. **Spectral Resolving Power:** Applying short-term (1-month) Fast Fourier Transforms (FFT) introduces severe spectral leakage. Expanding the temporal window to a full year ($T = 365$ days), combined with Hann windowing, provides the required mathematical resolution ($\Delta f \approx 0.00274$ cycles/day) to cleanly separate closely aligned physical components (e.g., $M_2$ vs. $S_2$).

## 🛠 Methodology

* **Data Engineering:** Automated ingestion and auditing of raw NOAA datasets, implementing 3rd-order spline interpolation to satisfy strict constant-time-step DSP requirements.

* **Time-Domain Analysis (Method I & II):** Development of a baseline extremum-search model, followed by a dynamically calibrated algorithm utilizing prominence filtering and an astronomical $14.7$-day interval constraint.

* **Frequency-Domain Analysis (DSP):** Implementation of detrended, windowed (Hann) FFT to isolate individual harmonic drivers ($M_2$, $S_2$, $K_1$, $O_1$) and compute regional energy distributions.

## 📈 Astronomical Validation

The time-domain tracking model was validated against true astronomical ephemeris data for January 2026. The results confirm sub-two-day precision in semi-diurnal regimes and complete divergence in the meteorologically driven Galveston basin.

| Station | Boundary Event | Actual Moon Date | Detected Peak Date | Absolute Error |
| :--- | :--- | :--- | :--- | :--- |
| **Juneau, Alaska** | Full Moon | 2026-01-03 | 2026-01-05 | 2 days |
| **Juneau, Alaska** | New Moon | 2026-01-18 | 2026-01-20 | 2 days |
| **Los Angeles, CA** | Full Moon | 2026-01-03 | 2026-01-03 | 0 days |
| **Los Angeles, CA** | New Moon | 2026-01-18 | 2026-01-19 | 1 day |
| **Galveston, TX** | Full Moon | 2026-01-03 | *Not Found* | N/A (Algorithmic Failure) |

## ⚠️ Limitations of the Study
To maintain scientific transparency, the operational boundaries of this analysis are explicitly acknowledged:

* **Spatial Constraints:** Evaluated three North American stations; findings are regional, not universally generalized.

* **Data Origin:** Relies exclusively on the NOAA tide gauge network.

* **Meteorological Tensors:** The dataset lacked direct barometric pressure and wind vectors, preventing the explicit mathematical mapping of the weather interference observed in Galveston.

* **Astronomic Independence:** The pipeline operates independently of real-time astronomical ephemeris libraries, requiring a single manual parameter seed (`first_phase`) for path labeling.

## 🔮 Future Work: Machine Learning Integration
Because Fourier transforms function as descriptive tools rather than forecasting architectures, the next project phase transitions to **predictive forecasting**:

* **Deep Learning Architectures:** Developing Multi-Layer Perceptrons (MLPs) and Recurrent Neural Networks (LSTMs) using `PyTorch` to process non-linear hydrodynamic variations.

* **Multivariate Feature Engineering:** Integrating atmospheric pressure vectors and wind anomalies to dynamically correct weather-driven distortions, specifically targeting the "Galveston Anomaly".

## 📁 Repository Structure

```text
├── data/
│   ├── processed/                       # Cleaned, interpolated, and standardized datasets
│   └── raw/                             # Original NOAA datasets (.csv)
├── notebooks/               
│   ├── images/                          # Plots and diagnostic graphs
│   └── sprawozdanie.ipynb               # Main project notebook
├── requirements/
│   └── requirements.txt                 # Python dependencies
├── src/                                 # Reusable analytical and visualization functions
│   ├── analyze_tides.py                 # Baseline time-domain peak detection (Method I)
│   ├── analyze_tides_pro.py             # Advanced interval-based detection (Method II)
│   ├── data_prep.py                     # Automated NOAA data auditing and cleaning
│   ├── drawing_function.py              # Spectral analysis plotting module
│   ├── plot_fourier_universal.py        # Naive FFT implementation (unwindowed)
│   └── plot_fourier_universal_Hann.py   # Advanced FFT implementation with Hann window
├── .gitignore                           # Ignores cache and local environment files
└── README.md                            # Project documentation
```


## 🚀 Setup

### In Bash:

```bash
# Clone the repository
git clone [https://github.com/dawidbuler-bit/Tidal_Dynamics_and_Spectral_Analysis.git](https://github.com/dawidbuler-bit/Tidal_Dynamics_and_Spectral_Analysis.git)

cd tidal-analysis-fft

# Install the required data science packages
pip install -r requirements/requirements.txt
```


