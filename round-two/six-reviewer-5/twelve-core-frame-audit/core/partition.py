"""Independent recursive closed-box coverage decoder and strict scope binding."""
import json
from fractions import Fraction as F
from pathlib import Path
from frame import LABELS,CONTACTS,TESTS

ROOT=(F(14,25),F(593,1000),F(-5,2),F(5,2))
BRANCHES=(('bad',-1,-1),('bad',1,-1),('bad',1,1),('g-half',-1,1))
CODES='0123456789abcdefghijklmnopqrstuvwxyzABCDEF'
LITERALS=[['chart'],['empty-necessary-intersection'],['no-real-V'],['outside-target-g-half']]
LITERALS += [['W-pair',7,j] for j in (1,2,4,8,10)]
LITERALS += [['pair',6,8]] + [['pair',a,b] for a,b in TESTS if (a,b)!=(6,8)]

def decode(directory):
    p=Path(directory)
    plan=json.loads((p/'PLAN.json').read_text())
    table=json.loads((p/'LITERALS.json').read_text())
    if table!={'format':1,'codes':CODES,'literals':LITERALS}:raise ValueError('literal table binding')
    if plan.get('format')!=1 or plan.get('lattice_bits')!=80:raise ValueError('source format/precision')
    if plan.get('labels')!=list(LABELS) or plan.get('contacts')!=[list(x) for x in CONTACTS]:raise ValueError('physical label/contact scope')
    if tuple(map(F,plan.get('box',[])))!=ROOT:raise ValueError('root domain')
    trees=plan.get('trees',[])
    if len(trees)!=4:raise ValueError('complete branch cover')
    leaves=[];records=[]
    for idx,(tree,branch) in enumerate(zip(trees,BRANCHES)):
        if (tree.get('mode'),tree.get('epsilon'),tree.get('eta'))!=branch:raise ValueError('ordered target scope')
        word=tree.get('tree');cursor=0;nodes=0;area=F(0);maxdepth=0;count=0
        if not isinstance(word,str) or not word or len(word)>20000:raise ValueError('prefix size')
        def visit(box,depth):
            nonlocal cursor,nodes,area,maxdepth,count
            if depth>22 or cursor>=len(word):raise ValueError('prefix depth/truncation')
            code=word[cursor];cursor+=1;nodes+=1;maxdepth=max(maxdepth,depth)
            if code in ('T','Z'):
                axis=0 if code=='T' else 2
                cut=(box[axis]+box[axis+1])/2
                left=list(box);right=list(box);left[axis+1]=cut;right[axis]=cut
                visit(tuple(left),depth+1);visit(tuple(right),depth+1)
            else:
                if code not in CODES:raise ValueError('unknown leaf')
                literal=LITERALS[CODES.index(code)]
                if literal[0]=='outside-target-g-half' and branch[0]!='g-half':raise ValueError('target-specific witness leaked')
                count+=1;area+=(box[1]-box[0])*(box[3]-box[2])
                leaves.append((idx,branch,box,literal))
        visit(ROOT,0)
        if cursor!=len(word):raise ValueError('unused prefix suffix')
        if area!=(ROOT[1]-ROOT[0])*(ROOT[3]-ROOT[2]):raise ValueError('area cover')
        if nodes!=2*count-1:raise ValueError('full binary partition')
        records.append(dict(branch=list(branch),leaves=count,nodes=nodes,maxdepth=maxdepth,normalized_area='1'))
    if [r['leaves'] for r in records]!=[7861,1675,1675,880]:raise ValueError('frozen complete leaf census')
    return leaves,records

