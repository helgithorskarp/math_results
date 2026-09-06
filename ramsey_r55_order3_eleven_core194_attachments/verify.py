#!/usr/bin/env python3
"""Fresh reconstruction of all nine complete moving-profile formulas."""
from pathlib import Path
import argparse
import json
import time
import prepare


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    source=a.source_work.resolve();work=a.work.resolve()
    prepare.profiles.require(work!=source and not work.is_relative_to(prepare.ROOT.parent),'fresh external verification path')
    prepare.profiles.require(not work.exists(),'verification directory must be fresh')
    before=time.monotonic();old=json.loads((source/'result.json').read_text())
    prepare.profiles.require(old['complete'] and old['solver_calls']==0 and prepare.sources()==old['contract']['sources'],'complete frozen construction')
    # The stored JSON turns integer histogram keys into strings. Compare the
    # complete records in the same serialization domain without dropping fields.
    fresh=json.loads(json.dumps(prepare.build(work)))
    for key in fresh:prepare.profiles.require(fresh[key]==old[key],'fresh complete '+key+' differs')
    prepare.profiles.require(prepare.sources()==old['contract']['sources'],'sources unchanged after verification')
    result=dict(verified=True,cases=fresh['cases'],solver_calls=0,whole_core_exclusions=[],seconds=round(time.monotonic()-before,6),
        base=fresh['base_generation']['formula'],joint_profiles=119,moving_cases=9,
        local_audit=fresh['local_audit'],full_corruptions_rejected=fresh['full_corruptions_rejected'])
    prepare.atomic(work/'verification.json',result)
    print('PASS fresh119profile certificate and9full UNTESTED formulas; '+str(result['seconds'])+'s')
