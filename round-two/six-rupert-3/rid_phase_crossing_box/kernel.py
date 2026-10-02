"""Exact physical affine controls, full central box tensors and semantic controls."""
from functools import lru_cache
from geometry import F,Q,Z,O,dot,cross,sub,midpoint,need


@lru_cache(maxsize=50000)
def scalar(a,b):return dot(a,b)


PAIRS=[(i,j) for i in range(4) for j in range(i,4)]


def coefficients(cut,T,domain):
    if cut['kind']=='support':
        v=cut['v'];vs=[dot(v,c) for c in T];values=[]
        for phase in domain['phases']:
            support=phase['supports'][cut['support']]
            for m,h in zip(support['raw'],support['H']):
                a=dot(m,v);f=cross(v,m);ns=[dot(m,c) for c in T];fs=[dot(f,c) for c in T]
                values.extend((a-h)-(a+h)*scalar(T[i],T[j])+ns[i]*vs[j]+ns[j]*vs[i]+fs[i]+fs[j]
                              for i,j in PAIRS)
        return values
    k=cut['k'];r=domain['box'][0];dx=sub(domain['box'][1],r);dy=sub(domain['box'][3],r)
    def L(r,c):return dot(r,k[1:])+k[0]*dot(r,c)+dot(cross(k[1:],r),c)
    A=[L(r,c) for c in T];X=[L(dx,c) for c in T];Y=[L(dy,c) for c in T]
    rr=dot(r,r);rx=dot(r,dx);ry=dot(r,dy);xx=dot(dx,dx);xy=dot(dx,dy);yy=dot(dy,dy)
    values=[]
    for i,j in PAIRS:
        p00=A[i]*A[j]-rr;p10=A[i]*X[j]+A[j]*X[i]-2*rx;p01=A[i]*Y[j]+A[j]*Y[i]-2*ry
        p20=X[i]*X[j]-xx;p11=X[i]*Y[j]+X[j]*Y[i]-2*xy;p02=Y[i]*Y[j]-yy
        values.extend(p00+F(Q(u,2))*p10+F(Q(v,2))*p01+F(Q(u*(u-1),2))*p20
                      +F(Q(u*v,4))*p11+F(Q(v*(v-1),2))*p02 for u in range(3) for v in range(3))
    return values


def literal_gap(cut,c,r,phase,DATA):
    if cut['kind']=='gauge':
        k=cut['k'];s=-dot(r,c)*k[0]-dot(tuple(r[j]+cross(r,c)[j] for j in range(3)),k[1:])
        return s*s-dot(r,r)
    sup=phase['supports'][cut['support']];m=cross(sup['E'],r);h=dot(m,DATA['V'][sup['source_endpoints'][0]])
    c2=dot(c,c);v=cut['v'];cxv=cross(c,v)
    Rv=tuple(((1-c2)*v[j]+2*c[j]*dot(c,v)+2*cxv[j])/(1+c2) for j in range(3))
    return (1+c2)*(dot(m,Rv)-h)


def independent_check(cut,T,values,domain,DATA):
    def source(r,phase):
        at=[literal_gap(cut,c,r,phase,DATA) for c in T]
        return [at[i] if i==j else 2*literal_gap(cut,midpoint(T[i],T[j]),r,phase,DATA)-(at[i]+at[j])/2 for i,j in PAIRS]
    if cut['kind']=='support':
        exact=[v for phase in domain['phases'] for r in phase['R'] for v in source(r,phase)]
    else:
        B=domain['box'];grid=[[tuple(B[0][k]+F(Q(u,2))*(B[1][k]-B[0][k])+F(Q(v,2))*(B[3][k]-B[0][k])
                                    for k in range(3)) for v in range(3)] for u in range(3)]
        sampled=[[source(r,None) for r in row] for row in grid]
        exact=[]
        def quad(a,b,c):return [a,2*b-(a+c)/2,c]
        for j in range(10):
            first=[quad(*(sampled[u][v][j] for u in range(3))) for v in range(3)]
            tensor=[quad(*(first[v][u] for v in range(3))) for u in range(3)]
            exact.extend(x for row in tensor for x in row)
    need(exact==values,'literal two-stage source/box polarization differs')
    return len(exact)

def structural(forest):
    allrows=forest['internal_nodes']+forest['leaves'];keys={(x['root'],x['path']) for x in allrows}
    need(len(keys)==len(allrows),'duplicate subdivision node')
    need(all((ri,'') in keys for ri in range(108)),'omitted quotient face/shell root')
    for row in forest['internal_nodes']:
        need((row['root'],row['path']+'0') in keys and (row['root'],row['path']+'1') in keys,'omitted closed bisection child')


def negative_controls(forest,example,domain,DATA):
    import copy
    controls=[]
    for title,mutation in [
        ('omit complete shell root',lambda f: f['internal_nodes'].__setitem__(slice(None),[x for x in f['internal_nodes'] if x['root']!=0]) or f['leaves'].__setitem__(slice(None),[x for x in f['leaves'] if x['root']!=0])),
        ('omit a closed leaf child',lambda f:f['leaves'].pop(next(i for i,x in enumerate(f['leaves']) if x['path']))),
        ('duplicate literal leaf',lambda f:f['leaves'].append(copy.deepcopy(f['leaves'][0])))]:
        bad=copy.deepcopy(forest);mutation(bad)
        try:structural(bad)
        except ValueError as e:controls.append({'control':title,'rejection':str(e)});continue
        raise ValueError('damaged source coverage accepted')
    cut,T=example;bad=copy.copy(cut);bad['v']=tuple(-x for x in cut['v'])
    need(any(x<=Z for x in coefficients(bad,T,domain)),'wrong antipodal source accepted as same witness')
    controls.append({'control':'replace original source by antipodal original','rejection':'same witness has a nonpositive coefficient'})
    need(Q(9,8)**2*392/4>1,'unsupported local radius1/2 accepted')
    controls.append({'control':'unsupported local collar1/2','rejection':'exact squared closure exceeds one'})
    r=domain['q'];c=(-r[1],r[0],Z);c2=dot(c,c);V=DATA['V'];plane=c;second=cross(r,plane)
    original={(dot(plane,v),dot(second,v)) for v in V};rotated=set()
    for v in V:
        w=tuple(((1-c2)*v[j]+2*c[j]*dot(c,v)+2*cross(c,v)[j])/(1+c2) for j in range(3))
        rotated.add((dot(plane,w),dot(second,w)))
    need(original==rotated and c2>F(Q(1,625)),'actual central companion differs')
    need(all(dot(n,c)<=DATA['height'] for n in DATA['normals']),'central companion not in body chart')
    kz=(Z,Z,Z,O);L=dot(r,kz[1:])+dot(cross(kz[1:],r),c)
    need(L*L>dot(r,r),'central companion not rejected by closest-shadow gauge')
    controls.append({'control':'drop central gauges or omit H_n G shadows','rejection':'actual nonzero body-chart equal shadow survives; central gauge rejects its representative'})
    need(domain['record']['obsolete_old_support_rejected_on_new_half'],'false old support accepted on new phase')
    controls.append({'control':'transport old support7 through phase seam','rejection':'actual original19 has a negative old gap at a new-phase corner'})
    newcorners=domain['phases'][1]['record']['actual_corner_hulls']
    need(any(len(x['actual_hull'])==18 for x in newcorners),'false old16 full boundary accepted on new phase')
    controls.append({'control':'use old16-ring for new-phase physical area','rejection':'all-original hull at new-phase corners has18 actual corners'})
    return controls
