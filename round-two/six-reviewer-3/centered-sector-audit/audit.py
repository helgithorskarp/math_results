#!/usr/bin/env python3
"""Independent full third-tensor centered-real response on a proved branch."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact_numbers import K,I,need,embedding,enclose,up,down,chebyshev,evaluate,derivative
from third import T
from system import system
from controls import run as controls

HERE=Path(__file__).resolve().parent


def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()


def inverse(matrix,scalar):
    n=len(matrix);rows=[list(r)+[scalar(int(i==j)) for j in range(n)] for i,r in enumerate(matrix)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if rows[i][j]!=0),None);need(pivot is not None,'inverse pivot')
        rows[j],rows[pivot]=rows[pivot],rows[j];scale=rows[j][j];rows[j]=[x/scale for x in rows[j]]
        for i in range(n):
            if i!=j:
                factor=rows[i][j];rows[i]=[x-factor*y for x,y in zip(rows[i],rows[j])]
    out=[r[n:] for r in rows]
    for a,b in ((matrix,out),(out,matrix)):
        need(all(sum((a[i][k]*b[k][j] for k in range(n)),scalar(0))==int(i==j) for i in range(n) for j in range(n)),'every entry of both inverse products')
    return out


def constants():
    c=K((0,1,0));y0=1/(3*(1+c));H=14*y0;U=-8*(F(2,3)-y0);h=(c-5)/3
    x=(U+h*H)/8;y=x-h*H/2
    return c,[x,y,H/2,K((-F(1,6),-F(4,3),F(4,3))),(c-1)/3,H/4-1-y]


def initial():
    c,values=constants();G,U,_=system(T.variable(K(0),0),[T.variable(x,i+1) for i,x in enumerate(values)],c)
    B0=[[K(g.h.get((0,i+1),0)) for i in range(1,6)] for g in G]
    B1=[[K(g.t.get((0,0,i+1),0))/2 for i in range(1,6)] for g in G];Y=inverse(B0,K)
    U0=[K(u.v) for u in U];U1=[K(u.g.get(0,0)) for u in U];w0=list(map(K,(0,1,0,0,F(1,2))))
    ts=chebyshev([0,1]);us=chebyshev([0,2]);affine=[];force_formula=[]
    for phase in (K(-F(1,2)),-c):
        need(evaluate(us[8],phase)==0,'both fixed ninth-root phases')
        affine.append(([-F(9,4)*evaluate(us[7],phase),F(9,7)*evaluate(us[6],phase),evaluate(derivative(us[8]),phase)],[-F(9,4)*(evaluate(ts[8],phase)-1),F(9,7)*(evaluate(ts[7],phase)-1)]))
        force_formula.append((-F(9,7)*evaluate(us[6],phase),-F(9,7)*(evaluate(ts[7],phase)-1)))
    formula=[[*affine[0][0],K(0),K(0)],
             [*affine[1][0][:2],K(0),affine[1][0][2],K(0)],
             [*affine[0][1],K(0),K(0),K(0)],
             [*affine[1][1],K(0),K(0),K(0)],list(map(K,(2,-1,0,0,2)))]
    need(B0==formula,'all twenty-five entries of universal affine first-order block')
    need(U0==[force_formula[0][0],force_formula[1][0],force_formula[0][1],force_formula[1][1],K(0)],'all five initial forcing entries from the direct closed primitive')
    need(all(sum((a*b for a,b in zip(r,w0)),K(0))==-u for r,u in zip(B0,U0)),'universal initial split response')
    rhs=[-u-sum((a*b for a,b in zip(r,w0)),K(0)) for r,u in zip(B1,U1)]
    w1=[sum((a*b for a,b in zip(r,rhs)),K(0)) for r in Y]
    ell=6*(1+values[0])+2*values[5]-2*w1[-1]
    need(ell==K((-F(4441,540),F(7046,135),-F(2288,45))),'credited exact9033/9080 asymptotic coefficient')
    for j in range(3):
        v=[K(F((i+2)*(j+1),i+j+3)) for i in range(6)]
        gc,uc,_=system(T.variable(K(0),0),[T.variable(x,i+1) for i,x in enumerate(v)],c)
        need([[K(g.h.get((0,i+1),0)) for i in range(1,6)] for g in gc]==B0 and [K(u.v) for u in uc]==U0,'generic-parameter affine block and initial forcing')
    record={'initial_five_block':[[x.record() for x in r] for r in B0],'initial_five_block_eta_derivative':[[x.record() for x in r] for r in B1],'initial_five_block_inverse':[[x.record() for x in r] for r in Y],'initial_forcing':[x.record() for x in U0],'initial_forcing_eta_derivative':[x.record() for x in U1],'initial_response':[x.record() for x in w0],'initial_response_eta_derivative':[x.record() for x in w1],'reviewed_ell':ell.record()}
    return values,Y,w0,w1,record


def matvec(m,v):return [sum((a*b for a,b in zip(r,v)),I(0)) for r in m]


def certify(values,Yfield,w0field,w1field,radius):
    c=embedding();center=[enclose(x,c) for x in values];box=[x+I(-radius,radius) for x in center];epsilon=F(1,65536);eta=T.variable(I(0,epsilon),0)
    G,U,aux=system(eta,[T.variable(x,i+1) for i,x in enumerate(box)],c)
    B=[[I(g.h.get((0,i+1),0)) for i in range(1,6)] for g in G]
    B1=[[I(g.t.get((0,0,i+1),0))/2 for i in range(1,6)] for g in G];U1=[I(u.g.get(0,0)) for u in U]
    Y=[[enclose(x,c) for x in r] for r in Yfield];w0=[enclose(x,c) for x in w0field];wstar=[enclose(x,c) for x in w1field]
    defect=[[I(int(i==j))-sum((Y[i][k]*B[k][j] for k in range(5)),I(0)) for j in range(5)] for i in range(5)]
    D=[[up(x.absmax()) for x in r] for r in defect];beta=max(sum(r) for r in D);need(beta<1,'uniform first-five-block regularity')
    residual=[-u-v-z for u,v,z in zip(U1,matvec(B1,w0),matvec(B,wstar))];pre=matvec(Y,residual);rabs=[up(x.absmax()) for x in pre]
    scalar_error=up(max(rabs)/(1-beta))
    resolvent=inverse([[F(int(i==j))-D[i][j] for j in range(5)] for i in range(5)],F)
    need(all(x>=0 for r in resolvent for x in r),'nonnegative exact componentwise Neumann resolvent')
    errors=[up(sum(a*b for a,b in zip(r,rabs))) for r in resolvent];need(all(x<=scalar_error for x in errors),'componentwise response refines whole infinity error')
    response=[x+I(-e,e) for x,e in zip(wstar,errors)];et=eta.v;A=I(aux['A'].v);W=I(aux['W'].v);alpha=1+box[0];omega=box[5]
    need(A.lo>0 and W.lo>0,'positive physical curvature denominators')
    L=2*alpha*(3-3*et*alpha+et.square()*alpha.square())/(A**3)+omega*(2+et*omega)/W.square()-2*response[-1]/W.square()
    need(-5<L.lo<=L.hi<-3,'original centered-real curvature window')
    return {'parameter_radius':str(radius),'c_interval':c.record(),'center':[x.record() for x in center],'whole_box':[x.record() for x in box],'five_block_enclosure':[[x.record() for x in r] for r in B],'five_block_eta_difference_quotient_enclosure':[[x.record() for x in r] for r in B1],'forcing_eta_difference_quotient_enclosure':[x.record() for x in U1],'five_block_defect':[[x.record() for x in r] for r in defect],'absolute_defect_majorant':[[str(x) for x in r] for r in D],'five_block_beta_upper':str(beta),'preconditioned_response_residual':[x.record() for x in pre],'absolute_residual_majorant':list(map(str,rabs)),'scalar_response_error_upper':str(scalar_error),'nonnegative_componentwise_resolvent':[[str(x) for x in r] for r in resolvent],'componentwise_response_error_upper':list(map(str,errors)),'response_next_eta_coefficient_enclosure':[x.record() for x in response],'relative_curvature_difference_quotient':L.record()}


def main():
    p=argparse.ArgumentParser();p.add_argument('--emit-fixture',type=Path);p.add_argument('--fixture',type=Path,default=HERE/'EXPECTED.json');p.add_argument('--author-fixture',type=Path);args=p.parse_args()
    control=controls();values,Y,w0,w1,exact=initial();full=certify(values,Y,w0,w1,F(1,1024));tight=certify(values,Y,w0,w1,F(19,65536))
    need(F(full['five_block_beta_upper'])<F(1,50) and F(full['scalar_response_error_upper'])<F(9,20),'original full-box quantitative response margins')
    need(F(tight['relative_curvature_difference_quotient'][0])>-F(33,8) and F(tight['relative_curvature_difference_quotient'][1])<-F(129,32),'sharper whole effective centered-curvature window')
    strengthened={'relative_curvature_strict_interval':['-33/8','-129/32'],'least_eigenvalue_strict_lower':'eta^2*(1-(33/8)*eta)','least_eigenvalue_strict_upper':'eta^2*(1-(129/32)*eta)','local_stability_supremum_strict_lower':'1/2-(33/16)*eta','local_stability_supremum_strict_upper':'1/2-(129/64)*eta','common_real_eigenvalue_strict_eta2_coefficient':'15/4','squared_norm_split':2,'squared_norm_common':6,'parent_branch_box_dependency':'review9174 proved ||v(eta)-v0||<19eta for positive eta; no researcher estimate is a runtime calculation input'}
    record={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','method':'full seven-axis symmetric third derivative tensors; literal derivative-factor integration; exact Fraction intervals; nonnegative componentwise Neumann resolvent','eta_max':'1/65536','controls':control,'exact_initial_split':exact,'full_parent_cube':full,'review9174_certified19eta_box':tight,'strengthened_consequences':strengthened}
    if args.author_fixture:
        author=json.loads(args.author_fixture.read_text());need(canonical(exact)==canonical(author['initial']),'entire independent initial split algebraic record versus original')
    if args.emit_fixture:args.emit_fixture.write_text(json.dumps(record,indent=2)+'\n')
    else:need(canonical(record)==canonical(json.loads(args.fixture.read_text())),'entire independent frozen fixture')
    print('PASS independent centered-real third-tensor certificate',sha256(canonical(record)).hexdigest())
    print(json.dumps({'full':{k:full[k] for k in ('five_block_beta_upper','scalar_response_error_upper','componentwise_response_error_upper','relative_curvature_difference_quotient')},'tight':{k:tight[k] for k in ('five_block_beta_upper','scalar_response_error_upper','componentwise_response_error_upper','relative_curvature_difference_quotient')}},indent=2))


if __name__=='__main__':main()
