"""Serial bounded normal/O/cold readers and designated semantic/source controls."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import reader  # No mathematical module imports.


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    reader.fresh_output(args.out);args.out.mkdir(parents=True)
    reader.verify_sources();observations=[];encodings=[];phases={}
    for lane in ('normal','optimized','cold'):
        reader.barrier()
        with tempfile.TemporaryDirectory(prefix='first-boundary-cold-') as tmp:
            source=HERE
            if lane=='cold':
                source=Path(tmp)/'source';source.mkdir()
                for name in reader.EARLY+('SOURCE.json','EXPECTED.json'):
                    shutil.copyfile(HERE/name,source/name)
            directory=args.out/lane;directory.mkdir()
            for script,phase in (('reader.py',None),('adverse.py','semantic'),
                                 ('adverse.py','rebound'),('adverse.py','source')):
                stem='mathematics' if phase is None else phase
                cmd=[sys.executable,'-I']+(['-O'] if lane=='optimized' else [])+[str(source/script),
                     '--out',str((directory/(stem+'.json')).resolve())]
                if phase:cmd+=['--phase',phase]
                else:cmd+=['--whole-out',str((directory/'whole-private.json').resolve())]
                start=time.monotonic()
                result=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
                observation=dict(lane=lane,script=script,phase=phase,command=cmd,
                    returncode=result.returncode,wall_seconds=time.monotonic()-start,
                    stdout=result.stdout,stderr=result.stderr)
                observations.append(observation)
                (args.out/'CHILDREN.json').write_text(json.dumps(observations,indent=2)+'\n')
                reader.require(result.returncode==0,'incomplete designated child '+lane+' '+stem+' '+result.stderr[-800:])
                if phase:
                    phases.setdefault(phase,[]).append((directory/(stem+'.json')).read_bytes())
            encodings.append(((directory/'mathematics.json').read_bytes(),
                              (directory/'whole-private.json').read_bytes()))
    reader.require(encodings[0]==encodings[1]==encodings[2],
                   'ENTIRE normal/O/cold compact AND full original record equality')
    for phase,values in phases.items():
        reader.require(values[0]==values[1]==values[2], 'ENTIRE normal/O/cold rejection record equality '+phase)
    result=dict(agent='six-downset-1',role='researcher',status='ALL NEW SOURCE DELIVERY GATES COMPLETE',
        actual_children=len(observations),actual_exit_codes=[o['returncode'] for o in observations],
        compact=reader.binding(encodings[0][0]),whole=reader.binding(encodings[0][1]),
        phases={p:reader.binding(v[0]) for p,v in phases.items()},
        whole_bytes_compared_before_digest=True,normal_optimized_cold_equal=True,
        observations_file='CHILDREN.json',source_commit=None,graph_ref=None,
        formalized=False,independent_review=False)
    (args.out/'GATES.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    main()
