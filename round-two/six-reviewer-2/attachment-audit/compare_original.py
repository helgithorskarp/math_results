"""Late, separate adapter to all frozen original fixture matrix hashes.

Read only after the reviewer core/whole record/proof were sealed. Imports
reviewer code only; never imports or executes the target's Python modules.
The unchanged target native normal/O runs are a separate corroboration.
"""
import argparse,json,signal
from pathlib import Path
from audit import cube,singles,uniform_two,build,census,stars
from linear import need,digest,canonical

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('60s comparison guard')));signal.alarm(60)
    p=argparse.ArgumentParser();p.add_argument('original_results');p.add_argument('--expected');a=p.parse_args()
    original=json.loads(Path(a.original_results).read_text());rows=[];positions=0;whole=0
    for fixture in original['fixtures']:
        inputs=[];native_family=list(range(1<<fixture['n']));offset=fixture['n'];input_hashes=[]
        for spec in fixture['inputs']:
            generators={'cube':cube,'singletons':singles,'uniform_rank_two':uniform_two}
            need(spec['kind'] in generators,'known published input baseline')
            data=generators[spec['kind']](spec['parameter']);S,C,t=data
            # Native uniform families sort masks; compare full private cores too.
            native_S=sorted(S) if spec['kind']=='uniform_rank_two' else S
            ix=[S[1:].index(T) for T in native_S[1:]]
            native_C=[[C[i][j] for j in ix] for i in ix]
            need(digest(native_C)==spec['core_sha256'],'every original private core byte encoding')
            need(len(S)==spec['N'] and t==spec['s'],'native input exact scope')
            inputs.append((spec['mark'],data));input_hashes.append(digest(native_C))
            for T in native_S[1:]:native_family.extend([T<<offset,(T<<offset)|(1<<spec['mark'])])
            offset+=max(S).bit_length()
        r,S,M,s,K,labels,C=build(fixture['n'],inputs);lookup={T:i for i,T in enumerate(S)}
        need(set(native_family)==set(S),'all original physical sets')
        ix=[lookup[T] for T in native_family];CP=[[C[i-1][j-1] for j in ix[1:]] for i in ix[1:]]
        MP=[[M[i][j] for j in ix] for i in ix]
        need(digest(CP)==fixture['core_sha256'],'all original core entries via full matrix encoding')
        need(digest(MP)==fixture['matrix_sha256'],'all original whole entries via full matrix encoding')
        for own,native in [('n','n'),('N','N'),('s','s'),('load','loads'),('k','k'),('strict','strict'),
                           ('core_rank','core_rank'),('lower_rank','lower_rank'),('boundary_nu','equality_input_nullity'),
                           ('empty_energy','actual_empty_energy'),('empty_loop','actual_empty_loop'),
                           ('ordered_core_positions','ordered_core_positions')]:
            need(canonical(r[own])==fixture[native],'full original mathematical field '+native)
        need(fixture['q']==1<<(fixture['n']-1),'native q')
        positions+=len(C)**2;whole+=len(M)**2
        row={'label':fixture['label'],'N':r['N'],'s':s,'lower_rank':r['lower_rank'],
             'core_sha256':digest(CP),'matrix_sha256':digest(MP),'input_hashes':input_hashes}
        if len(S)<=24:
            cr,winners=census(S);ss=stars(S)
            star_masks=sorted(sum(1<<i for i,T in enumerate(S[1:]) if T&b) for b,t in ss.items() if t==s)
            need(cr['maximum']==s and winners==star_masks,'native complete maximum-family census, including weak boundary')
            row['maximum_family_census']=cr
        rows.append(row)
    # Independent coordinate transport, using rebuilt mixed output twice.
    _,S,M,s,*_=build(3,[(0,cube(2)),(1,cube(1))]);_,other,Q,other_s,*_=build(3,[(2,cube(2)),(0,cube(1))])
    permutation={0:2,1:0,2:1,3:4,4:3,5:5};lookup={T:i for i,T in enumerate(other)}
    relabel=lambda T:sum(1<<permutation[i] for i in range(6) if T>>i&1)
    need(other_s==s and all(M[i][j]==Q[lookup[relabel(T)]][lookup[relabel(U)]]
                          for i,T in enumerate(S) for j,U in enumerate(S)),'native 256-coordinate transport')
    out={'agent':'six-reviewer-2','role':'independent mathematical reviewer','method':'post-seal adapter; reviewer modules only',
         'fixtures':rows,'all_core_positions':positions,'all_whole_positions':whole,
         'coordinate_transport_positions':len(S)**2,'censuses':sum('maximum_family_census' in r for r in rows)}
    if a.expected:need(canonical(out)==json.loads(Path(a.expected).read_text()),'full adapter frozen equality')
    print(json.dumps(canonical(out),sort_keys=True,indent=2));signal.alarm(0)

if __name__=='__main__':main()
