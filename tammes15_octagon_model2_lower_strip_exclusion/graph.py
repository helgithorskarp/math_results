"""Exact graph reduction and complete clique search; no solver dependency."""

def verify_deletions(adjacency,deletions):
    active=(1<<len(adjacency))-1
    for step in deletions:
        if type(step) is not list or len(step)!=2 or any(type(k) is not int for k in step):
            raise ValueError('integer domination pair')
        v,w=step
        if not (0<=v<len(adjacency) and 0<=w<len(adjacency)) or v==w:
            raise ValueError('distinct bounded domination pair')
        if not active&(1<<v) or not active&(1<<w) or adjacency[v]&(1<<w):
            raise ValueError('live nonadjacent domination pair')
        if (adjacency[v]&active)&~(adjacency[w]&active):
            raise ValueError('current-neighborhood containment fails')
        active&=~(1<<v)
    return active

def clique(adjacency,size=7,maxstates=2000000,active=None):
    states=0
    def color_order(candidates):
        order=[];colors=[];color=0
        while candidates:
            color+=1;available=candidates
            while available:
                bit=available&-available;v=bit.bit_length()-1
                order.append(v);colors.append(color);candidates^=bit
                available&=~bit;available&=~adjacency[v]
        return order,colors
    def visit(candidates,chosen):
        nonlocal states
        states+=1
        if states>maxstates:raise RuntimeError('incomplete clique search: state budget')
        needed=size-len(chosen)
        if needed==0:return chosen
        if candidates.bit_count()<needed:return None
        order,colors=color_order(candidates)
        for v,color in zip(reversed(order),reversed(colors)):
            if color<needed:return None
            bit=1<<v
            found=visit(candidates&adjacency[v],chosen+[v])
            if found is not None:return found
            candidates&=~bit
        return None
    result=visit((1<<len(adjacency))-1 if active is None else active,[])
    return result,states
