#!/usr/bin/env python3
"""Fresh serial proof replay; author replay/representation check is optional."""
from pathlib import Path
import argparse,hashlib,json,sys
from reproduce import child,ROOT
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--author-directory',type=Path);a=p.parse_args()
    if a.work.exists():raise RuntimeError('require a fresh work directory')
    for name in ('first-seal.json','extra-seal.json'):
        s=json.loads((ROOT/name).read_bytes());pins=s.get('source_sha256',{'classify.py':s.get('classify_sha256')})
        for file,sha in pins.items():
            if digest(ROOT/file)!=sha:raise RuntimeError('sealed source changed: '+file)
    a.work.mkdir(parents=True);mode=['-O','-B'] if sys.flags.optimize else ['-B'];runs={}
    for name in ('reproduce','classify','certificates'):
        raw,runs[name]=child([sys.executable,*mode,ROOT/(name+'.py'),'--work',a.work.resolve()]);(a.work/(name+'-validation.json')).write_bytes(raw)
        if name!='reproduce':
            frozen=ROOT/('EXTRA.json' if name=='classify' else 'CERTIFICATES.json')
            if frozen.exists() and frozen.read_bytes()!=raw:raise RuntimeError('whole '+name+' record differs')
    for name in ('NORMAL_FORMS.json','ISOMORPHISMS.json','FOUR_CLASS_EXAMPLES.json'):
        if (a.work/name).read_bytes()!=(ROOT/name).read_bytes():raise RuntimeError('whole compact certificate differs: '+name)
    if a.author_directory:
        source=a.author_directory.resolve();author_work=a.work.resolve()/'author'
        manifest=json.loads((ROOT/'AUTHOR_SOURCE.json').read_bytes())
        for entry in manifest['files']:
            path=source/Path(entry['path']).name
            if not path.is_file() or path.stat().st_size!=entry['bytes'] or digest(path)!=entry['sha256']:raise RuntimeError('exact author source differs: '+entry['path'])
        raw,runs['author_replay']=child([sys.executable,*mode,source/'reproduce.py','--work',author_work]);(a.work/'author-validation.json').write_bytes(raw)
        raw,runs['author_compare']=child([sys.executable,*mode,ROOT/'compare_author.py','--work',a.work.resolve(),'--author-work',author_work]);(a.work/'AUTHOR_COMPARISON.json').write_bytes(raw)
        if raw!=(ROOT/'AUTHOR_COMPARISON.json').read_bytes():raise RuntimeError('whole author comparison record differs')
    records={name:json.loads((a.work/name).read_bytes()) for name in ('MATHEMATICS.json','classify-validation.json','certificates-validation.json')}
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();(a.work/'COMPLETE.json').write_bytes(raw)
    print(json.dumps({'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','complete':True,'python':sys.version.split()[0],'optimized':bool(sys.flags.optimize),'native_threads':1,'serial_math_jobs':1,'fixed_child_seconds':60,'whole_complete_bytes':len(raw),'whole_complete_sha256':hashlib.sha256(raw).hexdigest(),'author_replay_requested':bool(a.author_directory),'runs':runs},sort_keys=True))
if __name__=='__main__':main()
