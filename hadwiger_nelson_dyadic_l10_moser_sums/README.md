# Exact L10–Moser contact class: 448 points, four colours, unchanged atom interfaces

Every one of the **28 phases** defined below gives a genuine **448-point**
plane unit-distance graph with chromatic number **four**. Sixteen graphs have
2,216 strict unit edges; twelve have 2,202. Moreover, every proper four-colour
pattern of each of the three marked source atoms extends to every graph,
considering the atoms individually.

Thus the tested assembly neither meets the sub-509 objective nor strengthens
these particular source interfaces. This is a finite construction result. It
does not exclude other phases, independent rotations of the first two atoms,
joint prescriptions on several atoms, or other plane supports.

The construction combines a ten-vertex VND atom with two Moser spindles.
It differs from the earlier
[mixed Moser–L10 palette](../hadwiger_nelson_mixed_moser_l10_sums/README.md):
the new phases adjoin `sqrt(5)` and create actual additional contacts.
No theorem about that earlier finite support is used here. The unrestricted
published comparison remains Parts's 509-vertex graph, also identified in
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4).
This package makes no record or priority claim.

## Exact construction

Identify the plane with the complex numbers. Put

```text
omega = (1+i sqrt(3))/2,   eta = (5+i sqrt(11))/6,
M = {0, 1, omega, 1+omega, eta, eta*omega, eta*(1+omega)}.
```

The ten-point atom `L` consists, in order, of

```text
0, 1, i sqrt(2), 1+i sqrt(2), f, 1+f,
1/2+s sqrt(6)/6 + i(sqrt(2)/2+t sqrt(3)/6),
```

