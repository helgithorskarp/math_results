"""Exercise both complete redirected strata with literal full-edge checks.

Fixtures are explicitly non-Ramsey 43-vertex graphs. The local nineteen-
vertex graph is good19 and red-K4-free after color reversal.
"""
from pathlib import Path
from itertools import combinations
import argparse
import copy
import json
import random
from receiver import run, augment_blue, Lookup, decode, validate
from verify_receiver import check


def encoded(a):
    bits=sum(a[u][v]<<k for k,(u,v) in enumerate(combinations(range(43),2)))
    return dict(n=43,red_hex=format(bits,'0226x'))


def fixture(r):
    obj=json.loads((Path(__file__).resolve().parent/'CONTROL_19.json').read_text())
    local=decode(obj); a=[[0]*43 for _ in range(43)]
    red=[list(range(4*i,4*i+4)) for i in range(r)]
    blue=[list(range(4*i,4*i+4)) for i in range(r,7)]; core=list(range(28,43))
    for B in red:
        for u,v in combinations(B,2):a[u][v]=a[v][u]=1
    for i,j in combinations(range(r),2):
        for x,y in ((x,y) for x in range(4) for y in range(4)):
            a[4*i+x][4*j+y]=a[4*j+y][4*i+x]=int((x+y)%4<2)
    for B in red:
        for D in blue:
            for x,y in ((x,y) for x in range(4) for y in range(4)):
                a[B[x]][D[y]]=a[D[y]][B[x]]=int((x+y)%4<2)
    V=blue[0]+core
    for u,v in combinations(range(19),2):a[V[u]][V[v]]=a[V[v]][V[u]]=1-local[u][v]
    if r==5:
        for u in blue[0]:
            for v in blue[1]:a[u][v]=a[v][u]=1
    validate(a,red,blue,core)
    return dict(encoded(a),red=red,blue=blue,core=core)


def transport_controls(data, output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    lookup=Lookup(data);rng=random.Random(550034);results=[];bad_rejections=0
    for r in (5,6):
        for rep in range(3):
            src=fixture(r)
            if rep:
                a=decode(src);p=list(range(43));rng.shuffle(p)
                aa=[[0]*43 for _ in range(43)]
                for u,v in combinations(range(43),2):aa[p[u]][p[v]]=aa[p[v]][p[u]]=a[u][v]
                src=dict(encoded(aa),red=[[p[u] for u in B] for B in src['red']],
                         blue=[[p[u] for u in B] for B in src['blue']],core=[p[u] for u in src['core']])
            aug=augment_blue(decode(src),src['red'],src['blue'],src['core'])
            if aug['status']!='BLUE_PACKING_AUGMENTATION' or aug['red']!=src['red']:
                raise ValueError('direct mixed-stratum augmentation control')
            packet=run(src,lookup);result=check(src,packet,data)
            if packet['status']!='GLOBAL_REDIRECT_NOT_ORIGINAL_TASK_UNSAT':
                raise ValueError('fixture must exercise transport')
            if packet['destination']['status']!='MONOCHROMATIC_FIVE':
                raise ValueError('fixture is not a target witness')
            (output/f'r{r}-{rep}-source.json').write_text(json.dumps(src,sort_keys=True,indent=2)+'\n')
            (output/f'r{r}-{rep}-packet.json').write_text(json.dumps(packet,sort_keys=True,indent=2)+'\n')
            results.append(dict(result,source_r=r,direct_destination_q=len(aug['red'])+len(aug['blue']),
                                final_q=len(packet['packing']['red'])+len(packet['packing']['blue']),
                                final_r=len(packet['packing']['red']),potential_moves=packet['potential_moves']))
            for mode in range(4):
                bad=copy.deepcopy(packet)
                if mode==0:bad['destination']['new_to_old'][0]=bad['destination']['new_to_old'][1]
                elif mode==1:bad['destination']['task']='bo1-q7-r5-c000000'
                elif mode==2:bad['destination']['graph']['red_hex']=format(int(bad['destination']['graph']['red_hex'],16)^1,'0226x')
                else:bad['new_original_task_verdict']=True
                try:check(src,bad,data)
                except ValueError:bad_rejections+=1
                else:raise ValueError('corrupt transport accepted')
    # Early physical-five return is also a complete, checkable receiver outcome.
    src=fixture(6);a=decode(src)
    V=src['blue'][0]+[src['core'][0]]
    for u,v in combinations(V,2):a[u][v]=a[v][u]=0
    src.update(encoded(a));validate(a,src['red'],src['blue'],src['core'])
    packet=run(src,lookup);five=check(src,packet,data)
    if five['status']!='PHYSICAL_MONOCHROMATIC_FIVE_VERIFIED':raise ValueError('early obstruction')
    result=dict(status='BOTH_WHOLE_STRATUM_RECEIVERS_EXERCISED',full43_transports=results,
                corrupt_packets_rejected=bad_rejections,early_five_checked=True,
                fixture_scope='non-Ramsey full43 controls; no good43 is supplied')
    (output/'TRANSPORT_EXPECTED.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('output');args=p.parse_args()
    print(json.dumps(transport_controls(args.data,args.output),sort_keys=True,indent=2))
