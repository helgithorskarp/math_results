"""Late untrusted-author data comparisons and independently checked counting DAG.

No author program is imported. The independent census is already frozen.
"""
from pathlib import Path
from collections import Counter
import argparse,copy,json,hashlib
from carrier import *
from controls import reject

def counting(cert,adj):
    require(set(cert)=={'nodes','root_node'},'certificate header')
    nodes=cert['nodes'];root=cert['root_node'];allbits=(1<<len(adj))-1
    require(type(root)is int and 0<=root<len(nodes),'root ordinal')
    require(nodes[root]['domain']==allbits and nodes[root]['required']==9,'full target root')
    states=set();children=[]
    for i,n in enumerate(nodes):
        P=n['domain'];k=n['required'];c=n['count'];kind=n['kind']
        require(all(type(x)is int for x in (P,k,c))and 0<=P<=allbits and 0<=k<=9 and c>=0,'node typed domain/count')
        require((P,k)not in states,'unique counting state');states.add((P,k))
        child=[]
        if kind=='positive':require(k==0 and c==1,'positive leaf')
        elif kind=='cardinality':require(P.bit_count()<k and c==0,'cardinality leaf')
        elif kind=='proper_colors':
            classes=n['classes'];covered=0
            require(0<len(classes)<k and c==0,'color target/count')
            for C in classes:
                require(type(C)is int and C>0 and C&~P==0 and not covered&C,'color partition domain')
                for v in bits(C):require(adj[v]&C==0,'color independence')
                covered|=C
            require(covered==P,'complete color cover')
        elif kind=='split':
            v=n['vertex'];a=n['without'];b=n['with']
            require(type(v)is int and 0<=v<len(adj)and P>>v&1 and k>0,'split vertex')
            require(type(a)is int and type(b)is int and 0<=a<i and 0<=b<i,'preceding split children')
            Q=P^(1<<v)
            require((nodes[a]['domain'],nodes[a]['required'])==(Q,k),'exact exclusion child')
            require((nodes[b]['domain'],nodes[b]['required'])==(Q&adj[v],k-1),'exact inclusion child')
            require(c==nodes[a]['count']+nodes[b]['count'],'additive count');child=[a,b]
        else:raise ValueError('unknown rule')
        children.append(child)
    reachable=set();todo=[root]
    while todo:
        i=todo.pop()
        if i in reachable:continue
        reachable.add(i);todo.extend(children[i])
    require(reachable==set(range(len(nodes))),'all nodes reachable')
    positives=[];todo=[(root,())]
    while todo:
        i,chosen=todo.pop();n=nodes[i]
        if n['count']==0:continue
        if n['kind']=='positive':
            require(len(chosen)==9,'positive path nine vertices');positives.append(tuple(sorted(chosen)))
        else:
            require(n['kind']=='split','positive internal node')
            todo.extend([(n['without'],chosen),(n['with'],chosen+(n['vertex'],))])
    require(len(positives)==len(set(positives))==nodes[root]['count'],'path expansion exact count')
    return tuple(sorted(positives)),dict(sorted(Counter(n['kind']for n in nodes).items()))