where `f=(-1+i)sqrt(2)/2` and the last four points use
`(s,t)=(-1,-1),(-1,1),(1,-1),(1,1)`. This is the rectangular two-diamond
realization of the `L10,2` atom illustrated in
[Voronov, Neopryatnaya and Dergachev, Figures 2 and 8](https://arxiv.org/html/2106.11824v4).
The displayed coordinates, all 17 unit edges, and its colour demand are
verified here without importing a graph file or a solver assertion.

Let `P=L+M`. It has **64 distinct points and 212 unit edges**. Choose nonzero
differences `a in P-P`, `b in M-M` for which

```text
A=|a|^2 and B=|b|^2 are rational,
S=A+B-1,
Delta=4*A*B-S^2 is positive,
Delta/5 is a nonzero rational square r^2.
```

The phase class consists of all distinct values

```text
v = (-S +/- i*r*sqrt(5))/(2*conjugate(a)*b).
```

This definition concerns a specified rational-norm contact class; it is not
the full contact census. There are 94 eligible rational-norm differences of
`P`, 22 of `M`, and exactly 28 distinct resulting phases. Each has two ordered
difference-pair representations. Both signs are retained. Define

```text
X_v = P + v*M = L + M + v*M.
```

Each `v` is a unit complex number outside
`K0=Q(i,sqrt(2),sqrt(3),sqrt(11))`. The sum map `P x M -> X_v` is injective:
a collision with different Moser coordinates would express `v` as a quotient
of two nonzero `K0` elements. Hence the physical order is exactly `64*7=448`.
The ambient coordinates lie in `K0(sqrt(5))`.

The Cartesian edges number `212*7+64*11=2188`. The exact geometry finds
**14 or 28 further unit edges**, including any contacts beyond those used to
select the phase. These are coupled physical graphs, not abstract Cartesian
products assumed to be realizations. [PROOF.md](PROOF.md) gives the reduction.

## Complete selected interfaces

Use the marked copies `L+0+0`, `0+M+0`, and `0+0+vM`. Up to a global
permutation of four colour names, their proper colour-pattern counts are
respectively **178, 16, 16**. For every phase and every such pattern, the
certificate supplies a full proper four-colouring with that restriction.
This verifies **5,880 pattern/phase pairs**.

The statement is individual surjectivity of each restriction map. It does
not say that arbitrary prescriptions on several marked atoms extend
simultaneously. The auxiliary union of address-edge lists used by the
producer is only a certificate-sharing device, not another claimed physical
plane graph.

The compact [certificate](certificate.json) has **717 colour words**, packed
at two bits per point, and is **117,901 bytes**. The checker evaluates
12,994,800 claimed edge inequalities. A seven-point Moser copy supplies the
lower bound four, so positive words prove exact chromatic number four.

## Reproduction and trust boundary

From a full checkout, Python 3.11+ and its standard library suffice:

```sh
python3 -B hadwiger_nelson_dyadic_l10_moser_sums/verify.py --check-expected
python3 -O -B hadwiger_nelson_dyadic_l10_moser_sums/verify.py --check-expected
python3 -B hadwiger_nelson_dyadic_l10_moser_sums/controls.py
cd hadwiger_nelson_dyadic_l10_moser_sums
sha256sum -c SHA256SUMS
```

The checker reconstructs all physical points twice, compares them entrywise,
and checks **2,803,584 unordered pairs** using two exact coefficient
calculations. The producer uses bit-indexed multiquadratic arithmetic; the
reference uses square-free radicands and their gcd multiplication law.
A necessary rational-coefficient equality accelerates both complete scans;
all surviving nonconstant coefficients are still checked. There is no
floating-point predicate in the proof replay. The two complete edge lists
must agree entrywise for each phase.

The checker enumerates source patterns independently by pinning a real unit
triangle and trying all colours on the remaining vertices. It decodes each
word, checks every edge claimed by its phase mask, normalizes its source
restrictions, and verifies complete coverage. It needs no SAT verdict or
refutation file. Controls reject malformed words and masks, a nonunit vector
passing the rational-coefficient filter, and faulty selection of a pinned
colour from a multi-valued Boolean model.

Optional positive-certificate regeneration uses `python-sat==1.8.dev17`
and bundled CaDiCaL 1.5.3, in an external environment:

```sh
python3 -m venv /tmp/hn-l10-moser-env
/tmp/hn-l10-moser-env/bin/pip install -r \
  hadwiger_nelson_dyadic_l10_moser_sums/requirements.txt
/tmp/hn-l10-moser-env/bin/python -B \
  hadwiger_nelson_dyadic_l10_moser_sums/produce.py \
  --output /tmp/hn-l10-moser-certificate.json
python3 -B hadwiger_nelson_dyadic_l10_moser_sums/verify.py \
  --certificate /tmp/hn-l10-moser-certificate.json
```

The formula has four Boolean variables per vertex, a nonempty-colour clause
at each vertex, and equal-colour exclusions on every edge. Positive source
pins select the required colour during decoding. At-most-one clauses are
unnecessary: adjacent nonempty true-colour sets are disjoint. An unsuccessful
auxiliary-supergraph query only triggers individual positive queries; its
UNSAT/UNKNOWN status is not a proof premise. Each query has a 200,000-conflict
cap and failure to complete the positive cover aborts production.

The recorded producer made 773 queries in about 24 seconds. Full exact replay
took about 39 seconds. See [VALIDATION.json](VALIDATION.json) for the measured
runs and source identities. Solver versions can change the chosen positive
words; regenerated output must pass the checker, and need not match a
historical word stream to prove the same statement.

Trust remains in elementary independence of the multiquadratic basis,
the written finite reduction, complete loops, and Python exact arithmetic.
These are author-run checks, not independent-author review or formal proof.
Large exploratory outputs, paper downloads, and solver environments are not
published. Discovery Net's local committed index was stale at height 4,363;
repository evidence was refreshed through commit
`44e2a03` before publication. Broadcast status is recorded separately.

The tested class is retired for construction work. Its actual coupling edges
do not strengthen any of the three selected atom interfaces individually.
It gives no reason to enlarge this sum or widen its phase window without a
new construction mechanism or a useful joint constraint.
