"""Check bounded ordinal leaves using only the sealed independent geometry."""
import collections,json,sys,time,hashlib
from pathlib import Path
from fractions import Fraction as F
from partition import decode
from frame import scalar_frame,all_points,dot,chart_gap,NecessaryEmpty
from enclosure import Box,SCALE

def predicate(branch,box,literal):
    t,z=Box(*box[:2]),Box(*box[2:]);kind=literal[0]
    if kind=='chart':
        gap=chart_gap(t,z)
        return gap.lo>0,F(gap.lo,SCALE),kind
    try:a=scalar_frame(t,z)
    except NecessaryEmpty:
        return True,None,'independent-necessary-empty'
    except ArithmeticError:return False,None,'arithmetic-unresolved'
    if kind=='empty-necessary-intersection':return False,None,kind
    if kind=='no-real-V':return a['g'].hi<0,F(-a['g'].hi,SCALE),kind
    if kind=='outside-target-g-half':
        if branch[0]!='g-half':raise ValueError('g-half witness outside target')
        return a['g'].lo>SCALE//2,F(a['g'].lo,SCALE)-F(1,2),kind
    try:
        if kind=='W-pair':gap=a['s']-t if literal[2]==10 else dot(a['W'],a['b'][literal[2]],t)-t
        elif kind=='pair':
            points=all_points(a,branch[1],branch[2]);gap=dot(points[literal[1]],points[literal[2]],t)-t
        else:raise ValueError('unrecognized mathematical predicate')
        return gap.lo>0,F(gap.lo,SCALE),kind
    except NecessaryEmpty:return True,None,'independent-necessary-empty'
    except ArithmeticError:return False,None,'arithmetic-unresolved'

def main():
    root=Path(__file__).resolve().parent.parent
    start,stop=map(int,sys.argv[1:3])
    if not 0<=start<stop<=12091 or stop-start>2500:raise ValueError('bounded explicit ordinal range')
    leaves,coverage=decode(root/'author')
    clock=time.monotonic();failures=[];counts=collections.Counter();margins={};digest=hashlib.sha256()
    for ordinal in range(start,stop):
        if time.monotonic()-clock>40:raise RuntimeError('fixed40s logical guard; incomplete')
        idx,branch,box,literal=leaves[ordinal]
        ok,margin,meaning=predicate(branch,box,literal)
        counts[meaning]+=1
        if ok and margin is not None:
            if meaning not in margins or margin<margins[meaning]:margins[meaning]=margin
        if not ok:failures.append(dict(ordinal=ordinal,tree=idx,box=list(map(str,box)),literal=literal,reason=meaning))
        digest.update(json.dumps([ordinal,ok,str(margin),meaning],separators=(',',':')).encode()+b'\n')
    record=dict(range=[start,stop],complete=True,executed=stop-start,failed=len(failures),counts=dict(counts),
                margins={k:str(v) for k,v in margins.items()},records_sha256=digest.hexdigest(),coverage=coverage)
    (root/f'independent-{start}-{stop}.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    (root/f'failures-{start}-{stop}.json').write_text(json.dumps(failures,sort_keys=True,indent=2)+'\n')
    print(json.dumps(record,sort_keys=True))
    if failures:raise ValueError('one or more interval witnesses remain unresolved')

if __name__=='__main__':main()
