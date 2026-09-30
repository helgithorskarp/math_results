"""Exact independent geometry for P17 charge vectors; standard library only."""
from pathlib import Path
import argparse
import copy
import itertools
import json


TILE=tuple(sorted((x,y) for y,lo,hi in ((0,1,3),(1,0,3),(2,0,3),(3,2,4),(4,3,5))
                  for x in range(lo,hi+1)))
QUADS=((0,0),(-1,0),(-1,-1),(0,-1))
SIGNS=((1,1),(-1,1),(-1,-1),(1,-1))


def require(truth,message):
    if not truth:raise ValueError(message)


def point_image(point,turns,mirror):
    x,y=point
    if mirror:x=-x
    for _ in range(turns):x,y=-y,x
    return x,y


def square_image(shape,turns,mirror):
    """Transform centers, then recover the lower corners of unit squares."""
    result=[]
    for x,y in shape:
        a,b=point_image((2*x+1,2*y+1),turns,mirror)
        require(a%2==b%2==1,'a transformed center is not odd')
        result.append(((a-1)//2,(b-1)//2))
    return tuple(sorted(result))


def normalize(shape):
    a=min(x for x,y in shape);b=min(y for x,y in shape)
    return tuple(sorted((x-a,y-b) for x,y in shape))


def orientations():
    return tuple(sorted({normalize(square_image(TILE,k,m)) for k in range(4) for m in (False,True)}))


def vertices(shape):
    return sorted({(x+dx,y+dy) for x,y in shape for dx in (0,1) for dy in (0,1)})


def quarters(shape,tx2,ty2,vertex):
    """Literal rectangle membership of the four quarter-offset points."""
    return tuple(any(4*x+2*tx2<4*vertex[0]+sx<4*x+2*tx2+4
                     and 4*y+2*ty2<4*vertex[1]+sy<4*y+2*ty2+4 for x,y in shape)
                 for sx,sy in SIGNS)


def corners(amount):
    result=[]
    for v in vertices(TILE):
        q=quarters(TILE,0,0,v)
        if sum(q)==amount:result.append((v,q.index(amount==1)))
    return result


def rectangles(shape,tx2,ty2):
    return [(2*x+tx2,2*y+ty2,2*x+tx2+2,2*y+ty2+2) for x,y in shape]


def rectangle_overlap(first,second):
    return any(max(a,e)<min(c,g) and max(b,f)<min(d,h)
               for a,b,c,d in first for e,f,g,h in second)


def pixels(shape,tx2,ty2):
    return {(2*x+tx2+dx,2*y+ty2+dy) for x,y in shape for dx in (0,1) for dy in (0,1)}


def connected(shape):
    require(bool(shape),'empty shape')
    reached={next(iter(shape))};pending=list(reached)
    while pending:
        x,y=pending.pop()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            p=x+dx,y+dy
            if p in shape and p not in reached:reached.add(p);pending.append(p)
    return reached==shape


def disc(shape):
    """Edge connection, no alternating vertex sectors, complement flood fill."""
    if not connected(shape):return False
    for v in vertices(shape):
        q=tuple((v[0]+dx,v[1]+dy) in shape for dx,dy in QUADS)
        if q in ((True,False,True,False),(False,True,False,True)):return False
    lo_x,hi_x=min(x for x,y in shape)-1,max(x for x,y in shape)+1
    lo_y,hi_y=min(y for x,y in shape)-1,max(y for x,y in shape)+1
    free={(x,y) for x in range(lo_x,hi_x+1) for y in range(lo_y,hi_y+1)}-shape
    return connected(free)


def interior(shape,union):
    return all((v[0]+dx,v[1]+dy) in union for v in vertices(shape) for dx,dy in QUADS)


def intrinsic_source(shapes,pose,vertex):
    oi,tx2,ty2=pose;shape=shapes[oi];maps=[]
    for k in range(4):
        for mirror in (False,True):
            image=square_image(shape,k,mirror)
            if normalize(image)==TILE:maps.append((k,mirror,min(x for x,y in image),min(y for x,y in image)))
    require(len(maps)==1,'the provider does not have a unique orientation inverse')
    k,mirror,ox,oy=maps[0]
    a,b=point_image((2*vertex[0]-tx2,2*vertex[1]-ty2),k,mirror)
    require(a%2==b%2==0,'an incoming provider is not at an integral corner')
    v=a//2-ox,b//2-oy
    reentrant=[p for p,q in corners(3)]
    require(v in reentrant,'received source is not a reentrant corner')
    return reentrant.index(v)


def audit(witness):
    shapes=orientations();raw=witness['pose_codes_doubled_translation']
    require(len(shapes)==8 and len(corners(1))==9 and len(corners(3))==5,'changed P17 geometry')
    require(isinstance(raw,list) and bool(raw),'empty or malformed pose list')
    require(all(isinstance(p,list) and len(p)==3 and all(type(z) is int for z in p)
                and 0<=p[0]<len(shapes) for p in raw),'malformed pose code')
    require(raw[0]==[shapes.index(TILE),0,0],'root is not canonical P17')
    boxes=[rectangles(shapes[i],x,y) for i,x,y in raw]
    require(not any(rectangle_overlap(a,b) for a,b in itertools.combinations(boxes,2)),
            'strict whole-footprint rectangle overlap')
    cells=[pixels(shapes[i],x,y) for i,x,y in raw];union=set().union(*cells)
    require(len(union)==68*len(raw),'packing area differs')
    require(disc(union),'the packing union is not a disc')
    require(interior(cells[0],union),'root is not strictly interior')
    tips=corners(1);providers=[];received=set();vector=[0]*5
    for i,pose in enumerate(raw[1:],1):
        oi,x,y=pose;row=[];labels=[]
        for j,(v,q) in enumerate(tips):
            bits=quarters(shapes[oi],x,y,v)
            if sum(bits)==3 and not bits[q]:
                require(j not in received,'two providers supply the same tip')
                label=intrinsic_source(shapes,pose,v)
                row.append(j);labels.append(label);vector[label]+=1;received.add(j)
        if row:
            require(interior(cells[i],union),'an actual incoming provider is not strictly interior')
            providers.append({'copy':i,'tips':row,'source_labels':labels})
    require(vector==witness['expected_source_vector'],'source charge vector differs')
    return {'name':witness['name'],'copies':len(raw),'area':17*len(raw),
            'root_and_all_incoming_providers_interior':True,'disc':True,
            'source_vector':vector,'providers':providers,'received_tips':sorted(received)}


def run(data):
    require(data.get('schema')==1 and data.get('tile')==[list(p) for p in TILE],'changed input tile or schema')
    require(len(data['witnesses'])==3,'this certificate requires exactly three witnesses')
    result=[audit(q) for q in data['witnesses']]
    require([q['source_vector'] for q in result]==[[2,0,0,2,2],[1,2,2,0,0],[0,2,2,1,1]],'wrong obstruction vectors')
    # A nonnegative integer combination contradicts every balanced nonzero weight vector.
    excess=[[a-1 for a in q['source_vector']] for q in result]
    coefficients=[3,2,2]
    total=[sum(a*row[j] for a,row in zip(coefficients,excess)) for j in range(5)]
    require(total==[1,1,1,1,1],'algebraic obstruction differs')
    combined=[sum(a*q['source_vector'][j] for a,q in zip(coefficients,result)) for j in range(5)]
    require(combined==[8,8,8,8,8] and sum(coefficients)==7,'quantitative receipt identity differs')
    witness_optimal_weights=[4,3,3,2,2]
    receipts=[sum(a*b for a,b in zip(q['source_vector'],witness_optimal_weights)) for q in result]
    require(sum(witness_optimal_weights)==14 and receipts==[16,16,16],
            'three-witness minimax equality differs')
    return {'agent':'six-heesch-1','role':'researcher','witnesses':result,
            'combination_coefficients':coefficients,'combined_source_vector':combined,
            'combined_excess_vector':total,'receipt_lower_factor':'8/7',
            'three_witness_minimax_equality_weights':witness_optimal_weights,
            'status':'exact disc counterexamples to every nonzero nonnegative balanced source weighting'}


def controls(data):
    rejected=0
    first=data['witnesses'][0]
    bad=copy.deepcopy(first);bad['pose_codes_doubled_translation'].append(bad['pose_codes_doubled_translation'][1][:])
    examples=[bad]
    bad=copy.deepcopy(first);bad['expected_source_vector'][0]+=1;examples.append(bad)
    bad=copy.deepcopy(first);bad['pose_codes_doubled_translation'][0][1]=2;examples.append(bad)
    bad=copy.deepcopy(first);bad['pose_codes_doubled_translation']=[bad['pose_codes_doubled_translation'][0]];examples.append(bad)
    for bad in examples:
        try:audit(bad)
        except (ValueError,KeyError,TypeError):rejected+=1
        else:raise ValueError('malformed certificate was accepted')
    return rejected


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=Path(__file__).with_name('witnesses.json'))
    p.add_argument('--out',type=Path)
    a=p.parse_args();data=json.loads(a.input.read_text());result=run(data)
    result['malformed_controls_rejected']=controls(data)
    rendered=json.dumps(result,indent=2)+'\n'
    if a.out:a.out.write_text(rendered)
    print(rendered,end='')


if __name__=='__main__':main()
