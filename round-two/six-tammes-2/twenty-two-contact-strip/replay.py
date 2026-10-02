"""Literal prefix-tree checks. No adaptive witness or subdivision chooser."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
import hashlib,json
import model as m
HERE=Path(__file__).resolve().parent
INSTRUCTIONS=json.loads((HERE/'INSTRUCTIONS.json').read_text())
EXPECTED_INSTRUCTIONS=[['outside-target-z-out'],['outside-target-t-low']]+[
    ['primitive',*x] for x in ([['chart'],['empty-necessary-intersection'],['no-real-V']]+
    [['W-pair',7,j] for j in (1,2,4,8,10,13)]+[['pair',*p] for p in m.e.PAIRS])]+[
    ['whole-cell-centered-pair',*p] for p in m.e.PAIRS]
if INSTRUCTIONS!=EXPECTED_INSTRUCTIONS:raise ValueError('fixed literal witness meanings')

def require(ok,message):
    if not ok:raise ValueError(message)

def replay(data):
    require(data['format']==1 and data['lattice_bits']==80,'fixed format and precision')
    mode=data['mode'];require(mode in ('z-out','t-low','dz-68'),'specified proof target')
    derivative=mode=='dz-68'
    target=['577/1000','593/1000','9/10','19/20'] if derivative else ['14/25','593/1000','-5/2','5/2']
    require(data['box']==target and data['branch']==[-1,1],'full fixed domain and sole retained branch')
    low,high,za,zb=map(Q,target);tree=data['tree'];position=0
    nodes=0;leaves=0;maximum=0;counts=Counter()
    derivative_upper=None;smallest_gap=None
    def walk(td,ti,zd,zi):
        nonlocal position,nodes,leaves,maximum,derivative_upper,smallest_gap
        nodes+=1;maximum=max(maximum,td+zd)
        require(position<len(tree),'complete partition tree')
        char=tree[position];position+=1
        if char in ('T','Z'):
            require(td+zd<22,'existing finite subdivision guard')
            if char=='T':walk(td+1,2*ti,zd,zi);walk(td+1,2*ti+1,zd,zi)
            else:walk(td,ti,zd+1,2*zi);walk(td,ti,zd+1,2*zi+1)
            return
        require(position<len(tree),'two-digit literal leaf opcode')
        code=char+tree[position];position+=1
        require(all(c in '0123456789abcdef' for c in code),'hexadecimal leaf opcode')
        i=int(code,16)
        left=low+(high-low)*ti/2**td;right=left+(high-low)/2**td
        a=za+(zb-za)*zi/2**zd;b=a+(zb-za)/2**zd
        if derivative:
            require(code=='ff','literal derivative target')
            P,t,regularity=m.enclosed(left,right,a,b)
            bound=m.pair_gap(P,t,(6,8)).dz.h
            require(bound<0,'strict whole-cell derivative sign')
            derivative_upper=bound if derivative_upper is None else max(derivative_upper,bound)
            instruction=['strict-dz-68']
        else:
            require(i<len(INSTRUCTIONS),'known leaf instruction')
            instruction=INSTRUCTIONS[i];kind=instruction[0]
            if kind=='outside-target-z-out':
                require(mode=='z-out' and a>Q(9,10) and b<Q(7,5),'strict parameter strip interior')
            elif kind=='outside-target-t-low':
                require(mode=='t-low' and left>Q(577,1000),'strict lower-threshold interior')
            elif kind=='primitive':
                require(m.e.verify_witness(m.I(left,right),m.I(a,b),-1,1,'bad',instruction[1:]) is True,'literal prerequisite interval witness')
            else:
                require(kind=='whole-cell-centered-pair' and tuple(instruction[1:]) in m.e.PAIRS,'specified centered packing pair')
                P,t,regularity=m.enclosed(left,right,a,b)
                gap=m.pair_gap(P,t,tuple(instruction[1:])).v.l
                require(gap>0,'strict whole-cell packing violation')
                smallest_gap=gap if smallest_gap is None else min(smallest_gap,gap)
        leaves+=1;counts[instruction[0]]+=1
    walk(0,0,0,0)
    require(position==len(tree),'no trailing partition data')
    canonical=json.dumps(data,sort_keys=True,separators=(',',':')).encode()
    return {'mode':mode,'nodes':nodes,'leaves':leaves,'maximum_total_depth':maximum,
            'witness_counts':dict(sorted(counts.items())),
            'canonical_plan_sha256':hashlib.sha256(canonical).hexdigest(),
            'derivative_upper':None if derivative_upper is None else str(Q(derivative_upper,m.S)),
            'smallest_centered_packing_gap':None if smallest_gap is None else str(Q(smallest_gap,m.S)),
            'full_closed_rectangle_covered':True,'all_literal_strict_witnesses_verified':True}
