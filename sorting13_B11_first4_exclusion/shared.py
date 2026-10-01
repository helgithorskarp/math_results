"""Pinned public inputs and the complete first(4,10) quota selector."""
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
    # Lexicographic combinations(range(11),2): (4,10) has index39.
    selected=[[i,code,e,n] for i,(code,e,n) in enumerate(table) if e==11 and ((int(code)>>78)&3)]
    assert len(selected)==54 and sum(r[3] for r in selected)==488655
    fresh=[r for r in selected if all((int(r[1])>>(2*k)&3)<=1 for k in range(55))]
    imported=[r for r in selected if r not in fresh]
    assert len(fresh)==45 and sum(r[3] for r in fresh)==440190
    assert [r[0] for r in imported]==[80,84,87,195,199,202,283,287,290]
    assert sum(r[3] for r in imported)==48465
    return f,selected,fresh,imported


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
    assert len(tails)==7 and all(t['budget']==11 for t in tails)
    assert [(t['parent_index'],t['image'],t['case']) for t in tails]==[
        (182,0,0),(192,24,301),(196,0,0),(270,74,285),
        (273,75,288),(275,40,301),(288,0,0)]
    return tails


def residual_tails(output):
    return [t for t in all_tails(output) if t['parent_index']!=192]


def tail_path(output,tail):
    return output/f"tail_class{tail['parent_index']:03d}_image{tail['image']:03d}.cnf"
