"""Literal prefix source trees: 0..5 bisect an edge; S/G choose an actual cut.

Each of 108 strings is one complete closed source root. No proposal signs,
coordinates, floating metadata or external certificate corpus is an input.
"""
from pathlib import Path
import json,re
from kernel import need,EDGES,encode,structural
HERE=Path(__file__).resolve().parent

def load_forest(cell,domain):
    row=json.loads((HERE/'forests.json').read_text())[cell]
    need(row['bounds']==domain['record']['receiving_rectangle_in_s_units'],'literal tree receiver bounds differ')
    need(len(row['roots'])==108,'exactly108 complete closed source trees required')
    branches=[];leaves=[]
    for ri,text in enumerate(row['roots']):
        tokens=iter(text.split(','))
        def walk(path):
            need(len(path)<=40,'source depth outside certificate grammar')
            token=next(tokens,None);need(token is not None,'incomplete source tree')
            if token in '012345' and len(token)==1:
                i,j=EDGES[int(token)];branches.append({'root':ri,'path':path,'edge':[i,j]})
                walk(path+'0');walk(path+'1');return
            need(re.fullmatch(r'[SG](0|[1-9][0-9]*)',token) is not None,'malformed literal cut token')
            k=int(token[1:]);kind='support' if token[0]=='S' else 'gauge'
            need(k<(540 if kind=='support' else 60),'cut index outside actual inventory')
            leaves.append({'root':ri,'path':path,'kind':kind,'cut':k+(540 if kind=='gauge' else 0)})
        walk('');need(next(tokens,None) is None,'orphan tree token')
    labels=[]
    for cut in domain['cuts']:
        label={'kind':cut['kind']}
        if cut['kind']=='support':label.update(support=cut['support'],source=cut['source'])
        else:label['k']=encode(cut['k'])
        labels.append(label)
    result={'internal_nodes':branches,'leaves':leaves,'cut_labels':labels,
            'receiving_closed_rectangle_in_s_units':row['bounds'],'source_roots':108,
            'actual_source_root_alpha':'1/22','pending':[]}
    structural(result)
    return result
