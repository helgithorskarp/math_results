"""Entry-level comparison and literal controls for the complete p3 census.

This checker does not certify pair-clique coverage from a saved flag. The
second complete all-labeled monotone DFS supplies separate coverage; all of
its pools and terminal sets must equal the transported first enumeration.
"""
import argparse
import copy
import hashlib
import json
import resource
import time
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE=Path(__file__).resolve().parent
import literal as l
import model as m


def require(p,why):
    if not p:
        raise ValueError(why)


def integer(x,low=0,high=(1<<64)-1):
    require(type(x) is int and low<=x<=high,'exact integer domain')


def ordered(values,size,high):
    require(type(values) is list and len(values)==size,'list cardinality')
    for x in values:
        integer(x,0,high-1)
    require(values==sorted(set(values)),'strict ordered unique domain')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--expected',type=Path,default=HERE/'expected.json')
    args=ap.parse_args()
    started=time.monotonic()
    root=args.work
    manifest=[]
    for i,line in enumerate((root/'cases.txt').read_text().splitlines()):
        parts=list(map(int,line.split()))
        require(len(parts)==8 and parts[0]==i,'manifest index/shape')
        ordered(parts[1:4],3,7);ordered(parts[4:7],3,35)
        integer(parts[7],1,6);require(6%parts[7]==0,'case multiplicity')
        manifest.append(parts)
    require(len(manifest)==38313 and sum(c[7] for c in manifest)==229075,'manifest coverage')
    records=[]
    producer_paths=sorted(root.glob('producer-*.jsonl'))
    require(bool(producer_paths),'producer phases absent')
    expected_first=0
    for path in producer_paths:
        first=int(path.stem.split('-')[-1])
        require(first==expected_first,'producer phase gap/overlap')
        lines=iter(path.open())
        footer=None;expected=first
        for line in lines:
            z=json.loads(line)
            if z.get('segment'):
                require(footer is None,'duplicate producer footer')
                footer=z;continue
            require(footer is None and z['index']==expected,'producer ordered prefix')
            expected+=1
            c=manifest[z['index']]
            require(z['weight']==c[7] and type(z['weight']) is int,'producer weight')
            require(type(z['base_blue_valid']) is bool,'producer base Boolean')
            ordered(z['pool'],len(z['pool']),35)
            co=z['compatibility'];require(len(co)==len(z['pool']),'compatibility size')
            for i,x in enumerate(co):
                integer(x,0,(1<<len(co))-1)
                require(not (x>>i&1),'compatibility self bit')
                for j,y in enumerate(co):
                    require((x>>j&1)==(y>>i&1),'compatibility symmetry')
            for q in ('7','8'):
                for k in ('cliques','blue_valid','degree_valid','two_color_valid'):
                    integer(z['targets'][q][k])
            records.append(z)
        require(footer is not None and footer['first']==first and footer['next']==expected,'producer footer coverage')
        expected_first=expected
    require([z['index'] for z in records]==list(range(38313)),'producer full representative coverage')
    g=m.geometry();native=l.geometry()
    require(native[1]==[g[2],g[3]],'independent ground orbit identities')
    maps=sorted(set(tuple(tuple(x) for x in entry) for entry in m.centralizer(g)))
    require(len(maps)==6,'effective ground action')
    keys={(tuple(c[1:4]),tuple(c[4:7])):c[0] for c in manifest}
    require(len(keys)==38313,'unique representative keys')
    positive={i:{7:{},8:{}} for i in range(38313)}
    leaf_counts={7:Counter(),8:Counter()}
    previous=None
    critical_hash=hashlib.sha256()
    for path in producer_paths:
        first=int(path.stem.split('-')[-1])
        for line in (root/f'critical-{first:05}.txt').open():
            critical_hash.update(line.encode())
            parts=list(map(int,line.split()));idx,q,good=parts[:3];D=parts[3:]
            integer(idx,0,38312);require(q in (7,8) and good in (0,1),'critical target/flag')
            ordered(D,q,35)
            key=(idx,q,tuple(D))
            require(previous is None or previous<key,'unique sorted critical leaves')
            previous=key;leaf_counts[q][idx]+=1
            pool=records[idx]['pool']
            require(set(D)<=set(pool),'critical pool membership')
            positions=[pool.index(d) for d in D]
            require(all(records[idx]['compatibility'][a]>>b&1 for a,b in combinations(positions,2)),
                    'critical deletion compatibility')
            if good:
                c=manifest[idx];J=tuple(c[1:4]);P=tuple(c[4:7])
                literal=l.rows(native,J,P,D)
                bitrows=m.graph(g,J,P,D)
                require(bitrows==[sum(1<<v for v in row) for row in literal],'literal adjacency control')
                s=m.literal_summary(literal)
                require(not any(x[2]=='blue' for x in s['violations']),'literal blue validity')
                positive[idx][q][tuple(D)]=(len(s['violations']),all(7<=d<=10 for d in s['degrees']))
    for idx,r in enumerate(records):
        for q in (7,8):
            t=r['targets'][str(q)];p=positive[idx][q]
            require(t['cliques']==leaf_counts[q][idx],'every producer critical leaf recorded')
            require(t['blue_valid']==len(p) and t['degree_valid']==sum(d for b,d in p.values()),'producer positive counts')
            require(t['two_color_valid']==sum(b==0 for b,d in p.values()),'producer two-color count')
            minimum=min((b for b,d in p.values()),default=-1)
            require(t['best_red_bad']==minimum,'producer actual best defect count')
            if p:
                require(tuple(t['best']) in p and p[tuple(t['best'])][0]==minimum,'producer best control exists')
    joins=list(combinations(range(7),3));promotions=list(combinations(range(35),3))

    def validate_record(z,expected_index,literal_check=True):
        require(set(z)=={'index','joins','promotions','base_blue_valid','pool','attempted','good','targets'},'native schema')
        integer(z['index'],0,229074);require(z['index']==expected_index,'native gap/overlap')
        ordered(z['joins'],3,7);ordered(z['promotions'],3,35)
        J=tuple(z['joins']);P=tuple(z['promotions'])
        require(J==joins[expected_index//6545] and P==promotions[expected_index%6545],'native labeled indexing')
        require(type(z['base_blue_valid']) is bool,'native base Boolean')
        ordered(z['pool'],len(z['pool']),35)
        for name in ('attempted','good'):
            require(len(z[name])==9,'depth vector shape')
            for value in z[name]:integer(value)
        require(all(a>=b for a,b in zip(z['attempted'],z['good'])),'native prefix counts')
        require(z['good'][0]==z['attempted'][0]==0 and z['good'][1]==len(z['pool']),
                'native initial depth controls')
        images=[((tuple(sorted(v[i] for i in J)),tuple(sorted(b[i] for i in P))),r)
                for v,r,b in maps]
        canonical,red_map=min(images,key=lambda x:x[0])
        require(canonical in keys,'canonical case absent')
        idx=keys[canonical];producer=records[idx]
        require(z['base_blue_valid']==producer['base_blue_valid'],'native base vs transported producer')
        require(sorted(red_map[d] for d in z['pool'])==producer['pool'],'native pool vs transported producer')
        require(set(z['targets'])=={'7','8'},'native terminal schema')
        for q in (7,8):
            candidates=z['targets'][str(q)]
            require(type(candidates) is list and len(candidates)==z['good'][q],'native complete positive count')
            decoded={}
            for candidate in candidates:
                require(set(candidate)=={'D','red_bad','degrees'},'native candidate schema')
                D=candidate['D'];ordered(D,q,35)
                require(set(D)<=set(z['pool']),'native candidate pool membership')
                integer(candidate['red_bad'],0,231);require(type(candidate['degrees']) is bool,'degree Boolean')
                image=tuple(sorted(red_map[d] for d in D))
                require(image not in decoded,'duplicate native terminal set')
                decoded[image]=(candidate['red_bad'],candidate['degrees'])
                if literal_check:
                    rows=l.rows(native,J,P,D);summary=m.literal_summary(rows)
                    require(not any(x[2]=='blue' for x in summary['violations']),'native positive literal blue predicate')
                    require(candidate['red_bad']==len(summary['violations']),'native literal red spine count')
                    require(candidate['degrees']==all(7<=d<=10 for d in summary['degrees']),'native literal degree diagnostic')
            require(decoded==positive[idx][q],'entry-level complete native deletion sets')
        return idx

    expected=0;weights=Counter();red_hist=Counter();degree_count=0;native_hash=hashlib.sha256();control=None
    code_hash=hashlib.sha256((HERE/'independent.cpp').read_bytes()).hexdigest()
    for meta in sorted(root.glob('native-*.metadata.json')):
        info=json.loads(meta.read_text())
        require(info['source_sha256']==code_hash and info['segment']['first']==expected,'native metadata/source coverage')
        file=meta.with_name(meta.name.replace('.metadata.json','.jsonl'))
        footer=None;phase_first=expected
        for line in file.open():
            z=json.loads(line)
            if z.get('segment'):
                require(footer is None,'native duplicate footer');footer=z;continue
            native_hash.update(line.encode())
            require(footer is None,'native cases follow footer')
            idx=validate_record(z,expected);weights[idx]+=1;expected+=1
            for c in z['targets']['7']:
                red_hist[c['red_bad']]+=1;degree_count+=c['degrees']
                if control is None:control=copy.deepcopy(z)
        require(footer is not None and footer['first']==phase_first and footer['next']==expected and
                footer['total']==229075 and footer['complete']==(expected==229075),'native footer coverage')
        require(footer==info['segment'],'actual footer differs from metadata')
    require(expected==229075,'full native domain required')
    if expected==229075:
        require(all(weights[i]==c[7] for i,c in enumerate(manifest)),'every centralizer multiplicity independently observed')
    require(control is not None,'positive native control missing')
    validate_record(control,control['index'])
    damages=[]

    def reject(name,change,index=None):
        damaged=copy.deepcopy(control);change(damaged)
        try:validate_record(damaged,control['index'] if index is None else index)
        except (ValueError,KeyError,TypeError,IndexError):damages.append(name);return
        raise ValueError('damaged record accepted: '+name)

    reject('omitted-labeled-case',lambda x:None,index=control['index']+1)
    reject('pool-truncation',lambda x:x['pool'].pop())
    reject('Boolean-base-as-integer',lambda x:x.update(base_blue_valid=int(x['base_blue_valid'])))
    reject('Boolean-count',lambda x:x['good'].__setitem__(7,True))
    reject('omitted-positive-set',lambda x:x['targets']['7'].pop())
    reject('duplicate-positive-set',lambda x:x['targets']['7'].append(copy.deepcopy(x['targets']['7'][0])))
    reject('forged-red-count',lambda x:x['targets']['7'][0].update(red_bad=x['targets']['7'][0]['red_bad']+1))
    reject('forged-degree-flag',lambda x:x['targets']['7'][0].update(degrees=not x['targets']['7'][0]['degrees']))
    reject('forged-pass-flag',lambda x:x.update(verified=True))
    summary=dict(status='COMPLETE_ENTRY_LEVEL_AGREEMENT',
                 native_cases=expected,representatives=38313,
                 critical={str(q):dict(representative=sum(leaf_counts[q].values()),
                       labeled=sum(manifest[i][7]*n for i,n in leaf_counts[q].items())) for q in (7,8)},
                 blue_valid={str(q):dict(representative=sum(len(positive[i][q]) for i in positive),
                       labeled=sum(manifest[i][7]*len(positive[i][q]) for i in positive)) for q in (7,8)},
                 actual_native_red_bad_histogram=dict(sorted(red_hist.items())),
                 actual_native_degree_valid=degree_count,damage_controls=damages,
                 critical_sha256=critical_hash.hexdigest(),native_inventory_sha256=native_hash.hexdigest())
    primary_text=(HERE/'primary21.rows').read_text()
    primary_lines=primary_text.splitlines()
    require(len(primary_lines)==21 and all(len(row)==21 and set(row)<={'0','1'} for row in primary_lines),
            'primary fixture domain')
    primary=[{v for v,bit in enumerate(row) if bit=='1'} for row in primary_lines]
    kg=[{v for v in range(21) if native[0][u].isdisjoint(native[0][v])} for u in range(21)]
    sharp_J=(0,1,2);sharp_P=(2,26,29);sharp_D=(2,8,11,14,16,23,27)
    controls={'KG21':m.literal_summary(kg),'primary21':m.literal_summary(primary),
              'sharp_p3':dict(joins=sharp_J,promotions=sharp_P,deletions=sharp_D,
                             summary=m.literal_summary(l.rows(native,sharp_J,sharp_P,sharp_D)))}
    require(not controls['KG21']['violations'] and controls['KG21']['edges']==105,'classical KG control')
    require(not controls['primary21']['violations'] and controls['primary21']['edges']==93,'primary21 control')
    require(controls['sharp_p3']['summary']['edges']==102 and
            len(controls['sharp_p3']['summary']['violations'])==21 and
            all(v[2]=='red' for v in controls['sharp_p3']['summary']['violations']),'sharp positive control')
    summary['controls']=controls
    summary['case_manifest_sha256']=hashlib.sha256((root/'cases.txt').read_bytes()).hexdigest()
    require(args.expected.is_file(),'frozen fixture must exist before checking')
    canonical=lambda x: json.dumps(json.loads(json.dumps(x)),sort_keys=True,separators=(',',':'))
    require(canonical(summary)==canonical(json.loads(args.expected.read_text())),'frozen mathematical evidence mismatch')
    args.output.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))
    print('seconds',time.monotonic()-started,'peak_rss_kib',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__=='__main__':main()
