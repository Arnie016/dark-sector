"""Render stored SIMULATED MODEL CSV; does not rerun the calculation."""
import csv
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt

out = Path(__file__).resolve().parent / 'output'
with (out / 'SIMULATED_phase_scan.csv').open() as stream:
    data = list(csv.DictReader(stream))
a = [float(row['a_radians']) for row in data]
with matplotlib.rc_context({'svg.fonttype': 'none', 'svg.hashsalt': 'N03-v1'}):
    fig, ax = plt.subplots(figsize=(10, 5.8))
    for key, label, style in [
        ('P_fixed_c1', 'Fixed field amplitude; phase averaged', '-'),
        ('P_rayleigh_c1', 'Sampled field amplitudes OR matched Gaussian phase noise', '--'),
        ('P_c0', 'No incoming coherence; phase-only effects invisible', ':')]:
        ax.plot(a, [float(r[key]) for r in data], linewidth=2.5, linestyle=style, label=label)
    ax.set(xlabel='Added phase scale a (radians; dimensionless)', ylabel='Probability of the original + channel',
           xlim=(0,6), ylim=(0.2,1.04), title='SIMULATED MODEL | A pattern depends on what was averaged')
    ax.grid(alpha=0.18)
    ax.legend(frameon=False, loc='upper right', bbox_to_anchor=(1,0.95), fontsize=9)
    fig.text(0.5,0.018,'Ideal two-state system; zero vacuum phase. No measured neutrino events or detector response.',
             ha='center',fontsize=9)
    fig.tight_layout(rect=(0,0.05,1,1))
    fig.savefig(out/'SIMULATED_phase_visibility.svg',metadata={'Date':None})
    fig.savefig(out/'SIMULATED_phase_visibility.png',dpi=250)
    plt.close(fig)
