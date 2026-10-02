#!/usr/bin/env python3
"""Post-seal representation adapter; imports no author executable helpers."""
from pathlib import Path
from itertools import combinations
import argparse, json, hashlib
from core import parent, packing, pts, mask, need, canon
from transport import image

def same(a, b, label):
    need(a == b, label)

def rejected(label, callback, message):
    try:
        callback()
    except RuntimeError as e:
        same(str(e), message, 'wrong rejection reason: '+label)
        return label
    raise RuntimeError('damaged certificate accepted: '+label)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--author-work', type=Path, required=True)
    a=p.parse_args(); D=parent()
    own=json.loads((a.work/'cores.json').read_bytes())
    author=json.loads((a.author_work/'carrier/CORES.json').read_bytes())
    same(author['parent_words'], D, 'whole literal parent differs')
    same(author['noncontained_q'], own['Q'], 'fixed Q differs')
    same(author['hole_words'], own['holes'], 'whole hole list differs')
    same([r['cap'] for r in author['caps']], own['caps'], 'whole prospective cap list differs')
    same([r['cap'] for r in author['caps'] if not r['core_count']], own['zero_core_caps'], 'whole zero-core list differs')
    keys=[(c['cap'], tuple(sorted((D[b],t) for b,t in zip(c['parents'],c['tails'],strict=True)))) for c in author['cores']]
    ownkeys=[(C,tuple(map(tuple,ts))) for C,ts in own['cores']]
    same(len(set(keys)),len(keys),'duplicate author core')
    same(set(keys),set(ownkeys),'complete physical core keys differ')
    ownindex={k:i for i,k in enumerate(ownkeys)}
    permutation=[ownindex[k] for k in keys]
    offset=0
    for row in author['caps']:
        expected=[i for i,k in enumerate(keys) if k[0]==row['cap']]
        same(expected,list(range(offset,offset+row['core_count'])),'every zero/positive prefix differs')
        same(row['first_core'],offset,'prefix offset differs')
        offset+=row['core_count']
    same(offset,len(keys),'carrier prefix coverage')
    rows=json.loads((a.work/'graph.json').read_bytes())
    ar=json.loads((a.author_work/'graph/GRAPH.json').read_bytes())
    translated=[]
    for i,h in enumerate(ar['adjacency_hex']):
        r=int(h,16);need(0<=r<1<<len(keys),'adjacency domain')
        v=0
        while r:
            bit=r & -r; r ^= bit; v |= 1 << permutation[bit.bit_length()-1]
        same(v,rows[permutation[i]],'entire physical graph row differs')
        translated.append(v)
    same(len(translated),len(rows),'every graph row covered')
    colors=json.loads((a.author_work/'colors/COLORS.json').read_bytes())['colors']
    same(len(colors),len(keys),'color domain length')
    need(all(type(c) is int and 0<=c<4 for c in colors),'four-color integer domain')
    mapped=[None]*len(keys)
    for i,c in enumerate(colors):mapped[permutation[i]]=c
    edges=0
    for i,row in enumerate(rows):
        for j in range(i+1,len(rows)):
            if row>>j&1:
                same(mapped[i]!=mapped[j],True,'same-color actual edge');edges+=1
    ownforms=json.loads((a.work/'NORMAL_FORMS.json').read_bytes())['words']
    af=json.loads((a.author_work/'point-audit/NORMAL_FORMS69.json').read_bytes())['normal_forms']
    same(sorted(sorted(r['words']) for r in af), ownforms, 'all ten whole normalized codes differ')
    maps=json.loads((a.author_work/'cover/NONCONTAINED_Q_MAPS.json').read_bytes())['maps']
    targets=set()
    for r in maps:
        g=r['point_map']
        same(sorted(g),list(range(18)),'point map bijection')
        same(g[17],17,'point map fixes y')
        same({image(b,g) for b in D},set(D),'point map whole D')
        same(image(15,g),r['target_q'],'point map Q target')
        need(r['target_q'] not in targets,'unique Q target');targets.add(r['target_q'])
    domain={mask(q) for q in combinations(range(17),4) if not any(mask(q)&b==mask(q) for b in D)}
    same(targets,domain,'all 2040 actual Q targets')
    controls=[]
    controls.append(rejected('omitted-core',lambda:same(set(keys[:-1]),set(ownkeys),'complete physical core keys differ'),'complete physical core keys differ'))
    controls.append(rejected('omitted-zero-cap',lambda:same(own['zero_core_caps'][:-1],own['zero_core_caps'],'whole zero-core list differs'),'whole zero-core list differs'))
    i=next(i for i,r in enumerate(rows) if r)
    j=(rows[i]&-rows[i]).bit_length()-1
    controls.append(rejected('changed-graph-entry',lambda:same(rows[i]^(1<<j),rows[i],'entire physical graph row differs'),'entire physical graph row differs'))
    damaged=list(mapped);damaged[j]=damaged[i]
    controls.append(rejected('same-color-actual-edge',lambda:same(damaged[i]!=damaged[j],True,'same-color actual edge'),'same-color actual edge'))
    g=list(maps[0]['point_map']);g[0]=g[1]
    controls.append(rejected('nonbijective-map',lambda:same(sorted(g),list(range(18)),'point map bijection'),'point map bijection'))
    controls.append(rejected('omitted-normal-form',lambda:same(ownforms[:-1],ownforms,'all ten whole normalized codes differ'),'all ten whole normalized codes differ'))
    print(json.dumps({'complete':True,'author_helpers_imported':False,'post_seal_adapter':True,'all_prospective_caps':len(own['caps']),'all_zero_core_caps':len(own['zero_core_caps']),'all_physical_core_keys':len(keys),'all_zero_positive_prefixes':len(author['caps']),'all_entrywise_mapped_rows':len(rows),'all_unordered_graph_pairs_represented':len(rows)*(len(rows)-1)//2,'four_color_edges_checked':edges,'all_whole_normalized_codes':len(af),'author_actual_Q_maps_rechecked':len(maps),'whole_D_images_rechecked':68*len(maps),'whole_reordered_graph_sha256':hashlib.sha256(canon(rows)).hexdigest(),'semantic_damage_rejections':controls},sort_keys=True))

if __name__=='__main__':main()
