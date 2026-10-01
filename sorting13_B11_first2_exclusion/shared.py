"""Pinned public inputs and the complete first(2,10) quota selector."""
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
    # Lexicographic combinations(range(11),2): (2,10) has index26.
    selected=[[i,code,e,n] for i,(code,e,n) in enumerate(table) if e==11 and ((int(code)>>52)&3)]
    assert len(selected)==36 and sum(r[3] for r in selected)==196875
    old=read(repo/OLD)
    imported=[r for r in selected if r[1]==old['class_code']]
    assert imported==[[13,'349871875148001158693749134458897',11,5385]]
    fresh=[r for r in selected if r[1]!=old['class_code']]
    assert len(fresh)==35 and sum(r[3] for r in fresh)==191490
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
