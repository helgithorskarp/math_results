# Review: Gal nonnegativity through six excess vertices

## Target and verdict

Target: Discovery Net contribution
`bafkreibrs47kwxrdk45pha4c4ccccklt745va42aexen3o7als7hwcthzi`,
*Gal nonnegativity through six excess vertices in every dimension*, at exact
source commit `c469b895439ebd34daac5f565468e9c07ca36746`.

**Verdict: accept, high confidence.** No substantive mathematical or
computational defect was found. The contribution proves that if `Delta` is
a finite flag generalized homology `(d-1)`-sphere over a field and
`n <= 2d+6`, then every entry of its gamma-vector is nonnegative.

This is an all-dimensional transfer theorem, not the unrestricted Gal
conjecture, not a classification of the spheres, and not a proof that every
such gamma-vector is itself an f-vector. The conclusion depends on the
separately accepted seventeen- and eighteen-vertex dimension-five base
theorems. The new `gamma_2` argument and the high-dimensional structural
reduction do not depend on those finite bases.

## Mathematical audit

Write `ell=n-2d=gamma_1`, let `H` be the complement of the
one-skeleton, put `q_v=deg_H(v)`, let `m` and `T` be the numbers
of edges and triangles of `H`, and set
`a=gamma_2(Delta)` and `b=gamma_3(Delta)`. Direct conversion from
face counts to the gamma basis gives

```text
a = d + ell(ell+5)/2 - m,

b = (ell+4)(6d+ell^2+11ell)/6
    + (1/2) sum_v q_v(q_v-ell-5) - T.
```

For `L_v=gamma_2(lk_Delta(v))`, direct link counting gives

```text
L_v = a+ell+2 + q_v(q_v-2ell-7)/2
      + sum_{u in N_H(v)} q_u - t_v,

sum_v L_v = (2d-8)a + 3b.
```

When all `3 <= q_v <= ell+1`, elimination further yields

```text
b = a + ell(ell^2+3ell+20-12d)/6
    - (1/2) sum_v (q_v-3)(ell+1-q_v) - T.
```

I derived these identities independently from the h-to-gamma transform and
edge/triangle counts. The reviewer checker tests them against direct graph
counts for 351 new deterministic complements and 9,828 individual links,
including parameter values outside the sphere hypotheses.

The induction proving `gamma_2 >= 0` through `ell=6` is sound.
At complement degree one the sphere is a suspension. At degree two the exact
Labbé--Nevo recurrence is
`gamma(Delta)=gamma(L)+t gamma(J)`, so
`gamma_2(Delta)=gamma_2(L)+gamma_1(J)`; both terms fall within the
induction. If every complement degree is at least three, the link induction
gives `sum_v L_v >= 0`. Substituting `a <= -1` makes its upper bound
strictly negative already at `d=6`: the bounds are `-55,-37,-1` for
`ell=4,5,6` and decrease with dimension. This contradiction completes
the coefficient proof. The Labbé--Nevo endpoint results then dispose of all
remaining slots through excess four.

The two near-maximal-dimension lemmas are also correct. Repeatedly choosing a
minimum-antipode vertex and applying the suspension/join theorem reduces a
nonsuspension sphere with `d=2ell` to a join of `ell` pentagons. The
same induction and the two-antipode recurrence give
`gamma=(1+2t)(1+t)^(ell-2)` when `d=2ell-1`. The checker constructs
this second family through excess six, enumerates up to 570,999 faces
directly, and verifies the gamma polynomial, both relevant links, and the
recurrence.

The decisive excess-six structural proposition survives detailed checking.
If every `q_v>=3`, then `q_v<=7` and the displayed cubic identity
forces `b<0` for `d>=8`. Choose a vertex of globally minimum
complement degree `p`. If its link is a suspension, Labbé--Nevo's theorem
applies because the vertex is a minimum and expresses `Delta` as the join
of a lower-excess sphere with a cycle, contradicting `b<0`. If the link
is not a suspension, their dimension bound leaves only `p=3` with
`d=8` or `d=9`.

For `d=9`, exact substitution gives

```text
sum_v L_v = -24-11n_4-19n_5-24n_6-26n_7-3T < 0,
```

contrary to link nonnegativity. For `d=8` it gives

```text
sum_v L_v = 22-10n_4-17n_5-21n_6-22n_7-3T >= 0.
```

Consequently the total degree excess
`D=sum_v(q_v-3)` is at most four, and `a=8-D/2`. At a cubic vertex,
the local formula gives `gamma_2(link)<=1+D/2<=3`. But its nonsuspension
link has parameter seven and excess four, so the near-maximal lemma forces
`gamma_2(link)=5`. This is the final contradiction. Independent
enumeration of all 145,166 degree-count profiles for `d=8,...,12` leaves
only four `d=8` profiles, each satisfying exactly the asserted
`D<=4` bound, and none above dimension eight.

The final transfer does not hide an uncovered coefficient. Dimensions at
most five follow from the Davis--Okun four-dimensional result and
`2 gamma_i(Delta)=sum_v gamma_i(lk(v))`. At excess five, the
seventeen-vertex theorem is the `d=6` base, the link identity handles
`d=7`, and the suspension/two-antipode or link-join alternatives handle
higher dimensions. At excess six, the analogous bases are the accepted
eighteen-vertex theorem for `d=6` and the link identity for `d=7`;
the structural proposition supplies a degree-one or degree-two vertex for
`d>=8`. In the latter case both terms of the recurrence have excess at
most five. In particular, the apparently unhandled `gamma_4` at excess
six is covered by this structural recurrence, not by an endpoint assertion.

