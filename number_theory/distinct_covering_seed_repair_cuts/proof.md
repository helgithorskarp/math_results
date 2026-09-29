# A resource obstruction to changing one class of the minimum-seven seed

Author: **six-covering-1**, role **researcher**, 2026-09-29. The campaign uses
a shared signing identity; the author name records actual authorship.

## Exact statement

Let S be the 66 congruences in `seed_m7.json`, transcribed from Section 7 of
[Zhang–Zhang](https://arxiv.org/html/2607.19029). Let F be S with its class
6 modulo 7 deleted. Thus F has 65 distinct moduli, minimum exactly 8, and
LCM B=10080.

**Lemma.** A finite covering C of all integers by congruences with pairwise
distinct moduli and minimum **exactly 8**, containing at least 64 of the
65 specified congruences in F, has LCM at least **50400**.

Containment refers to the residue as well as the modulus. The possible
changed class may be reassigned or omitted. Arbitrarily many new classes
may be added. This is a restriction on proximity to one specified seed,
not an unrestricted lower bound on L_min(8). It shows that a construction
of period at most 40320 must change at least two designated seed classes.

The [previous construction](../distinct_covering_min8_prime_lift) at period
70560 retains all 65 classes. Therefore this larger repair family has least
LCM in [50400,70560]. The endpoints are not claimed equal.

## Complete reduction of this family

The verifier checks directly that S covers every residue modulo B, and
that the moduli of F are precisely all divisors d of B with d>=8. It also
checks, for **each** m in F, that the other 64 moduli still have LCM B.

Suppose a covering C as in the lemma had LCM L<50400. Choose a modulus m
such that all 64 classes of F other than its m-class occur in C. If C
contains all 65, any m can be chosen. The fixed classes force B|L, so

    L = tB,  t in {1,2,3,4}.

Every modulus of C divides its actual LCM L. If modulus m does not occur
in C, adjoin any class a modulo m; this preserves distinctness, covering,
actual LCM, and minimum exactly eight, because m|B|L. Otherwise let a be
the residue of its unique modulus-m class. Thus any surviving case may
be assumed to include one normalized phase a in {0,...,m-1} for this modulus.
No normalization of other phases is used.

First apply the individual-hole capacity bound before fixing a. Let H be
the uncovered residues modulo B of the fixed 64 classes. At L=tB these
lift to H_L={x+kB: x in H, 0<=k<t}. For an available new modulus d|L,

    C_L(d) = max_a |{x in H_L: x=a mod d}|.

A necessary condition for covering is sum_d C_L(d)>=|H_L|, since each
available modulus can be used at most once. For the generator, putting
g=gcd(B,d) and w(g)=max_a |{x in H: x=a mod g}| gives the exact formula

    C_L(d) = (t g/d) w(g).

This follows by counting solutions to the two congruences modulo B and d.
The verifier does **not** assume that formula: it forms H_L explicitly and
counts every residue class directly. The available d include the freed m.
Strictly deficient sums exclude their entire phase spaces.

All 260 rows (65 freed moduli times four possible multipliers) are checked.
The only survivors are:

| t | Proposed LCM | Freed moduli surviving the capacity bound |
|---:|---:|:---|
| 1 | 10080 | none |
| 2 | 20160 | none |
| 3 | 30240 | 8,9,10,12,15,18,24,30,36,45,72,90 |
| 4 | 40320 | 8,16 |

This is a complete reduction for the stated repair family. It makes no
claim about a bounded search outside that family.

## A resource inequality for identical residual children

This strengthens the finite-horizon residual-fiber count in
[six-covering-3's reduction](../distinct_covering_prime_tower/proof.md) by
charging children that cannot be completed with a single new congruence.
The following argument is included in full.

Let p be prime, gcd(p,M)=1, and let fixed classes have period p^s M.
Consider a proposed period p^(s+h) M. Suppose every remaining available
modulus is p^(s+j)d, where 1<=j<=h and d belongs to a finite set D of
divisors of M. Each such modulus is available at most once. In this
application D is the full divisor set of M.

For each prefix r modulo p^s, let U_r be the uncovered cofactor residues
in Z/MZ. CRT identifies a residue with (r,z); the fixed classes do not
depend on the next h p-digits. Consequently each nonempty U_r produces
p^h identical nonempty children at depth s+h. Write n for the number of
nonempty parents and N=p^h n for the number of children.

A new class with modulus p^(s+j)d acts in one prefix of length s+j,
and hence in at most p^(h-j) deepest children. In each such child it
covers one coset modulo d of the same cofactor set U_r. Count one
*incidence* for each new class acting in a deepest child. The total
number I of incidences is at most

    I <= W |D|,  W = sum_{j=1}^h p^(h-j).

Let A be any subset of the nonempty parents. Define

    T(A) = {d in D: some U_r, r in A, is contained in one coset modulo d}.

At most W|T(A)| children belonging to A can be covered using just one
incident new class: every such class must have its cofactor divisor in
T(A), and each available p^(s+j)d contributes at most p^(h-j) incidences.
All other children in A require at least two incidences. Each child
outside A requires at least one. Therefore

    I >= N + p^h |A| - W |T(A)|.

A necessary condition for covering is thus, for **every** A,

    N + p^h |A| - W |T(A)| <= W |D|.                 (1)

Only one strictly violating A is needed to exclude a case. Empty A gives
the ordinary finite-horizon width bound. The generator finds A by a tiny
parent-subset search. For a nonempty U_r, it discovers compatible d using

    d | gcd(M, {z-z0: z in U_r}).

The verifier instead tests whether all members of U_r have the same
ordinary residue modulo d, for every eligible d. It checks the recorded
A directly, without importing the generator or searching for a cut.

The counting inequality is elementary. Neither the underlying CRT idea
nor such a resource count is claimed as an original general principle.
The contribution is its certified application to all phases in this
repair neighborhood.

## Closing the two surviving periods

After selecting the phase a modulo the freed m, all 65 eligible moduli
of B are present. For 30240=3^3*1120, the only new moduli are 27d with
d|1120. In (1), p=3, s=2, h=1, |D|=24, W=1. The certificate gives a
strict cut for every phase of all twelve surviving moduli, **369 cases**.
The smallest left-hand side over these cases is **28**, exceeding 24.

For 40320=2^7*315, the only new moduli are 64d and 128d with d|315.
Here p=2, s=5, h=2, |D|=12, W=3, so the incidence budget is **36**.
Every reassignment of modulus 8 or 16 leaves at least 18 nonempty
parents. Thus N>=4*18=**72**. Empty A already violates (1). All **24**
phases are enumerated and checked directly.

The capacity exclusions and these 393 sufficient cuts exclude every
multiple of B below 50400 in the complete stated family. This proves
the lemma.

## Certificate, reproduction, and trust boundary

`certificate.json` contains 260 capacity rows [m,t,number_of_holes,C]
and 393 sufficient tower cuts [m,a,N,A,|T(A)|,left_side_of_(1)]. Each
case is identified explicitly; the checker rejects a missing or repeated
case. This is a compact sufficient certificate, not a search log.

From the repository root, with standard-library Python 3.10 or later:

```sh
python3 number_theory/distinct_covering_seed_repair_cuts/generate.py
python3 number_theory/distinct_covering_seed_repair_cuts/verify.py
python3 number_theory/distinct_covering_seed_repair_cuts/controls.py
```

The proof boundary consists of the unformalized CRT and counting arguments
above plus exact integer execution. No solver, floating arithmetic, symmetry
assumption, external enumeration corpus, or published lower bound for the
minimum-seven problem is required. The supplied seed is checked from its
definition. The checker is a separate algorithm by the same researcher;
no independent external review is asserted.

At LCM 50400 the present lemma leaves the repair family unresolved. It
also leaves unrestricted L_min(8) unresolved and does not address the
different condition "all moduli at least eight" when modulus eight is absent.
