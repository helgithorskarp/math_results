# Actual octic collision moment reduction

Actual author **six-sendov-2**, role **researcher**. Complete ordinary
author proof, **unformalized and independently unreviewed**.

[PROOF.md](PROOF.md) derives the actual angular value and its whole
three-parameter gradient after factoring one double original root on
mu3=mu5=0. It retains all six real roots of the remaining original
sextic. A rank-one formula gives the exact extra collision cost and
its normal splitting derivative. A nonsymmetric single-double local
maximum must have strictly negative algebraic center value at the
collision and satisfy a quantitative cost-compensation condition.
At an exact triple, the full critical polynomial is repeated, yet the
canceled chart gives a valid value and explicit second-order necessary
condition. No collision optimizer or global first-power claim follows.

The standard-library checker is self-contained. Python3.11+:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/collision-moment-reduction/verify.py
python3 -I -B -O round-two/six-sendov-2/collision-moment-reduction/verify.py
```

Both must reproduce the complete18857-byte canonical record SHA256
`a5f6ec31e5424970d60e4b17200cb31b5cd952841009e3823ce1a012e68c22f3`,
seven controls (six actual and one infeasible), all full moving-node
first derivatives at the actual controls, two full triple second
derivatives, and nine mathematical damage rejections. External fixture
comparison is whole-byte and type-sensitive; a damaged coefficient,
missing field, extra field or altered field type fails in normal and
optimized modes. Controls are not an enumeration of the real domain.

Optional SymPy1.14: compare_cas.py independently derives and compares
all237 whole universal polynomial maps using symbolic division and
logarithmic/Laurent series. It imports no checker code. It is a
same-author algebra comparison, not independent mathematical review.

Validation used CPython3.12.14, serial children, six native thread
variables1, fixed50-second guards and unchanged1CPU2GiB. Normal/optimized checks took0.479/0.651s; normal/optimized cold
checks took0.417/0.608s. Core plus fixture children
peaked at22624KiB. The optional all237-map CAS comparison took
0.984s, with maximum peak across all children
59944KiB. No resource limit was hit or increased.
Classical continuous feasibility, compression, interlacing, inverse
updates and local-extremum arguments remain ordinary proof obligations.
[LITERATURE.md](LITERATURE.md) gives primary status, exact source inputs
and the boundary of this result's novelty and trust.
