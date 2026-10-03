"""Bind freshly checked preparation outputs; no previous arrays are read."""
import hashlib
import json
from pathlib import Path

from controls import operations_allow
from run_preparations import need, pair

ROOT = Path(__file__).resolve().parent


def main():
    operations_allow()
    pair('checked03')
    pair('free-cut-independent-03-04')
    evidence = []
    for name in ('branch03.json','cuts03.json'):
        data = (ROOT/'work'/name).read_bytes()
        evidence.append({'path':'work/'+name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    result = {'generated_evidence':evidence,'fresh_original_inputs':True}
    (ROOT/'work/preparation-bindings.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
