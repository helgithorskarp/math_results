"""Independent integral260-system generator in two-component radical DAGs."""
import hashlib,json
from functools import lru_cache
from digit import T,Z,expr
from geometry import model,Radical,dot,LABELS,CONTACTS
from gram import det,adj
from census import classify,CAPS,PLANES

def generate():
    m=model();R=m['R'];O=m['Omega'];Y=m['Y'];V=dict(Y)
    for k,(n,u) in CAPS.items():V[k]=[Radical(O*x,0,R) for x in n]
    rhs={k:(T*O if k in LABELS else CAPS[k][1]*O) for k in PLANES}
    G={(i,j):dot(V[i],V[j]) for i in PLANES for j in PLANES if i<=j}
    def product(i,j):return G[min(i,j),max(i,j)]
    @lru_cache(None)
    def hash_expr(p):
        if p.op=='c':data=['integer',p.args[0]]
        elif p.op in ['t','z']:data=['variable',p.op]
        else:data=[p.op,*[hash_expr(x) for x in p.args]]
        return hashlib.sha256(json.dumps(data,separators=(',',':')).encode()).hexdigest()
    def rad(p):return p if isinstance(p,Radical) else Radical(p,0,R)
    def root_record(name,kind,p):
        p=rad(p)
        return {'name':name,'kind':kind,'constant_sha256':hash_expr(p.p),'linear_sha256':hash_expr(p.q),
            'constant_degree_bounds':[p.p.dt,p.p.dz],'linear_degree_bounds':[p.q.dt,p.q.dz]}
    base=[]
    base.append({'name':'w_squared_equals_R','kind':'eq','explicit_raw_w_square':True,'R_sha256':hash_expr(R)})
    for i in LABELS:base.append(root_record('unit_'+str(i),'eq',product(i,i)-O*O))
    for i,j in CONTACTS:base.append(root_record('contact_'+str(i)+'_'+str(j),'eq',product(i,j)-T*O*O))
    base.append(root_record('positive_w','gt',Radical(0,1,R)))
    base.append(root_record('strict_original_regularity','gt',2*m['G']-m['a']**4*m['C']**2))
    for name,p in [('t_lower',25*T-14),('t_upper',593-1000*T),('z_lower',5*Z-6),('z_upper',7-5*Z),('original_chart',1-m['b']**2*Z**2)]:base.append(root_record(name,'ge',p))
    for q,i in enumerate(LABELS):
        for j in LABELS[q+1:]:base.append(root_record('packing_'+str(i)+'_'+str(j),'ge',-product(i,j)+T*O*O))
    results=[]
    for row in classify():
        if row['case']!='residual':continue
        tri=row['triple'];A=[[product(i,j) for j in tri] for i in tri];D=det(A);B=adj(A)
        lam=[sum(B[k][l]*rhs[tri[l]] for l in range(3)) for k in range(3)]
        X=[sum(lam[k]*V[tri[k]][j] for k in range(3)) for j in range(3)]
        norm=sum(lam[k]*rhs[tri[k]] for k in range(3))
        roots=[root_record('regular_basis','gt',D)]
        for j in PLANES:roots.append(root_record('closed_feasible_'+str(j),'ge',D*rhs[j]-dot(V[j],X)))
        roots.append(root_record('long_vertex','ge',norm-D))
        # Complete per-branch comparator/name domain, not just a matching count.
        all_roots=base+roots;names=[p['name'] for p in all_roots]
        if len(names)!=len(set(names)):raise ValueError('duplicate branch predicate')
        if len([p for p in all_roots if p['kind']=='eq'])!=33 or len([p for p in all_roots if p['kind']=='gt'])!=3 or len([p for p in all_roots if p['kind']=='ge'])!=86:raise ValueError('complete branch predicate census')
        results.append({'triple':tri,'roots':roots,'all122_predicate_names':names,
            'whole122_predicate_sha256':hashlib.sha256(json.dumps(all_roots,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
    output={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','variable_order':['t','z','w'],
        'defining_radical':'w>0,w*w=R; two components reduce all products modulo this equality',
        'base_roots':base,'whole260_branches':results,'full_expression_nodes_hashed':hash_expr.cache_info().currsize,
        'scope':'necessary regular long vertices only; no native56194-node hash, branch feasibility or capacity verdict'}
    hash_expr.cache_clear();return output

if __name__=='__main__':print(json.dumps(generate(),sort_keys=True,separators=(',',':')))
