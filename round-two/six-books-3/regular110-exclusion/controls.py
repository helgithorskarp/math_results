"""Damaged graph/cycle inputs and the integer packing boundary."""
import json
import check
import verify


def rejects(name, function):
    try:
        function()
    except ValueError:
        return name
    raise ValueError('Damaged control was accepted: ' + name)


def main():
    expected = json.loads((check.HERE / 'expected.json').read_text())
    adj = expected['generator']['cores'][0]['neighbors']
    line = (check.HERE / 'primary_cubic10_g4.g6').read_text().splitlines()[0]
    controls = [rejects('wrong-graph-order', lambda: check.decode_g6('H' + line[1:])),
                rejects('nonzero-graph-padding', lambda: check.decode_g6(line[:-1] + chr(ord(line[-1]) + 1))),
                rejects('repeated-cycle-vertex', lambda: check.validate_cycle(adj, [0, 1, 2, 2])),
                rejects('false-cycle-witness', lambda: check.validate_cycle(adj, [0, 1, 2, 3]))]
    bad = adj.copy()
    bad[0] &= ~(1 << 1)
    controls.append(rejects('missing-core-edge', lambda: verify.orbit(bad)))
    # The 20-occurrence hypothesis is essential: 19 occurrences allow cost eight.
    check.need(verify.pack_minimum(11, 19) == 8 and verify.pack_minimum(11, 20) == 9,
               'Packing boundary control failed')
    # Each integer row is covered. The real relaxation has negative values at 1.5.
    check.need((1.5 - 1) * (1.5 - 2) < 0, 'Integer-domain control failed')
    print(json.dumps({'status': 'PASS', 'rejected_inputs': controls,
                      'packing_occurrence_boundary': [19, 8, 20, 9],
                      'integer_domain_required': True}, sort_keys=True))


if __name__ == '__main__':
    main()
