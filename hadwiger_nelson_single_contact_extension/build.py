"""Generate compact positive witnesses for the two cubic exceptions."""
import argparse,json,hashlib,time
from itertools import product
from pathlib import Path
from colour import GRAPHS,canonical,colour
HERE=Path(__file__).resolve().parent

def generate():
    patterns=sorted({canonical(p)[0] for p in product(range(4),repeat=6)})
    cert={name:{''.join(map(str,p)):''.join(map(str,colour(6,edges,p))) for p in patterns}
          for name,edges in GRAPHS.items()}
    return cert

def encoded(cert):return (json.dumps(cert,separators=(',',':'),sort_keys=True)+'\n').encode()

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--discover',action='store_true');a=p.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic();cert=generate();raw=encoded(cert)
    if not a.discover and raw!=(HERE/'certificate.json').read_bytes():raise ValueError('certificate mismatch')
    (out/'certificate.json').write_bytes(raw)
    result={'canonical_patterns_per_graph':len(cert['K33']),'canonical_witnesses':sum(map(len,cert.values())),
        'labelled_list_profiles_per_graph':4**6,'certificate_sha256':hashlib.sha256(raw).hexdigest(),
        'certificate_bytes':len(raw),'native_solver_calls':0,'seconds':time.monotonic()-start}
    (out/'build.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
