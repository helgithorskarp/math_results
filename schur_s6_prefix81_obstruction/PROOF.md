# The fixed-prefix obstruction

Write `[N]={1,...,N}`. A classical Schur colouring is a map
`c:[N] -> {1,...,k}` for which no positive `x,y` with `x+y <= N` have
`c(x)=c(y)=c(x+y)`. The case `x=y` is included.

## Elementary deduction rule

Associate a nonempty set `D(v)` of possible colours to each integer `v`.
Initially, fixed integers have their prescribed singleton sets and all other
integers have `{1,...,k}`. Given a triple `x+y=z` and a target
`t in {x,y,z}`, if every **other distinct vertex** has singleton domain `{a}`,
then delete `a` from `D(t)`.

This rule is sound: if a Schur colouring satisfied all earlier restrictions
and had `c(t)=a`, all vertices of that triple would have colour `a`, which is
forbidden. Induction on the deductions shows that every hypothetical colouring
satisfying the initial fixed entries must take each `c(v)` in its current
`D(v)`. An empty domain therefore disproves the existence of such a colouring.

Taking distinct vertices handles doubling in both directions. If `x=y`,
fixing `x` excludes its colour from `2x`, and fixing `2x` excludes its colour
from `x`. Treating the two copies of `x` as separate unknowns would lose the
second implication.

## Application to the specified 81 entries

Let `b` be the full explicit word in `baseline.txt`. Its first 81 entries are
the sole hypotheses of the obstruction. Set `N=537`, `k=6`,
`D(v)={b(v)}` for `v<=81`, and `D(v)={1,...,6}` otherwise.

Each row `[t,a,x,y]` of `prefix81_proof.json` instructs the checker to apply
the preceding rule to target `t`, colour `a`, and triple `(x,y,x+y)`.
The checker verifies positive ordered summands, the interval boundary, target
membership, singleton premises, and actual deletion of a present colour.
It rejects unfinished deductions and steps after a contradiction.

All 351 rows pass these tests; the last deletion empties `D(537)`. Hence no
Schur six-colouring of `[1,537]` has that fixed prefix. The certificate includes
23 doubling deductions, so it proves a statement about classical Schur
colourings, without substituting a weak-Schur condition.

The complete `baseline.txt` is itself checked by direct enumeration of
`z=2,...,536` and `x=1,...,floor(z/2)`, with `y=z-x`. This covers every
unordered Schur triple, including every repeated-summand triple, exactly once.
It establishes that the explicit starting word is a valid known 536-colouring;
it is not part of the argument excluding extensions of the prefix.

If a hypothetical colouring agrees on the prefix with a global relabelling
`pi(b)`, apply `pi^{-1}` to all its colours. This preserves every equality or
inequality between colours and gives the already excluded case. This proves
the relabelling-invariant form of the statement.

No claim about an unrestricted colouring of `[1,537]` follows. Such a colouring,
if it exists, must violate these prefix assumptions.
