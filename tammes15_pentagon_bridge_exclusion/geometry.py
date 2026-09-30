"""Exact two-orientation maps for arbitrary marked B ears."""
from patches import unfolding,dot,t,one,zero,H
HI=[[(one/(one-t) if i==j else zero)-t/((one-t)*(one+2*t)) for j in range(3)] for i in range(3)]
DH=(one-t)**2*(one+2*t)

def cross(x,y):
    return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]

def matvec(m,x):
    return [sum((a*b for a,b in zip(row,x)),zero) for row in m]

def to_field(f,x):
    return f.div(f.element(x.n),f.element(x.d))

def sum_field(f,terms):
    result=f.zero
    for term in terms:result=f.add(result,term)
    return result
from polynomial import need


def b_constants(model):
    b=model['B'];p,q=b['ears'];k=b['kappa'];bcross=cross(b['b'][p],b['b'][q])
    betas={j:(dot(x,b['b'][p]),dot(x,b['b'][q])) for j,x in b['b'].items()}
    lambdas={j:DH*sum((x*y for x,y in zip(vector,bcross)),zero)/(one-k*k) for j,vector in b['b'].items()}
    return betas,lambdas


def branch_rat(model,case,orientation):
    n=model['n'];u,v=case['u'],case['v'];k=model['B']['kappa'];normal=matvec(HI,cross(u,v))
    betas,lambdas=b_constants(model);result={}
    for j in model['B']['b']:
        b1,b2=betas[j];c1=(b1-k*b2)/(one-k*k);c2=(b2-k*b1)/(one-k*k)
        result[j+n]=[c1*x+c2*y+orientation*lambdas[j]*z for x,y,z in zip(u,v,normal)]
    return {**model['A']['a'],**result}


def branch_field(model,case,orientation,f):
    n=model['n']
    a={i:tuple(to_field(f,x) for x in v) for i,v in model['A']['a'].items()}
    u,v=[tuple(to_field(f,x) for x in vector) for vector in (case['u'],case['v'])]
    k=to_field(f,model['B']['kappa']);den=f.sub(f.one,f.mul(k,k))
    raw=[f.sub(f.mul(u[1],v[2]),f.mul(u[2],v[1])),f.sub(f.mul(u[2],v[0]),f.mul(u[0],v[2])),f.sub(f.mul(u[0],v[1]),f.mul(u[1],v[0]))]
    hi=[[to_field(f,x) for x in row] for row in HI]
    normal=[sum_field(f,(f.mul(x,y) for x,y in zip(row,raw))) for row in hi]
    betas,lambdas=b_constants(model);b={}
    for j in model['B']['b']:
        b1,b2=(to_field(f,x) for x in betas[j])
        c1=f.div(f.sub(b1,f.mul(k,b2)),den);c2=f.div(f.sub(b2,f.mul(k,b1)),den)
        magnitude=f.mul(f.number(orientation),to_field(f,lambdas[j]))
        b[j+n]=tuple(sum_field(f,(f.mul(c1,x),f.mul(c2,y),f.mul(magnitude,z))) for x,y,z in zip(u,v,normal))
    p,q=model['B']['ears']
    need(b[p+n]==u and b[q+n]==v,'fixed B ears')
    anchors,_=unfolding(model['B']['edges'],5)
    need(all(f.dot(b[i+n],b[j+n])==(f.one if i==j else f.t) for i in anchors for j in anchors if i<=j),'B anchor Gram')
    return {**a,**b}
