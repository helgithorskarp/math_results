"""One bounded serial audit child. Isolated normal/optimized Python supported."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import argparse,hashlib,json
from field import need
import jets
import literal_controls


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--profile',type=int,choices=range(4))
    parser.add_argument('--record',type=Path)
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--no-fixture',action='store_true')
    args=parser.parse_args()
    primary=jets.run()
    out=primary if args.profile is None else literal_controls.run(primary,(args.profile,))
    mode='primary'if args.profile is None else 'profile-'+str(args.profile)
    data=json.dumps(out,sort_keys=True,separators=(',',':')).encode()
    receipt={'mode':mode,'record_sha256':hashlib.sha256(data).hexdigest(),'record_bytes':len(data),
             'coefficient_comparisons':out.get('coefficient_comparisons',0),
             'literal_comparisons':out.get('literal_comparisons',0),
             'mathematical_damages_rejected':out.get('mathematical_damages_rejected',[])}
    if not args.no_fixture:
        expected=json.loads(args.expected.read_text())
        need(expected['modes'][mode]==receipt,'complete independently generated record fingerprint')
    if args.record:args.record.write_bytes(data+b'\n')
    print(json.dumps(receipt,sort_keys=True))


if __name__=='__main__':main()
