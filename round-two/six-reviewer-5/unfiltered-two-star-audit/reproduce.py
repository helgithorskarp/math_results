"""Cold, serial, offline reproduction against previously frozen records."""
import argparse
import json
import resource
from pathlib import Path
import audit
import controls

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',required=True);args=parser.parse_args()
    work=Path(args.work).resolve();base=audit.HERE.resolve()
    audit.need(work!=base and base not in work.parents, 'generated outputs must stay outside source directory')
    work.mkdir(parents=True,exist_ok=True)
    controlled=controls.run()
    record,witnesses,transports,seconds=audit.run()
    audit.need(record==json.loads((base/'EXPECTED.json').read_text()), 'whole frozen mathematical record differs')
    audit.need(witnesses==json.loads((base/'WITNESSES.json').read_text()), 'whole frozen positive witnesses differ')
    (work/'transports.json').write_bytes(audit.encode(transports)+b'\n')
    (work/'result.json').write_bytes(audit.encode(record)+b'\n')
    result={'status':'PASS_COLD_COMPLETE_UNFILTERED_REVIEW','controls':controlled,
            'expected_sha256':audit.digest(record),'witnesses_sha256':audit.digest(witnesses),
            'maximum_total':record['maximum_total'],'maximum_lambda4_total':record['maximum_lambda4_total'],
            'seconds':seconds,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (work/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
