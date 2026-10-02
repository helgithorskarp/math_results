#!/usr/bin/env python3
"""FLOATING tetrahedral discovery for an outer proper-body source shell.

Certificates are candidates until exact reconstruction, covering and every
tensor Bernstein sign have passed. A stopped tree leaves undecided regions.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json,resource,time
import numpy as np
import proposal as D

def prepare():
    points,polygon,cert,facets,vertices=D.load()
    raw=np.c_[np.ones(len(polygon)),polygon];middle=np.r_[1.,polygon.mean(axis=0)]
    actual=json.loads(D.GEOMETRY.read_text())
    edges=np.array([row['edge']for row in actual['actual_edge_rows']],dtype=int)
    directions=points[edges[:,1]]-points[edges[:,0]]
    normals=np.cross(directions[None,:,:],raw[:,None,:])
    heights=np.einsum('vei,ei->ve',normals,points[edges[:,0]])
    triples=[];weights=[];orientations=[]
    for triple in itertools.combinations(range(len(edges)),3):
        i,j,k=triple
        W=np.array([np.cross(directions[j],directions[k]),np.cross(directions[k],directions[i]),np.cross(directions[i],directions[j])])
        w=raw@W.T
        orientation=1 if np.min(w)>1e-9 else(-1 if np.max(w)<-1e-9 else 0)
        if orientation:triples.append(triple);weights.append(orientation*w);orientations.append(orientation)
    r_pairs=[(i,j)for tri in actual['receiver_triangle_indices']for no,i in enumerate(tri)for j in tri[no:]]
    q_pairs=list(itertools.combinations_with_replacement(range(4),2))
    faces=actual['source_faces']
    if not triples:raise ValueError('No strictly positive whole-quadrilateral cofactor proposals; no theorem')
    return dict(points=points,raw=raw,edges=edges,directions=directions,normals=normals,
                heights=heights,middle=middle,triples=np.array(triples,dtype=int),
                weights=np.array(weights),orientations=orientations,r_pairs=r_pairs,q_pairs=q_pairs,
                facets=facets,vertices=vertices,faces=faces,receiver_triangles=actual['receiver_triangle_indices'])

def find(data,tet):
    points,normal,h=data['points'],data['normals'],data['heights']
    center=tet.mean(axis=0)
    q1=tet[[i for i,j in data['q_pairs']]];q2=tet[[j for i,j in data['q_pairs']]]
    dot=np.einsum('ki,ki->k',q1,q2)
    w=data['weights'];choices=[]
    for tri,ids in enumerate(data['receiver_triangles']):
        receiver_center=data['raw'][ids].mean(axis=0)
        moving=np.argmax(D.cayley(points,center)@np.cross(data['directions'],receiver_center).T,axis=0)
        P=points[moving]
        transformed=((1-dot)[None,:,None]*P[:,None,:]
                     +np.einsum('ei,ki->ek',P,q2)[:,:,None]*q1[None,:,:]
                     +np.einsum('ei,ki->ek',P,q1)[:,:,None]*q2[None,:,:]
                     +np.cross((q1+q2)[None,:,:],P[:,None,:]))
        gap=h[:,:,None]*(1+dot)-np.einsum('vei,eki->vek',normal,transformed)
        g=gap[:,data['triples'],:].transpose(1,0,2,3)
        coeff=[]
        for a,b in data['r_pairs'][tri*6:(tri+1)*6]:
            coeff.append(.5*(np.einsum('ki,kij->kj',w[:,a],g[:,b])+np.einsum('ki,kij->kj',w[:,b],g[:,a])))
        worst=np.max(np.array(coeff),axis=(0,2));no=int(np.argmin(worst))
        choices.append(dict(receiver_triangle=tri,triple_index=no,
                edges=data['edges'][data['triples'][no]].tolist(),
                moving_originals=moving[data['triples'][no]].tolist(),
                cofactor_orientation=data['orientations'][no],
                maximum_floating_bernstein_coefficient=float(worst[no])))
    return max(c['maximum_floating_bernstein_coefficient']for c in choices),dict(receiver_stresses=choices)

def run(args):
    started=time.monotonic();deadline=started+args.seconds
    data=prepare();vertices=data['vertices'];ratio=float(F(args.ratio))
    if not 0<ratio<1:raise ValueError('Source shell ratio')
    stack=[];roots=[]
    for fno,face in enumerate(data['faces']):
        for i in range(1,4):
            ids=[face[0],face[i],face[i+1]];A,B,C=vertices[ids]
            for part,tet in enumerate([[ratio*A,ratio*B,ratio*C,C],[ratio*A,ratio*B,B,C],[ratio*A,A,B,C]]):
                tag=dict(face=fno,face_triangle=ids,frustum_part=part)
                no=len(roots);roots.append(tag)
                stack.append((np.array(tet),no,'',0))
    leaves=[];failed=[];processed=0;subdivisions=0
    while stack and processed<args.nodes and time.monotonic()<deadline:
        tet,root,path,depth=stack.pop();processed+=1
        margin,candidate=find(data,tet)
        if margin<-args.margin:
            leaves.append(dict(root=root,path=path,depth=depth,kind='three_support_stress',maximum_floating_bernstein_coefficient=margin,**candidate))
        elif depth>=args.depth:
            failed.append(dict(root=root,path=path,depth=depth,maximum_floating_bernstein_coefficient=margin))
        else:
            pairs=list(itertools.combinations(range(4),2))
            a,b=max(pairs,key=lambda ij:np.linalg.norm(tet[ij[0]]-tet[ij[1]]))
            # Record the actual chosen edge: longest-edge decisions are FLOATING.
            midpoint=(tet[a]+tet[b])/2
            first=tet.copy();first[b]=midpoint
            second=tet.copy();second[a]=midpoint
            suffix=f'{a}{b}'
            stack.append((second,root,path+suffix+'1',depth+1))
            stack.append((first,root,path+suffix+'0',depth+1));subdivisions+=1
    portable=[]
    for leaf in leaves:
        z={k:leaf[k]for k in ('root','path','depth','kind')}
        if leaf['kind']=='three_support_stress':z['receiver_stresses']=[{k:s[k]for k in ('receiver_triangle','edges','moving_originals','cofactor_orientation')}for s in leaf['receiver_stresses']]
        portable.append(z)
    out=dict(status='FLOATING_SHELL_COVER_CANDIDATE_COMPLETE'if not stack and not failed else 'FLOATING_SHELL_COVER_INCOMPLETE',
             ratio=args.ratio,faces=data['faces'],roots=roots,leaves=portable,failed_leaves=failed,pending=len(stack),pending_nodes=[dict(root=root,path=path,depth=depth,source_tetrahedron=tet.tolist())for tet,root,path,depth in stack],processed_nodes=processed,subdivisions=subdivisions,receiver_triangle_indices=data['receiver_triangles'],positive_cofactor_triple_count=len(data['triples']))
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    digest=hashlib.sha256(Path(args.output).read_bytes()).hexdigest()
    config=json.loads((Path(__file__).resolve().parent/'configuration.json').read_text())
    if digest!=config['expected_forest_sha256']:raise ValueError('Different or incomplete source proposal forest; no reproduced certificate')
    print(json.dumps(dict(status=out['status'],leaves=len(leaves),subdivisions=subdivisions,sha256=digest,elapsed_seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ratio',default='1/21');p.add_argument('--seconds',type=float,default=40.)
    p.add_argument('--nodes',type=int,default=10000);p.add_argument('--depth',type=int,default=18)
    p.add_argument('--margin',type=float,default=1e-10);p.add_argument('--output',default=str(Path(__file__).resolve().parent/'.generated/forest.json'))
    run(p.parse_args())
