"""PRIVATE separate standard-library proof of all compact inverse identities.

No producer, recipe, physical sector or polynomial-engine imports. Unchanged
source2252bca supplies the separate closed forms and integer/Fraction decoder.
Degree-complete Cartesian grids prove rational identities, not extrapolation.
The physical projection/completeness bridge remains an ordinary written proof.
"""
import os
for v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[v] = '1'
from pathlib import Path
import sys, json, signal, time, resource, argparse
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from hashlib import sha256
from independent import forms, Degree, require, add_degree, max_degree
from coefficient_check import Decoder

SCALARS = ('Eu', 'Ev', 'Et', 'mean', 'A', 'B', 'D', 'kappa')
DOMAIN = 'q>=4,h>=2 auxiliary; physical integerh>=2,q=2^(n-1),integern>=3'


def independent_model(q, h, x, y):
    D0 = 3 * h; s = q + D0; N = 2 * q + 12 * h; ell = 6 * h + 1
    c = 9 * (ell - q + 1) / (2 * ell * s)
    a = 3 * h * (ell - q + 1) / (2 * ell * s * (h - 1)); b = -2 * a
    common = (q - 1 + (2 * q - 3) * D0) / (ell * ell)
    mu = (s - 3) / 3 - common - 2 * s * c * c / (9 * (h - 1))
    beta = 2 * s / 3 - 4 * s * c * c * (h + 3) / (27 * (h - 1))
    nu = 2 * h * mu / (2 * h - 1)
    # The separate closed normalized floor-one cap plus I is the full cap
    # resolvent matrix. This imports no original-row producer.
    normalized = forms(q, h)['standard']
    H4 = [[normalized[i][j] + int(i == j) for j in range(4)] for i in range(4)]
    zu = [0, c * h / (3 * (h - 1)), 0, 3]
    zv = [b, c / (3 * (h - 1)), 1, 1]
    H2 = [[N - s * (1 + c * c), c * beta / 2],
          [3 * c * s, N - 3 * beta / 2]]
    rhs2 = [-c / 6, F(1, 2)]
    identities = {}
    for col, rhs in enumerate((zu, zv)):
        for i in range(4):
            identities[f'standard-{col}-{i}'] = sum((H4[i][j] * x[j][col] for j in range(4)), 0) - rhs[i]
    for i in range(2):
        identities[f'trace-{i}'] = sum((H2[i][j] * y[j][0] for j in range(2)), 0) - rhs2[i]
    g = [2 * s / 3, 12 * s, 2 * beta, 2 * nu]
    Eu = sum((g[i] * zu[i] * x[i][0] for i in range(4)), 0)
    Ev = sum((g[i] * zv[i] * x[i][1] for i in range(4)), 0)
    Et = (-2 * s * c * y[0][0] + beta * y[1][0]) / h
    mean = nu / (2 * h * (N - 3 * nu)); gamma = (h - 1) / (2 * h)
    scalars = dict(Eu=Eu, Ev=Ev, Et=Et, mean=mean,
                   A=(12 + gamma * Eu + 9 * mean) / N,
                   B=(2 + gamma * Ev + 2 * Et + mean) / N,
                   D=(3 - 3 * mean) / N, kappa=2 / nu + 4 / beta)
    return identities, scalars


def field_degree(field):
    return Degree(1, field.n.degree, field.degree) if field.n.terms else Degree()


def check(data):
    require(set(data) == {'domain', 'standard_solution', 'trace_solution', 'scalars'}, 'entire compact certificate key set')
    require(data['domain'] == DOMAIN, 'exact unbounded physical domain')
    require(set(data['scalars']) == set(SCALARS), 'all eight energies and lower inverse scalar')
    require(len(data['standard_solution']) == 4 and all(len(row) == 2 for row in data['standard_solution']), 'all eight standard coefficients')
    require(len(data['trace_solution']) == 2 and all(len(row) == 1 for row in data['trace_solution']), 'both trace coefficients')
    decoder = Decoder()
    x = [[decoder.field(z) for z in row] for row in data['standard_solution']]
    y = [[decoder.field(z) for z in row] for row in data['trace_solution']]
    energy = {k:decoder.field(data['scalars'][k]) for k in SCALARS}
    dx = [[field_degree(z) for z in row] for row in x]
    dy = [[field_degree(z) for z in row] for row in y]
    dz, ds = independent_model(Degree(1, (0, 1)), Degree(1, (1, 0)), dx, dy)
    obligations = []
    bound = (0, 0)
    for name, expression in dz.items():
        degree = Degree(expression)
        if degree.n is None:
            degree_bound = (0, 0)
        else:
            degree_bound = degree.n
        require(max(degree_bound) <= 512, 'unchanged polynomial-degree guard for complete inverse equation')
        bound = max_degree(bound, degree_bound)
        obligations.append(dict(identity=name, h_degree=degree_bound[0], q_degree=degree_bound[1], type='full inverse equation'))
    for name, expression in ds.items():
        degree = Degree(expression); field = energy[name]
        degree_bound = max_degree(add_degree(degree.n, field.degree), add_degree(field.n.degree, degree.d))
        require(degree_bound is not None and max(degree_bound) <= 512, 'unchanged polynomial-degree guard for energy identity')
        bound = max_degree(bound, degree_bound)
        obligations.append(dict(identity=name, h_degree=degree_bound[0], q_degree=degree_bound[1], type='full energy identity'))
    require(len(obligations) == 18, 'all ten inverse and eight energy identities')
    nodes = 0
    for h in range(2, 3 + bound[0]):
        for q in range(4, 5 + bound[1]):
            xx = [[z.value(h, q) for z in row] for row in x]
            yy = [[z.value(h, q) for z in row] for row in y]
            zero, computed = independent_model(F(q), F(h), xx, yy)
            require(all(z == 0 for z in zero.values()), 'EVERY complete original compact inverse equation')
            for name in SCALARS:
                require(computed[name] == energy[name].value(h, q), 'EVERY complete rational energy identity')
            nodes += 1
    return dict(complete=True, domain=DOMAIN, exact_inverse_identities=10,
                exact_energy_identities=8, grid_bound=list(bound), grid_nodes=nodes,
                identity_node_equalities=18 * nodes,
                all_positive_denominator_polynomials=len(decoder.positive),
                all_positive_denominator_factor_occurrences=decoder.factor_occurrences,
                obligations=obligations,
                trust='Separate same-author exact integer/Fraction identities and complete degree bounds; original projections, full-space necessity and Woodbury remain ordinary unformalized proof. No independent review verdict.')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('certificate'); ap.add_argument('--output'); args = ap.parse_args()
    state = Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state / n).exists() for n in ('PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json')), 'operational barrier')
    def alarm(a, b):
        raise TimeoutError('unchanged60s separate inverse identity checker guard')
    signal.signal(signal.SIGALRM, alarm); signal.alarm(60); started = time.monotonic()
    raw = Path(args.certificate).read_bytes(); result = check(json.loads(raw)); signal.alarm(0)
    out = dict(agent='six-downset-1', role='researcher', status='PASS: separate all ten inverse and eight energy coefficient identities',
               certificate_sha256=sha256(raw).hexdigest(), result=result,
               seconds=time.monotonic()-started, peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, optimized=sys.flags.optimize)
    destination = Path(args.output) if args.output else Path(__file__).resolve().parent/'work'/f'checked-inverse-O{sys.flags.optimize}.json'
    destination.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'result'} | {k:v for k,v in result.items() if k != 'obligations'}), flush=True)


if __name__ == '__main__':
    main()
