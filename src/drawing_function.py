import matplotlib.pyplot as plt

def _draw_spectrum_plots(freq_pos, amp_pos, file_name, mode_title, months):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Top plot: Full Spectrum
    ax1.plot(freq_pos, amp_pos, color='royalblue', linewidth=1.2)
    ax1.set_xlim(0, 5)
    ax1.set_title(f"Full Spectrum ({mode_title}) - {file_name} [{months} months]", fontsize=14)
    ax1.set_ylabel("Amplitude [m]", fontsize=12)
    ax1.grid(True, linestyle=':', alpha=0.7)
    
    # Bottom plot: Diagnostic Zoom
    ax2.plot(freq_pos, amp_pos, color='firebrick', linewidth=1.5)
    ax2.set_xlim(0.5, 3.0)
    ax2.set_yscale('log')
    ax2.set_title("DIAGNOSTIC ZOOM (Logarithmic Scale)", fontsize=12)
    ax2.set_xlabel("Frequency [cycles / day]", fontsize=12)
    ax2.set_ylabel("Amplitude [m] - log10", fontsize=12)
    ax2.grid(True, which="both", linestyle=':', alpha=0.5)
    
    # Reference lines for key tidal constituents
    ax2.axvline(x=1.0, color='orange', linestyle='--', linewidth=2, label='Diurnal (e.g., K1, O1)')
    ax2.axvline(x=1.932, color='green', linestyle='--', linewidth=2, label='M2 (Lunar semi-diurnal)')
    ax2.axvline(x=2.0, color='red', linestyle=':', linewidth=2, label='S2 (Solar semi-diurnal)')
    
    # Lower limit to prevent scale distortion from near-zero values
    ax2.set_ylim(max(amp_pos.min(), 1e-5), amp_pos.max() * 1.5)
    ax2.legend(loc='lower right', framealpha=0.9)
    
    plt.tight_layout()
    plt.show()