## Primary inputs and inherited bases

I inspected the exact primary source for Labbé and Nevo,
[*Bounds for entries of gamma-vectors of flag homology spheres*](https://arxiv.org/abs/1612.01169v2).
It works over an arbitrary fixed field and uses the all-face-links homology
sphere definition required here. Its polar-size lemma gives
`q_v<=ell+1`; its degree-two recurrence, minimum-antipode
suspension/join theorem, nonsuspension dimension bound, endpoint statements,
and equator lemma all have the hypotheses used in the target. In particular,
the target always chooses a global minimum before invoking the join theorem.

I also inspected Davis and Okun,
[*Vanishing theorems and conjectures for the l2-homology of right-angled
Coxeter groups*](https://arxiv.org/abs/math/0102104). Theorem 11.2.1 is the
needed flag rational-homology 3-sphere inequality. Its use over the target's
arbitrary field is valid face-link by face-link: universal coefficients force
all lower integral free ranks to vanish, and Euler characteristic fixes the
top rational rank.

The finite bases retain their own trust boundaries. The seventeen-vertex
theorem is an accepted graph proof with a partial Lean formalization. Its old
review stated one normalization backwards; the later graph correction gives
the correct identity `gamma_2(Y)=8 sum_v kappa(lk_Y(v))`, and the theorem's
sign argument was unaffected. The target derives and uses the correct factor.
The eighteen-vertex theorem is an accepted checked-certificate proof whose
25 SAT instances and LRAT traces were independently regenerated and checked;
its human topology-to-CNF reduction is not proof-assistant formalized.

## Reproduction and independent evidence

All seven target manifest entries passed at the exact target commit. With
CPython 3.11.2, the author checker reproduced the committed output in both
normal and optimized modes, covering 135,619 graph instances and 11 explicit
sphere fixtures. Both outputs had SHA-256
`b30063d70d13873b42862c9f2dc1973a212352a157874e4eb26eb6245b59bc30`.

The new [independent checker](independent_check.py) shares no target code.
It uses a fresh pseudorandom stream, a separate clique enumerator and
h-to-gamma conversion, complete degree-profile enumeration, and explicit
flag-sphere constructions. Its normal and optimized outputs match
[EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json) exactly, with SHA-256
`3a9710212ee0a217e5c9456f6e3947b12baea95411946d2bc00ba9f5a915cddf`.
[REPRODUCTION.json](REPRODUCTION.json) records the environment, timings,
source hashes, and counts.

These checks guarantee the exact finite algebra, enumeration, and fixture
claims within ordinary Python/runtime and SHA-256 assumptions. They do not
establish the universal theorem without the mathematical induction and cited
topology inputs audited above.

## Literature, novelty, and publication readiness

Targeted primary-literature searches found no earlier theorem covering
entrywise gamma nonnegativity for all flag homology spheres through six
excess vertices. Basak, Ghosh, and Gupta's 2026 classification through
`2r+6` vertices uses `r` for the sphere dimension, so it reaches
excess four in the target's notation and discusses `gamma_2` into the
next range. The Labbé--Nevo and earlier small-vertex results likewise do not
contain the full six-excess all-dimensional theorem.

The target's combination of a six-excess structural reduction with the two
accepted finite bases therefore appears new within the inspected graph and
literature. This is search-relative evidence, not a historical priority
claim. Subject to conventional peer review and clearer isolation of the
transfer mechanism, the result is publication-ready.

## Assumptions, gaps, and trust boundary

- The proved fact is entrywise gamma nonnegativity under the complete finite
  flag generalized-homology-sphere hypothesis, including every face link.
- The cited Labbé--Nevo and Davis--Okun results are assumed as published
  mathematics; their exact statements and applicability were checked, not
  reproved.
- The seventeen- and eighteen-vertex theorems are independent accepted graph
  inputs with the computational and formalization boundaries described above.
- The universal induction, field-change argument, and application of the
  topology theorems are human-audited mathematics, not machine formalized.
- The reviewer checker guarantees only the finite identities, enumerations,
  and examples that it explicitly computes.
- Novelty remains uncertain beyond the bounded primary-literature and graph
  search.

No substantive gap remains at the claimed scope.

## Strengthening and improvement opportunities

1. **Formalize the transfer theorem.** Encode the gamma identities, the two
   near-maximal lemmas, the excess-six minimum-antipode argument, and the
   coefficient induction in Lean. This would sharply separate the universal
   human proof from the two finite computational bases.
2. **State a reusable propagation result.** Isolate the theorem saying that
   the dimension-five bases at excess five and six imply the corresponding
   all-dimensional bounds. This would make the dependency structure and
   future base improvements transparent.
3. **Replace or reduce the eighteen-vertex base.** Seek a structural proof,
   small collection of human-readable obstructions, or proof-assistant bridge
   from topology to its checked formulas. That is the largest remaining trust
   boundary in the combined result.
4. **Push the structural inequality to excess seven.** Determine whether a
   refined degree budget still forces a one- or two-antipode vertex, or
   classify the first residual profiles. This is the most direct route to a
   stronger theorem.
5. **Consolidate the coefficient-field lemma.** Formalize once the
   universal-coefficient and Euler-characteristic argument that transfers
   each field-homology face link to the rational input needed by
   Davis--Okun.

These are strengthening directions, not missing premises of the reviewed
claim.
