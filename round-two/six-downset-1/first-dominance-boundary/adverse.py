"""Designated mathematical and source-before-import damages, never crash-as-proof."""
import argparse
import copy
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import reader  # Standard-library-only until verify_sources and modules.


def bad(name, operation, message):
    try:
        operation()
    except ValueError as exc:
        reader.require(str(exc)==message, 'wrong designated guard: '+name+': '+str(exc))
        return dict(name=name,guard=message,mathematical_rejection=True)
    raise ValueError('damaged mathematics accepted: '+name)


def semantic():
    m = reader.modules(); g=m['geometry']; c=m['counts']; o=m['original']; cr=m['count_reader']
    F=m['common'].F
    output = []
    for name,n,counts,message in (
        ('large-target-original',11,[4,3,2],'unchanged literal n<=6'),
        ('r5N98',5,[3,2,2,2,2],'unchanged original N80 parent guard BEFORE construction'),
        ('unequal-r4N82',4,[4,3,2,2],'unchanged original N80 parent guard BEFORE construction'),
        ('h11',4,[11,2,2],'unique heavy literal h<=10'),
        ('F8',4,[4,2,2],'qualified total F>=9')):
        output.append(bad(name,lambda n=n,counts=counts:g.preflight(n,counts),message))
    output.append(bad('empty-count-list',lambda:c.scalars(8,[]), 'bounded count inputs before scalar lists'))
    output.append(bad('noncanonical-rational',lambda:m['common'].rat('1/01'), 'canonical rational spelling'))
    output.append(bad('negative-original-direction',lambda:m['common'].full_positive_solve(
        [[F(1),F(0)],[F(0),F(-1)]],[[F(1),F(-1)]],False),
        'full original V positive leading minor'))
    seed = g.build(4,[4,3,2])
    packet=copy.deepcopy(seed); packet['family'][0]=1
    output.append(bad('missing-ACTUAL-empty',lambda:o.read(4,[4,3,2],packet),
                      'whole original downset label sequence and ACTUAL empty'))
    packet=copy.deepcopy(seed); packet['rows'][0][0]=str(F(packet['rows'][0][0])+1)
    output.append(bad('corrupted-empty-row',lambda:o.read(4,[4,3,2],packet), 'ALL original constant equations'))
    packet=copy.deepcopy(seed); packet['a'][-1]=str(F(packet['a'][-1])+1)
    output.append(bad('uncentered-repair',lambda:o.read(4,[4,3,2],packet), 'both original repair directions centered'))
    for name,key,change,message in (
        ('gamma-negative','gamma_interval',lambda v:['-1',v[1]],'whole gamma isolation interval'),
        ('gamma-sign','gamma_endpoint_sigma',lambda v:[v[0],v[0]],'both complete gamma endpoint signs'),
        ('FIRST-top','top_FIRST_interval',lambda v:[v[0],v[0]],'whole original FIRST top interval'),
        ('FIRST-boundary','delta_FIRST_interval',lambda v:['1',v[1]],'complete radical FIRST-upper ordering'),
        ('cap-zero-directions','exact_cap_interval',lambda v:['1',v[1]],'whole cap/gamma identity'),
        ('false-original-allocation','large_original_constructed',lambda v:True,'root certificate original-count scope')):
        packet=c.isolate(11,[4,3,2]); packet[key]=change(packet[key])
        output.append(bad(name,lambda:cr.validate(packet,11,[4,3,2]),message))
    return output


def copied_source(target):
    target.mkdir()
    for name in reader.EARLY+('SOURCE.json','EXPECTED.json'):
        shutil.copyfile(HERE/name,target/name)


