#!/usr/bin/env python3
"""Decode literal mathematical trees; no search, compression or float arithmetic.

An internal node [edge,left,right] records both closed midpoint children.
A negative integer -1-i names leaf i. Stress rows are seven small integers,
not precomputed coefficients. The exact checker recomputes every sign.
"""
from pathlib import Path
import argparse,hashlib,itertools,json
HERE=Path(__file__).resolve().parent
EDGES=list(itertools.combinations(range(4),2))
def require(b,s):
    if not b:raise ValueError(s)
def decode(cell,config):
    cfg=config['cells'][str(cell)];p=HERE/cfg['forest_file'];raw=p.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==cfg['forest_input_sha256'],'literal tree input fingerprint')
    x=json.loads(raw)
    require(set(x)=={'schema','cell_id','ratio','edges','stress_rows','receiver_patterns','leaf_stress_rows','root_trees'},'exact transparent tree schema')
    require(x['schema']=='closed-midpoint-source-trees-v1'and x['cell_id']==cell and x['ratio']==cfg['ratio'],'literal named receiving cell and source core')
    cert=json.loads((HERE/'local_certificate.json').read_text())
    actual_edges=sorted({tuple(c[:2])for d in cert['duals']for c in d['contacts']})
    require(x['edges']==list(map(list,actual_edges)),'every labelled directed support is from the actual current contact certificate')
    fans=[str(i)for i in range(len(cfg['receiver_triangle_indices']))]
    for pattern in x['receiver_patterns']:
        require(type(pattern)==list and pattern==sorted(set(pattern)),'literal ordered distinct receiving paths')
        for fan in fans:
            paths=[p for p in pattern if type(p)==str and p[:1]==fan]
            require(paths==[fan]or paths==[fan+str(i)for i in range(4)],'every closed receiving fan occurs whole or in ALL four children')
        require(all(p[:1]in fans and len(p)in(1,2)and all(z in'0123'for z in p[1:])for p in pattern),'no extraneous receiving path')
    for s in x['stress_rows']:
        require(type(s)==list and len(s)==7 and all(type(a)==int for a in s),'seven literal physical stress integers')
        require(s[0]in(-1,1)and len(set(s[1:4]))==3 and all(0<=a<len(actual_edges)for a in s[1:4])and all(0<=a<92 for a in s[4:]),'actual stress orientation, distinct supports and original moving vertices')
    roots=[]
    for no,face in enumerate(config['source_faces']):
        for i in range(1,4):
            for part in range(3):roots.append(dict(face=no,face_triangle=[face[0],face[i],face[i+1]],frustum_part=part))
    require(len(roots)==len(x['root_trees'])==108,'all canonical closed source frustum roots')
    leaves=[None]*len(x['leaf_stress_rows']);splits=0
    def visit(node,root,path):
        nonlocal splits
        require(len(path)//3<=cfg['source_depth_limit'],'declared unchanged source depth')
        if type(node)==int:
            index=-1-node;require(node<0 and 0<=index<len(leaves)and leaves[index]is None,'exactly one terminal occurrence of every source leaf')
            row=x['leaf_stress_rows'][index]
            require(type(row)==list and row and all(type(a)==int for a in row),'literal receiving pattern and stress indices')
            require(0<=row[0]<len(x['receiver_patterns']),'actual receiving pattern')
            pattern=x['receiver_patterns'][row[0]]
            require(len(row)==1+len(pattern)and all(0<=a<len(x['stress_rows'])for a in row[1:]),'one selected physical stress per declared closed receiving piece')
            ss=[]
            for p,no in zip(pattern,row[1:]):
                s=x['stress_rows'][no]
                ss.append(dict(receiver_triangle=int(p[0]),receiver_path=p,cofactor_orientation=s[0],edges=[list(actual_edges[i])for i in s[1:4]],moving_originals=s[4:]))
            leaves[index]=dict(root=root,path=path,depth=len(path)//3,kind='three_support_stress',receiver_stresses=ss);return
        require(type(node)==list and len(node)==3 and type(node[0])==int and 0<=node[0]<6,'internal node specifies one literal edge and BOTH children')
        splits+=1;a,b=EDGES[node[0]]
        for child in range(2):visit(node[1+child],root,path+str(a)+str(b)+str(child))
    for root,node in enumerate(x['root_trees']):visit(node,root,'')
    require(all(l is not None for l in leaves)and len(leaves)==cfg['source_leaves']and splits==cfg['source_midpoint_nodes']and len(leaves)-splits==108,'entire exact labelled forest, no omitted leaf/root')
    require(sum(len(l['receiver_stresses'])for l in leaves)==cfg['receiving_stress_pieces'],'complete declared source/receiving product count')
    return dict(status='LITERAL_CLOSED_SOURCE_FOREST',ratio=cfg['ratio'],faces=config['source_faces'],roots=roots,leaves=leaves,pending=0,failed_leaves=[],receiver_triangle_indices=cfg['receiver_triangle_indices'],subdivisions=splits)
def main(args):
    config=json.loads((HERE/'configuration.json').read_text());f=decode(args.cell,config);raw=(json.dumps(f,indent=2,sort_keys=True)+'\n').encode()
    if 'expanded_forest_sha256'in config['cells'][str(args.cell)]:require(hashlib.sha256(raw).hexdigest()==config['cells'][str(args.cell)]['expanded_forest_sha256'],'entire decoded forest fingerprint')
    p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    print(json.dumps(dict(cell=args.cell,source_roots=108,leaves=len(f['leaves']),midpoint_nodes=f['subdivisions'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cell',type=int,required=True,choices=(22,));p.add_argument('--output',required=True);main(p.parse_args())
