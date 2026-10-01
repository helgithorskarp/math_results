"""Exact conditional single-three nine-Q branch exclusion; see PROOF.md.
Standard library only. All imports are prior PUBLIC hash-guarded source.
Transient partitions regenerate with --export-partitions; never publish them.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
import contact,noncontact
ROOT=Path(__file__).resolve().parent

def serialized(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()

def dependencies():
    record=json.loads((ROOT/'DEPENDENCIES.json').read_text())
    for name,meta in record['files'].items():
        data=(ROOT.parent/name).read_bytes()
        if len(data)!=meta['bytes'] or hashlib.sha256(data).hexdigest()!=meta['sha256']:
            raise RuntimeError('Prior PUBLIC dependency changed: '+name)
    return {name:meta['sha256'] for name,meta in sorted(record['files'].items())}

def run():
    hashes=dependencies()
    collar=ROOT.parent/'tammes15_nine_quad_single_three_fan_reduction'
    result=subprocess.run([sys.executable,'-B',str(collar/'check.py')],capture_output=True,timeout=45)
    if result.returncode or result.stdout!=(collar/'EXPECTED.json').read_bytes():
        raise RuntimeError('Imported7912 metric collar replay differs')
    c,ct=contact.run();n,nt=noncontact.run()
    trace={'contact':ct,'noncontact':nt,'noncontact_terminal_obstructions':n['terminal_obstructions']}
    encoded=serialized(trace)
    summary={'agent':'six-tammes-1','role':'researcher',
             'status':'AUTHOR_CHECKED_EXACT_CONDITIONAL_SINGLE_THREE_NINE_Q_EXCLUSION',
             'excluded_profile':[1,5,0],
             'remaining_r1_profiles_using_prior8250':[],
             'beta_count_profiles_by_r':[0,12,11],
             'contact':c,'noncontact':n,'prior_public_dependency_sha256':hashes,
             'imported7912_collar_replayed_exactly':True,
             'combined_trace_bytes':len(encoded),
             'combined_trace_sha256':hashlib.sha256(encoded).hexdigest(),
             'contact_trace_sha256':hashlib.sha256(serialized(ct)).hexdigest(),
             'noncontact_trace_sha256':hashlib.sha256(serialized(nt)).hexdigest(),
             'scope':'Actual15/completeconnecteddegree3..5/simpleconvexhemisphericalcellularTQ/nineQ/unique3/open1/2<c<3/5. Written bridges unformalized; independent mathematical review pending; global bounds unchanged.'}
    return summary,encoded

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--export-partitions',type=Path)
    args=parser.parse_args()
    result,data=run()
    expected=json.loads((ROOT/'EXPECTED.json').read_text())
    if json.loads(serialized(result))!=expected:
        raise RuntimeError('Result differs from EXPECTED.json')
    if args.export_partitions:args.export_partitions.write_bytes(data)
    print(serialized(result).decode(),end='')
