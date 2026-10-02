"""Postseal comparison adapter. Byte-check all immutable target inputs BEFORE import."""
import sys,json,hashlib,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent

def gate(directory):
    pins=json.loads((HERE/'TARGET_ACCESS.json').read_text())['whole_files']
    for name,pin in pins.items():
        data=(directory/name).read_bytes()
        if len(data)!=pin['bytes'] or hashlib.sha256(data).hexdigest()!=pin['sha256']:raise ValueError('native byte pin differs BEFORE import: '+name)
    return pins

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: export_target.py IMMUTABLE_NATIVE_DIRECTORY OUTPUT_JSON')
    directory=Path(sys.argv[1]).resolve();gate(directory);sys.path.insert(0,str(directory))
    spec=importlib.util.spec_from_file_location('late_target',directory/'verify.py');native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    scalar=[];physical=[];identity=native.identity;gid=native.gid;zid=native.zid
    def scalar_capture(rows,name,lhs,rhs):
        identity(rows,name,lhs,rhs)
        scalar.append({'name':name,'lhs':native.encoded(lhs),'rhs':native.encoded(rhs)})
    def gaussian_capture(rows,name,lhs,rhs):
        gid(rows,name,lhs,rhs)
        for k,label in [(0,' real'),(1,' imaginary')]:scalar.append({'name':name+label,'lhs':native.encoded(lhs[k]),'rhs':native.encoded(rhs[k])})
    def phase_capture(rows,name,lhs,rhs):
        zid(rows,name,lhs,rhs)
        physical.append({'name':name,'lhs':[[native.encoded(p) for p in side] for side in lhs],'rhs':[[native.encoded(p) for p in side] for side in rhs]})
    native.identity=scalar_capture;native.gid=gaussian_capture;native.zid=phase_capture
    record=native.build_record();wanted=json.loads((directory/'EXPECTED.json').read_text())
    if native.canonical(record)!=native.canonical(wanted):raise ValueError('whole freshly reconstructed native record mismatch')
    output={'record':record,'entire_scalar_coefficient_maps':scalar,'entire_physical_field_maps':physical,'target_record_sha256':hashlib.sha256(native.canonical(record)).hexdigest(),'whole_sources_checked_before_import':True,'comparison_only_after_seal':True}
    Path(sys.argv[2]).write_text(json.dumps(output,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'scalar_maps':len(scalar),'physical_maps':len(physical),'native_record_sha256':output['target_record_sha256'],'comparison_only_after_seal':True}))
