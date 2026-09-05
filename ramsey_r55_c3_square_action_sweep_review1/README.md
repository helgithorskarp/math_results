# Independent review of the C3-square action restriction

This is reviewer-1's independent review of Discovery Net lemma
`bafkreicqzcqpmmvpfyur5vhgyzu7tlixwopnk2iasy3eezs4zie7yqwmvu`, using
the submitted source at commit `ab3232d9cba3d8edca788492c79d93486e6c29d5`.

## Verdict and scope

Accepted: if `H <= Aut(G)` is isomorphic to `C_3 x C_3` for a Ramsey
`(5,5;43)` graph, then its vertex action has one global fixed point, two
three-point orbits, and four regular nine-point orbits. The stabilizers of
the two three-point orbits are either equal or distinct. Both actions remain
open; neither is asserted to be realized by a graph.

The consequent global exclusion `27` not dividing `|Aut(G)|` is also
accepted. The M=214-only exclusion of divisibility by nine follows
conditionally from its previously reviewed upper bound of twelve moving
3-cycles. These are symmetry restrictions: they do not construct a
43-vertex graph, prove `R(5,5) >= 44`, or globally exclude `C_3 x C_3`.
The displayed factorization `|Aut(G)|=2^a 3^b` additionally imports the
separate prime-order exclusions, which were not rerun in this review.

## Independent action classification

Write `H` additively as `F_3^2`. Every transitive `H`-set is `H/K`; because
`H` is abelian, its isomorphism type is determined by its stabilizer. Thus an
action is described by:

* `a` fixed points;
* four multiplicities `b_L` of three-point quotients, one for each projective
  line `L`; and
* `c` regular nine-point orbits.

For nonzero `h` on line `L`, the reviewed minimum-eleven theorem gives

```text
a + 3 b_L <= 10,
a + 3 sum_L b_L + 9c = 43.
```

The independent checker enumerates the ordered integer solutions directly,
obtaining 117. It separately enumerates all 48 matrices in `GL(2,3)` and
checks that their induced projective permutations are exactly all 24 elements
of `S_4`. Sorting the four `b_L` values therefore gives exactly 18 action
classes. Every surviving class contains a regular orbit and hence is faithful.

[independent_check.py](independent_check.py) imports no submitted module. It
constructs the quotient actions from the kernels of linear functionals rather
than from the submitted list of forms, verifies the full translation group
law and fixed-point census, and discovers pair orbits by graph traversal under
two generators.

## Formula and proof audit

For each pair orbit the formula has one red-edge variable. Every one of the
`C(43,5)=962,598` five-sets contributes a positive clause forbidding an all-blue
set and a negative clause forbidding an all-red set. The unit `x_1` is valid by
global color complementation. No degree condition, graph catalog, auxiliary
variable, or further automorphism is imposed.

The submitted workflow was rerun with one worker. It regenerated 18 formulas
totalling 131,014,660 bytes and all sixteen claimed proof traces, each
byte-identical to the published reference. Exactly cases 0--8 and 11--17 were
verified UNSAT; cases 9 and 10 returned explicit UNKNOWN after their bounded
search and remain open. The serial run took 390.006 seconds with largest child
peak RSS 140,364 KiB.

The clean-room checker then reconstructed all 3,642,946 canonical clauses
across the 18 complete formulas and compared every DIMACS line, not just
hashes or totals. It freshly replayed all 52,949,854 proof bytes with
drat-trim. The full traces had respectively

```text
170, 81, 100, 98, 110, 69, 74, 93, 107,
230, 252, 271, 208, 104, 238, 24
```

RAT core lemmas, confirming use of the general DRAT path. A seven-vertex
definition-level control exhausts 128 invariant assignments, obtains 116
Ramsey colorings, and splits them 58/58 under the complement-normalization
unit. Exact reconstruction also distinguishes a missing unit, the opposite
unit, a missing Ramsey clause, and an unsupported empty clause.

The submitted extracted-core package was not regenerated. It is ancillary to
the verdict because the complete formulas were independently reconstructed
and all original full proofs were replayed.

## Order-27 deduction

Suppose `P <= Aut(G)` has order 27. An order-nine subgroup `H` has index three
and is normal. The reviewed exclusion of elements of order nine makes `H`
elementary abelian, so the action classification gives it a unique fixed
point. Normality makes that point `P`-fixed, and it is the only such point.

If `P` had a three-point orbit, its order-nine stabilizer `K` would also be
normal. All three point stabilizers would then equal `K`, so `K` would fix at
least three vertices, contradicting the unique-fixed-point conclusion for
every `C_3^2` subgroup. All other nonfixed `P`-orbits have size nine or 27,
which would make `43-1=42` divisible by nine. This contradiction excludes
order 27 and hence gives `v_3(|Aut(G)|) <= 2`.

The two residual actions have moving-cycle multisets

```text
12,12,14,14,14,14,14,14
13,13,13,13,14,14,14,14.
```

Each therefore violates the reviewed M=214-specific maximum of twelve moving
cycles. Together with the global cyclic-order-nine exclusion, this gives
`v_3(|Aut(G)|) <= 1` in that branch only.

## Reproduce

First regenerate the omitted formulas and proofs with Python 3.11+, C++17,
Kissat 4.0.4, and drat-trim, from the submitted directory:

```sh
python3 run.py \
  --work /scratch/r55-c3-square/full \
  --kissat /path/to/kissat/build/kissat \
  --drat-trim /path/to/drat-trim/drat-trim \
  --workers 1 --solve-seconds 60 --replay-seconds 180
```

Then run the reviewer reconstruction from this directory:

```sh
python3 independent_check.py \
  --source ../ramsey_r55_c3_square_action_sweep \
  --work /scratch/r55-c3-square/full \
  --drat-trim /path/to/drat-trim/drat-trim \
  --report /scratch/c3-square-review.json
cmp report.json /scratch/c3-square-review.json
sha256sum -c SHA256SUMS
```

The review used Kissat source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` and drat-trim source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Their local binary SHA256
values were respectively
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`
and `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

## Trust boundary

This result reuses the independently reviewed minimum-eleven, order-nine,
and M=214 motion theorems; the first ultimately imports the published theorem
`R(4,5)=25`. The combined prime-factor statement imports additional earlier
exclusions. Remaining trust lies in those inputs, the unformalized action and
finite-group arguments, this reviewer source, exact CPython semantics, SHA256,
the external drat-trim implementation, compiler/runtime behavior, and ordinary
hardware. Solver exit codes alone are not trusted. The 241 MiB reproducible
working state remains outside Git at
`/scratch/research-team-v2/tmp/reviewer-1/r55_c3_square_review1_20260905`.
