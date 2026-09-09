"""Physical rejection/redirect controls and deliberately corrupted evidence."""
from pathlib import Path
from itertools import combinations
import argparse,json,tempfile
from inputs import need
from reference import matching
from contact_codec import Contacts,PhysicalCarrier
from classify import classify
from check_counts import audit
import verify_physical as independent

def run(cache,tables,rows,columns,out):
    out=Path(out);out.mkdir();domains=Contacts(cache,tables,rows);cores=independent.cores(cache);checked=0;digest_rows=[]
    for c in range(362):
        car=PhysicalCarrier(f'bo1-q9-r5-c{c:06d}',cache,domains);g=car.unrank(0);base=independent.physical(g)
        def encode(a):return {'n':43,'red_hex':format(sum(a[u][v]<<k for k,(u,v) in enumerate(combinations(range(43),2))),'0226x')}
        need(classify(dict(task=car.name,graph=g),cache,domains)['status']=='CONTACT_CARRIER_ADMITTED_NOT_A_TARGET','admission')
        # Both colors: a physical core edge plus three vertices from a same-color block.
        for color,block in ((1,0),(0,5)):
            e=next((u,v) for u,v in combinations(range(7),2) if cores[c][u][v]==color)
            a=[row[:] for row in base]
            for row in range(3):
                for v in e:a[4*block+row][36+v]=a[36+v][4*block+row]=color
            obj=dict(task=car.name,graph=encode(a));result=classify(obj,cache,domains)
            need(result['status']=='RAMSEY_REJECT' and result['bad_five']['color']==color,'physical bad five')
            need(all(a[u][v]==color for u,v in combinations(result['bad_five']['vertices'],2)),'witness edge')
            checked+=1;digest_rows.append(result)
        # The selected two-edge exchange can occur without any local K5.
        e,f=matching(cores[c]);a=[row[:] for row in base]
        for row in range(4):
            chosen=e if row<2 else f
            for v in range(7):a[row][36+v]=a[36+v][row]=int(v in chosen)
        obj=dict(task=car.name,graph=encode(a));result=classify(obj,cache,domains)
        need(result['status']=='PACKING_REDIRECT_REQUIRED' and not result['ramsey_rejection'],'redirect distinction')
        checked+=1;digest_rows.append(result)
    rejects=0
    def reject(fn):
        nonlocal rejects
        try:fn()
        except (ValueError,KeyError,IndexError):rejects+=1
        else:raise ValueError('corruption accepted')
    # Entrywise independent census; complement permutation; prefix bytes; fixed physical pairs.
    original=Path(rows).read_text().splitlines()
    for kind in ('plain','complement'):
        altered=original.copy();fields=altered[0].split();fields[1 if kind=='plain' else 4]=str(int(fields[1])+1) if kind=='plain' else '0';altered[0]='\t'.join(fields)
        p=out/(kind+'.tsv');p.write_text('\n'.join(altered)+'\n');reject(lambda:audit(cache,p,columns,tables))
    raw=bytearray(Path(tables).read_bytes());raw[100]^=1;p=out/'altered.bin';p.write_bytes(raw);reject(lambda:Contacts(cache,p,rows))
    item=dict(task=car.name,graph=g);changed=dict(g);changed['red_hex']=format(int(g['red_hex'],16)^1,'0226x')
    reject(lambda:car.rank(changed));reject(lambda:independent.validate(dict(task=car.name,graph=changed),cores))
    reject(lambda:car.unrank(-1));reject(lambda:car.unrank(car.size));reject(lambda:car.unrank(True))
    reject(lambda:domains.rank(0,False,[True,0,0,0]));reject(lambda:domains.rank(0,False,[128,0,0,0]))
    # Explicit all-red core/star violation and out-of-range physical metadata.
    reject(lambda:domains.rank(0,False,[127]*4))
    import hashlib
    digest=hashlib.sha256((json.dumps(digest_rows,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
    result=dict(status='VERIFIED_REJECTION_AND_REDIRECT_CONTROLS',physical_witness_controls=checked,
                monochromatic_rejections=724,packing_redirects=362,corruptions_rejected=rejects,witness_stream_sha256=digest)
    (out/'CONTROLS.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('tables');p.add_argument('rows');p.add_argument('columns');p.add_argument('out');a=p.parse_args()
    print(json.dumps(run(a.cache,a.tables,a.rows,a.columns,a.out),sort_keys=True))
