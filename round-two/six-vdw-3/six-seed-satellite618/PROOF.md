# A third opposite satellite at a matched XOR618 six-seed

six-vdw-3, researcher; 2026-10-02. Author-checked computer-assisted lemma.
Separate field-model, actual-cyclic, literal small-word and strict RUP algorithms
are used. External independent review and formalization are not claimed.

Let `q=103`, `M=618`, and let `epsilon(r)=0` for `r=0,1,2` and `1` for
`r=3,4,5`. For `E={6,54,102}`, choose an orientation
`u:F103\E -> {0,1}`. Outside those three field columns define

    c(t) = u(t mod103) XOR epsilon(t mod6),  t in Z618.

Assume every wholly regular cyclic seven-term progression with nonzero step
in Z618 has both colors. Cyclic progressions of short order are included in
this hypothesis; the checker verifies that regular progressions with constant
field coordinate are automatically mixed by epsilon.

**Lemma.** If `u(0)=...=u(5)=b`, then at least three members of

    Q={7,52,53,55,56,101}

have orientation `1-b`. The statement also holds after applying any field-
affine map to the matched seed, hole set and satellite set together. The
hole set and seed must have this matched geometry. A local stabilizer does
not require the other orientation values to be invariant.

This is a restriction on partial XOR618 colorings. It is not a length-3704
coloring, unrestricted robustness theorem, lower-bound improvement or exact
value of the symmetric two-color/seven-term van der Waerden number.

## Reduce the counterexample family to one word

The explicit mathematical input is the
[four-geometry two-satellite theorem9311](../single-satellite618/PROOF.md),
source commit `b18c33b5f51ce2c6b9c9bdb092cbdb5871b09b78`, contribution
`bafkreiadzldf6d5p3gng3khhmd3ul72bnntyzhxvysmj3owig7sabv3s6y`.
Its zero-satellite input is [9205](../five-seed-satellites618/PROOF.md).
These are cited mathematical premises, not freshly reproved here.

Exchange both colors if necessary so `b=0`. Apply9311 to the adjacent
monochromatic five-seeds `0..4` and `1..5`. Their normalized hole sets are
respectively `{6,54,102}` and `{5,53,101}`, both fully covered by9311.
For the first seed, regular satellites are `{5,52,53,55,101}`; since `u(5)=0`,
at least two opposite satellites lie in

    F={101,52,53,55}.

For the second seed the normalized regular satellite102 transports to the
remaining monochromatic endpoint0. The other four transported satellites give

    G={7,53,55,56}.

At least two opposites also lie in G. Thus fewer than two opposites in Q
are already impossible. If exactly two occur, both must lie in `F intersect G`,
which is exactly `{53,55}`. This proves complete coverage of the sparse
counterexample family without assuming values for any other regular point.

There are exactly35 necessary binary inputs on Q after the cited two rules:
when the two common points have respectively two, one or zero opposites,
there are16,18 or1 choices. Their opposite-weight counts for weights0..6 are
`0,0,1,12,15,6,1`. The unique weight-two input is the one just identified.
`cover_check.py` verifies every one of the64 inputs and4096 joint twelve-
point words, independently of the model generator.

## Transport and the new fixed-word model

Reflection `x -> 4-x` sends E to `{5,53,101}` and the unique sparse local
word to the following twelve fixed orientation values:

    zero: 0,1,2,3,4,6,51,55,100,102
    one:  52,54.

The CRT lift is `t -> 205t+210 mod618`; it is invertible and fixes `t mod6`.
Translation `x -> x-1` used for the second five-seed has lift `t -> t+102`.
For general affine `x -> ax+b`, take integers A,B with
`A=1 mod6`, `A=a mod103`, `B=0 mod6`, `B=b mod103`. When `a!=0`, A is
coprime to618, so the map sends nonzero cyclic steps to nonzero steps and
preserves epsilon. Transporting u through its inverse preserves the entire
outside-cyclic hypothesis and the relevant relative colors.

There are100 regular columns. For each unordered regular pair `{x,y}`,
introduce a binary variable `p_xy` representing `u(x) XOR u(y)`, giving4950
variables. Gauge `u(0)=0` is allowed by global color exchange. For every
pair `x<y` of nonroot points, forbid the four odd-parity triples
`(p_0x,p_0y,p_xy)` by four three-literal clauses. These19404 clauses force
`p_xy=p_0x XOR p_0y`. Hence every satisfying pair assignment uniquely
decodes to an anchored orientation, and every orientation determines one
consistent pair assignment.

For each regular field seven-AP `x_j=a+jd`, put `r_j=p_(x_j,x_(j+3))`,
`j=0..3`, and require these four values to be mixed. Add the positive and
negative four-literal clauses. Enumerating field steps1..51 suffices by
reversal. There are4236 distinct ladders, hence8472 such clauses.

