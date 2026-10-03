"""Portable semantic corruption controls, after the complete scalar cover replay.

Actual positive ground records are cached only for the damaged invocations.
Expensive embeddings can be omitted there because the positive invocation
already recomputed all 1042 complete original-input embeddings.
"""
import copy
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent


def main():
    start = time.monotonic()
    spec = importlib.util.spec_from_file_location('separate_scalar_cover_with_control_cache', ROOT / 'check_cover.py')
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    data = json.loads((ROOT / 'generated/cover-produced.json').read_text())
    original = data['mathematical']
    checked = json.loads((ROOT / 'generated/cover-checked-normal.json').read_text())
    other = json.loads((ROOT / 'generated/cover-checked-optimized.json').read_text())
    c.need(checked['mathematical'] == other['mathematical'] and
           c.digest(checked['mathematical']) == '5da3911448df2171ae2823136b750a57ac6fd87d24d546a342cfade4b44484c4' and
           c.digest(original) == 'f81df63d10258d3560c7915e617d04f9f8caf76cfd961dc517b607e2bf6066ab',
           'full positive scalar cover is absent or changed')
    g = checked['mathematical']
    c.GROUND_CACHE = (g['fresh_original_ground_records'], {4: 11, 5: 11, 6: 11, 7: 13, 9: 11, 10: 12},
                      g['fresh_ground_assignments'], g['early_negative_original_checks'])
    controls = []

    def add(name, change):
        p = copy.deepcopy(data)
        change(p['mathematical'])
        # Supply the correct digest of the semantically damaged packet,
        # so a superficial source seal is never the intended rejection.
        p['entire_mathematical_record_sha256'] = c.digest(p['mathematical'])
        controls.append((name, p))

    add('literal_prefix_endpoint', lambda m: m['literal_prefix'][-1].__setitem__(1, 5))
    add('missing_labelled_binary_forest', lambda m: m['all900_raw_binary_forests'].pop())
    add('changed_actual_forest_charge', lambda m: m['all900_raw_binary_forests'][0]['stages'][0][0][0].__setitem__(1, 0))
    add('omitted_complete_semigroup_edge', lambda m: m['three_input_library']['all_edges'].pop())
    add('changed_whole_library_function', lambda m: m['three_input_library']['states'][0]['columns'].__setitem__(0, 0))
    add('missing_retained_BG_word', lambda m: m['all_retained_raw_BG_words'].pop())
    add('different_ordered_Q_function', lambda m: m['all_retained_raw_BG_words'][0]['actual_Q_key'].__setitem__(0,
        m['all_retained_raw_BG_words'][0]['actual_Q_key'][0] ^ 1))
    add('missing_full_prefix_function_class', lambda m: m['whole_Q_function_classes'].pop())
    add('changed_minimum_length_representative', lambda m: m['whole_Q_function_classes'][0]['shortest_word'].append([4, 5]))
    add('changed_eligible_minimum_length_raw_binding', lambda m: m['whole_Q_function_classes'][0]['minimum_length_raw_ids'].append(-1))
    add('changed_live_structural_partner', lambda m: m['whole_Q_function_classes'][0]['heads'][0].__setitem__('partner', 8))
    rejected = []
    for name, packet in controls:
        try:
            c.inspect(packet, ground=False, embed=False)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('damaged semantic catalogue accepted: ' + name)
    c.need(len(rejected) == len(controls), 'damaged catalogue did not receive a rejection')
    math = {'positive_scalar_cover_math_sha256': checked['entire_mathematical_record_sha256'],
            'damaged_packet_hashes_recomputed': True, 'catalogue_damages_rejected': rejected,
            'complete_three_binary_exclusion': False, 'controls_cache_source': 'full independently recomputed ground records'}
    output = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'ALL_PRIVATE_CATALOGUE_SEMANTIC_DAMAGES_REJECTED',
              'mathematical': math, 'entire_mathematical_record_sha256': c.digest(math),
              'seconds': time.monotonic() - start, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    target = ROOT / 'generated' / ('catalogue-damages-optimized.json' if __import__('sys').flags.optimize else 'catalogue-damages-normal.json')
    target.write_text(json.dumps(output, separators=(',', ':')) + '\n')
    print(json.dumps(output))


if __name__ == '__main__':
    main()
