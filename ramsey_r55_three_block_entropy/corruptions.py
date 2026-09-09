"""Reject incomplete or false numerical/projection certificates."""
from pathlib import Path
import argparse,json,shutil
from verify import verify

def run(producer,checker,global_file,out):
    out=Path(out);out.mkdir();producer=Path(producer);checker=Path(checker);rejected=[]
    def reject(label,p=producer,c=checker,g=global_file):
        try:verify(p,c,g)
        except (ValueError,KeyError,StopIteration):rejected.append(label)
        else:raise ValueError('accepted corruption: '+label)
    for kind in ('read','root_upper','missing_class','class_weight','decimal'):
        x=json.loads(Path(global_file).read_text())
        if kind=='read':x['classes'][0]['read']+=1
        elif kind=='root_upper':x['classes'][0]['probability_upper']['numerator']=0
        elif kind=='missing_class':x['classes'].pop()
        elif kind=='class_weight':x['classes'][0]['before']+=1
        else:x['removed_lower_decimal']='0.99'
        path=out/(kind+'.json');path.write_text(json.dumps(x));reject(kind,g=path)
    for name in ('PROFILE.tsv','HISTOGRAM.tsv','RR.bin','TOTALS.tsv'):
        copy=out/name.replace('.','_');copy.mkdir()
        for p in checker.iterdir():
            if p.is_file():shutil.copyfile(p,copy/p.name)
        path=copy/name;raw=bytearray(path.read_bytes());raw[len(raw)//2]^=1;path.write_bytes(raw);reject(name,c=copy)
    return dict(status='VERIFIED_NUMERICAL_CERTIFICATE_CORRUPTIONS',rejected=len(rejected),cases=rejected)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('producer');p.add_argument('checker');p.add_argument('global_file');p.add_argument('out');a=p.parse_args()
    print(json.dumps(run(a.producer,a.checker,a.global_file,a.out),sort_keys=True))