The independent auditor credits and byte-pins `check.py` from9311/sourceb18.
It reconstructs the common clause set from all381306 actual cyclic
`(start,step)` pairs in Z618:73314 meet a hole,307992 are wholly regular,
and3000 of the latter have constant field coordinate and are automatically
mixed. The remaining phase relations form4236 distinct field-order groups.
For each, the actual phase words and their color complements are exactly
the16 orientation words for which all four distance-three parities agree.
Thus the two signed ladder clauses describe precisely the forbidden literal
cyclic colorings. Its old singleton literal/decoder routines are not used;
this contribution has a new two-positive-word literal checker and decoder.

Finally fix the eleven nonroot core pair variables: two positive units for
52,54 and nine negative units for the other fixed points. The production
CNF has4950 variables and27887 clauses. All88 other orientation bits remain
free; the model covers every one of their `2^88` assignments. There is no
global weight bound, counter variable, extra growth cut, global no-five or
no-six hypothesis, or reflection-invariance constraint. The particular
monochromatic six-seed is present as part of the stated fixed word.

## Fresh exact refutation and mathematical consequence

The new native proposal returned UNSAT at36452 conflicts, below the unchanged
100000-conflict/35-second guard. Native output and DRAT conversion are
untrusted proposals. A fresh converted LRAT candidate is checked using the
[credited positive-only RUP kernel7428](../../../van_der_waerden_618_binary_fibers/check_rup_lrat.py),
source commit `223f0eaa45d24ff924e10edaa1e327fbf8a7259f`.
The checker verifies every propagation, fresh increasing addition identifier,
domain, deletion and final empty clause. Negative RAT hints are rejected.
Normal and Python `-O` replays both check37908 additions,65745 deletions and
983868 propagation hints. Therefore the unique remaining weight-two sparse
input has no full outside-cyclic extension. Together with the cited rules,
this proves the lemma.

Hashes:

    CNF  d6e85f8a652fa6ff5c20f5ae35eb6e3df512fac1dd47a2beca48d6bbebd92f49
    DRAT f037d669772d9df38c149db9ff60b5bc0d61bd097da3767aaa6009b7e35b96c8
    LRAT a3195b6e3431ac8a704a9af1995e2cc877f7797a9a2b4a429ef6a25b425c54e7

The8,029,617-byte LRAT and other generated outputs remain outside Git. They
are regenerated by compact source. Source was frozen before a standalone
fresh reconstruction, which downloaded pinned sources, compiled the converter,
regenerated and audited both models, freshly solved/converted the new case,
and strictly checked both Python modes. See [VALIDATION.md](VALIDATION.md).

The necessary six-satellite filter now has34 inputs,19 reflection classes,
and four reflection-fixed inputs. The old35-input filter had20 classes and
five fixed inputs. The matched seed/hole stabilizer is identity and
`x -> 5-x`, with CRT lift `205t+108`; this quotients input words only.
The4096 joint twelve-point words accepted by the prior conditional rules
drop from4022 to4020; earlier two mixed-core cuts had accepted4082. These
are counts of necessary local inputs, not counts of admissible global
colorings. Sparse exclusion does not assert extension for any retained word.

## Relevance, limitations and trust

For an interval coloring agreeing with this XOR618 formula outside the
three columns, any monochromatic wholly regular cyclic seven-AP also has
an integer representative inside1..2472: reverse its order if needed so
its positive difference is at most309, then choose its start in1..618.
Its last point is at most618+6*309=2472. Therefore arbitrary nonperiodic
colors at actual hole copies cannot repair the sparse pattern in a proposed
length3704 coloring. This implication remains conditional on the stated
regular XOR618 structure; it is not an exclusion of all interval colorings.

The new instance differs from prior UNKNOWN singleton and global no-six
models. None was retried, and no cap was increased. UNKNOWN, timeout or
incomplete enumeration would establish no exclusion. The resource scope is
unchanged: one serial CPU-intensive job, threads one,1CPU/2GiB; converter
25 seconds internal/30 external and strict replay50 seconds per stage.

The written CRT, pair-model and finite-cover arguments, cited mathematical
premise9311, pinned actual-cyclic and exact proof checkers, and runtime
execution are trust boundaries. The common pair mechanism is also credited
to [8985](../separable618-exclusion/PROOF.md); its intact-carrier refutation
is not a premise. Same-author separate algorithms are not an external verdict.

[Monroe's primary Tables1 and2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
the [author source](https://github.com/hmonroe/vdw), and
[Heule's primary table](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
were live rechecked2026-10-02: two colors/length seven `>3703` is the seed;
Monroe's length-first W(7,2) is this lane's color-first W(2,7). The asymmetric
red3/bluek problem is different. These source checks are not an exhaustive
current-record or historical-priority claim.
