"""Fresh canonical-domain audit: phase-prefix rejection versus component RGS.

Consumes a freshly reconstructed first-stage record, never a target record.
All rows, including small repair sets and failed essentiality, are retained.
"""
import itertools,json,math,sys
from pathlib import Path
FREE=((0,2,3,4),(1,2,3,5,6),(3,6),(1,4,7),(2,5,8))

def need(ok,why):
    if not ok:raise ValueError(why)

def updates(d,a,state):
    mentions=[]
    if d%5==0:mentions.append((0,a%5))
    if d%7==0:mentions.append((1,a%7))
    if d%9==0:mentions.append((2+a%3,a%9))
    nxt=list(state)
    for b,v in mentions:
        if v not in FREE[b]:continue
        i=FREE[b].index(v)
        if i>nxt[b]:return None
        if i==nxt[b]:nxt[b]+=1
    return tuple(nxt)

def prefix_rows(ds):
    def walk(i,phases,state):
        if i==len(ds):yield phases,math.prod(math.prod(range(len(f)-k+1,len(f)+1))for f,k in zip(FREE,state));return
        d=ds[i]
        for a in range(d):
            nxt=updates(d,a,state)
            if nxt is not None:yield from walk(i+1,phases+(a,),nxt)
    yield from walk(0,(),(0,0,0,0,0))

def rgs_values(size,fixed,free):
    def walk(row,k):
        if len(row)==size:
            yield row,math.prod(range(len(free)-k+1,len(free)+1));return
        for a in tuple(fixed)+tuple(free[:min(k+1,len(free))]):
            yield from walk(row+(a,),k+(a in free and free.index(a)==k))
    return list(walk((),0))

def ternary_values(mods):
    def walk(i,row,ks):
        if i==len(mods):
            yield row,math.prod(math.prod(range(len(FREE[b+2])-k+1,len(FREE[b+2])+1))for b,k in enumerate(ks));return
        if mods[i]==3:
            for a in range(3):yield from walk(i+1,row+(a,),ks)
        else:
            options=[0]+[a for b in range(3)for a in FREE[b+2][:min(ks[b]+1,len(FREE[b+2]))]]
            for a in options:
                nk=list(ks)
                if a:
                    b=a%3
                    if FREE[b+2].index(a)==ks[b]:nk[b]+=1
                yield from walk(i+1,row+(a,),tuple(nk))
    return list(walk(0,(),(0,0,0)))

