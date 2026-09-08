"""Produce the arithmetic word in Q(zeta24), using FLINT polynomial arithmetic."""
from pathlib import Path
import argparse, hashlib, json
from flint import fmpz_poly as Poly

S = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    cert = json.loads((S / 'CERTIFICATE.json').read_text())
    raw = (args.work / 'exact_points.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == cert['inputs']['exact_points.json']['sha256'], 'point identity')
    data = json.loads(raw)
    require(data['denominator'] == 96, 'coordinate denominator')
    f = Poly([1, 0, 0, 0, -1, 0, 0, 0, 1])
    t = Poly([0, 1])
    one, zero = Poly([1]), Poly([])
    powers = [t ** j % f for j in range(24)]
    ii = powers[6]
    rad = [one, powers[3] + powers[21], powers[2] + powers[22]]
    rad.append(rad[1] * rad[2] % f)
    require(ii * ii % f == -one, 'i')
    require(all(x * x % f == n * one for x, n in zip(rad, (1, 2, 3, 6))), 'radical bridge')
    colours = []
    for v, row in enumerate(data['points']):
        a = sum((row[j] * rad[j] for j in range(4)), zero)
        b = sum((row[j + 8] * rad[j] for j in range(4)), zero)
        numerator = (a + ii * b) % f
        divisor = 32 if v <= 32256 else 4
        coefficients = [int(numerator[j]) for j in range(8)]
        require(all(x % divisor == 0 for x in coefficients), 'dyadic integrality at vertex ' + str(v))
        colour = 0
        for j, x in enumerate(coefficients):
            if (x // divisor) % 2:
                colour ^= (1, 2, 3)[j % 3]
        colours.append(colour)
    word = bytes([4] + colours[1:32257] + [(1, 0, 2, 3)[c] for c in colours[32257:]])
    args.output.write_bytes(word)
    print(json.dumps({'vertices': len(word), 'five_colour_word_sha256': hashlib.sha256(word).hexdigest(),
                      'field': 'Q[t]/(t^8-t^4+1)', 'all_coefficient_divisibility_checks_passed': True,
                      'solver_calls': 0}, indent=2))


if __name__ == '__main__':
    main()
