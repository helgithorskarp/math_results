"""Serial offline full reproduction against previously frozen evidence."""
import argparse
import json
from pathlib import Path
import resource
import time
import audit,bridge,controls,cyclic,lower
from core import HERE,digest,require

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);args=p.parse_args()
    work=Path(args.work).resolve();require(work!=HERE and HERE not in work.parents,'generated outputs must stay outside source');work.mkdir(parents=True,exist_ok=True)
    started=time.monotonic()
    controlled=controls.check()
    record,carrier_seconds=audit.audit(work)
    record.update(ordinary_bridge=bridge.check(),literal_witnesses=lower.all_witnesses(),controls=controlled,cyclic_word_orbits=cyclic.audit())
    record=json.loads(json.dumps(record,sort_keys=True))
    require(record==json.loads((HERE/'EXPECTED.json').read_text()),'whole frozen mathematical record differs')
    (work/'result.json').write_text(json.dumps(record,sort_keys=True)+'\n')
    receipt={'status':'PASS_COLD_FULL_INVOLUTION_REVIEW','expected_sha256':digest(record),'maximum_code_size':69,'multiplicity3_maximum':56,'multiplicity4_maximum':58,'cycle_power_types':14,'cyclic_type_10_6_1_1_maximum':4,'carrier_seconds':carrier_seconds,'seconds':time.monotonic()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (work/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,sort_keys=True))

if __name__=='__main__':main()
