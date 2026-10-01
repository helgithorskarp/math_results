"""Literal witness replay of prefix partitions; no adaptive selector."""
from pathlib import Path
from collections import Counter
import hashlib,json,signal,sys,time
import enclosures as m
WITNESSES=[['chart'],['empty-necessary-intersection'],['no-real-V'],['outside-target-g-half']]+[['W-pair',7,j] for j in (1,2,4,8,10,13)]+[['pair',*p] for p in m.PAIRS]
CODES='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSUVWXY'
LOOKUP=dict(zip(CODES,WITNESSES))
def require(ok,message):
    if not ok:raise ValueError(message)
def replay(data):
    require(data['format']==1 and data['lattice_bits']==80,'fixed format and dyadic precision')
    require(data['box']==['14/25','593/1000','-5/2','5/2'],'full fixed parameter rectangle')
    mode=data['mode'];require(mode in ('bad','g-half'),'specified proof target')
    expected={(-1,-1),(1,-1),(1,1)} if mode=='bad' else {(-1,1)}
    actual=[(x['epsilon'],x['eta']) for x in data['trees']]
    require(len(actual)==len(expected) and set(actual)==expected,'every target branch once')
    counts=Counter();maximum=0;leaves=0;nodes=0
    for tree in data['trees']:
        epsilon,eta=tree['epsilon'],tree['eta'];tokens=iter(tree['tree'])
        def walk(td,ti,zd,zi):
            nonlocal maximum,leaves,nodes
            nodes+=1;maximum=max(maximum,td+zd)
            try:code=next(tokens)
            except StopIteration:raise ValueError('truncated partition')
            if code in ('T','Z'):
                require(td+zd<22,'finite permitted subdivision depth')
                if code=='T':walk(td+1,2*ti,zd,zi);walk(td+1,2*ti+1,zd,zi)
                else:walk(td,ti,zd+1,2*zi);walk(td,ti,zd+1,2*zi+1)
                return
            require(code in LOOKUP,'literal leaf instruction')
            expected_witness=LOOKUP[code];t,z=m.box(td,ti,zd,zi)
            actual_witness=m.verify_witness(t,z,epsilon,eta,mode,expected_witness)
            require(actual_witness is True,f'strict stored witness {mode} {(epsilon,eta,td,ti,zd,zi)} {expected_witness} versus {actual_witness}')
            leaves+=1;counts[expected_witness[0]]+=1
        walk(0,0,0,0)
        require(next(tokens,None) is None,'no trailing partition data')
    canonical=json.dumps(data,sort_keys=True,separators=(',',':')).encode()
    return {'mode':mode,'nodes':nodes,'leaves':leaves,'maximum_total_depth':maximum,'witness_counts':dict(sorted(counts.items())),'canonical_plan_sha256':hashlib.sha256(canonical).hexdigest(),'full_closed_rectangle_covered':True,'literal_strict_witnesses_verified':True}
if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda s,f:(_ for _ in ()).throw(TimeoutError('160-second witness replay guard')))
    signal.alarm(160)
    modes=sys.argv[1:] or ['bad','g-half']
    print(json.dumps([replay(json.loads((Path(__file__).resolve().parent/('PLAN-'+mode+'.json')).read_text())) for mode in modes],indent=2))
