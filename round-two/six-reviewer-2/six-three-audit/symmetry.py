"""Full original-family CRT image audit, no target data or executable imports."""
import json,sys,math
from pathlib import Path
PERIOD=10080
PLACED=((8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6),(48,14),(96,86))

def need(ok,why):
    if not ok:raise ValueError(why)

def factors(m):
    out=[]
    for p in(2,3,5,7):
        q=1
        while m%p==0:m//=p;q*=p
        if q>1:out.append(q)
    need(m==1,'prime support');return out

def crt(values,mods):
    M=math.prod(mods);return sum(v*(M//p)*pow(M//p,-1,p)for v,p in zip(values,mods))%M

def main(mode):
    need(mode in('literal','crt'),'mode');originals=[m for m in range(8,PERIOD+1)if PERIOD%m==0];gens=[]
    for p,free in((5,(0,2,3,4)),(7,(1,2,3,5,6)),(9,(3,6)),(9,(1,4,7)),(9,(2,5,8))):
        for a,b in zip(free,free[1:]):gens.append((p,a,b))
    records=[]
    for p,a,b in gens:
        def image(q,v):
            if q==p:return b if v==a else a if v==b else v
            return v
        physical_checks=0;rows=[]
        if mode=='literal':
            physical=[crt([image(q,n%q)for q in(32,9,5,7)],(32,9,5,7))for n in range(PERIOD)]
            need(sorted(physical)==list(range(PERIOD)),'period bijection')
            for m in originals:
                images=[None]*m
                for n in range(PERIOD):
                    phase=n%m;v=physical[n]%m
                    if images[phase]is None:images[phase]=v
                    else:need(images[phase]==v,'one SAME-original phase image')
                    physical_checks+=1
                need(sorted(images)==list(range(m)),'family bijection');rows.append({'m':m,'phase_images':images})
        else:
            for m in originals:
                mods=factors(m);images=[crt([image(q,v%q)for q in mods],mods)for v in range(m)];need(sorted(images)==list(range(m)),'CRT family bijection');rows.append({'m':m,'phase_images':images})
            # Three-only branches are fixed because every 9 generator preserves branches.
            physical_checks=len(originals)*PERIOD
        maps={r['m']:r['phase_images']for r in rows}
        need(all(maps[m][a]==a for m,a in PLACED),'literal and forced phases fixed')
        records.append({'generator':[p,a,b],'family_images':rows,'placed_fixed':[list(x)for x in PLACED],'physical_membership_domain_size':physical_checks})
    return {'originals':originals,'generators':records,'summary':{'generators':len(gens),'original_families':len(originals),'phase_images':sum(sum(len(r['phase_images'])for r in g['family_images'])for g in records),'physical_membership_domain_size':sum(g['physical_membership_domain_size']for g in records),'group_size':math.factorial(4)*math.factorial(5)*math.factorial(2)*math.factorial(3)**2},'trust':'CRT family map and ordinary first-appearance orbit proof required; agreement alone not completeness'}
if __name__=='__main__':
    need(len(sys.argv)==3,'mode output');x=main(sys.argv[1]);Path(sys.argv[2]).write_bytes(json.dumps(x,sort_keys=True,separators=(',',':')).encode()+b'\n');print(json.dumps(x['summary']))
