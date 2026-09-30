"""Meaningful malformed-certificate controls, separate from discovery."""
import copy
import json
from pathlib import Path
from check_packings import check, InvalidCertificate


def main():
    original = json.loads(Path(__file__).with_name('packings.json').read_text())
    controls = {}
    data = copy.deepcopy(original)
    data['field'] = 313
    controls['wrong_field'] = data
    data = copy.deepcopy(original)
    data['cases'].pop()
    controls['missing_parameter_case'] = data
    data = copy.deepcopy(original)
    data['cases'][0]['coefficients'] = [0]
    controls['zero_polynomial'] = data
    data = copy.deepcopy(original)
    data['cases'][1] = copy.deepcopy(data['cases'][0])
    controls['duplicate_parameter_case'] = data
    data = copy.deepcopy(original)
    data['cases'][0]['aps'][0] = [1, 2]
    controls['root_used'] = data
    data = copy.deepcopy(original)
    data['cases'][0]['aps'][0] = [2, 1]
    controls['bichromatic_AP'] = data
    data = copy.deepcopy(original)
    data['cases'][0]['aps'][1] = data['cases'][0]['aps'][0][:]
    controls['overlapping_residue_supports'] = data
    data = copy.deepcopy(original)
    data['cases'][0]['aps'][0][1] = 0
    controls['zero_difference'] = data
    data = copy.deepcopy(original)
    data['cases'][0]['aps'][0][1] = 311
    controls['field_zero_difference'] = data
    data = copy.deepcopy(original)
    data['cases'][0]['aps'][0][0] = 0
    controls['zero_position'] = data
    data = copy.deepcopy(original)
    data['cases'][0]['aps'][0][0] = 312
    controls['unnormalized_position'] = data
    data = copy.deepcopy(original)
    data['cases'][0]['aps'].pop()
    controls['missing_packing_member'] = data
    data = copy.deepcopy(original)
    data['packing_size'] = 21
    controls['unsupported_stronger_bound'] = data
    rejected = {}
    for name, data in controls.items():
        try:
            check(data)
        except InvalidCertificate as exc:
            rejected[name] = str(exc)
        else:
            raise AssertionError(f'Accepted malformed certificate: {name}')
    print(json.dumps({'status': 'ALL_MALFORMED_CERTIFICATE_CONTROLS_REJECTED',
                      'rejected_controls': rejected, 'count': len(rejected)}, sort_keys=True))


if __name__ == '__main__':
    main()
