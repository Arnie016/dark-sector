from pathlib import Path
import json,hashlib,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent;path=root/'GWTC-5.0-events.json';sha='5a15bccb5e1764e67feece022711f740a7e616b8c6b866c08b114741c846fb70';assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
events=json.loads(path.read_text())['events'];assert len(events)==161 and len({k.rsplit('-v',1)[0] for k in events})==161
r=list(events.values());mass=np.array([x['mass_1_source'] is not None for x in r]);snr=np.array([x['network_matched_filter_snr'] for x in r]);far=np.array([x['far'] for x in r]);assert np.isfinite(snr).all() and np.isfinite(far).all()
out={'input_sha256':sha,'events_in_api_snapshot':len(r),'source_mass_available':int(sum(mass)),'source_mass_unavailable':int(sum(~mass)),'far_lt_one':{'n':int(sum(far<1)),'source_mass_available':int(sum((far<1)&mass))},'far_gte_one':{'n':int(sum(far>=1)),'source_mass_available':int(sum((far>=1)&mass))},'median_snr_mass_available':float(np.median(snr[mass])),'median_snr_mass_unavailable':float(np.median(snr[~mass])),'no_mass_far_lt_one':[k for k,x in events.items() if x['mass_1_source'] is None and x['far']<1],'caveat':'Descriptive missingness in a public API snapshot, not an independent rate, physical inference, causal effect or a defect claim.'}
(root/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(8.5,4.6),layout='constrained'); bins=np.arange(7,25,1)
for mask,label,col in [(mass,'Source mass available','#34758b'),(~mass,'Source mass missing','#d88d4c')]:ax.hist(snr[mask],bins=bins,histtype='step',lw=2,label=label,color=col)
ax.set(xlabel='Reported network signal-to-noise ratio',ylabel='Number of catalog entries',title='GWTC-5.0 metadata: mass availability and SNR');ax.text(.98,.98,'Shown range: 7–24; higher values omitted',ha='right',va='top',transform=ax.transAxes,fontsize=9);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.legend(frameon=False);fig.savefig(root/'snr-availability.png',dpi=170);plt.close(fig);print(json.dumps(out,indent=2))
