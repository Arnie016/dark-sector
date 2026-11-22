#!/usr/bin/env python3
"""Run four existing research analyses in a temporary workspace and check key outputs."""
import argparse, json, math, os, shutil, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--mergers',type=Path,required=True)
p.add_argument('--radio',type=Path,required=True)
p.add_argument('--chandra',type=Path,required=True)
p.add_argument('--catalog',type=Path,required=True)
a=p.parse_args()
for label,path in vars(a).items():
 if not path.is_file():raise SystemExit(f'Missing {label} input: {path}')
inputs={label:path.resolve() for label,path in vars(a).items()}
dirs=['three-hundred-radio-benchmark','psz2-centroid-shift','psz2-radio-region-sensitivity','psz2-multiwavelength','collision-time-quantization','pericenter-time-distance-association']
def close(actual,expected,tol):
 if not math.isfinite(actual) or abs(actual-expected)>tol:raise AssertionError(f'{actual} differs from {expected} beyond {tol}')
with tempfile.TemporaryDirectory(prefix='merger-paper-replay-') as td:
 base=Path(td)
 for d in dirs:shutil.copytree(ROOT/d,base/d)
 env=os.environ.copy();env['MPLBACKEND']='Agg';env['MPLCONFIGDIR']=str(base/'mpl-config')
 jobs=[('three-hundred-radio-benchmark',[]),('psz2-centroid-shift',[inputs['chandra']]),('psz2-radio-region-sensitivity',[inputs['radio'],inputs['catalog']]),('collision-time-quantization',[inputs['mergers']])]
 for folder,args in jobs:
  result=subprocess.run([sys.executable,str(base/folder/'analyze.py'),*[str(x) for x in args]],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  if result.returncode:raise SystemExit(f'{folder} failed:\n{result.stderr[-4000:]}')
  print(f'PASS {folder}')
 s=json.loads((base/'three-hundred-radio-benchmark'/'summary.json').read_text());close(s['curves']['clusters/R200']['at_1_0_gyr'],4102.946611567108,1e-7);close(s['curves']['clusters/2R200']['at_1_0_gyr'],8428.12644264615,1e-7)
 s=json.loads((base/'psz2-centroid-shift'/'summary.json').read_text());close(s['shift_from_image'],.06933273393951442,1e-9)
 if s['number_apertures']!=26:raise AssertionError('Unexpected aperture count')
 s=json.loads((base/'psz2-radio-region-sensitivity'/'summary.json').read_text());close(s['pair_delta_kpc_range'][0],42.1633766788414,1e-5);close(s['pair_delta_kpc_range'][1],63.61766309496817,1e-5)
 s=json.loads((base/'collision-time-quantization'/'summary.json').read_text());expected={'1':(1428,1193),'0':(549,16)}
 for k,(n,modal) in expected.items():
  if (s['selected_groups'][k]['events'],s['selected_groups'][k]['modal_time_events'])!=(n,modal):raise AssertionError('Unexpected event counts')
 print('PASS selected numerical outputs; see protocol for scientific limitations')