def component_rows(ds):
    i5=[i for i,d in enumerate(ds)if d%5==0];i7=[i for i,d in enumerate(ds)if d%7==0];it=[i for i,d in enumerate(ds)if d%3==0]
    ts=[9 if ds[i]%9==0 else 3 for i in it]
    patterns=[rgs_values(len(i5),(1,),FREE[0]),rgs_values(len(i7),(0,4),FREE[1]),ternary_values(ts)]
    maps=[]
    for i,d in enumerate(ds):
        mods=([9 if d%9==0 else 3]if d%3==0 else[])+([5]if d%5==0 else[])+([7]if d%7==0 else[])
        maps.append((mods,[(d//p)*pow(d//p,-1,p)for p in mods]))
    rows=[]
    for (p5,w5),(p7,w7),(pt,wt)in itertools.product(*patterns):
        d5=dict(zip(i5,p5));d7=dict(zip(i7,p7));dt=dict(zip(it,pt));ph=[]
        for i,d in enumerate(ds):
            values=([dt[i]]if i in dt else[])+([d5[i]]if i in d5 else[])+([d7[i]]if i in d7 else[])
            ph.append(sum(v*c for v,c in zip(values,maps[i][1]))%d)
        rows.append((tuple(ph),w5*w7*wt))
    rows.sort();return rows

def main(mode,record,lo,hi):
    need(mode in('prefix','component'),'mode');R=record['parents']['2'];blocks=record['phase_blocks'];out=[]
    initial=tuple(x+2520*k for x in R for k in range(4));universe=(1<<len(initial))-1
    low_cells=sum(1<<(4*i)for i in range(len(R)))
    packing=[]
    for size in(1,2,4,8,16,32,64,128):
        mask=sum(((1<<(2*size))-1)<<(8*size*j)for j in range((len(R)+2*size-1)//(2*size)))
        packing.append((3*size,mask))
    def pack(quad):
        for shift,mask in packing:quad=(quad|(quad>>shift))&mask
        return quad
    # Bind packing to each actual four-cell basis and the complete boundary.
    for i in range(len(R)):need(pack(1<<(4*i))==1<<i,'physical quartet packing basis')
    need(pack(low_cells)==(1<<len(R))-1,'physical quartet packing full domain')
    literal={n:i for i,n in enumerate(initial)}
    placed=sum(1<<i for i,n in enumerate(initial)if n%16==2)
    native={}
    def actual_phase(d,kind,arm,a):
        power=16 if kind=='H'else 32;binary=10 if kind=='H'else arm
        return binary+power*((a-binary)*pow(power,-1,d)%d)
    def cells(d,kind,arm,a):
        key=(d,kind,arm,a)
        if key not in native:
            m=(16 if kind=='H'else 32)*d;v=actual_phase(d,kind,arm,a)
            native[key]=sum(1<<literal[n]for n in range(v,10080,m)if n in literal)
        return native[key]
    odd={d:[sum(1<<i for i,x in enumerate(R)if x%d==a)for a in range(d)]for d in record['domain']['original_cofactors']}
    for bi in range(lo,hi):
        block=blocks[bi];H=block['H'];Q=block['Q'];ds=H+Q;rows=[];generator=prefix_rows(ds)if mode=='prefix'else component_rows(ds)
        armslist=[()]if not Q else[(10,26),(26,10)]
        for phases,w in generator:
            for arms in armslist:
                original=[actual_phase(d,'H',10,a)for d,a in zip(H,phases[:len(H)])]+[actual_phase(d,'Q',arm,a)for d,arm,a in zip(Q,arms,phases[len(H):])]
                if mode=='prefix':
                    hs=[odd[d][a]for d,a in zip(H,phases[:len(H)])];qs=[odd[d][a]for d,a in zip(Q,phases[len(H):])]
                    HU=0
                    for f in hs:HU|=f
                    if Q:common=qs[0]&qs[1]
                    else:common=0
                    repair=HU|common;exclusive=[]
                    for i,f in enumerate(hs):
                        other=0
                        for j,g in enumerate(hs):
                            if i!=j:other|=g
                        exclusive.append((f&~other&~common&repair).bit_count()>0)
                    for f in qs:exclusive.append((common&~HU&repair).bit_count()>0)
                else:
                    fs=[cells(d,'H',10,a)for d,a in zip(H,phases[:len(H)])]+[cells(d,'Q',arm,a)for d,arm,a in zip(Q,arms,phases[len(H):])]
                    cover=placed
                    for f in fs:cover|=f
                    # Each initial hole owns four consecutive actual physical cells.
                    quad=cover&(cover>>1)&(cover>>2)&(cover>>3)&low_cells
                    repair=pack(quad);full_cells=quad|(quad<<1)|(quad<<2)|(quad<<3);exclusive=[]
                    for i,f in enumerate(fs):
                        other=placed
                        for j,g in enumerate(fs):
                            if i!=j:other|=g
                        exclusive.append((f&~other&full_cells&universe).bit_count()>0)
                rows.append({'odd_phases':list(phases),'Q_arms':list(arms),'original_phases':original,'orbit_weight':w,'repair_mask_hex':format(repair,'x'),'repair_size':repair.bit_count(),'exclusive_initial_witness':exclusive,'survives_necessary_tests':repair.bit_count()>=87 and all(exclusive)})
        rows.sort(key=lambda r:(r['odd_phases'],r['Q_arms']));out.append({'block':bi,'H':H,'Q':Q,'rows':rows,'canonical_rows':len(rows),'raw_weight':sum(r['orbit_weight']for r in rows)})
    return out

if __name__=='__main__':
    need(len(sys.argv)==6,'mode fresh first-stage record lo hi output');mode,src,lo,hi,out=sys.argv[1:];record=json.loads(Path(src).read_bytes());x=main(mode,record,int(lo),int(hi));raw=json.dumps(x,sort_keys=True,separators=(',',':')).encode()+b'\n';Path(out).write_bytes(raw);print(json.dumps({'blocks':[int(lo),int(hi)],'canonical_rows':sum(r['canonical_rows']for r in x),'raw_weight':sum(r['raw_weight']for r in x),'survivors':sum(sum(z['survives_necessary_tests']for z in r['rows'])for r in x),'bytes':len(raw)}))
