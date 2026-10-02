"""bounded remaining-order exploration; no negative inference from failure."""
from fractions import Fraction as F
from pathlib import Path
import json
import time
import orbits
from exact import digest, schur_psd
from literal import require
from variance import bound, scalar_record


def necessary(q, k):
    # Credited9434 strengthened original R-annihilating upper dual.
    N = (q*q+13*q+16)//2-k
    s = 3*q+4
    h = F(1, 3*q+5)
    alpha = F(q*(q+1), 2)+3*(q+1)*h
    e = F(q*q+(13-6*k)*q+2*k*k-10*k+14, 2)
    gap = N-s
    rr = 3+F(2, q)
    d = N-2*s+rr
    ww = (s-rr)/(q-1)
    az, aw = (k-1)*(ww-1), 1+k*(ww-1)
    a0 = F((2*k+1)*q+k)-F(2*k, q)
    Q0 = e-(k*az*az+(q-k)*aw*aw)/gap-4*q*(k-1)**2/d
    Delta = alpha-2*k*h-2*h*(a0/gap+F(4*q*(1-k), d))
    require(Delta > 0, 'credited universal dual derivative orientation')
    return Q0, Delta


def run():
    records = []
    for k in range(5, 25):
        q = bound(k)-5
        data = orbits.forms(q, k)
        Q0, derivative = necessary(q, k)
        scalar = scalar_record(q, k)
        record = {'q': q, 'k': k, 'N': data['N'], 'Q0': str(Q0),
                  'credited_dual_Delta': str(derivative), 'm': scalar['strict_scalar_margin'],
                  'forms_digest': digest(orbits.encoded(data))}
        try:
            zero_rank = schur_psd(data['U0'])
            record['U0_exact_PSD_rank'] = zero_rank
        except ValueError as exc:
            record['U0_exact_PSD_check_failure'] = str(exc)
            record['failed_check_is_not_ansatz_nonexistence'] = True
        if Q0 < 0:
            record['status'] = 'credited9434 all-real ansatz exclusion'
        elif record.get('U0_exact_PSD_rank') == 23:
            delta = None
            for exponent in range(21):
                candidate = F(1, 2**exponent)
                try:
                    if orbits.floor(data, F(0), F(0), candidate) == 23:
                        delta = candidate
                        break
                except ValueError:
                    pass
            require(delta is not None, 'bounded exact floor search needs saved follow-up if exhausted')
            mu = min(delta, F(data['N']-2*data['s']))
            kap = min(F(1, 8), mu/(4*(16*data['s']+1)))
            trade = kap/24
            G, H = orbits.evaluate(data, kap, trade)
            star = [F(bool(c & 1)) for c, z, w in data['keys']]
            require(sum(d*x for d, x in zip(data['sizes'], star)) == data['s']
                    and all(sum(G[i][j]*star[j] for j in range(23)) == 0 for i in range(23)),
                    'entire fixed greatest-star kernel')
            require(schur_psd(G) == 22 and orbits.floor(data, kap, trade, 3*mu/4) == 23,
                    'exact repaired fixed-space lower rank and quantitative cap')
            record.update({'status': 'exact positive full-cap construction via credited9546 complement/repair/lift',
                           'zero_fixed_cap_floor': str(delta), 'whole_zero_cap_floor': str(mu),
                           'kappa': str(kap), 't': str(trade), 'whole_repaired_cap_floor': str(3*mu/4),
                           'repaired_fixed_lower_rank': 22, 'repaired_fixed_cap_rank': 23,
                           'new_beyond_9546_m_criterion': F(scalar['strict_scalar_margin']) <= 0})
        else:
            record['status'] = 'UNRESOLVED all-parameter ansatz, failed U0/m has no negative meaning'
        records.append(record)
    return {'agent': 'six-downset-3', 'role': 'researcher', 'status': 'exact finite sample; no infinite classification',
            'quantifiers': 'integers5<=k<=24,q=b(k)-5 only; arbitrary Z transported by symmetry',
            'records': records, 'negative_mechanism': '9434 original all-real R-annihilating dual ONLY',
            'positive_bridge': '9546 full complement/generic lower repair/actual empty lift; unformalized and no independent review'}


if __name__ == '__main__':
    start = time.perf_counter()
    result = run()
    result['record_sha256'] = digest(result)
    Path(__file__).with_name('SAMPLE.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'seconds': time.perf_counter()-start, 'digest': result['record_sha256'],
                      'cases': [{k: r[k] for k in ('k', 'q', 'status', 'm', 'Q0')}
                                for r in result['records']]}))
