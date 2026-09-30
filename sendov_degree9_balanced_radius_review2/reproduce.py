"""Pin native inputs, replay sequentially, compare every coefficient privately.

The independent audit is a separate process with no author imports.
The native-export subprocess is solely a disclosed comparison adapter.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def require(ok, reason):
    if not ok:
        raise ArithmeticError(reason)


def native_export(source, output):
    sys.path.insert(0, str(source))
    import verify as native
    import algebra as a
    from itertools import product
    summary=native.build_summary()
    hs, oc=a.origin_coefficients()
    norm=a.chebyshev_norm(oc)
    raw=a.add(a.add(norm,a.scale(a.ONE,-3)),a.scale(a.A,2))
    q=a.divide_delta(a.coupled_axis(a.coupled_axis(raw,1),2))
    delta=q
    for axis in range(3):delta=a.affine_axis(delta,axis,Fraction(1),Fraction(0))
    values=[]
    for lo,hi in native.BOXES:
        ds,beta=a.bernstein(a.affine_axis(q,0,lo,hi))
        indices=product(*(range(n+1) for n in ds))
        values.append([str(beta.get(m,Fraction(0))) for m in indices])
    data={'norm':[[list(m),str(v)] for m,v in sorted(norm.items())],
          'quotient_delta':[[list(m),str(v)] for m,v in sorted(delta.items())],
          'origin_bernstein':values,
          'polar':summary['polar']['bernstein_coefficients']}
    output.write_text(json.dumps(data,separators=(',',':'))+'\n')


def run(command):
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',
             MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    process=subprocess.run(command,env=env,capture_output=True,text=True,timeout=55)
    require(process.returncode==0, process.stderr+'\n'+process.stdout)
    return process.stdout


def main():
    here=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser()
    parser.add_argument('--input-dir',type=Path,
                        default=here.parent/'sendov_degree9_balanced_radius_origin_gap')
    parser.add_argument('--native-export',type=Path,help=argparse.SUPPRESS)
    args=parser.parse_args()
    source=args.input_dir.resolve()
    manifest=json.loads((here/'INPUT.json').read_text())
    for name,digest in manifest['sha256'].items():
        require(sha256((source/name).read_bytes()).hexdigest()==digest,
                'native input pin mismatch: '+name)
    if args.native_export:
        native_export(source,args.native_export)
        return
    python=[sys.executable,'-I','-B']+(['-O'] if not __debug__ else [])
    with tempfile.TemporaryDirectory(prefix='sendov-radius-review2-') as temporary:
        independent=Path(temporary)/'independent.json'
        author=Path(temporary)/'native.json'
        independent_stdout=run(python+[str(here/'audit.py'),'--export',str(independent)])
        summary=json.loads(independent_stdout)
        run(python+[str(source/'verify.py')])
        run(python+[str(here/'reproduce.py'),'--input-dir',str(source),
                    '--native-export',str(author)])
        ours=json.loads(independent.read_text());theirs=json.loads(author.read_text())
        for key in ['norm','quotient_delta','origin_bernstein']:
            require(ours[key]==theirs[key], 'complete native comparison: '+key)
        require(summary['polar']['coefficients']==theirs['polar'], 'seven polar entries')
        require(sum(map(len,ours['origin_bernstein']))+len(theirs['polar'])==6487,
                'complete coefficient inventory')
        expected=json.loads((source/'expected.json').read_text())
        ours_witness=summary['radial_obstruction'];native_witness=expected['monotonicity_obstruction']
        for key,other in [('slacks','strict_disk_slacks'),('origin_values','normalized_origin_squared_unit_radial'),
                          ('difference','radial_minus_unit'),('polar_values','polar_squared_unit_radial')]:
            require(ours_witness[key]==native_witness[other], 'exact witness comparison: '+key)
    print('PASS: independent norm, delta quotient and all 6487 individual rational coefficients match.')
    print('60 direct definition checks; 5 malformed controls; exact radial obstruction.')
    print('Proved radius-difference width (1-a)/20000, 50 times the original, with gap (1-a)/8.')
    print('Unrestricted unequal radii and the general first-power endpoint remain open here.')


if __name__=='__main__':main()
