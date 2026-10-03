"""Independent first-stage six/three audit; no target imports or data inputs.

Two phase representations and two partition recurrences, explicitly sharing
model definitions, orchestration and record schema. Written proof exposed.
This file does not prove the final six/three exclusion.
"""
import itertools,json,math,functools,hashlib,sys
from pathlib import Path
P=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
O=(5,7,9,15,21,35,45,63,105,315)

def need(ok,why):
    if not ok:raise ValueError(why)

def main(mode):
    need(mode in('partition','matching'),'mode')
    if mode=='partition':
        R=tuple(n for n in range(2520)if all(n%m!=a for m,a in P))
        parents={s:tuple(n for n in R if n%8==s)for s in(2,6)}
        encode=lambda xs:sum(1<<n for n in xs)
        count=int.bit_count
        union=lambda a,b:a|b
        def family(d,points):return[encode(n for n in points if n%d==a)for a in range(d)]
    else:
        covered=set().union(*(set(range(a,2520,m))for m,a in P));R=tuple(sorted(set(range(2520))-covered))
        parents={s:tuple(sorted(set(range(s,2520,8))&set(R)))for s in(2,6)}
        encode=frozenset;count=len;union=lambda a,b:a|b
        def family(d,points):
            whole=set(points);return[frozenset(set(range(a,2520,d))&whole)for a in range(d)]
    whole=encode(R);pm={s:encode(xs)for s,xs in parents.items()}
    allco=(1,3)+O;native={s:{d:family(d,parents[s])for d in allco}for s in(2,6)}
    caps={d:max(map(count,native[2][d]))for d in allco};need(caps=={d:max(map(count,native[6][d]))for d in allco},'both actual parent populations')
    base=[m for m in range(8,2521)if 2520%m==0 and m not in{d for d,a in P}]
    footprint={m:family(m,R)for m in base}
    if mode=='matching':total={m:[0]*m for m in base}
    if mode=='matching':
        for m in base:
            for n in R:total[m][n%m]+=1
    small=[];small_entries=0
    for d in(5,9):
        for a in range(d):
            right=family(d,parents[6])[a];S=union(pm[2],right);k=count(S);budget=k-177;pop={};sums=[]
            if mode=='matching':
                inside={m:[0]*m for m in base}
                for m in base:
                    for n in S:inside[m][n%m]+=1
            for m in base:
                if mode=='partition':row=[[count(f&S),count(f&~S)]for f in footprint[m]]
                else:row=[[inside[m][b],total[m][b]-inside[m][b]]for b in range(m)]
                pop[m]=row;sums.append(max([0]+[out for protected,out in row if protected<=budget]));small_entries+=len(row)
            outside=count(whole)-k
            small.append({'d':d,'phase':a,'shadow':sorted(S)if mode=='matching'else[n for n in R if S>>n&1],'size':k,'budget':budget,'outside_need':outside,'bound':sum(sums),'deficit':outside-sum(sums),'phase_populations':pop,'omission_allowed':True})
    pairs={};rawpairs=[]
    for i,j in itertools.combinations(range(10),2):
        values=[count(union(a,b))for a in native[2][O[i]]for b in native[2][O[j]]]
        pairs[i,j]=max(values);rawpairs.append({'original_cofactors':[O[i],O[j]],'values':values})
    @functools.cache
    def group(mask):
        if not mask:return 0
        i=(mask&-mask).bit_length()-1;rest=mask^(1<<i)
        if mode=='partition':
            value=caps[O[i]]+group(rest)
            for j in range(i+1,10):
                if rest>>j&1:value=min(value,pairs[i,j]+group(rest^(1<<j)))
            return min(150,value)
        return min(150,sum(caps[O[j]]for j in range(10)if mask>>j&1)-saving(mask))
    @functools.cache
    def saving(mask):
        if not mask:return 0
        i=(mask&-mask).bit_length()-1;rest=mask^(1<<i);value=saving(rest)
        for j in range(i+1,10):
            if rest>>j&1:value=max(value,caps[O[i]]+caps[O[j]]-pairs[i,j]+saving(rest^(1<<j)))
        return value
    @functools.cache
    def qarms(mask):
        if mask.bit_count()<2:return 0
        first=mask&-mask;sub=(mask-1)&mask;value=0
        while sub:
            other=mask^sub
            if sub&first and other:
                overlap=sum(caps[math.lcm(O[i],O[j])]for i in range(10)if sub>>i&1 for j in range(10)if other>>j&1)
                value=max(value,min(group(sub),group(other),overlap))
            sub=(sub-1)&mask
        return value
    masks={k:[sum(1<<i for i in xs)for xs in itertools.combinations(range(10),k)]for k in range(6)}
    inventories=[];summary=[];blocks=[]
    for h in range(6):
        q=5-h;rows=[]
        for H in masks[h]:
            for Q in masks[q]:
                bound=min(150,group(H)+qarms(Q));row={'H':[O[i]for i in range(10)if H>>i&1],'Q':[O[i]for i in range(10)if Q>>i&1],'bound':bound};rows.append(row)
                if bound>=87 and q!=1:
                    rawweight=math.prod(row['H']+row['Q'])*(2 if q==2 else 1);blocks.append({**row,'raw_phase_tuples':rawweight})
        inventories.append({'h':h,'q':q,'rows':rows});summary.append({'h':h,'q':q,'inventory_rows':len(rows),'maximum':max(x['bound']for x in rows),'reaching87':sum(x['bound']>=87 for x in rows)})
    # Full physical parent6 four-lift repair calculation for the forced odd3 pair.
    quarter=32;forced=[]
    for A in range(14,48,16):
        for B in range(22,96,32):
            actual=[]
            for x in parents[6]:
                lifts=[x+2520*k for k in range(4)]
                if all(n%32==6 or n%48==A or n%96==B for n in lifts):actual.append(x)
            forced.append({'H_original':48,'H_phase':A,'Q_original':96,'Q_phase':B,'repair_set':actual,'size':len(actual)})
    fulltuple=sum(x['raw_phase_tuples']for x in blocks)
    return {'domain':{'period':10080,'base_period':2520,'prefix':[list(x)for x in P],'placed_tail':[[16,2],[32,6]],'essential16_32_required':True,'minimum_exactly8':True,'actual_LCM_proper_divisor_allowed':True,'selected_unproductive_tails_allowed':True,'original_cofactors':list(O),'unused_BASE_originals':base,'BASE_original_phase_count':sum(base)},'initial_R':list(R),'parents':parents,'single_phase_populations':{s:{d:[count(f)for f in fs]for d,fs in native[s].items()}for s in(2,6)},'single_maxima':caps,'small_shadows':small,'raw_pair_unions':rawpairs,'group_bounds':[group(mask)for mask in range(1024)],'Q_arm_bounds':[qarms(mask)for mask in range(1024)],'inventories':inventories,'inventory_summary':summary,'phase_blocks':blocks,'forced_parent6_phase_rows':forced,'summary':{'R_size':len(R),'parent_sizes':[len(parents[s])for s in(2,6)],'small_shadows':len(small),'small_phase_entries':small_entries,'raw_pair_entries':sum(len(r['values'])for r in rawpairs),'inventory_rows':sum(len(x['rows'])for x in inventories),'relevant_phase_blocks':len(blocks),'relevant_full_raw_phase_tuples':fulltuple}}

if __name__=='__main__':
    need(len(sys.argv)==3,'mode and output path required');record=main(sys.argv[1]);raw=json.dumps(record,sort_keys=True,separators=(',',':')).encode();Path(sys.argv[2]).write_bytes(raw+b'\n');print(json.dumps({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'summary':record['summary'],'inventories':record['inventory_summary'],'small_bounds':[[r['d'],r['phase'],r['size'],r['bound'],r['deficit']]for r in record['small_shadows']],'forced6_counts':[r['size']for r in record['forced_parent6_phase_rows']]},sort_keys=True))
