"""Independently reconstruct finite cells, pose groups and inverse incidences.

Reuses the documented Boolean compiler after replacing its forward geometric
incidence data. The geometric domains and every entry are independently checked.
"""
from collections import defaultdict
import json
from model import BASE,Model

NEIGHBORS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def reconstructed(scale=2,depth=2):
    fixture=json.loads((BASE/'seed.json').read_text())
    radius=scale+1
    cells=set()
    for a,b in fixture['tile']:
        for x in range(scale*a-radius,scale*a+radius+1):
            for y in range(scale*b-radius,scale*b+radius+1):
                if max(abs(x-scale*a),abs(y-scale*b),abs(x+y-scale*(a+b)))<=radius:
                    cells.add((x,y))
    cells=tuple(sorted(cells));index={p:i+1 for i,p in enumerate(cells)}
    options=[];groups=[]
    for j,record in enumerate(fixture['placements']):
        if record['level']>depth:continue
        row=[]
        for dx,dy in ((0,0),) if j==0 else ((0,0),)+NEIGHBORS:
            a,b,c,d,x,y=record['pose']
            row.append(len(options))
            options.append({'copy':j,'level':record['level'],'delta':(dx,dy),
                            'pose':(a,b,c,d,scale*x+dx,scale*y+dy),
                            'y':len(cells)+len(options)+1})
        groups.append(tuple(row))
    xmin=min(x for x,y in cells);xmax=max(x for x,y in cells)
    ymin=min(y for x,y in cells);ymax=max(y for x,y in cells)
    corners=((xmin,ymin),(xmin,ymax),(xmax,ymin),(xmax,ymax))
    images=[]
    for option in options:
        a,b,c,d,u,v=option['pose']
        images.extend((a*x+b*y+u,c*x+d*y+v) for x,y in corners)
    qxmin=min(x for x,y in images);qxmax=max(x for x,y in images)
    qymin=min(y for x,y in images);qymax=max(y for x,y in images)
    incidence=defaultdict(list);zstart=len(cells)+len(options)+1
    # Enumerate world coordinates, then solve A*p=q-t for each potential pose.
    for x in range(qxmin,qxmax+1):
        for y in range(qymin,qymax+1):
            for o,option in enumerate(options):
                a,b,c,d,u,v=option['pose'];det=a*d-b*c
                assert det in (-1,1)
                p=(det*(d*(x-u)-b*(y-v)),det*(-c*(x-u)+a*(y-v)))
                if p in index:incidence[x,y].append(zstart+o*len(cells)+index[p]-1)
    model=Model(scale,depth)
    assert model.cells==cells and model.x==index
    assert model.options==options and model.groups==groups
    assert dict(model.incidence)==dict(incidence)
    model.incidence=incidence
    model.prefix=[]
    last=zstart+len(options)*len(cells)-1;model.u=[]
    for k in range(depth+1):
        row={}
        for q,occupants in sorted(incidence.items()):
            prefix=tuple(z for z in occupants if options[(z-zstart)//len(cells)]['level']<=k)
            if prefix:row[q]=prefix
        model.prefix.append(row);u={}
        for q in row:last+=1;u[q]=last
        model.u.append(u)
    assert model.core_variables==last
    return model