def run(own,native,author):
    own=Path(own);native=Path(native);author=Path(author)
    model=json.loads((native/'model/ORBIT_MODEL.json').read_text())
    U=universe();full=tuple(o for o in U if len(o)==5 and admissible(o))
    author_full=tuple(sorted(tuple(r['words'])for r in model['admissible_five_word_orbits']))
    require(author_full==full,'all1125 full physical orbit entries')
    ownstars=tuple(tuple(c)for c in json.loads((own/'stars.json').read_text()))
    authorstars=tuple(sorted(tuple(r['words'])for r in json.loads((native/'roots/ROOTS.json').read_text())))
    require(ownstars==authorstars,'all100 literal root entries')
    g=json.loads((native/'equality/GRAPH.json').read_text());rows=tuple(tuple(o)for o in g['residual_orbits'])
    independent_rows=tuple(tuple(o)for o in json.loads((own/'residual.json').read_text()))
    require(set(rows)==set(independent_rows)and len(rows)==len(independent_rows),'exact residual orbit domain')
    adj=graph(rows);require(adj==g['adjacency'],'every actual adjacency entry')
    cert=json.loads((author/'COUNT_CERTIFICATE.json').read_text())
    require((author/'COUNT_CERTIFICATE.json').read_bytes()==(native/'equality/COUNT_CERTIFICATE.json').read_bytes(),'public/regenerated certificate bytes')
    positive,counts=counting(cert,adj)
    prefix=tuple(sorted(g['root_words']+g['invariant_cycle_words']))
    expanded=tuple(sorted(tuple(sorted(prefix+tuple(x for i in C for x in rows[i])))for C in positive))
    owncompletions=tuple(tuple(c)for c in json.loads((own/'completions.json').read_text()))
    authorcompletions=tuple(sorted(tuple(r['words'])for r in json.loads((native/'equality/COMPLETIONS68.json').read_text())))
    require(expanded==owncompletions==authorcompletions,'all32 physical completions/DAG paths')
    ownlabelled=tuple(tuple(c)for c in json.loads((own/'labelled.json').read_text()))
    authorlabelled=tuple(tuple(c)for c in json.loads((native/'saturation/ALL_CODES.json').read_text()))
    require(ownlabelled==authorlabelled,'all5850 ordered literal entries')
    ownclasses=json.loads((own/'centralizer_classes.json').read_text());C=json.loads((author/'CLASSIFICATION.json').read_text())
    class_sets=[set(tuple(c)for c in cl)for cl in ownclasses]
    classmap=[]
    for row in C['classes']:
        rep=tuple(row['representative_words']);matches=[i for i,cl in enumerate(class_sets)if rep in cl]
        require(len(matches)==1 and len(class_sets[matches[0]])==row['labelled_size'],'literal class representative and full population')
        classmap.append(matches[0])
    require(sorted(classmap)==list(range(len(ownclasses))),'all eight classes bijection')
    constructions=json.loads((author/'CONSTRUCTIONS.json').read_text())
    require(constructions['exact_normalized_code_count']==32,'construction count')
    require(sorted((r['old_seed_word'],r['erased_seed_point'],r['replacement_orbit'])for r in constructions['moving_replacement_rules'])==sorted((r[0],r[1],r[2])for r in json.loads((own/'RESULT.json').read_text())['moving_rules']),'all24 expanded moving replacement rules')
    damages=[]
    def damaged(name,edit):
        z=copy.deepcopy(cert);edit(z);damages.append(reject(name,lambda:counting(z,adj)))
    root=cert['root_node'];nodes=cert['nodes'];color=next(i for i,n in enumerate(nodes)if n['kind']=='proper_colors');split=next(i for i,n in enumerate(nodes)if n['kind']=='split');card=next(i for i,n in enumerate(nodes)if n['kind']=='cardinality');positive_node=next(i for i,n in enumerate(nodes)if n['kind']=='positive')
    damaged('root domain omits vertex',lambda z:z['nodes'][root].__setitem__('domain',z['nodes'][root]['domain']^1))
    damaged('root required target altered',lambda z:z['nodes'][root].__setitem__('required',8))
    damaged('false additive root count',lambda z:z['nodes'][root].__setitem__('count',33))
    damaged('zero-target shared leaf count',lambda z:z['nodes'][positive_node].__setitem__('count',0))
    damaged('false cardinality leaf',lambda z:z['nodes'][card].__setitem__('required',0))
    damaged('color cover omitted vertex',lambda z:z['nodes'][color]['classes'].__setitem__(0,z['nodes'][color]['classes'][0]&(z['nodes'][color]['classes'][0]-1)))
    damaged('color cover repeated class',lambda z:z['nodes'][color]['classes'].append(z['nodes'][color]['classes'][0]))
    damaged('self-dependent split child',lambda z:z['nodes'][split].__setitem__('with',split))
    damaged('wrong exclusion child',lambda z:z['nodes'][split].__setitem__('without',z['nodes'][split]['with']))
    damaged('unknown inference rule',lambda z:z['nodes'][0].__setitem__('kind','arbitrary_zero'))
    damaged('duplicate state/unreachable node',lambda z:z['nodes'].append(copy.deepcopy(z['nodes'][0])))
    allfields={'all_physical_words':sum(len(o)for o in U),'admissible_orbit_entries':len(full),'literal_root_entries':len(ownstars),'residual_orbit_entries':len(rows),'adjacency_bit_entries':len(rows)**2,'count_certificate_nodes':len(nodes),'count_certificate_sha256':hashlib.sha256((author/'COUNT_CERTIFICATE.json').read_bytes()).hexdigest(),'certificate_rule_counts':counts,'all_positive_path_entries':len(positive),'whole_completion_entries':len(expanded),'whole_labelled_entries':len(ownlabelled),'labelled_words_compared':sum(map(len,ownlabelled)),'original_class_to_own_class':classmap,'expanded_moving_rule_entries':24,'semantic_DAG_rejections':damages,'original_executable_imports':False}
    print(json.dumps(allfields,sort_keys=True,separators=(',',':')));return allfields

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--own',required=True);p.add_argument('--native',required=True);p.add_argument('--author',required=True);p.add_argument('--expect');a=p.parse_args();z=run(a.own,a.native,a.author)
    if a.expect:require(z==json.loads(Path(a.expect).read_text()),'late complete comparison record')
