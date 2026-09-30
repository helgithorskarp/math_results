"""Complete five-clique search with a proper-coloring pruning bound."""
def five_clique(adjacency,maxstates=2000000,active=None):
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
        needed=5-len(chosen)
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
