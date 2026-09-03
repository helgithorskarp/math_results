# Dahlberg's length-four involution symmetry: a descent-set refinement

## Claim status

This directory records an **exact finite verification** and an elementary
symmetry-reduction lemma.  It does not claim a proof for arbitrary `n`.

For a permutation `w`, let `Des(w)={i:w(i)>w(i+1)}`.  The computation verifies
for every `0 <= n <= 15` and every `D` contained in `[n-1]` that

```text
#{w in I_n(1432): Des(w)=D}
  = #{w in I_n(2134): Des(w)=[n-1] minus D}.                 (1)
```

This is stronger in the verified range than the major-index identity conjectured
by Samantha Dahlberg, because summing (1) with weight `q^(sum D)` gives

```text
MI_n(1432;q) = q^(n choose 2) MI_n(2134;q^-1).
```

The source reports computation only for `m,n <= 9`.  The descent-set refinement
and its verification through `n=15` appear to be new to the sources searched,
but this is a search-relative novelty statement, not a priority claim.

## Reverse-complement reduction

For `w` in `S_n`, define `rc(w)(i)=n+1-w(n+1-i)`.  Conjugating by the reversal
permutation shows that `rc` preserves involutions.  It also preserves classical
pattern containment and satisfies

```text
rc(1432)=3214,       rc(2134)=1243,
Des(rc(w))={n-i:i in Des(w)}.
```

Reflection `D -> {n-i:i in D}` commutes with complementation in `[n-1]`.
Consequently, (1) for any fixed `n` implies, without further computation,

```text
#{w in I_n(1243): Des(w)=D}
  = #{w in I_n(3214): Des(w)=[n-1] minus D}.                 (2)
```

Thus a proof of the stronger `1432/2134` statement would settle both nontrivial
length-four cases of Dahlberg's involution conjecture.

## Completeness of the production enumeration

Every involution of `[n]` has a unique parent obtained from the cycle containing
`n`: delete the fixed point `n`, or delete both entries of its 2-cycle and
standardize.  Conversely, append a fixed point to an involution of `[n-1]`, or
insert a unique 2-cycle `(i,n)` into one of `[n-2]`.  Since classical pattern
avoidance is hereditary, pruning a child exactly when it contains the forbidden
pattern loses no avoider.  This proves completeness and absence of duplication
for the generating tree in `verify_pruned.py`.

The four optimized pattern tests encode their defining inequalities with exact
integer bit masks.  Before the main run, each is compared with literal
four-subsequence standardization on **every permutation through `S_7`**.  At each
level, the avoider total is also checked against the independently known Motzkin
recurrence.

`independent_bruteforce.py` has a separate trust path: it enumerates all
involutions, does no avoidance pruning, standardizes every four-subsequence, and
checks both pairs directly through `n=11`.  It separately checks the involution
totals against `a_n=a_(n-1)+(n-1)a_(n-2)`.

## Reproduction

Tested with CPython 3.11.2 on Debian 12; there are no third-party dependencies,
floating-point operations, random choices, solvers, or external input files.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 dahlberg_length4_descent_census/verify_pruned.py --max-n 15
PYTHONDONTWRITEBYTECODE=1 python3 dahlberg_length4_descent_census/independent_bruteforce.py --max-n 11
```

The final lines should be

```text
verified descent-set complementation for 1432/2134 through n=15; reverse-complement proves the same finite range for 1243/3214
independent definition-level replay passed through n=11
```

The production output includes a SHA-256 digest of each complete descent-set
counter at every `n`, so later runs can compare all coefficients rather than only
aggregate counts.

## Failed structural route

RSK tableau transposition is a tempting universal descent-complementing map on
involutions, but it does not map either avoidance class correctly.  The smallest
obstructions occur at `n=5`: it sends `35142` to `21435`, and sends `14523` to
`32154`.  The first source permutation avoids `1432` while its image contains
`2134`; the second avoids `1243` while its image contains `3214`.  A proof must
therefore use more than tableau transposition alone.

## Source

Samantha Dahlberg, *Permutation Statistics and Pattern Avoidance in
Involutions*, Section 6, Conjecture 6.13,
<https://arxiv.org/abs/1709.08252>.