def source_controls(rebound):
    if rebound:
        cases = (
            ('original-empty-resolvent-score','counts.py',
             'a=9+3*x/(h*d[0])','a=9-F(1,1000)+3*x/(h*d[0])',
             'three new free-level count/original inverse products'),
            ('FIRST-derivative-sign','original.py',
             "physical_derivative=-dot(biK,[dot(row,biK) for row in Gm])",
             "physical_derivative=dot(biK,[dot(row,biK) for row in Gm])",
             'exact count derivative equals ENTIRE physical inverse-square energy'),
            ('original-radical-endpoint','original.py',
             'delta=(mixed/den,-sign*alpha/den)','delta=(mixed/den,sign*alpha/den)',
             'EVERY new original free-level endpoint kernel'),
            ('theta-zero-baseline','counts.py',
             'g0=F(q-1,6*h)+F(3*h,2*q)+F(3*sum(counts),2*q*q)',
             'g0=1+F(q-1,6*h)+F(3*h,2*q)+F(3*sum(counts),2*q*q)',
             'exact useful original Schur baseline'))
    else:
        cases = tuple((name,filename,None,None,'source pin mismatch '+filename) for name,filename in
                      (('counts-source','counts.py'),('proof-source','PROOF.md'),('reader-self','reader.py')))
        cases += (('source-census','SOURCE.json',None,None,'whole early source census'),)
    output = []
    for name,filename,before,after,message in cases:
        with tempfile.TemporaryDirectory(prefix='first-boundary-adverse-') as tmp:
            root=Path(tmp); source=root/'source'; copied_source(source)
            pins=json.loads((source/'SOURCE.json').read_text())
            marker=root/'IMPORTED'
            if not rebound:
                text=(source/'geometry.py').read_text()
                prefix='from pathlib import Path as _MarkerPath\n_MarkerPath('+repr(str(marker))+').write_text("imported")\n'
                (source/'geometry.py').write_text(prefix+text)
                pins['early']['geometry.py']=reader.binding((source/'geometry.py').read_bytes())
            if filename=='SOURCE.json':
                del pins['early']['counts.py']
            else:
                text=(source/filename).read_text()
                if rebound:
                    reader.require(text.count(before)==1, 'unique semantic source laboratory edit')
                    text=text.replace(before,after)
                else:
                    text+='\n# designated source damage\n'
                (source/filename).write_text(text)
                if rebound:
                    pins['early'][filename]=reader.binding((source/filename).read_bytes())
            (source/'SOURCE.json').write_bytes(reader.encoded(pins))
            cmd=[sys.executable,'-I']+(['-O'] if sys.flags.optimize else [])+[str(source/'reader.py'),'--out',str(root/'output.json')]
            result=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
            reader.require(result.returncode==1 and result.stderr.rstrip().endswith('ValueError: '+message),
                           'wrong designated child rejection: '+name+' '+result.stderr[-500:])
            reader.require(not (root/'output.json').exists(), 'damaged child produced success output')
            if not rebound:
                reader.require(not marker.exists(), 'arithmetic imported before source rejection')
            output.append(dict(name=name,guard=message,returncode=result.returncode,
                source_rebound=rebound,source_before_arithmetic_import=not rebound,
                mathematical_rejection=rebound))
    return output


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=('semantic','source','rebound'),required=True)
    parser.add_argument('--out',type=Path,required=True); args=parser.parse_args()
    reader.fresh_output(args.out)
    def expire(_signal,_frame):
        raise TimeoutError('unchanged60s; timeout is never a designated rejection')
    signal.signal(signal.SIGALRM,expire);signal.alarm(60);start=time.monotonic()
    reader.verify_sources()
    records=semantic() if args.phase=='semantic' else source_controls(args.phase=='rebound')
    raw=reader.encoded(dict(agent='six-downset-1',role='researcher',phase=args.phase,
                           status='DESIGNATED FIRST-BOUNDARY REJECTIONS',records=records))
    reader.require(len(raw)<=reader.MAX_BYTES,'unchanged32MiB');args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_bytes(raw);reader.barrier();signal.alarm(0)
    print(json.dumps(dict(status='DESIGNATED FIRST-BOUNDARY REJECTIONS COMPLETE',
        phase=args.phase,rejections=len(records),whole=reader.binding(raw),
        seconds=time.monotonic()-start,peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))


if __name__=='__main__':
    main()
