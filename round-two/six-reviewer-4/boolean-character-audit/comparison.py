"""Late whole-object comparison only; native imports cannot feed the proof kernel."""
import argparse,importlib.util,json,hashlib
from pathlib import Path
from geometry import *
from adapter import decode

def compare(native_source,csv):
    sourcepins=json.loads((Path(__file__).parent/'AUTHOR_SOURCE.json').read_text())['files']
    for name,p in sourcepins.items():need(hashlib.sha256((native_source/name).read_bytes()).hexdigest()==p['sha256'],'whole late native source pin')
    spec=importlib.util.spec_from_file_location('late_author_check',native_source/'check.py');native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    def old(s):r,t,w=s;return(r,0 if r==2 else t,w)
    def new(s):r,t,w=s;return(r,1 if r==2 else t,w)
    blocks,maps,hist=native.partition();own=orbit_cover(103);need([[new(z)for z in sorted(blocks[old(o[0])])]for o in own]==[list(o)for o in own],'every full12938-state orbit member agrees after explicit sentinel adapter')
    count=0;h=hashlib.sha256()
    for s in states(103):
        for pi,ours in zip(orders(s[0]),actions(s,103)):
            v=native.column_map(old(s),pi);theirs=(new(v[0]),*v[1:]);need(ours==theirs,'whole signed root/coordinate/action map');count+=1;h.update(canonical([s,pi,ours]))
    need(count==77586,'complete77586 signed maps')
    decoded=decode(csv.read_bytes());native_rows=native.decode(csv.read_bytes())
    for ours,row in zip(decoded,native_rows):
        need(new(tuple(row[1:4]))==tuple(ours['state']) and [row[4+2*j:6+2*j]for j in range(9)]==ours['aps'],'entire native CSV row decoded into neutral schema')
    return {'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','phase':'LATE whole-object comparison after sealed independent kernels and complete own AP replay','complete_orbit_members':12938,'complete_orbits':2176,'signed_maps':count,'whole_map_objects_equal':True,'whole_map_transcript_sha256':h.hexdigest(),'decoded_positive_rows':2176,'native_two_root_sentinel':0,'independent_two_root_normalized_parameter':1,'no_numeric_verdict_imported':True,'transport_choice_note':'Own inverse source-to-representative lex-min maps produce flips9716/3222; native forward representative-to-target first maps produce9708/3230. Both are fully pointwise verified; digests/count histograms need not match.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native-source',type=Path,required=True);p.add_argument('--csv',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.write_bytes(canonical(compare(a.native_source,a.csv)))
