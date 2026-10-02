"""Literal critical products, simple original roots and individual normals."""
from prior import F, I, need, G, Jet, convolution, evaluate, derivative, cx
from normal import partials
from eta_derivative import Dual


def det(matrix):
    # Independent permutation determinant, including singular damage controls.
    from itertools import permutations
    n = len(matrix)
    out = F(0)
    for perm in permutations(range(n)):
        sign = (-1)**sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = F(sign)
        for i, j in enumerate(perm):
            term *= matrix[i][j]
        out += term
    return out


def run():
    checks, damages, records = 0, [], []
    def check(ok, label):
        nonlocal checks
        need(ok, label)
        checks += 1
    def reject(name, predicate):
        try:
            need(predicate, 'damaged mathematics ' + name)
        except ValueError:
            damages.append(name)
            return
        raise ValueError('damaged mathematics accepted ' + name)
    for b in (F(1, 8), F(1, 16), F(1, 32)):
        eta, q0, a = b*b, F(3), 1 - b*b
        x, y = F(-2, 3), (a - 4*b) / eta
        v = [x, y, q0*q0, 0, 0, F(0)]
        p, qs = partials(eta, v)
        velocities = [
            [G(eta), G(eta)],
            [G(0, b/(2*q0)), G(0, -b/(2*q0))],
            [G(-eta*eta*y/(2*q0), b*eta/2), G(eta*eta*y/(2*q0), b*eta/2)],
            [G(eta/(2*q0)), G(-eta/(2*q0))],
        ]
        heavy0 = [G(eta*y, b*q0), G(eta*y, -b*q0)]
        normalized = [eta, eta, G(0, eta*b), G(0, eta*b)]
        polynomial_records, gradient_records = [], []
        for axis, speed in enumerate(velocities):
            roots = [Jet(G(eta*x)) for _ in range(6)]
            roots += [Jet([root, velocity, 0]) for root, velocity in zip(heavy0, speed)]
            raw = [Jet(1)]
            for root in roots:
                raw = convolution(raw, [-root, Jet(1)])
            primitive = [Jet(0)] + [9*z/F(j+1) for j, z in enumerate(raw)]
            primitive[0] -= evaluate(primitive, a)
            actual = [z.v[1] for z in primitive]
            expected = [normalized[axis]*G(z) for z in qs[axis]]
            expected += [G(0)]*(10-len(expected))
            check(len(actual) == 10 and actual == expected, 'all ten anchored individual-heavy partial coefficients')
            check(evaluate(actual, a) == 0, 'marked root remains fixed under each literal partial')
            polynomial_records.append([z.record() for z in actual])
            distance2 = [(a-root).re**2+(a-root).im**2 for root in heavy0]
            check(distance2 == [(5*b)**2]*2, 'literal heavy distances use actual individual roots')
            Qdot = [-2*((a-root).conjugate()*velocity).re for root, velocity in zip(heavy0,speed)]
            Fdot = sum(-d/(2*(5*b)**3) for d in Qdot)
            expected_gradient = [2*eta*(4*b)/(5*b)**3, -eta/(5*b)**3, 0, 0][axis]
            check(Fdot == expected_gradient, 'both original heavy objective gradients and odd cancellation')
            gradient_records.append(str(Fdot))
            damaged = list(actual)
            damaged[0] += G(1)
            reject('anchored-constant', damaged == expected)
            reject('root-coordinate-scale', [2*z for z in actual] == expected)
        combo = [G(qs[0][j])/2 + (a-eta*y)*G(qs[1][j]) if j < len(qs[1]) else G(qs[0][j])/2 for j in range(len(qs[0]))]
        direct = cx.primitive(cx.scale(convolution(cx.power([-eta*x,1],6),[a,-1]),9),a)
        check(combo == [G(z) for z in direct], 'whole cancelled multiplier primitive')
        reject('missing-half-in-cancelled-primitive', [2*z for z in combo] == [G(z) for z in direct])

        # A separate polynomial has four known simple unit ORIGINAL roots.
        uppers = [G(F(-3,5),F(4,5)),G(F(-5,13),F(12,13))]
        original_roots = [G(a), *uppers, *(z.conjugate() for z in uppers), *map(G,[F(-3,4),F(-1,4),F(1,4),F(3,4)])]
        original = [G(1)]
        for root in original_roots:
            original = convolution(original,[-root,G(1)])
        pd = derivative(original)
        raw_normals, upper_quotients, root_velocities = [], [], []
        for root in [*uppers, *(z.conjugate() for z in uppers)]:
            check(evaluate(original,root)==0 and evaluate(pd,root)!=0, 'actual simple original-root fixture')
            row, speeds, quotients = [], [], []
            for axis in range(4):
                pb = normalized[axis]*evaluate(qs[axis],root)
                speed = -pb/evaluate(pd,root)
                check(evaluate(pd,root)*speed+pb==0, 'entire differentiated actual root equation')
                ratio = pb/(root*evaluate(pd,root))
                norm_derivative = (root.conjugate()*speed).re
                check(norm_derivative == -ratio.re, 'actual half squared-modulus derivative')
                row.append(norm_derivative);speeds.append(speed);quotients.append(ratio)
            raw_normals.append(row);root_velocities.append(speeds)
            if len(upper_quotients)<2:upper_quotients.append(quotients)
        for k in range(2):
            for axis in range(4):
                check(raw_normals[k+2][axis] == (1 if axis<2 else -1)*raw_normals[k][axis], 'both lower-root parity signs')
                check(root_velocities[k+2][axis] == (1 if axis<2 else -1)*root_velocities[k][axis].conjugate(), 'both actual conjugate root velocities')
        even = [[raw_normals[k][j]/eta for j in range(2)] for k in range(2)]
        odd = [[raw_normals[k][j]/(eta*b*uppers[k].im) for j in [2,3]] for k in range(2)]
        determinant = det(raw_normals)
        expected_det = 4*eta**5*uppers[0].im*uppers[1].im*det(even)*det(odd)
        check(determinant == expected_det and determinant!=0, 'whole 4x4 normal determinant and factor four')
        reject('lost-half-sum-pair-factor', determinant == expected_det/4)
        altered = [row[:] for row in raw_normals]
        for k in [2,3]:
            for j in [2,3]:altered[k][j] = raw_normals[k-2][j]
        reject('conjugated-entire-odd-partial', det(altered)==determinant)
        e = even
        rhs = [F(-3,5),F(7,11)]
        mu = [(rhs[0]*e[1][1]-e[1][0]*rhs[1])/det(e), (e[0][0]*rhs[1]-rhs[0]*e[0][1])/det(e)]
        full_gradient = [-2*eta*sum(mu[k]*even[k][j] for k in range(2)) for j in range(2)] + [F(0),F(0)]
        individual_gradient = [sum(-mu[k%2]*raw_normals[k][j] for k in range(4)) for j in range(4)]
        check(full_gradient==individual_gradient and full_gradient[:2]==[-2*eta*x for x in rhs], 'all four individually counted dual equations and factor two')
        reject('paired-dual-used-as-individual', [2*x for x in individual_gradient]==full_gradient)
        reject('double-half-squared-metric', [[2*x for x in row] for row in raw_normals]==raw_normals)
        records.append({'sqrt_eta':str(b),'all_four_anchored_partial_coefficients':polynomial_records,'objective_gradients':gradient_records,'simple_original_roots':[z.record() for z in original_roots],'all_original_normal_rows':[[str(x) for x in row] for row in raw_normals],'raw_determinant':str(determinant),'individual_duals':list(map(str,mu))})
    derivative_controls = []
    for t in [F(1,7),F(3,11),F(4,9)]:
        # A separate literal two-coefficient convolution validates full quotient AD.
        a, b = Dual(I(t),I(F(2,3))), Dual(I(2+t),I(F(-3,5)))
        ratio = a/b
        exact = (F(2,3)*(2+t)-t*F(-3,5))/(2+t)**2
        check(ratio.dot==I(exact), 'entire rational quotient eta derivative')
        reject('dropped-quotient-denominator-motion', F(2,3)/(2+t)==exact)
        reject('reversed-quotient-denominator-motion', (F(2,3)*(2+t)+t*F(-3,5))/(2+t)**2==exact)
        for n in range(1,10):
            value = (a**n/b)
            expected = (n*t**(n-1)*F(2,3)*(2+t)-t**n*F(-3,5))/(2+t)**2
            check(value.dot==I(expected), 'all degrees in normalized root-map derivatives')
        derivative_controls.append([str(t),str(exact)])
    invalid = 0
    for operation in [lambda:Dual(I(-1,1)).inv(),lambda:Dual(I(0)).inv(),lambda:I(1,0),lambda:Dual(1)**-1]:
        try:operation()
        except ValueError:invalid+=1
        else:raise ValueError('invalid exact domain accepted')
    return {'checks':checks,'mathematical_damage_rejections':damages,'distinct_mathematical_damage_types':len(set(damages)),
            'invalid_domains_rejected':invalid,'three_literal_original_root_records':records,'rational_eta_derivative_controls':derivative_controls,
            'trust_boundary':'known simple-root fixtures check the universal metric/determinant/dual signs; separate critical-factor fixtures check the exact partials; neither supplies full branch or interval coverage'}
