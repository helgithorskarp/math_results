"""Exact column producer for the P22 cover and selected nested certificates.

The finite cover is reconstructed separately by numeric exhaustive events.
No heuristic search, solver or suffix depth is used.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent
PINS={'fixture.json':'93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6',
      'generate.py':'08a37678a11392ed46907ab30b2463d841e3e068764c09e410244490f2212381',
      'NESTED.md':'3c291c8796cc7586db522d515098debf769482dc5b2d6bf8467fd8aa03322433'}
MINIMUM_STEMS=[[[1,2],[3,4],[1,3]],[[1,3],[2,4],[1,2]],[[1,4],[2,3],[1,2]]]
NAMES=['A','B','C']

def checked(name,pin):
    raw=(ROOT/name).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=pin:
        raise ValueError('published dependency changed: '+name)
    return raw

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
    return obj

for filename,pin in PINS.items():checked(filename,pin)
g=load('p22_columns',ROOT/'generate.py')
q=load('p22_nested_columns',ROOT/'nested_generate.py')
s=g.semantic

def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()

def compact_family(family):
    return {'low_count':family['low_count'],'high_count':family['high_count'],
            'envelope':family['envelope'],'records_sha256':digest(family['records']),
            'summary':family['summary']}

def ordinary(records):
    entries=sorted([r[0],r[1],r[2],r[3],r[4]] for r in records)
    classes={}
    for r in entries:
        tag=tuple(r[2:4]);classes[tag]=max(classes.get(tag,-1),r[4])
    return {'records_sha256':digest(entries),
            'envelope':[[*z,d] for z,d in sorted(classes.items())],
            'mass':sum(2**d for d in classes.values())}

def cover():
    native=json.loads(checked('fixture.json',PINS['fixture.json']))['gates']
    prefix=native[:22]
    data={name:s.analyze_family(13,prefix,l,h) for name,l,h in
          [('two_minima',2,0),('one_maximum',0,1),('two_maxima',0,2),('mixed_pair',1,1)]}
    high=g.anchors.aggregate(13,data,'high')
    roots=[]
    for name,stem in zip(NAMES,MINIMUM_STEMS):
        gates=prefix+[[11,12]]+stem
        low=s.analyze_family(13,gates,2,0)
        hi=s.analyze_family(13,gates,0,2)
        roots.append({'name':name,'minimum_stem':stem,'prefix26_sha256':digest(gates),
                      'two_minima':ordinary(low['records']),
                      'two_maxima':ordinary(hi['records']),
                      'ten_wire_image':g.target(13,gates,2,12)})
    kernels=list(g.kernels())
    images=[]
    for root in roots:
        if root['name']=='B':continue
        base=prefix+[[11,12]]+root['minimum_stem']
        for i,kernel in enumerate(kernels):
            gates=base+kernel
            images.append({'stem':root['name'],'kernel_id':i,'prefix32_sha256':digest(gates),
                           'nine_wire_image':g.target(13,gates,2,11)})
    return {'schema':'native22-complete-equality-cover-v1','agent':'six-sorting-2',
            'role':'researcher','parent_files_sha256':PINS,'n':13,'size_budget':44,
            'small_size_lower_bound':35,'prefix_length':22,'prefix22_sha256':digest(prefix),
            'prefix22_families':{name:compact_family(a) for name,a in data.items()},
            'prefix22_high_anchor':high,'minimum_stems':roots,
            'minimum_event_word_count':6,'maximum_event_word_count':900,
            'maximum_kernel_count':45,'maximum_kernels':kernels,
            'closed_native_matching':'B','alternate_root_count':90,'alternate_roots':images}

def nested():
    native=json.loads(checked('fixture.json',PINS['fixture.json']))['gates']
    selected=json.loads((ROOT/'p22-fixture.json').read_text())
    expected=[(name,i) for name in ['A','C'] for i in range(45)]
    if [(c['stem'],c['kernel_id']) for c in selected['cases']]!=expected:
        raise ValueError('alternate cover incomplete')
    kernels=list(g.kernels());cases=[]
    for c in selected['cases']:
        stem=MINIMUM_STEMS[NAMES.index(c['stem'])]
        gates=native[:22]+[[11,12]]+stem+kernels[c['kernel_id']]
        rows=[q.witness(gates,lo,hi) for lo,hi in c['original_clampings']]
        tags=[tuple(r['pruning']['outer_record'][2:4]) for r in rows]
        if len(set(tags))!=len(tags):raise ValueError('selected current tags repeat')
        mass=sum(2**r['nested_label'] for r in rows)
        if mass<=2**44:raise ValueError('selected mass does not exclude this root')
        cases.append({'stem':c['stem'],'kernel_id':c['kernel_id'],
                      'prefix32_sha256':digest(gates),'selected_domains':rows,
                      'selected_classes':len(tags),'selected_mass':mass,
                      'total_lower_bound':(mass-1).bit_length(),
                      'maximum_individual_label':max(r['nested_label'] for r in rows)})
    return {'schema':'native22-selected-nested-certificate-v1','agent':'six-sorting-2',
            'role':'researcher','parent_files_sha256':PINS,'selected_fixture_sha256':
            hashlib.sha256((ROOT/'p22-fixture.json').read_bytes()).hexdigest(),
            'cover_certificate_sha256':hashlib.sha256((ROOT/'p22-cover.json').read_bytes()).hexdigest(),
            'n':13,'l':3,'h':3,'free_inputs':7,'size_budget':44,'root_length':32,
            'alternate_root_count':90,'remaining_roots':[],'cases':cases}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['cover','roots']);args=parser.parse_args()
    start=time.monotonic();data=cover() if args.stage=='cover' else nested()
    path=ROOT/('p22-cover.json' if args.stage=='cover' else 'p22-nested.json')
    path.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'status':'NATIVE22_COLUMN_CERTIFICATE_REGENERATED',
                      'agent':'six-sorting-2','role':'researcher','stage':args.stage,
                      'bytes':path.stat().st_size,
                      'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                      'seconds':time.monotonic()-start,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))

if __name__=='__main__':main()
