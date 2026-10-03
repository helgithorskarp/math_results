"""Independent final free BASE-shadow bound: bitmaps versus histograms.

The fresh complete phase census supplies the compact retained-mask set.
The driver/checker binds that set to every surviving canonical row.
Complete phase records remain accepted; no author corpus is read.
"""
import json,sys
from pathlib import Path

def need(ok,why):
    if not ok:raise ValueError(why)

def main(mode,first,phases):
    need(mode in('bitmap','histogram'),'mode');R=first['initial_R'];P2=first['parents']['2'];P6=first['parents']['6'];base=first['domain']['unused_BASE_originals']
    # Rediscover the forced physical original pair rather than import its 90-set.
    fixed=[x for x in P6 if all(n%32==6 or n%48==14 or n%96==86 for n in(x+2520*k for k in range(4)))]
    if all(type(p)is str for p in phases):
        shapes=sorted({int(p,16)for p in phases})
        need(len(shapes)==len(phases),'duplicate fresh repair shape')
    else:shapes=sorted({int(r['repair_mask_hex'],16)for b in phases for r in b['rows']if r['survives_necessary_tests']})
    records=[]
    if mode=='bitmap':
        RI=sum(1<<x for x in R);families={m:[sum(1<<x for x in R if x%m==a)for a in range(m)]for m in base}
    else:
        total={m:[0]*m for m in base}
        for m in base:
            for x in R:total[m][x%m]+=1
    for mask in shapes:
        parent=[x for i,x in enumerate(P2)if mask>>i&1];S=sorted(parent+fixed);budget=len(S)-177;rows=[];upper=0
        if mode=='bitmap':SI=sum(1<<x for x in S)
        else:
            inside={m:[0]*m for m in base}
            for m in base:
                for x in S:inside[m][x%m]+=1
        for m in base:
            if mode=='bitmap':values=[[(f&SI).bit_count(),(f&RI&~SI).bit_count()]for f in families[m]]
            else:values=[[inside[m][a],total[m][a]-inside[m][a]]for a in range(m)]
            maximum=max([0]+[b for a,b in values if a<=budget]);rows.append({'original':m,'phases':values,'outside_max_with_omission':maximum,'omission_allowed':True});upper+=maximum
        records.append({'parent2_mask_hex':format(mask,'x'),'parent2_holes':parent,'shadow':S,'size':len(S),'protected_budget':budget,'outside_need':len(R)-len(S),'outside_upper':upper,'deficit':len(R)-len(S)-upper,'BASE_phase_rows':rows})
    return {'fixed_parent6':fixed,'shapes':records,'summary':{'shapes':len(records),'BASE_originals':len(base),'phases_per_shape':sum(base),'all_phase_entries':len(records)*sum(base),'shadow_sizes':sorted({r['size']for r in records}),'outside_upper_range':[min(r['outside_upper']for r in records),max(r['outside_upper']for r in records)],'deficit_range':[min(r['deficit']for r in records),max(r['deficit']for r in records)]},'scope':'Conditional final shadow exclusion only; first-stage, symmetry, completeness and imported lower177/essentiality bridges are separately required.'}
if __name__=='__main__':
    need(len(sys.argv)==5,'mode fresh first record fresh phases output');mode,first,phases,out=sys.argv[1:];x=main(mode,json.loads(Path(first).read_bytes()),json.loads(Path(phases).read_bytes()));Path(out).write_bytes(json.dumps(x,sort_keys=True,separators=(',',':')).encode()+b'\n');print(json.dumps(x['summary']))
