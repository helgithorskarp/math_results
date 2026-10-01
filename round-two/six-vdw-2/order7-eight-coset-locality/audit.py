"""Independent literal-field positive certificate and union-cover checker.

Imports neither the certificate generator nor its pinned logarithm helper.
Every assertion of mathematical coverage uses explicit guards, including -O.
"""
from pathlib import Path
import argparse,hashlib,json,math,resource,time

def require(ok,msg):
    if not ok:raise ValueError(msg)

def rotation_controls():
    checked=0
    for half in range(2,7):
        for word in range(1<<(2*half)):
            colors=[(word>>i)&1 for i in range(2*half)]
            phase=[colors[i]^colors[i+half] for i in range(half)]
            for shift in range(2*half):
                rotated=[colors[(i+shift)%(2*half)]^colors[shift] for i in range(2*half)]
                require(rotated[0]==0,'small color normalization failed')
                require([rotated[i]^rotated[i+half] for i in range(half)]==
                        [phase[(i+shift)%half] for i in range(half)],
                        'small phase rotation or upper/lower wrap failed')
                checked+=1
    return checked

def check(path):
    data=json.loads(path.read_text())
    require(type(data)==dict and set(data)=={'schema','p','max_phase_cosets','records'},
            'unexpected certificate schema')
    require(data['schema']=='h7-local-phase-extension/v2' and type(data['p'])==int and
            data['p']==617 and type(data['max_phase_cosets'])==int and
            data['max_phase_cosets']==8,'wrong mathematical parameters')
    require(type(data['records'])==list and data['records'],'empty certificate')
    p=617
    require(all(p%d for d in range(2,math.isqrt(p)+1)),'field modulus not prime')
    require({pow(3,i,p) for i in range(616)}==set(range(1,p)),'3 not primitive')
    h={pow(3,88*j,p) for j in range(7)}
    require(len(h)==7 and all(a*b%p in h for a in h for b in h),'wrong H subgroup')
    slots={}
    for i in range(44):
        for sign in (1,-1):
            for v in h:
                x=sign*pow(3,i,p)*v%p
                require(x not in slots,'overlapping signed cosets')
                slots[x]=i+(44 if sign<0 else 0)
    require(set(slots)==set(range(1,p)),'signed field cosets incomplete')
    qr={v*v%p for v in range(1,p)}
    edges=set();retained=removed=0
    for a in range(p):
        for d in range(1,p):
            terms=[(a+j*d)%p for j in range(7)]
            if 0 in terms:removed+=1;continue
            retained+=1
            edges.add(tuple(sorted({slots[x] for x in terms})))
            require(len({int(x in qr) for x in terms})==2,'literal QR control failed')
    require((retained,removed,len(edges))==(375760,4312,26488),'wrong full AP census')
    basis={sum(1<<i for i in {v%44 for v in e}) for e in edges}
    require(len(basis)==12936 and min(m.bit_count() for m in basis)==4 and
            max(m.bit_count() for m in basis)==7,'wrong phase-projection census')
    canonical_cache={}
    def canonical(mask):
        # Coordinate translations differ from the generator's bit rotations.
        if mask not in canonical_cache:
            q=[i for i in range(44) if (mask>>i)&1]
            canonical_cache[mask]=min(sum(1<<((i-r)%44) for i in q) for r in range(44))
        return canonical_cache[mask]
    cover={};full=(1<<44)-1
    for record in data['records']:
        require(type(record)==dict and set(record)=={'phase_mask','witnesses'},'invalid record')
        text=record['phase_mask']
        require(type(text)==str and text.isascii() and text.isdecimal(),'invalid phase mask')
        mask=int(text)
        require(text==str(mask) and 0<mask<=full and 4<=mask.bit_count()<=8,
                'phase mask outside domain')
        require(mask==canonical(mask) and mask not in cover,'noncanonical/duplicate record')
        n=mask.bit_count();words=record['witnesses']
        require(type(words)==list and len(words)==1<<n,'incomplete phase cube')
        require(all(type(w)==int and 0<=w<1<<(2*n) and w%2==0 for w in words),
                'invalid normalized witness words')
        cover[mask]=words
    require({canonical(m) for m in basis}<=set(cover),'missing AP support in cover')
    closure_steps=0
    for mask in cover:
        if mask.bit_count()==8:continue
        for b in basis:
            union=mask|b
            if union.bit_count()<=8:
                require(canonical(union) in cover,'missing support union in cover')
                closure_steps+=1
    # An eight-set cannot grow under an eligible union; its closure is automatic.
    paired=[(edge,sum(1<<i for i in {v%44 for v in edge})) for edge in edges]
    positive_checks=max_local=0
    histogram={n:0 for n in range(4,9)}
    for mask,words in cover.items():
        q=[i for i in range(44) if (mask>>i)&1];n=len(q);histogram[n]+=1
        local=[edge for edge,scope in paired if scope&~mask==0]
        max_local=max(max_local,len(local))
        for phase,word in enumerate(words):
            colors={}
            for i,v in enumerate(q):
                colors[v]=(word>>i)&1;colors[v+44]=(word>>(i+n))&1
                require(colors[v]^colors[v+44]==((phase>>i)&1),'wrong witness phase')
            require(colors[q[0]]==0,'missing color normalization')
            require(all(len({colors[v] for v in edge})==2 for edge in local),
                    'monochromatic internal field AP')
            positive_checks+=1
    return {'status':'EXACT_EIGHT_COSET_LOCAL_PHASE_EXTENSION_VERIFIED',
            'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'field_APs':retained,'zero_APs_removed':removed,'signed_AP_supports':len(edges),
            'phase_supports':len(basis),'basis_rotation_orbits':len({canonical(m) for m in basis}),
            'cover_records':len(cover),'rank_histogram':histogram,'closure_steps':closure_steps,
            'positive_phase_witnesses':positive_checks,'max_local_NAE_edges':max_local,
            'QR_positive_controls':2,'small_rotation_controls':rotation_controls(),
            'partial_phase_assignments_covered':
            sum(math.comb(44,n)*2**n for n in range(9)),
            'establishes_full_H7_existence':False,'establishes_global_W_bound':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('certificate',type=Path);args=ap.parse_args()
    began=time.monotonic();result=check(args.certificate)
    result.update(seconds=time.monotonic()-began,
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
