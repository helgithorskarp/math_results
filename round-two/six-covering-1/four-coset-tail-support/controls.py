"""Both independent engines reject compact certificate-field damage."""
from copy import deepcopy
import json
from pathlib import Path

import audit
import check


def main():
    expected = json.loads((Path(__file__).resolve().parent / 'expected.json').read_text())
    damages = [('candidate_target_size', 180), ('free_resource_mass', 599),
               ('other_twenty_resource_mass', 243), ('canonical_phase_multisets', 350),
               ('canonical_copy_partitions', 854), ('phase_partition_cases', 598499)]
    counts = {}
    for name, engine in [('complete_bitset', check), ('physical_written_proof', audit)]:
        result = engine.compute()
        engine.validate(result, expected)
        rejected = 0
        for field, value in damages:
            changed = deepcopy(result)
            changed[field] = value
            try:
                engine.validate(changed, expected)
            except RuntimeError:
                rejected += 1
            else:
                raise RuntimeError(name + ' accepted damaged resource/domain field')
        changed = deepcopy(result)
        changed['selected_seven_top_scores'][1]['maximum_hits'] -= 1
        try:
            engine.validate(changed, expected)
        except RuntimeError:
            rejected += 1
        else:
            raise RuntimeError(name + ' accepted a false sharp selected-seven bound')
        counts[name] = rejected
    print(json.dumps({'status': 'DAMAGE_CONTROLS_PASSED', 'damages_per_engine': counts,
                      'legitimate_baselines_passed': True,
                      'false_sharp_profile_bound_rejected': True}))


if __name__ == '__main__':
    main()
