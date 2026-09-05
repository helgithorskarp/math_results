#!/usr/bin/env python3
"""Direct eight-basis integer geometry for the two 26-contact realizations."""
from pathlib import Path
from hashlib import sha256
from itertools import permutations
import importlib.util,json

HERE=Path(__file__).resolve().parent
PATH=HERE.parent/'hadwiger_nelson_mixed505_anchor0/check_example.py'
if sha256(PATH.read_bytes()).hexdigest()!='1eb7d3d376eb7eabd52019c66083a38699d40b289e6b4b7967c0c29971e6150c':
    raise ValueError('integer radical helper pin mismatch')
spec=importlib.util.spec_from_file_location('radicals',PATH)
R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)


def point(a):
    x,b,c,d=a
    return R.basis(k0=x,k6=b),R.basis(k2=c,k4=d)


def main():
    A=R.read_points(159);V=R.read_points(214)
    # Integer numerators: t has denominator 6, A and V denominator 12.
    t=(R.basis(k0=5),R.basis(k4=1))
    original=[tuple(R.scale(z,6) for z in point(a)) for a in A]
    rotated=[R.complex_multiply(t,point(a)) for a in A]
    B=list(dict.fromkeys(original+rotated))
    R.require(len(B)==292 and B[0]==(R.ZERO,R.ZERO),'incorrect inner union')
    example=json.loads((HERE/'maximum_example.json').read_text())
    q=example['anchor'];R.require(q==10 and V[q]==(0,0,2,0),'wrong anchor')
    R.require(example['T']==['-1/3','0','0','1/3'] and
              example['W']==['-5/6','0','0','-1/6'],'wrong example polynomial')
    H=[point(tuple(x-y for x,y in zip(v,V[q]))) for v in V]
    labels=[j for j in range(214) if j!=q]
    libB=R.read_colors(HERE.parent/'hadwiger_nelson_nonmono159_moser_triple/colors_B.txt',
                      292,'b9285f2967686bf5458588c6f949173ac8795412a7ffd94a60d687e5a8c260a3')
    libV=R.read_colors(HERE.parent/'hadwiger_nelson_mixed505_anchor0/colors_H.txt',
                      214,'25a072d1c55cef2318b76cd849ce3096091d25b37981c83bc11d00c416393b58')
    perms=[(0,)+p for p in permutations((1,2,3))]
    results=[]
    for epsilon in (-1,1):
        u=(R.basis(k0=-1,k5=-epsilon),R.basis(k4=1,k1=-epsilon))
        R.require(R.norm(u)==R.basis(k0=36),'multiplier is not unit')
        T=(R.basis(k0=-2),R.basis(k4=2));W=(R.basis(k0=-5),R.basis(k4=-1))
        uu,Tu=R.complex_multiply(u,u),R.complex_multiply(T,u)
        R.require(all(R.add(R.add(uu[k],R.scale(Tu[k],-1)),R.scale(W[k],6))==R.ZERO
                      for k in (0,1)),'multiplier fails quadratic')
        image=[R.complex_multiply(u,h) for h in H]
        R.require(image[q]==(R.ZERO,R.ZERO),'misplaced anchor')
        points=B+[image[j] for j in labels]
        R.require(len(points)==len(set(points))==505,'unexpected point overlap')
        edges=[];cross=[];left=right=0
        for i,(x,y) in enumerate(points):
            for j in range(i+1,len(points)):
                X,Y=points[j]
                delta=(R.add(x,R.scale(X,-1)),R.add(y,R.scale(Y,-1)))
                if R.norm(delta)!=R.basis(k0=72**2):continue
                edges.append((i,j))
                if j<292:left+=1
                elif i==0 or i>=292:right+=1
                else:cross.append((i,labels[j-292]))
        R.require((len(edges),left,right,len(cross))==(2254,1251,977,26),'incorrect strict edge set')
        R.require(cross==[tuple(e) for e in example['cross_edges']],'incorrect maximum cross-edge class')
        witness=None
        for ib,cb in enumerate(libB):
            for iv,cv in enumerate(libV):
                for ip,perm in enumerate(perms):
                    colors=cb+tuple(perm[cv[j]^cv[q]] for j in labels)
                    if all(colors[i]!=colors[j] for i,j in edges):
                        witness=(ib,iv,ip);break
                if witness is not None:break
            if witness is not None:break
        R.require(witness is not None,'no proper coloring for direct graph')
        results.append({'epsilon':epsilon,'anchor':q,'vertices':505,'strict_unit_edges':len(edges),
                        'new_cross_edges':len(cross),'coloring_witness':witness,
                        'edge_sha256':sha256(json.dumps(edges).encode()).hexdigest(),
                        'color_sha256':sha256(bytes(colors)).hexdigest()})
    print(json.dumps({'real_radicals':[2,3,11],'coordinate_scale':72,
                      'all_pairs_per_realization':127260,'unit_and_quadratic_checked':True,
                      'proper_colorings_checked':True,'realizations':results},indent=2))


if __name__=='__main__':main()
