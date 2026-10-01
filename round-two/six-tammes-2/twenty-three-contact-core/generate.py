"""Regenerate the exact four-branch and packing certificate, with no float input."""
from pathlib import Path
import argparse,json
import check

CONFIG={'format':1,'interval':[[14,25],[593,1000]],'bernstein_pieces':8,
        'noncontact_pieces':16,'sqrt_scale':10**6,'noncontact_upper':'1/2',
        'edges':[list(e) for e in check.EDGES],
        'root_bracket':['0.59260590292507377809642492233275','0.59260590292507377809642492233276']}
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--prerequisite-root',type=Path,default=check.ROOT)
 parser.add_argument('--output',type=Path,required=True)
 args=parser.parse_args()
 funcs,base=check.derive(args.prerequisite_root)
 data={**CONFIG,'functions':check.manifest(funcs)}
 args.output.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'status':'GENERATED','functions':len(funcs),'canonical_certificate_sha256':check.digest(data)}))
