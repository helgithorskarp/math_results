"""Pin the entire 13-executable/2-JSON input closure before any parent import."""
from pathlib import Path
from hashlib import sha256
import json
ROOT=Path(__file__).resolve().parent.parent
def check(optional=False):
    record=json.loads(Path(__file__).with_name('INPUTS.json').read_text())
    counts={kind:0 for kind in ('mandatory executable','optional CAS executable','whole mathematical input')}
    for name,row in record['inputs'].items():
        counts[row['kind']]+=1
        if row['kind']=='optional CAS executable' and not optional:continue
        data=(ROOT/name).read_bytes()
        if len(data)!=row['bytes'] or sha256(data).hexdigest()!=row['sha256']:
            raise ValueError('Changed complete defining input: '+name)
    if list(counts.values())!=[13,2,2]:raise ValueError('Changed entire declared input closure')
    return counts
