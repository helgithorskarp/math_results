"""Full higher tangent and normal responses, with no symmetric restriction.

The analytic moving-parameter comparison is proved in PROOF.md. This module
checks the exact differentials and the full real-polynomial coefficients
on the complete thirteen-dimensional second tangent space and the complete
sixteen-dimensional third correction space.
"""
from math import comb


def build(context):
    P, J, K = (context[name] for name in ['P', 'J', 'K'])
    H, b2, rho, uz, up = (context[name] for name in ['H', 'b2', 'rho', 'uz', 'up'])
    eta, roots, w3, w4 = (context[name] for name in ['eta', 'roots', 'w3', 'w4'])
    c, v = context['c'], context['v']
    sigma = K(3)/8 - (K(3)*w3/2 + (1-v)*w4)/20
    k = rho*up + sigma*H
    checks = 0

    def equal(a, b, label):
        nonlocal checks
        if a != b:
            raise RuntimeError(label)
        checks += 1

    hs = [1, -1, 0, 0, 0, 0, 0, 0]
    us = [up, up, *([uz]*6)]
    gradient_u = [K(us[j]) + rho*b2*hs[j]**2 for j in range(8)]
    gradient_hbar = [2*rho*b2*hs[j]*us[j] + 4*sigma*b2**2*hs[j]**3
                     for j in range(8)]
    equal(gradient_u, [uz]*8, 'full eight-dimensional real gradient')
    equal(gradient_hbar, [2*b2*k*a for a in hs],
          'full eight-dimensional imaginary gradient')
    equal(w3*context['A'][0]/8 + w4*context['A'][1]/8, 1,
          'positive dual real normalization')
    equal(w3*context['B'][0]/7 + w4*context['B'][1]/7, 1,
          'positive dual imaginary normalization')

    def polynomial_and_objective(h, u):
        powers = [J()]
        for n in range(1, 9):
            pn = J()
            for j in range(n//2+1):
                order = n-j
                if order <= 4:
                    pn += eta**order * sum(
                        (u[a]**(n-2*j)*h[a]**(2*j) for a in range(8)), J()
                    ) * (K((-1)**j*comb(n, 2*j))*b2**j)
            powers.append(pn)
        es = [J(1)]
        for n in range(1, 9):
            es.append(sum((es[n-j]*powers[j]*((-1)**(j-1))
                           for j in range(1, n+1)), J())/n)
        prim = {9-j: es[j]*K(9*(-1)**j)/(9-j) for j in range(9)}
        anchor = sum((a*(J(1)-eta)**z for z, a in prim.items()), J())
        pol = {**prim, 0: -anchor}
        jets = [{z: a.a[j] for z, a in pol.items() if a.a[j]} for j in range(5)]
        objective = J()
        from fractions import Fraction as F
        for j in range(8):
            delta = (J(1)-eta*(J(1)+u[j]))**2 + eta*h[j]**2*b2 - J(1)
            objective += sum((delta**n*a for n, a in enumerate(
                [F(1), F(-1, 2), F(3, 8), F(-5, 16), F(35, 128)])), J())
        return jets, objective

    base_jets, base_f = polynomial_and_objective([J(a) for a in hs],
                                                [J(a) for a in us])

    def linear_radial(jet, omega):
        # delta p0,...,delta p3=0. Thus delta r4=-omega delta p4/9;
        # the radial response is exactly -Re(delta p4(omega))/9.
        return sum((a*(omega**z).real_field() for z, a in jet.items()), P())/(-9)

    def subtract_jet(a, b):
        return {z: q for z in set(a) | set(b)
                if (q := a.get(z, P())-b.get(z, P()))}

    small = [P.var(j) for j in range(6)]
    pair = -sum(small, P())/2
    tau = [pair, pair, *small]
    real = [P.var(j) for j in range(6, 13)]
    real.append(-sum(real, P()))
    equal(sum(tau, P()), 0, 'complete second imaginary zero-mean space')
    equal(sum((a*b for a, b in zip(hs, tau)), P()), 0,
          'complete second imaginary norm-tangent space')
    equal(sum(real, P()), 0, 'complete second real zero-mean space')
    diff = sum((b*a for a, b in zip(gradient_hbar, tau)), P())
    diff += sum((b*a for a, b in zip(gradient_u, real)), P())
    equal(diff, 0, 'all thirteen second-tangent differentials vanish')
    tangent_jets, tangent_f = polynomial_and_objective(
        [J([a, 0, b]) for a, b in zip(hs, tau)],
        [J([a, 0, b]) for a, b in zip(us, real)])
    for order in range(4):
        equal(tangent_jets[order], base_jets[order],
              'complete tangent polynomial below fourth '+str(order))
        equal(tangent_f.a[order], base_f.a[order],
              'complete tangent objective below fourth '+str(order))
    tangent_p4 = subtract_jet(tangent_jets[4], base_jets[4])
    tangent_response = tangent_f.a[4]-base_f.a[4]
    tangent_response += linear_radial(tangent_p4, roots[0])*w3
    tangent_response += linear_radial(tangent_p4, roots[1])*w4
    equal(tangent_response, diff, 'entire second-tangent fourth dual trace')

    psi = [P.var(j) for j in range(8)]
    real3 = [P.var(j) for j in range(8, 16)]
    normal_jets, normal_f = polynomial_and_objective(
        [J([a, 0, 0, b]) for a, b in zip(hs, psi)],
        [J([a, 0, 0, b]) for a, b in zip(us, real3)])
    for order in range(4):
        equal(normal_jets[order], base_jets[order],
              'complete third-correction polynomial below fourth '+str(order))
        equal(normal_f.a[order], base_f.a[order],
              'complete third-correction objective below fourth '+str(order))
    R = sum(real3, P())
    Z = sum((a*b for a, b in zip(hs, psi)), P())*b2
    expected_p4 = {8: R*(-K(9)/8), 7: Z*(K(9)/7),
                   0: R*(K(9)/8)-Z*(K(9)/7)}
    normal_p4 = subtract_jet(normal_jets[4], base_jets[4])
    equal(normal_p4, expected_p4, 'full sixteen-dimensional fourth normal polynomial')
    equal(normal_f.a[4]-base_f.a[4], R-Z,
          'full sixteen-dimensional fourth normal objective')
    normal_response = normal_f.a[4]-base_f.a[4]
    normal_response += linear_radial(normal_p4, roots[0])*w3
    normal_response += linear_radial(normal_p4, roots[1])*w4
    equal(normal_response, 0, 'entire sixteen-dimensional fourth normal dual trace')
    return {'checks': checks, 'second_tangent_dimension': 13,
            'third_correction_dimension': 16, 'gradient_u': [a.record() for a in gradient_u],
            'gradient_hbar': [a.record() for a in gradient_hbar],
            'second_tangent_polynomial_hash': context['sha256'](
                str(sorted((z, a.digest()) for z, a in tangent_p4.items())).encode()
            ).hexdigest(),
            'full_tangent_dual_record': tangent_response.record(),
            'full_normal_dual_record': normal_response.record()}, {
                'tangent_response': tangent_response, 'normal_response': normal_response,
                'gradient_u': gradient_u, 'gradient_h': gradient_hbar,
                'tau': tau, 'real': real, 'P': P}
