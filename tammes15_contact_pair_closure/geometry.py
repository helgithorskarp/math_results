"""Exact affine contact-plane and unit-sphere intersection identities."""
from patches import one,zero,t,dot
from polynomial import need

HI=[[((one/(one-t)) if i==j else zero)-t/((one-t)*(one+2*t))
     for j in range(3)] for i in range(3)]
DH=(one-t)**2*(one+2*t)

def cross(x,y):
    return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]

def matvec(m,x):
    return [sum((a*b for a,b in zip(row,x)),zero) for row in m]

def lens(a,i,j):
    w=dot(a[i],a[j])
    c=[t/(one+w)*(x+y) for x,y in zip(a[i],a[j])]
    normal=matvec(HI,cross(a[i],a[j]))
    delta=DH*(one+w-2*t*t)/((one+w)**2*(one-w))
    need(dot(c,normal)==zero,'center-normal orthogonality')
    need(dot(c,a[i])==dot(c,a[j])==t,'center contact equations')
    need(dot(normal,a[i])==dot(normal,a[j])==zero,'normal contact equations')
    need(dot(normal,normal)==(one-w*w)/DH,'normal norm identity')
    need(dot(c,c)+delta*dot(normal,normal)==one,'unit-sphere identity')
    return c,normal,delta

def witness(a,c,normal,delta,k):
    alpha=dot(c,a[k])-t
    beta=dot(normal,a[k])
    return alpha,beta,alpha*alpha-delta*beta*beta
