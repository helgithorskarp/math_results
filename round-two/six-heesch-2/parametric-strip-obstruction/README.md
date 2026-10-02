# A conditional upper bound for the polyhex strip T_k

six-heesch-2, researcher. Author checked, unformalized and independently
unreviewed. No historical priority or new Heesch record is claimed.

For every integer k >= 6, this package defines an explicit 32-pose atlas
A2(k). It proves the following conditional statement:

> If the theoretical depth-two contact domain E2(T_k) is contained in A2(k),
> then Hc(T_k) <= Hh(T_k) <= 3, and T_k does not tile the plane.

**The inclusion E2(T_k) subset A2(k) is not proved for all k.** The package
proves two geometric obstructions for the literal atlas, for every k >= 6.
The remaining task is to establish or refute that domain inclusion. The
finite-five unmarked-polyhex target remains open.

The [proof](proof.md) gives the shape, atlas, definitions, all-length reduction
and conditional implication. The [column lemma](STRIP_COLUMN_LEMMA.md) explains
the exact interval geometry. The input [atlas.json](strip-parametric/atlas.json)
is an explicit definition, with no external private input.

Run from a checkout of this repository using Python 3.10 or later:

```sh
python3 round-two/six-heesch-2/parametric-strip-obstruction/verify.py
```

Tested with Python 3.11.2. Only the standard library and the existing published
geometry module [strip-t5/exact.py](../strip-t5/exact.py) are needed. Its expected
SHA256 is `265366ae7cc1e5b5ed60bc96075a32e5d56ac62e52da92080ab8752cdbf9285c`.
The runner builds compact certificates and then runs both search-free readers,
in normal and optimized Python, serially. Generated files are ignored. Expected
results and source hashes are in [expected.json](expected.json).

The root obstruction has 30 poses, seven demanded cells, 135 atomic predicates,
breakpoints 6,7,8, and a seven-node rejection. The pair obstruction has a
32-pose domain, 58 affine candidates, eight demanded cells, 181 atomic predicates,
breakpoints 6,7,8,9,10, and an eight-node rejection. Period is one in both cases.
Each reader rejects three damaged certificates. Reader evidence agrees under
normal/-O. No SAT solver, floating-point arithmetic, large proof corpus or
private closure file is required.

Trust boundary: the readers share the small symbolic geometry module. They
independently derive the breakpoint partition and check every certificate branch;
each representative is also audited with materialized axial-cell geometry.
The ordinary proof explains why the finite representatives cover every integer
k >= 6. This is not a proof-assistant formalization or an independent review.

The all-motion conditional implication uses the published
[hexagonal registration and pair-depth argument](../proof.md), graph8585,
sourcecf3b672f2bf53a076c057b44a6f1a087ef028fcd. The definitions of E_r and the
necessary-domain method are also detailed in [the T5 proof](../strip-t5/proof.md),
graph9051/sourcea5052d63996131ca4eaceb22c1293a6fd4f9a056. No square motion bridge
or private result about a different strip is imported.

Primary problem literature: [Kaplan 2022](https://arxiv.org/abs/2105.09438) and
[the polyform census](https://cs.uwaterloo.ca/~csk/heesch/). Their published
four-corona polyhex examples remain prior art.
