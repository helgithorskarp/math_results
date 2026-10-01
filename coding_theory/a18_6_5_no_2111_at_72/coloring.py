def proper_color(active,adj):
    order=[];bounds=[];color=0
    remaining=active
    while remaining:
        color+=1;available=remaining
        while available:
            bit=available&-available;v=bit.bit_length()-1
            order.append(v);bounds.append(color)
            remaining^=bit
            available&=~bit;available&=~adj[v]
    return order,bounds
