"""Whole original entry, anchor, loop, mass and residual checks for new points.

This audit does not use the recipe's reported mass, counts, or endpoint flags.
It derives every NN change from the new original matrix and the fixed data.
"""
from fractions import Fraction as F
from math import lcm
from original import digest, lift, require
from face import slack_identity


def endpoint_form(T):
    require(len(T) == 253 and all(len(row) == 253 for row in T),
            'ALL253 new residual coordinates')
    require(all(type(x) is F for row in T for x in row), 'exact rational residual domain')
    den = lcm(1024, *(x.denominator for row in T for x in row))
    require(all((den*x).denominator == 1 for row in T for x in row),
            'all new residual integer units')
    K = [[(den*x).numerator-den//1024*int(i == j)
          for j, x in enumerate(row)] for i, row in enumerate(T)]
    require(all(K[i][j] == K[j][i] for i in range(253) for j in range(253)),
            'whole new symmetric endpoint form')
    return den, K


def audit_new(base, tau, T, L):
    require(type(tau) is F and 0 <= tau <= F(1, 128), 'exact q17 real-line endpoint parameter')
    require(len(L) == 255 and all(len(row) == 255 for row in L),
            'ALL255 original positions including empty and anchor')
    require(all(type(x) is F for row in L for x in row), 'exact original rational domain')
    members = base['members']; proper = members[1:]; sets = list(map(frozenset, members))
    allowed = 0; minimum = None
    for i in range(255):
        require(sum(L[i]) == 255, 'EVERY original regular row')
        for j in range(255):
            require(L[i][j] == L[j][i], 'EVERY original symmetric position')
            m = (L[i][j]-55*int(i == j))/200
            if sets[i].isdisjoint(sets[j]):
                allowed += 1
                minimum = m if minimum is None else min(minimum, m)
                require(m >= tau/200, 'EVERY allowed original entry pays its floor')
            else:
                require(m == 0, 'EVERY original intersecting position is supported correctly')
    require(allowed == 50263 and minimum == tau/200, 'whole support census and attained floor')
    # These bind THIS explicit witness. They are not conditions on all minimizers:
    # star trades are unpenalized by the NN objective.
    prescribed_star = [i for i, v in enumerate(members)
                       if v == (0, 1, 2) or (len(v) == 2 and v[0] == 0 and v[1] >= 11)]
    require(len(prescribed_star) == 10 and all(L[0][i] == tau for i in prescribed_star),
            'declared abc and nine aY star-empty entries bind this witness, not every optimizer')
    centered = [255*int(0 in v)-55 for v in members]
    require(all(sum(L[i][j]*centered[j] for j in range(255)) == 0 for i in range(255)),
            'EVERY original centered-star relation')
    den, K = endpoint_form(T)
    Ti = [[(den*x).numerator for x in row] for row in T]
    lifted = lift(Ti, [int(0 in v) for v in members[2:]])
    require(all(den*L[i][j] == den+lifted[i][j] for i in range(255) for j in range(255)),
            'ALL65025 new original residual lift positions including empty and anchor')
    B = [i for i, v in enumerate(proper) if 0 not in v]
    C0 = base['C_num']; d0 = base['denominator']
    ell = [F(d0-sum(C0[i][j] for j in B), d0) for i in B]
    ell0 = F(sum(C0[i][j] for i in B for j in B)-54*d0, d0)
    changes = {(a, b): L[i+1][j+1]-1-F(C0[i][j], d0)
               for a, i in enumerate(B) for b, j in enumerate(B)
               if a < b and sets[i+1].isdisjoint(sets[j+1])}
    require(len(B) == 199 and len(changes) == 15930, 'all individual NN rows and unordered edges')
    identity = slack_identity(ell, ell0, changes)
    require(identity['minimum'] == F(556505, 8192) and
            identity['P'] == F(556505, 8192)+23*tau and
            identity['row_slack'] == 45*tau and identity['loop'] == tau and
            identity['row_loop_feasible'] and
            all(identity[k] == 0 for k in ('bad_bad_increase_penalty',
                                         'bad_good_absolute_penalty',
                                         'good_good_decrease_penalty')),
            'actual individual NN mass attains the entire sharp row/loop identity')
    require(L[0][0]-55 == tau, 'actual original empty loop retained with correct factor two')
    return {'tau': str(tau), 'allowed_positions': allowed, 'minimum_allowed_M': str(minimum),
            'all_original_lift_positions': 65025, 'proper_NN_rows': 199,
            'unordered_NN_edges': 15930, 'actual_positive_NN_mass': str(identity['P']),
            'actual_bad_row_slack': str(identity['row_slack']), 'actual_loop_slack': str(identity['loop']),
            'new_denominator': den, 'whole_shifted_K_sha256': digest(K),
            'whole_new_L_sha256': digest([[str(x) for x in row] for row in L]),
            'whole_new_T_sha256': digest([[str(x) for x in row] for row in T]),
            'whole_new_original_positions_checked': True}
