"""Generate constructive phase-extension certificates on <=8 J-cosets.

The independently checkable output stays outside the public source directory.
No solver or negative-search inference enters this positive certificate.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,resource,time
from collections import defaultdict

HERE=Path(__file__).resolve().parent
FULL=(1<<44)-1

def require(ok,msg):
    if not ok:raise ValueError(msg)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def generate():
    pins=json.loads((HERE/'SOURCE_PINS.json').read_text())
    path=HERE.parent/'order7-geometric-cut'/pins['file']
    require(digest(path)==pins['sha256'],'changed pinned field generator')
    spec=importlib.util.spec_from_file_location('pinned_field_generator',path)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    edges=helper.field_edges()
    basis={sum(1<<v for v in {x%44 for x in e}) for e in edges}
    require(all(4<=m.bit_count()<=7 for m in basis),'wrong projected support ranks')
    cache={}
    def canonical(m):
        if m not in cache:
            cache[m]=min(((m>>s)|(m<<(44-s)))&FULL for s in range(44))
        return cache[m]
    cover={canonical(m) for m in basis}
    queue=[m for m in sorted(cover) if m.bit_count()<8]
    small=sorted(m for m in basis if m.bit_count()<8)
    for mask in queue:
        for b in small:
            u=mask|b
            if u.bit_count()>8:continue
            u=canonical(u)
            if u not in cover:
                cover.add(u)
                if u.bit_count()<8:queue.append(u)
    buckets=defaultdict(list)
    for edge in edges:
        buckets[sum(1<<i for i in {v%44 for v in edge})].append(edge)
    records=[];scanned=0
    for scope in sorted(cover,key=lambda m:(m.bit_count(),m)):
        q=[v for v in range(44) if (scope>>v)&1];n=len(q)
        index={v:i for i,v in enumerate(q)}
        local=[];subset=scope
        while subset:
            local.extend(buckets.get(subset,()))
            subset=(subset-1)&scope
        masks={sum(1<<(index[v%44]+n*(v//44)) for v in edge) for edge in local}
        witnesses=[None]*(1<<n);missing=1<<n
        for word in range(0,1<<(2*n),2):
            scanned+=1
            if all(0<(word&mask)<mask for mask in masks):
                phase=(word^(word>>n))&((1<<n)-1)
                if witnesses[phase] is None:
                    witnesses[phase]=word;missing-=1
                    if not missing:break
        require(not missing,'incomplete positive phase coverage')
        records.append({'phase_mask':str(scope),'witnesses':witnesses})
    return {'schema':'h7-local-phase-extension/v2','p':617,'max_phase_cosets':8,
            'records':records},scanned

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();require(not args.output.exists(),'fresh output required')
    began=time.monotonic();certificate,scanned=generate()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(certificate,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'status':'GENERATED_PENDING_INDEPENDENT_CHECK',
                      'certificate_sha256':digest(args.output),
                      'cover_records':len(certificate['records']),
                      'phase_witnesses':sum(len(r['witnesses']) for r in certificate['records']),
                      'orientation_words_scanned':scanned,'seconds':time.monotonic()-began,
                      'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}),flush=True)

if __name__=='__main__':main()
