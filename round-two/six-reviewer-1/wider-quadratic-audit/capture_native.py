"""LATE producer instrumentation after pin checks, NOT independent mathematics."""
from pathlib import Path
import argparse,hashlib,json,sys

def main():
    ap=argparse.ArgumentParser();ap.add_argument('target',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
    target=a.target.resolve()
    pins=json.loads(Path(__file__).with_name('NATIVE_SOURCE.json').read_text())
    for name,item in pins['files'].items():
        data=(target/name).read_bytes()
        if len(data)!=item['bytes']or hashlib.sha256(data).hexdigest()!=item['sha256']:
            raise ValueError('producer source pin BEFORE import: '+name)
    sys.path.insert(0,str(target));import arithmetic as ar
    old=ar.identity;oldz=ar.zid;maps=[]
    def capture(rows,name,lhs,rhs):
        old(rows,name,lhs,rhs)
        maps.append({'name':name,'kind':'rational','lhs':ar.encoded(lhs),'rhs':ar.encoded(rhs)})
    def capturez(rows,name,lhs,rhs):
        oldz(rows,name,lhs,rhs)
        maps.append({'name':name,'kind':'gaussian-cyclotomic','lhs':[[ar.encoded(p)for p in side]for side in lhs],'rhs':[[ar.encoded(p)for p in side]for side in rhs]})
    ar.identity=capture;ar.zid=capturez
    import verify
    record=verify.build_record();wanted=json.loads((target/'EXPECTED.json').read_text(),object_pairs_hook=verify.pairs,parse_constant=verify.reject_constant)
    ar.need(ar.canonical(record)==ar.canonical(wanted),'entire unchanged producer record')
    out={'producer_whole_record_sha256':ar.sha256(ar.canonical(record)).hexdigest(),'full_maps':maps,'record':record,'trust':'LATE producer replay/instrumentation only. Independent comparison consumes this as data and imports no producer source.'}
    a.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'status':'PASS','producer_whole_record_sha256':out['producer_whole_record_sha256'],'complete_captured_maps':len(maps),'export_bytes':a.output.stat().st_size},sort_keys=True))

if __name__=='__main__':main()
