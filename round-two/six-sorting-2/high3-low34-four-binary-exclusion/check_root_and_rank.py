"""Small exact controls for ordinary structural statements; no j5 exclusion.

Credited literal scalar arithmetic, all original Q Boolean inputs and every
four-binary representative through every freed LOW head/balanced tail.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent
path=ROOT/'numeric.py'
if hashlib.sha256(path.read_bytes()).hexdigest()!='83c79d716581cdc8f947a21d9120a001624d8179fab8935817e28326f10bb041':
    raise ValueError('credited literal scalar arithmetic changed')
spec=importlib.util.spec_from_file_location('credited_literal_scalar',path)
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
D=(4,5,6,7,9,10)
UNITS=((4,1284,6160),(5,14,6176),(6,134,6208),(7,7,6272),(9,769,6656),(10,259,7168))


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    start=time.monotonic()
    cover=json.loads((ROOT/'generated/cover-produced.json').read_text())['mathematical']
    n.need(n.digest(cover)=='f9b99ef13250aef100e07aa37ce5d9aa6495bb5e59d2099b800216bd669ba523','entire checked cover changed')
    Q=cover['literal_prefix'];values=[n.bool_word(x,Q) for x in range(8192)]
    n.need(all(n.bool_word(x,Q)==y==6144+(1<<q) for q,x,y in UNITS),'literal six Q-unit controls fail')
    # A five-binary forest makes the maximum over D at port10. The
    # following identity shows that this port already has correct rank.
    rank=[int(any(y>>q&1 for q in D)) for y in values]
    n.need(rank==[int(x.bit_count()>=3) for x in range(8192)],'max DEAD is not actual rank10')
    entries=[];controls=0
    for c in cover['whole_Q_function_classes']:
        word=c['shortest_word'];forest=cover['all2700_binary_forests'][c['representative_forest_id']]
        roots={leaf:r for r,leaves in forest['components'] for leaf in leaves}
        expected=[6144+(1<<roots[q]) for q,x,y in UNITS]
        n.need([n.bool_word(y,word) for q,x,y in UNITS]==expected,'whole Q-prefix unit/root map differs')
        live=set(roots.values());freed=set(D)-live
        for q in sorted(freed):
            a,b,c0,d=sorted((1,2,3,min(8,q)))
            for u,v in (((a,b),(c0,d)),((a,c0),(b,d)),((a,d),(b,c0))):
                extension=word+[sorted((8,q)),list(u),list(v),sorted((min(u),min(v)))]
                actual=[n.bool_word(y,extension) for z,x,y in UNITS]
                n.need(actual==expected,'freed LOW head/balanced tail changes the rooted partition')
                controls+=len(actual)
        entries.append([forest['id'],[[q,roots[q]] for q in D],expected])
    math={'literal_prefix':Q,'six_original_unit_preimages':[list(x) for x in UNITS],
          'all8192_Q_outputs_sha256':n.digest(values),'all8192_DEAD_max_rank10_bits_sha256':n.digest(rank),
          'five_binary_final_root10_is_already_correct_sorted_rank':True,
          'all6400_freed_head_tail_root_controls_sha256':n.digest(entries),
          'all76800_six_unit_head_tail_checks':controls,
          'five_binary_specified_route_size44_G_length_ceiling':44-(28+5+1+3),
          'five_binary_exclusion':False,'global44_exclusion':False}
    n.need(controls==460800 and math['five_binary_specified_route_size44_G_length_ceiling']==7,
           'finite structural control coverage/budget differs')
    out={'agent':'six-sorting-2','role':'researcher','status':'COMPLETE_SMALL_ORDINARY_STRUCTURAL_CONTROLS_NOT_A_FIVE_BINARY_EXCLUSION',
         'mathematical':math,'whole_math_sha256':n.digest(math),'seconds':time.monotonic()-start,
         'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(out,separators=(',',':'))+'\n');print(json.dumps({k:v for k,v in out.items() if k!='mathematical'}))


if __name__=='__main__':main()
