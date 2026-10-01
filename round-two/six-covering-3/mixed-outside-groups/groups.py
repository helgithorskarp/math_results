"""Exact outside-pair budgets: union u, sum individual v footprints.

Author six-covering-3, researcher. Integer weights; no solver or threads.
The mathematical scope and fractional incidence condition are in proof.md.
"""

from math import gcd


def require(condition, message):
    if not condition:
        raise ValueError(message)


def histogram(weights, n):
    result = [0] * n
    for x, weight in enumerate(weights):
        result[x % n] += weight
    return result


class PairBudgets:
    def __init__(self, u, v, B=None):
        require(len(u) == len(v) and len(u) > 0, "wrong physical vector dimensions")
        require(all(type(w) is int and w >= 0 for w in (*u, *v)), "invalid weight")
        self.N = len(u)
        if B is not None:
            require(type(B) is int and B >= 6 and self.N % B == 0 and B % 6 == 0,
                    "invalid B part")
            rest = B
            for p in (2, 3):
                while rest % p == 0:
                    rest //= p
            require(rest == 1 and gcd(B, self.N // B) == 1, "invalid CRT B part")
        self.B = B
        self.u = tuple(u)
        self.w = tuple(a + b for a, b in zip(u, v))
        self._u_hist = {}
        self._w_hist = {}

    def hist(self, n, ordinary=False):
        require(type(n) is int and n > 0 and self.N % n == 0, "modulus must divide period")
        cache = self._u_hist if ordinary else self._w_hist
        if n not in cache:
            cache[n] = histogram(self.u if ordinary else self.w, n)
        return cache[n]

    def singleton(self, n):
        if self.B is not None:
            require(gcd(n, self.B) < self.B, "top resource is not an outside modulus")
        hist = self.hist(n)
        value = max(hist)
        return {"value": value, "phase": hist.index(value)}

    def pair(self, m, n):
        require(m != n, "pair resources must be distinct")
        hm, hn = self.hist(m), self.hist(n)
        B_part_lcm = None
        union_v = False
        if self.B is not None:
            bm, bn = gcd(self.B, m), gcd(self.B, n)
            require(bm < self.B and bn < self.B, "top resource is not an outside modulus")
            B_part_lcm = bm // gcd(bm, bn) * bn
            union_v = B_part_lcm < self.B
        g = gcd(m, n)
        L = m // g * n
        overlap = self.hist(L, ordinary=not union_v)
        best, phases = None, None

        def consider(value, a, b):
            nonlocal best, phases
            if best is None or value > best or (value == best and (a, b) < phases):
                best, phases = value, (a, b)

        # All compatible phase pairs, once each, by their common CRT class.
        for c, mass in enumerate(overlap):
            a, b = c % m, c % n
            consider(hm[a] + hn[b] - mass, a, b)

        # Incompatible pairs have zero intersection. For a fixed m coset,
        # its best n coset is among the two best distinct gcd cosets.
        if g > 1:
            am = [max(range(h, m, g), key=lambda a: (hm[a], -a)) for h in range(g)]
            bn = [max(range(h, n, g), key=lambda b: (hn[b], -b)) for h in range(g)]
            top = sorted(range(g), key=lambda h: (-hn[bn[h]], bn[h]))[:2]
            for h, a in enumerate(am):
                k = top[0] if top[0] != h else top[1]
                b = bn[k]
                consider(hm[a] + hn[b], a, b)
        return {"value": best, "phases": list(phases),
                "v_mode": "union" if union_v else "individual_sum",
                "B_part_lcm": B_part_lcm,
                "compatible_pairs": L, "incompatible_cosets": g if g > 1 else 0}


def fractional_pairs(budgets, outside, edges, scale=2):
    """Edge (m,n,c) has coefficient c/scale; singleton remainder restores 1.

    No optimum for the group selection is claimed. Every accepted literal
    choice has exact resource incidence one, including singleton remainders.
    Return the numerator of the outside budget with denominator scale.
    """
    require(type(scale) is int and scale >= 1, "invalid scale")
    outside = tuple(outside)
    require(len(set(outside)) == len(outside), "repeated outside resource")
    singles = {n: budgets.singleton(n) for n in outside}
    degrees = {n: 0 for n in outside}
    pairs, seen = [], set()
    for edge in edges:
        require(len(edge) == 3, "edge must give two resources and a numerator")
        m, n, c = edge
        require(type(m) is int and type(n) is int and m != n and m in degrees and n in degrees,
                "edge resource must be a free outside modulus")
        require(type(c) is int and 1 <= c <= scale, "invalid edge coefficient")
        key = tuple(sorted((m, n)))
        require(key not in seen, "repeated pair")
        seen.add(key)
        degrees[m] += c
        degrees[n] += c
        require(degrees[m] <= scale and degrees[n] <= scale, "resource incidence exceeds one")
        result = budgets.pair(m, n)
        pairs.append({"resources": [m, n], "numerator": c, **result})
    remainder = {n: scale - degrees[n] for n in outside}
    numerator = (sum(remainder[n] * singles[n]["value"] for n in outside)
                 + sum(p["numerator"] * p["value"] for p in pairs))
    singleton_numerator = scale * sum(singles[n]["value"] for n in outside)
    return {"scale": scale, "outside_numerator": numerator,
            "singleton_numerator": singleton_numerator,
            "saving_numerator": singleton_numerator - numerator,
            "singleton_remainders": {str(n): remainder[n] for n in outside},
            "pairs": pairs}
