"""Whole frozen standard-library verification; explicit checks survive -O."""
from pathlib import Path
from hashlib import sha256
import json
import time
import resource
import sys
import input_pins
input_pins.check()
import residual
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE))
import calibrate_actions
import check_coefficients
import controls
for helper in (calibrate_actions, check_coefficients, controls):
    residual.require(Path(helper.__file__).resolve().parent == SOURCE,
                     'source-local verification helper: '+helper.__name__)


def run():
    start = time.perf_counter()
    root = Path(__file__).resolve().parent
    frozen = json.loads((root/'EXPECTED.json').read_text())
    frozen_digest = frozen.pop('record_sha256')
    residual.require(residual.digest(frozen) == frozen_digest,
                     'complete frozen record digest')
    for name, wanted in frozen['certificates'].items():
        data = (root/name).read_bytes()
        residual.require(sha256(data).hexdigest() == wanted['file_sha256'],
                         'entire frozen certificate file: '+name)
        decoded = json.loads(data)
        saved = decoded.pop('record_sha256')
        residual.require(residual.digest(decoded) == saved == wanted['record_sha256'],
                         'entire frozen certificate record: '+name)
    actual = {}
    for name, function in (('CALIBRATION.json', calibrate_actions.run),
                           ('PORTABLE-CHECK.json', check_coefficients.run),
                           ('CONTROLS.json', controls.run)):
        function()
        actual[name] = json.loads((root/name).read_text())
        residual.require(actual[name] == frozen['outputs'][name],
                         'entire original replayed record: '+name)
    input_pins.check()
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'status': 'exact whole records pass; ordinary bridges unformalized; independent review pending',
              'frozen_record_sha256': frozen_digest,
              'complete_frozen_outputs_equal': True,
              'complete_certificates_equal': True,
              'all_ten_imported_executables_equal': True,
              'original_positions': 365514,
              'entire_original_first_moments': 9,
              'entire_original_second_moments': 6,
              'entire_cleared_forms': 8,
              'uniform_coefficients': 406,
              'norm_coefficient_counts': [10, 11],
              'semantic_damages_rejected': 6}
    result['record_sha256'] = residual.digest(result)
    (root/'RESULTS.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'digest': result['record_sha256'],
                      'frozen_digest': frozen_digest,
                      'seconds': time.perf_counter()-start,
                      'peak_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
    return result


if __name__ == '__main__':
    run()
