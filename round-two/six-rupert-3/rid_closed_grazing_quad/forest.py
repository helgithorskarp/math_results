"""Readable compact literal source forests; both children and all roots required."""
EDGES=[(i,j) for i in range(4) for j in range(i+1,4)]


def read_certificate(path,domain_record):
    lines=path.read_text().splitlines()
    if len(lines)!=108:raise ValueError('literal closed source forest omitted a root')
    nodes=[];leaves=[]
    for ri,line in enumerate(lines):
        prefix,sep,body=line.partition(': ')
        if not sep or prefix!=str(ri):raise ValueError('root ordering, identity or count differs')
        tokens=body.split();cursor=0
        def walk(bits):
            nonlocal cursor
            if cursor>=len(tokens):raise ValueError('literal closed bisection omitted a child')
            if len(bits)>40:raise ValueError('certificate depth exceeds the checked envelope')
            token=tokens[cursor];cursor+=1
            row={'root':ri,'path':bits}
            if token in ['b'+str(i) for i in range(6)]:
                row['edge']=list(EDGES[int(token[1:])]);nodes.append(row)
                walk(bits+'0');walk(bits+'1');return
            if token=='l':row['kind']='local'
            elif token.startswith(('s','g')) and token[1:].isdigit():
                ci=int(token[1:])
                if not (0<=ci<480 if token[0]=='s' else 480<=ci<540):raise ValueError('literal cut index or interpretation differs')
                row.update(kind='support' if token[0]=='s' else 'gauge',cut=ci)
            else:raise ValueError('unrecognized certificate token')
            leaves.append(row)
        walk('')
        if cursor!=len(tokens):raise ValueError('unconsumed/orphan certificate token')
    return {'internal_nodes':nodes,'leaves':leaves,'pending':[],'exact_receiving_domain':domain_record}


def write_certificate(forest):
    if forest.get('pending'):raise ValueError('incomplete floating proposal cannot become a full forest')
    entries={}
    for row in forest['internal_nodes']+forest['leaves']:
        key=(row['root'],row['path'])
        if key in entries:raise ValueError('duplicate proposal address')
        entries[key]=row
    consumed=set()
    def walk(ri,bits):
        key=(ri,bits)
        if key not in entries:raise ValueError('proposed closed tree omits a child/root')
        row=entries[key];consumed.add(key)
        if 'edge' in row:return ['b'+str(EDGES.index(tuple(row['edge']))),*walk(ri,bits+'0'),*walk(ri,bits+'1')]
        return ['l' if row['kind']=='local' else row['kind'][0]+str(row['cut'])]
    lines=[str(ri)+': '+' '.join(walk(ri,'')) for ri in range(108)]
    if consumed!=set(entries):raise ValueError('orphan proposal address')
    return '\n'.join(lines)+'\n'
