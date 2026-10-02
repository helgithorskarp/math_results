"""Cold self-contained check; explicit guards survive optimized Python."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import time
from audit import build
from controls import checks
from star_primitives import digest,require

HERE = Path(__file__).resolve().parent


def pin_inputs(base=HERE):
    inputs = json.loads((base/'INPUTS.json').read_text())
    require(len({r['path'] for r in inputs}) == len(inputs),'duplicate pin')
    for r in inputs:
        require(hashlib.sha256((base/r['path']).read_bytes()).hexdigest() == r['sha256'],'changed input: '+r['path'])
    return len(inputs)


def pin_controls(work):
    work.mkdir()
    inputs = json.loads((HERE/'INPUTS.json').read_text())
    shutil.copyfile(HERE/'INPUTS.json',work/'INPUTS.json')
    for row in inputs: shutil.copyfile(HERE/row['path'],work/row['path'])
    rejected = []
    for row in inputs:
        target = work/row['path']; original = target.read_bytes(); target.write_bytes(original+b' ')
        try: pin_inputs(work)
        except ValueError: rejected.append(row['path'])
        else: raise ValueError('changed pinned input accepted')
        target.write_bytes(original)
    pin_inputs(work)
    return rejected


def main():
    p = argparse.ArgumentParser(); p.add_argument('--work',type=Path,required=True); args = p.parse_args()
    require(not args.work.exists() or not any(args.work.iterdir()),'cold work directory must be empty')
    require(HERE not in (args.work.resolve(),*args.work.resolve().parents),'generated work must be outside source')
    started = time.monotonic(); pins = pin_inputs(); record = build(args.work); controls = checks()
    controls['changed_external_inputs_rejected'] = pin_controls(args.work/'input-controls')
    record = json.loads(json.dumps(record)); expected = json.loads((HERE/'EXPECTED.json').read_text())
    require(record == expected,'whole frozen independent mathematical record differs')
    require(time.monotonic()-started < 60,'INCOMPLETE fixed60-second whole-audit guard')
    (args.work/'RECORD.json').write_text(json.dumps(record,sort_keys=True)+'\n')
    result = {'status':'PASS_COLD_COMPLETE_P7_SELECTOR_REVIEW','mathematical_sha256':digest(record),
              'input_pins':pins,'coarse_rows':117,'refined_rows':138,'claimed_survivors_closed':50,
              'sharp_opposite_hub_maximum':61,'unit_opposite_hub_core_impossible':True,
              'new_E2t0_normalized_excluded':113,'new_E2t0_normalized_remaining':100,
              'controls':controls,'seconds':time.monotonic()-started}
    (args.work/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))


if __name__ == '__main__': main()
