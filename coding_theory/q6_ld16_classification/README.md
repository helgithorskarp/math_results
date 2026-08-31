# Unique optimum locating-dominating code in the binary 6-cube

## Result

Up to the full automorphism group of the binary hypercube,

\[
\operatorname{Aut}(Q_6)\cong \mathbb F_2^6\rtimes S_6,
\]

there is exactly one locating-dominating code of cardinality 16 in `Q_6`.
Consequently there are exactly 1,440 labelled optimum codes.  This unique
orbit has size 1,440 and its stabilizer has order 32.

Together with the Honkala--Laihonen--Ranto lower bound and the independently
checked 16-word construction in the sibling directory
`../q6_locating_dominating_16`, this classifies every optimum code because
`gamma^LD(Q_6) = 16`.

A canonical representative of the unique orbit is

```text
000000 000011 000101 001010 010100 011011 011101 011110
100110 101001 101100 101111 110001 110010 110111 111000
```

The reference representative used by the program has 48 non-codeword
signatures, distributed as 16 signatures of each cardinality 1, 2, and 3.
The uniqueness result turns two further checks into classification-wide
corollaries: every optimum code is an independent set, and its unordered
codeword-pair distance distribution is

\[
(A_2,A_3,A_4,A_5)=(32,48,24,16),
\]

with no pairs at distances 1 or 6.

## Exhaustive encoding

There is one Boolean variable `x_v` per vertex.  Domination is encoded by

\[
\bigvee_{w\in N[v]}x_w
\]

for every vertex `v`.  For every unordered pair `u,v`, location-domination is
encoded by

\[
x_u\lor x_v\lor
\bigvee_{w\in N[u]\mathbin\triangle N[v]}x_w.
\]

When `u` and `v` are both outside the code, this is exactly the requirement
that their signatures differ.  An exact-cardinality totalizer requires 16
codewords.  Requiring `000000` to be a codeword is lossless by vertex
transitivity.

The program enumerates all 1,440 images of a verified reference code under
the 46,080 automorphisms.  Exactly 360 distinct images contain `000000`; one
blocking clause is added for each.  The residual CNF is unsatisfiable, so no
second automorphism orbit exists.  The orbit--stabilizer theorem gives
`46080 / 1440 = 32`.

## Reproduce

Direct construction verification needs only Python 3.11 or later:

```bash
python3 classify_q6_ld16.py
```

For the exhaustive classification, install the pinned PySAT release into a
scratch virtual environment and run both bundled solver backends:

```bash
python3 -m venv /scratch/q6-ld16-venv
/scratch/q6-ld16-venv/bin/pip install -r requirements.txt
/scratch/q6-ld16-venv/bin/python classify_q6_ld16.py \
  --classify \
  --solvers cadical195 glucose42 \
  --write-cnf /scratch/q6-ld16-classification.cnf
sha256sum /scratch/q6-ld16-classification.cnf
```

The deterministic CNF has 832 variables and 7,243 clauses.  Its expected
SHA-256 is
`8a25d316b5063af1fef6e2265bfab48268c847a36b0258c5d8254d1c2cc7462c`.
The two backends independently return `UNSAT`.

## Trust boundary and novelty

The construction is checked by direct enumeration, without a solver.  The
classification is a finite computational result relying on (1) the stated CNF
encoding, (2) complete enumeration of the affine-coordinate automorphism
group, and (3) the correctness of the CaDiCaL 1.9.5 and Glucose 4.2 backends
bundled with PySAT 1.9.dev15.  No formal proof assistant checked these bridges.

Junnila, Laihonen, and Lehtila reported the best-known interval `16--18` for
`Q_6` in 2021.  Searches through August 2026 found no published resolution or
isomorphism classification.  The exact construction was independently found
by another Discovery Net researcher during this run; this directory records
the apparently new exhaustive uniqueness refinement, not priority for the
exact value alone.

## Sources

- I. Honkala, T. Laihonen, and S. Ranto, "On Locating-Dominating Codes in
  Binary Hamming Spaces," *DMTCS* 6(2), 2004, 265--282.
  https://doi.org/10.46298/dmtcs.322
- V. Junnila, T. Laihonen, and T. Lehtila, "Improved Lower Bound for
  Locating-Dominating Codes in Binary Hamming Spaces," *Designs, Codes and
  Cryptography* 90 (2022), 67--85.
  https://doi.org/10.1007/s10623-021-00963-8
