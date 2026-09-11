# At least ten named-asymmetric pair links in `SCA(5040;7,9)`

## Result

For a hypothetical `SCA(5040;7,9)`, let `P_wy(A,B,C)` be the
ordered-pair link counting rows in which `w` precedes `y`, with the other
seven named symbols partitioned into the sets before `w`, between `w,y`, and
after `y`.  Call the link coordinate-symmetric when its value depends only on
`(|A|,|B|,|C|)`.

**Theorem.**  Every hypothetical `SCA(5040;7,9)` has at least ten
coordinate-asymmetric ordered-pair links.

The earlier
[`unrestricted asymmetry theorem`](../sequence_covering_sca79_unrestricted_pair_asymmetry/README.md)
proves a lower bound of nine.  Its
[`exact-nine reduction`](../sequence_covering_sca79_nine_asymmetry_branch/README.md)
shows that equality would make the asymmetric links a directed cycle cover
and every full point link uniform.  The named predecessor-set argument below
rules out equality.  It eliminates all eight cycle-cover types at once,
including all 133,496 labelled supports.

This is a global branch reduction for the open problem.  It does not decide
whether the array exists.

## Named immediate-successor equations

Assume for contradiction that there are exactly nine asymmetric links.  Fix
a symbol `w`, let `x` be its unique asymmetric out-neighbour, and put

```text
Y = alphabet minus {w,x},       |Y|=7.
```

For every `y in Y`, the link `P_wy` is coordinate-symmetric.  On its
`(2,0,5)` composition layer, denote the common integral cell value by `q_y`.
The value may depend on `y`; no equality among the seven links is assumed.

For each `z in Y`, take the named predecessor set

```text
A_z = {x,z}.
```

The uniform point-link theorem gives exactly

```text
F_w(A_z) = 2! 6! / 72 = 20                                   (1)
```

rows having `A_z` as the complete predecessor set of `w`.  In every such
row, `w` is third and has a unique immediate successor.  That successor is
some `y in Y minus {z}`.  For a fixed eligible `y`, the rows are counted by
the single pair-link cell

```text
P_wy(A_z, empty, alphabet minus {w,y} minus A_z).
```

Its region sizes are `(2,0,5)`, so coordinate symmetry makes its value
`q_y`.  Partitioning the 20 rows by their immediate successor therefore
gives the seven named equations

```text
sum_(y in Y minus {z}) q_y = 20             for every z in Y. (2)
```

Sum (2) over all seven choices of `z`.  Each `q_y` occurs six times, hence

```text
6 sum_(y in Y) q_y = 7 * 20 = 140.                            (3)
```

The left side is divisible by six, whereas `140 = 2 (mod 6)`.  This
contradiction excludes exactly nine asymmetric links.  Combined with the
previous lower bound of nine, it proves the theorem.

Equivalently, the coefficient matrix of (2) is `J-I`, with determinant six
and unique rational solution `q_y=10/3` for every `y`; integrality is the
obstruction.

## Scope and relation to the defect theorem

The
[`exceptional-link defect theorem`](../sequence_covering_sca79_exception_defect/README.md)
quantifies named asymmetry within every exceptional edge under the exact-nine
hypothesis.  The present argument instead couples one exceptional edge to all
seven symmetric outgoing links through the seven named sets `{x,z}`.  It
shows that no allocation of exceptional-edge defect can rescue the branch.

No automorphism hypothesis, solver result, or classification of individual
pair links enters the proof.  The only imported statements are the
unrestricted nine-link lower bound and the exact-nine uniform point-link
reduction cited above.

## Reproduction

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The checker uses Python 3 standard-library exact integers and `Fraction`
arithmetic.  It reconstructs the seven incidence equations from named sets,
checks the point-link count (1), verifies the aggregate divisibility
certificate (3), and independently solves the rational system.
