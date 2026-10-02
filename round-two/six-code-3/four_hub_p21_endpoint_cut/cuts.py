"""Unit endpoint upper bound and closed-partition certificate producer."""
import hashlib
import json

def require(condition,message):
    if not condition:raise ValueError(message)

def expand(types,population):
    return [types[i] for i,count in population for _ in range(count)]

def endpoints(vertices):
    units={i for i,r in enumerate(vertices) if r['e']==0}
    ordinary={i for i in units if not vertices[i]['eligible']}
    external={i for i,r in enumerate(vertices) if r['e']>0 and not r['eligible']}
    D=sum(sum(vertices[i]['ss_hist']) for i in units)
    I=sum(min(sum(vertices[i]['ss_hist']),len(ordinary)-1) for i in ordinary)
    C=sum(vertices[i]['ss_hist'][0] for i in external)
    return units,ordinary,external,D,I,C

def potential_colours(vertices,i,j,units,external,equality):
    a,b=vertices[i],vertices[j]
    if i==j or (i in units and b['eligible']) or (j in units and a['eligible']):return []
    values=[c for c in range(5) if a['ss_hist'][c] and b['ss_hist'][c]]
    # Equality consumes colour-one capacity of every ineligible nonunit.
    # Other deficit colours are retained, even at equality.
    if equality and i not in units and j not in units and (i in external or j in external):
        values=[c for c in values if c!=0]
    return values

def one_cut(vertices):
    units,ordinary,external,D,I,C=endpoints(vertices)
    scalar=dict(unit_demand=D,internal_upper=I,external_upper=C)
    if D>I+C:return dict(kind='unit_capacity',**scalar)
    equality=D==I+C
    for root,row in enumerate(vertices):
        if row['k']:continue
        reached={root};frontier={root}
        while frontier:
            new={j for i in frontier for j in range(len(vertices))
                 if potential_colours(vertices,i,j,units,external,equality)}-reached
            reached|=new;frontier=new
        if len(reached)<len(vertices):
            return dict(kind='closed_partition',root=root,inside=sorted(reached),
                        outside=sorted(set(range(len(vertices)))-reached),
                        capacity_equality=equality,**scalar)
    return dict(kind='UNRESOLVED',**scalar)

def certificates(inventory):
    records=[]
    for branch in inventory['branches']:
        for template in branch['templates']:
            if template['failures']:continue
            vertices=expand(inventory['types'],template['population'])
            require(len(vertices)==14,'four-hub saturated population')
            record=dict(branch=[branch[k] for k in ('Q','T','X','tau')],
                        population=template['population'],**one_cut(vertices))
            require(record['kind']!='UNRESOLVED','physical candidate not excluded')
            records.append(record)
    return dict(agent='six-code-3',role='researcher',records=records)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
