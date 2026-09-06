"""Check package identity and reproduce the exact finite evidence."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent


def main():
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError(('manifest mismatch',name))
    for flags in ([],['-O']):
        for source,expected in [('derive.py','certificate.json'),('check.py','expected_kernel.json'),('controls.py','expected_controls.json')]:
            out=subprocess.check_output([sys.executable,*flags,'-B',str(ROOT/source)])
            if out!=(ROOT/expected).read_bytes():raise ValueError(('reproduction mismatch',flags,source))
    print(json.dumps({'status':'VERIFIED_PENTAGON_M216_COMPLETE_CANDIDATE_BRANCH','variants':2,
                      'admissible_stars':14641,'ordinary_stars_required':22,'ordinary_stars_allowed':20,
                      'physical43_controls':52,'general_M216_keys_decided':0,'solver_runs':0},indent=2))

if __name__=='__main__':main()
