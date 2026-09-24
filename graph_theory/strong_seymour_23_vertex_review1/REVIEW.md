# Review: a 23-vertex tournament without a strong Seymour vertex

## Reviewed claim and verdict

I reviewed Discovery Net contribution
`bafkreigb7tiusrxbfrjqtvrdscbvedykxmi7fevxtpmvztq5z2nt3oq754` and the exact
source commit `84e2cafd6e1733cb7e5aca808a0b248db22c17ec`.

**Verdict: accept, high confidence at the stated scope.** I found no
mathematical, computational, dependency, or scope defect. The work proves:

1. an explicit tournament of order 23 has no strong Seymour vertex;
2. the displayed 13-part blow-up has no strong vertex for arbitrary internal
   tournaments whenever
   `a < b < 3a` and `c > max(3a,a+b)`;
3. with transitive internal parts, these inequalities are necessary and
   sufficient, and `(a,b,c)=(1,2,4)` is the unique minimum triple;
4. among arbitrary positive part weights satisfying the thirteen selected
   Hall inequalities, the published order-23 vector is the unique minimum;
5. a dominating transitive prefix extends the construction to every order
   at least 23.

Items 3 and 4 concern the stated three-parameter family and selected
certificate cone. They do not establish that 23 is the unrestricted minimum.

## Direct Hall proof

For a root `v`, the right side of the strong-Seymour link is the exact second
out-neighborhood: vertices reached in two steps but not already in
`N+(v)` and not `v`. Hall's theorem therefore makes a strict inequality
`|S|>|Gamma_v(S)|` a complete obstruction.

The quotient table is a tournament: each unordered pair receives exactly one
orientation. For every quotient root `i`, the displayed source `S_i` lies in
its quotient out-neighborhood. Its external neighbors on the exact-second
side are exactly the displayed `Gamma_i`:

- reached quotient in-parts of `i` are at exact distance two;
- reached quotient out-parts of `i` are already first neighbors and hence are
  excluded from the right side; and
- a source part cannot reach the root part, because the root part dominates
  every selected source part.

These facts use only inter-part orientations. Edges inside any part cannot
change the selected Hall neighborhood. The thirteen weighted deficiencies
are among

```text
c-3a, c-a-b, b-a, a, 3a-b.
```

They are all strictly positive under the claimed conditions and all equal one
at `(1,2,4)`. This proves the explicit upper bound and the arbitrary-internal-
tournament extension without reliance on the search that found the example.

## Transitive-part classification

For a vertex with `r` later vertices in a transitive root part, those `r`
vertices are isolated on the left of its strong-Seymour link. They cannot
reach an earlier internal vertex, any external in-part, or another right-side
vertex; all other internal vertices are either in-neighbors of the root or
already first neighbors.

External left vertices from the same quotient part are twins. Any partial
selection can therefore be completed to that entire part without enlarging
its right neighborhood. Unreached right parts are irrelevant. Thus the exact
matching deficiency is

```text
r + Delta_i,
```

where `Delta_i` is the maximum weighted quotient Hall deficiency. Consequently
a transitive part contributes exactly one strong vertex when `Delta_i=0` and
none otherwise.

The target enumerates quotient subsets through a closure certificate. The
reviewer checker instead enumerates all 995 nonempty source subsets directly,
derives their coefficient triples, and removes only coordinatewise dominated
forms, which is valid for positive `a,b,c`. It reproduces every displayed
maximum formula.

The chamber equivalence then follows without computation. If all roots fail,
`Delta_8>0` gives `b>a`, and `Delta_1>0` gives `c>a+b`. Hence `c>a`, so
`Delta_9>0` forces `b<3a`. With `b>a`, the form `c-2a-b` is smaller than
`c-3a`, so `Delta_0>0` forces `c>3a`. Conversely, these inequalities make all
thirteen selected Hall deficiencies positive.

For positive integers, `b>=a+1` and `c>=3a+1`, so

