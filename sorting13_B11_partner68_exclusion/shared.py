"""Pinned public inputs and the complete allowed-partner (6,8) quota selector."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
CORES='sorting_networks/thirteen_repeated23_reduction'
COMMON='sorting_networks/thirteen_single_preparation_normal_form/fixture.json'
CLASSES='sorting_networks/thirteen_extreme_multiset_quotient/certificate.json'
OLD='sorting_networks/thirteen_class13_boundary_obstruction/certificate.json'


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode('ascii')).hexdigest()


def read(path):return json.loads(path.read_text())


def pins(repo):
    for row in read(HERE/'dependencies.json')['pinned_files']:
        assert hashlib.sha256((repo/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']


def program(repo,which):
    assert which in ('generate','verify')
    path=repo/CORES/(which+'.py')
    spec=importlib.util.spec_from_file_location('credited_'+which,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


def inputs(repo):
    pins(repo)
    f=read(repo/COMMON);table=read(repo/CLASSES)['class_table']
    assert len(table)==480 and digest(table)==f['parent_class_table_sha256']
    import itertools
    pairs=list(itertools.combinations(range(11),2))
    possible=(1,2,3,4,5,6,8)
    selected=[]
    for index,(code,events,orders) in enumerate(table):
        counts=[(int(code)>>(2*k))&3 for k in range(55)]
        partners=[i for i in possible if counts[pairs.index((i,10))]]
        if events==11 and max(counts)==1 and partners==[6,8]:
            selected.append([index,code,events,orders])
    assert len(selected)==36 and sum(r[3] for r in selected)==421920
    assert [r[0] for r in selected]==[389,390,391,392,393,394,395,396,397,399,400,401,402,403,404,405,406,407,416,417,418,419,420,421,422,423,424,426,427,428,429,430,431,432,433,434]
    # A zero high-profile component has a unique effective exit.
    component={0,1,2,3,4,6}
    assert sum(f['initial_high'])==15 and f['initial_high'][10]==1
    assert all(f['initial_high'][i]==0 for i in component)
    assert all(w%2==0 for w in f['initial_high'][:10])
    for index,code,events,orders in selected:
        edges=[pair for k,pair in enumerate(pairs) if (int(code)>>(2*k))&3]
        assert [pair for pair in edges if (pair[0] in component)!=(pair[1] in component)]==[(6,10)]
    return f,selected,selected,[]



def arguments():
    p=argparse.ArgumentParser()
    p.add_argument('--repository',type=Path,default=HERE.parent)
    p.add_argument('--output',type=Path,default=HERE/'generated')
    p.add_argument('--class-index',type=int)
    return p.parse_args()


def choose(fresh,index):
    chosen=[r for r in fresh if index is None or r[0]==index]
    assert chosen,'Class is outside the complete new cohort'
    return chosen


def all_tails(output):
    cert=read(HERE/'certificate.json');tails=[]
    for record in cert['records']:
        saved=read(output/f"class{record['parent_index']:03d}.json")
        assert digest(saved['tails'])==record['tails_sha256']
        tails.extend(saved['tails'])
    assert len(tails)==15 and all(t['budget']==11 for t in tails)
    assert [[t['parent_index'],t['image'],t['budget'],t['case']] for t in tails]==cert['residual_keys']
    return tails


def residual_tails(output):return all_tails(output)


def tail_path(output,tail):
    return output/f"tail_class{tail['parent_index']:03d}_image{tail['image']:03d}.cnf"
