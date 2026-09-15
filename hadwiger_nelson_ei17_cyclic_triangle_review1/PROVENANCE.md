# Provenance and source integrity

## Reviewed target

The target mathematical revision is
`abadf3d5f33005152f588fe0a2e2a52cf0d204eb`:

<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ei17_cyclic_triangle_full_input_stop>

Pinned target hashes:

- `verify.py`: `23dada3c84cf5574b5c78965d0f1df333bed1a67f3ea0c61ca407631070d74bc`
- `controls.py`: `a177fcafd4027a9aa8bcce230af7b490b6cb072f4f283aeafa0a892086dac9c8`
- `EXPECTED.json`: `7f767c0b83c1d8ff4ba9be13749b1486c60bf8e473e00c85c30c7c3c70442b30`

## EI17 dependency

The exact source package entered at
`9724508c76581b2283bbe65e02be77433a0146a4`.  This review directly pins and
parses:

- `seed_edges.json`:
  `b77a3a242467f2c1ed3f047914492e70a0da9cbe6ca8234941c8dd008e25e450`
- `seed_midpoint.json`:
  `fb712ad09168fa51814556641f31280acc8ad1e71a17a9878d1cfd55eeb96565`

It independently proves the root, faithful graph, and chromatic facts needed
by the cyclic theorem rather than importing the source checker.

The midpoint data are attributed to Silva Filho,
<https://arxiv.org/html/2607.19995>.  The primary page identifies the
triangle-free Exoo--Ismailescu EI17 graph, gives a 31-edge list, and includes
the displayed midpoint precision used by the package.  The review does not
import that paper's coordinate-field claims: its only geometric premise is the
independently certified local root.

## Record sources

- Parts, <https://arxiv.org/abs/2010.12665>.
- Haugland, <https://arxiv.org/abs/2608.04542>.

Both pages and the two GitHub branch links resolved successfully during the
review.  The stale Discovery ledger is not used to establish publication
priority or the record statement.
