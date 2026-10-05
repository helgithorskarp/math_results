"""Coherent source-bound reader; existing mathematical source is unchanged."""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from reader_binding import check, require


def load(root, name):
    spec = importlib.util.spec_from_file_location('source_reader_'+name, root/(name+'.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--semantic')
    parser.add_argument('--scratch', type=Path)
    parser.add_argument('--math-import-marker', type=Path)
    args = parser.parse_args(); root = Path(__file__).resolve().parent
    check(root)  # All defining source and two defining DATA, before math imports.
    if args.math_import_marker:
        args.math_import_marker.write_text('source bound; mathematical imports begin\n')
    if args.semantic:
        require(args.scratch is not None, 'semantic scratch directory required')
        args.scratch.mkdir(parents=True, exist_ok=True)
        suite, case = args.semantic.split(':', 1)
        if suite in ('transport', 'subset'):
            print(json.dumps(load(root, 'adverse').run(suite, case, args.scratch), indent=2))
            return
        require(suite == 'weighted', 'unknown semantic suite')
        mod = load(root, 'weighted_radius'); record = mod.record()
        gates = {
            'original_triple_indicator_all81': 'certificate original weights',
            'all_original_edge_product_census': 'certificate original edge products',
            'weighted_old_cap_lambda_coefficients': 'certificate original weighted comparison cap',
            'selected_lambda_affine': 'certificate concave lambda optimizer',
            'optimized_unnormalized_F_polynomial_low_to_high': 'certificate exact weighted polynomial',
            'weighted_root_strict_coarse_cage': 'certificate exact root cage',
        }
        require(case in gates, 'unknown weighted semantic field')
        bad = copy.deepcopy(record)
        if case == 'original_triple_indicator_all81':
            bad[case][0] = 1-bad[case][0]
        elif case == 'all_original_edge_product_census':
            bad[case]['(1+lambda)^2'] = 1
        else:
            bad[case][0] = '0'
        path = args.scratch/('weighted-'+case+'.json')
        path.write_text(json.dumps(bad, indent=2)+'\n')
        argv = sys.argv; sys.argv = ['weighted_radius.py', '--check', str(path)]
        try:
            mod.main()
        except ValueError as error:
            require(str(error) == gates[case], 'weighted damage reached wrong gate')
            print(json.dumps({'suite': suite, 'case': case, 'designated_gate': gates[case],
                              'rejected_exactly_at_designated_gate': True}, indent=2))
        else:
            raise ValueError('weighted damaged record unexpectedly accepted')
        finally:
            sys.argv = argv
        return
    components = {
        'subset': load(root, 'subset_radius').check(),
        'transport': load(root, 'check_transport').check(root/'TRANSPORT.json'),
        'critical_subset': load(root, 'critical_extension').check(),
        'weighted': load(root, 'weighted_radius').record(),
        'critical_weighted': load(root, 'weighted_critical').check(),
    }
    result = {'actual_agent': 'six-downset-3', 'role': 'researcher',
              'status': 'Source reader of previously paid private mathematics; ordinary all-real proofs separate',
              'components': components}
    raw = (json.dumps(result, indent=2)+'\n').encode()
    expected = json.loads((root/'EXPECTED.json').read_text())  # AFTER whole fresh math.
    for name, value in components.items():
        data = (json.dumps(value, indent=2)+'\n').encode(); pin = expected['whole_components'][name]
        require(len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['SHA256'],
                'ENTIRE component differs: '+name)
    require(len(raw) == expected['whole_result_bytes'] and
            hashlib.sha256(raw).hexdigest() == expected['whole_result_SHA256'], 'ENTIRE coherent result differs')
    sys.stdout.write(raw.decode())


if __name__ == '__main__':
    main()
