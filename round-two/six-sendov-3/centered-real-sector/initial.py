"""Regenerate the exact initial data; no prior checker or fixture is imported."""
from fractions import Fraction as F
from itertools import permutations

from arithmetic import K, require
from series import series_ring
from system import system


def constants():
    c=K((0,1,0));d=2*c*c-1
    y0=1/(3*(1+c));H=14*y0;U=-8*(F(2,3)-y0);rho=(c-5)/3
    x=(U+rho*H)/8;y=x-rho*H/2
    values=[x,y,H/2,K((-F(1,6),-F(4,3),F(4,3))),
            K((-F(1,3),F(1,3),0)),H/4-1-y]
    return c,d,values


def inverse(matrix):
    n=len(matrix)
    rows=[list(row)+[K(int(i==j)) for j in range(n)] for i,row in enumerate(matrix)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if rows[i][j]!=0),None)
        require(pivot is not None,'exact initial matrix has a pivot')
        rows[j],rows[pivot]=rows[pivot],rows[j]
        scale=rows[j][j];rows[j]=[v/scale for v in rows[j]]
        for i in range(n):
            if i!=j:
                scale=rows[i][j]
                rows[i]=[v-scale*w for v,w in zip(rows[i],rows[j])]
    result=[row[n:] for row in rows]
    for a,b in ((result,matrix),(matrix,result)):
        for i in range(n):
            for j in range(n):
                require(sum((a[i][k]*b[k][j] for k in range(n)),K(0))==int(i==j),
                        'every entry of both exact inverse products')
    return result


def determinant(matrix):
    n=len(matrix);rows=[list(row) for row in matrix];ans=K(1)
    for j in range(n):
        pivot=next((i for i in range(j,n) if rows[i][j]!=0),None)
        require(pivot is not None,'nonzero full initial determinant')
        if pivot!=j:
            rows[j],rows[pivot]=rows[pivot],rows[j];ans=-ans
        scale=rows[j][j];ans*=scale
        for i in range(j+1,n):
            scale2=rows[i][j]/scale
            rows[i]=[v-scale2*w for v,w in zip(rows[i],rows[j])]
    return ans


def permutation_determinant(matrix):
    ans=K(0);count=0;n=len(matrix)
    for p in permutations(range(n)):
        term=K(1)
        for i,j in enumerate(p):
            term*=matrix[i][j]
            if term==0:
                break
        if term!=0:
            count+=1
            parity=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2
            ans+=-term if parity else term
    return ans,count


def exact_initial(damage=None):
    c,d,values=constants()
    if damage=='initial-phase':
        values[3]+=F(1,1000)
    columns=[]
    Dual=series_ring(1,K);S=series_ring(2,Dual);eta=S([0,1])
    for axis in range(6):
        variables=[S(Dual([v,int(axis==j)])) for j,v in enumerate(values)]
        equations,aux=system(eta,variables,c)
        for eq in equations:
            require(eq.a[0]==0,'literal eta divisibility at the exact initial point')
            require(eq.a[1].a[0]==0,'every initial divided equation vanishes')
        if axis<3:
            if damage=='scaled-partial' and axis==0:
                aux['partials'][0][8]+=1
            for j in range(10):
                scaled=eta*aux['partials'][axis][j]
                require(all(aux['poly'][j].a[k].a[1]==scaled.a[k].a[0] for k in range(3)),
                        'literal scaled partial matches separate series differentiation')
        columns.append([eq.a[1].a[1] for eq in equations])
    jac=[list(row) for row in zip(*columns)]
    if damage=='initial-jacobian':
        jac[5][0]+=1
    det=determinant(jac);det2,terms=permutation_determinant(jac)
    desired=-F(8264970432,49)*(1+F(13,2)*c+7*c*c)
    require(det==det2==desired,'Gaussian and definition-level full determinant')
    Y=inverse(jac)
    B=[row[1:] for row in jac[:5]];invB=inverse(B)
    tail=[sum((invB[i][j]*(-jac[j][0]) for j in range(5)),K(0)) for i in range(5)]
    require(tail==[K(-3),K(0),K(0),K(0),K(3)],'five-constraint exact initial tangent')
    schur=jac[5][0]+sum((a*b for a,b in zip(jac[5][1:],tail)),K(0))
    cross=81*(3*(c+d)/56)*108/(1-c*c)
    require(schur==24*cross==F(629856,7)*(c+c*c),'initial scalar curvature24')
    record={'variables':['x','y','T','xi3','xi4','omega'],
            'values':[v.record() for v in values],
            'jacobian':[[v.record() for v in row] for row in jac],
            'inverse':[[v.record() for v in row] for row in Y],
            'five_block_inverse':[[v.record() for v in row] for row in invB],
            'determinant':det.record(),'nonzero_permutation_terms':terms,
            'constraint_tangent_tail':[v.record() for v in tail],
            'scalar_schur':schur.record(),'initial_curvature_factor':cross.record()}
    return values,jac,Y,invB,record
