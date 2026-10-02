import argparse,hashlib,json,pathlib
import rows,oracle

base=pathlib.Path(__file__).resolve().parent
def encode(value):return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
def compute():
    instance=json.loads((base/'fixtures.json').read_text());proof=rows.compute(instance['stars']);audit=oracle.compute(instance['stars'],proof)
    result={'agent':'six-reviewer-5','role':'independent mathematical reviewer','exact':proof,'independent_audit':audit}
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',type=pathlib.Path);args=p.parse_args();record=compute();raw=encode(record)
    if args.check:rows.need(raw==args.check.read_bytes(),'entire frozen normal/O record')
    print(raw.decode(),end='')