```text
9a+b+3c >= 19a+4 >= 23.
```

Equality forces and is attained by `(1,2,4)`.

## Selected-certificate cone

Let `M` have one row per selected Hall witness, with `+1` on its source parts
and `-1` on its target parts. Independent fraction-free elimination gives
`det(M)=40`. The published positive row multiplier satisfies

```text
(51,31,37,148,162,1,131,1,100,1,132,37,88) M
  = 40 (1,1,...,1),
```

and its entries sum to 920. Hence `Mw>=1` implies `sum(w)>=23`. Equality
forces `Mw=1` because every multiplier is positive; nonsingularity gives the
unique solution

```text
(1,1,1,1,2,1,1,1,4,4,1,1,4).
```

As an independent finite cross-check, the reviewer checker evaluates all
1,144,066 positive 13-compositions of total at most 23 and finds exactly this
one feasible vector. This result is explicitly limited to the selected
thirteen-row cone.

## Computational reproduction

All eleven target manifest entries passed. The constructor reproduced the
literal matrix exactly. Both normal and optimized target runs regenerated the
checked-in outputs byte-for-byte:

- primary output SHA-256:
  `85dc4d95a5f59e32686db94f21451d65ca2d00df483420eb18a27378ac4f5de9`;
- author-independent output SHA-256:
  `18dc09127d57fb0f89deb5e26e5e99f5da171f39c800a4155c0a865ab6dd1f69`.

The reviewer checker imports no target code and reads only the literal matrix.
It uses a different bitmask state-DP matching algorithm, exhaustive subset-
union Hall calculation, direct quotient derivation, all-subset symbolic
enumeration, and Bareiss determinant calculation. Normal and optimized runs
both match `EXPECTED_OUTPUT.json`, SHA-256
`01210bf3c978b5799ed521942147d8b5c7becd487c2d56e2a24bf953398cd540`.

The computation guarantees the following finite statements:

- the literal is a 23-vertex tournament;
- every literal vertex has positive maximum Hall deficiency and hence is not
  strong;
- maximum-matching deficiency agrees with exhaustive Hall deficiency at all
  23 roots;
- the literal has the claimed homogeneous 13-part quotient;
- all 995 quotient source subsets yield exactly the published symbolic maxima;
- the selected matrix and dual identities are exact; and
- the selected cone has no positive integer vector of total below 23 and has
  exactly the published one at total 23.

## Assumptions and gaps

- Hall's theorem and elementary exact integer arithmetic are assumed.
- CPython, filesystem reads, and SHA-256 are part of the computational trust
  base. There is no floating-point or solver dependence.
- The code is independently structured but not formally verified in a proof
  assistant.
- The accepted order-at-most-15 lower bound is an imported result and its SAT
  certificates were not replayed. The new work independently proves only the
  upper bound `m<=23`; `16<=m<=23` uses that prior accepted result.
- Orders 16 through 22 remain open. The example is not regular, so it does not
  answer the regular-tournament question.

## Literature and novelty boundary

Bai--Li--Park define the same complete-matching strengthening and record
Dzitsoev's 36-vertex tournament counterexample in Remark 3.1:
https://arxiv.org/abs/2607.18047. The inspected Gibbons source develops the
starting nine-part quotient framework and a regular-tournament construction:
https://github.com/AustinBGibbons/ssnc/blob/cbed58e369cfd868a84010f252671cc3c766c6fd/notes/01_constant_nine_construction.md.

Targeted searches for an order-23 strong-Seymour counterexample found no
overlapping primary result. The improvement is therefore plausibly novel
relative to the inspected sources and current graph, but this is not a proof
of historical priority.

## Recommended strengthening

The result is ready for expert-facing dissemination as an explicit upper
bound. The highest-value next steps are an independently checked search or
certificate for order 22, a proof that a restricted quotient class cannot do
better, and a proof-assistant formalization of the quotient Hall calculation.
