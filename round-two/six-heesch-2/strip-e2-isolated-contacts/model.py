"""Literal case bindings and the cited E1 premises used by the trees."""
import json
from pathlib import Path
import deps
import strip_parametric_geometry as G

HERE=Path(__file__).resolve().parent
I=((1,0,0,1),(0,0),(0,0))
CONTACTS={'U0':((1,0,0,1),(0,0),(1,1)),
          'U1':((1,0,0,1),(0,1),(1,1)),
          'U3upper':((1,0,0,1),(0,3),(1,2))}

def require(condition,message):
    if not condition:raise ValueError(message)

def freeze(x):
    if isinstance(x,dict):return {k:freeze(v) for k,v in x.items()}
    return tuple(freeze(v) for v in x) if isinstance(x,(tuple,list)) else x

def bind(data):
    require(data['minimum_k']==6 and [t['contact_name'] for t in data['trees']]==list(CONTACTS),
            'Changed parameter range or literal contacts')
    registry={}
    for directory in ('strip-e2-branches','strip-e2-forced-p','strip-e2-shift-exclusion'):
        for row in json.loads((HERE.parent/directory/'inputs.json').read_text())['cases']:
            if 'pose' in row:registry[directory+'/'+row['name']]=freeze(row['pose'])
    registry['strip-contact-domains/angle']=((2,-3,1,-2),(0,5),(0,3))
    registry['strip-e2-side5-exclusion/Q']=((2,-3,1,-1),(0,-1),(0,0))
    for name,row in data['cuts'].items():
        if name=='strip-contact-domains/identity_U6':
            require(row=={'rule':'identity_U6'},'Changed identity-U6 premise')
        else:
            require(name in registry and freeze(row)=={'pose':registry[name]},
                    'Changed published E1 premise: '+name)
    for tree in data['trees']:
        nodes=tree['nodes'];name=tree['contact_name']
        require(nodes and freeze(nodes[0]['fixed'])==(I,CONTACTS[name]),'Changed root fixed pair')
        seen={0}
        for index,node in enumerate(nodes):
            require(index in seen and node['name']==f'{name}_{index:02d}','Unreachable or mislabeled node')
            fixed=freeze(node['fixed']);expected=freeze(node['expected'])
            require(len(expected)==len(set(expected)) and len(expected)==len(node['children']),
                    'Missing or duplicate branch')
            for q,child in zip(expected,node['children']):
                require(type(child) is int and index<child<len(nodes),'Invalid child index')
                require(freeze(nodes[child]['fixed'])==fixed+(q,),'Child does not select the named supplier')
                seen.add(child)
            blocked=[freeze(b['pose']) for b in node['blocks']]
            require(len(blocked)==len(set(blocked)) and not set(blocked)&set(expected),
                    'Repeated blocker or blocked survivor')
            for block in node['blocks']:
                j=block['fixed_index']
                require(type(j) is int and 0<=j<len(fixed) and block['cut'] in data['cuts'],
                        'Invalid anchor or unknown E1 premise')
        require(len(seen)==len(nodes),'Incomplete tree reachability')

def blocker(data,node,block):
    fixed=freeze(node['fixed']);q=freeze(block['pose'])
    rel=G.relative(fixed[block['fixed_index']],q)
    name=block['cut'];cut=data['cuts'][name]
    if name=='strip-contact-domains/identity_U6':
        alternatives=[]
        for s in (rel,G.inverse(rel)):
            if s[0]==(1,0,0,1):
                alternatives.append(G.both(G.atom('eq',G.sub(s[1],(0,6))),
                    G.neg(G.either(G.atom('eq',G.sub(s[2],(-1,3))),
                                  G.atom('eq',G.sub(s[2],(-1,4)))))))
        match=G.either(*alternatives)
    else:
        p=freeze(cut['pose']);match=G.allowed(rel,(p,G.inverse(p)))
    return G.both(G.touching(rel),G.neg(G.intersection(rel)),match)

def original_demand(fixed,point):
    return G.both(G.neg(G.either(*(G.point_membership(f,point) for f in fixed))),
        G.either(*(G.point_membership(f,(G.sub(point[0],(0,u)),G.sub(point[1],(0,v))))
                   for f in fixed[:2] for u,v in G.UV_DIRS)))

def predicates(data,node):
    fixed=freeze(node['fixed']);p=freeze(node['point']);expected=freeze(node['expected'])
    return [original_demand(fixed,p),
        G.touching(G.relative(fixed[0],fixed[1])),
        *(G.neg(G.intersection(G.relative(f,q))) for i,q in enumerate(fixed) for f in fixed[:i]),
        *(G.both(G.point_membership(q,p),
                 *(G.neg(G.intersection(G.relative(f,q))) for f in fixed)) for q in expected),
        *(blocker(data,node,b) for b in node['blocks'])]
