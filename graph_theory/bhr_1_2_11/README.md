# A growable-realization certificate for BHR support `{1,2,11}`

## Result

Let

\[
L=\{1^a,2^b,11^c\},\qquad a,b,c\geq 1,
\quad v=a+b+c+1.
\]

If `L` satisfies the necessary divisor condition in the Buratti--Horak--Rosa
(BHR) conjecture, then `L` is the multiset of cyclic edge lengths of a
Hamiltonian path on `Z_v`.  Thus the BHR conjecture holds for the underlying
set `{1,2,11}`.

This closes the sole possible exception in Theorem 1.3 of Chand and Ollis,
[The Buratti--Horak--Rosa Conjecture Holds for Some Underlying Sets of Size
Three](https://arxiv.org/abs/2202.07733).  Novelty is calibrated to the sources
searched through September 3, 2026; no priority claim is made.

## Finite proof reduction

The cyclic length of `{r,s}` in `K_v` is
`min(|r-s|, v-|r-s|)`.  For this support the divisor condition simplifies
exactly to

1. `v >= 22`; and
2. if `11` divides `v`, then `a+b >= 10`.

Indeed, only divisors `2` and `11` can divide a member of the support.  The
condition for `2` is automatic because `a,c >= 1`, and the condition for `11`
is `c <= v-11`, equivalently `a+b >= 10`.

An `X`-growable realization with count vector `p=(a,b,c)` realizes every count
vector `q` such that, for each `x` in `X`, `q_x >= p_x` and
`q_x = p_x (mod x)`, while coordinates outside `X` stay equal to those of
`p`.  This is precisely the iteration of the growable-realization construction
in Theorem 2.1 of the paper above (also developed in
[Growable Realizations: a Powerful Approach to the BHR
Conjecture](https://arxiv.org/abs/2105.00980)).

There are 22 positive residue classes:

\[
a\equiv1\pmod 1,\quad b\equiv b_0\pmod2\ (b_0\in\{1,2\}),
\quad c\equiv c_0\pmod {11}\ (1\leq c_0\leq11).
\]

`certificate.json` contains 628 growable base paths covering all 22 classes;
the largest path has order 33.  Each record gives its count vector, path,
growable coordinates, and a valid growth position for each such coordinate.

The infinite coverage check is finite.  In one residue class, let `M_i` be the
largest certificate coordinate on axis `i`.  Clamp an arbitrary target
coordinate to the sentinel `M_i+i` whenever it exceeds `M_i`.  A certificate
record covers the target if and only if it covers the clamped vector: a
growable coordinate only tests a lower bound, while a non-growable coordinate
tests equality to a value at most `M_i`.  The verifier enumerates all such
clamped vectors and checks every pattern admitting an admissible lift.  There
are 9,544 of them.

## Verification

The checker uses only the Python 3 standard library:

```bash
python3 verify.py certificate.json
python3 -m unittest -v test_verify.py
```

Expected verifier output is in `expected.txt`.  It checks, from definitions:

- all 22 residue classes occur exactly once;
- every path is a permutation of `0,...,v-1` with exactly the claimed cyclic
  edge-length multiset;
- every growth position satisfies the stretched-edge incidence definition;
- one explicit application of each claimed growth operation gives the correct
  enlarged realization; and
- the 628 records cover every admissible symbolic boundary pattern.

To regenerate the certificate with the deterministic one-worker CP-SAT model:

```bash
python3 -m venv /scratch/bhr-1-2-11-venv
/scratch/bhr-1-2-11-venv/bin/pip install -r requirements.txt
/scratch/bhr-1-2-11-venv/bin/python generate.py \
  --output /scratch/bhr-1-2-11-certificate.json
python3 verify.py /scratch/bhr-1-2-11-certificate.json
cmp certificate.json /scratch/bhr-1-2-11-certificate.json
```

The reference run used CPython 3.11.2 and OR-Tools 9.14.6206.  Generation took
about two minutes on one CPU core.  Verification takes less than one second.

## Trust boundary

The CP-SAT solver is only a witness generator; no solver claim is trusted by
the theorem checker.  The finite evidence relies on CPython executing
`verify.py` correctly.  The bridge from the checked base paths to the infinite
families is the published growable-realization lemma and the elementary
clamping argument above; it is not proof-assistant formalized.  No search logs
or solver traces are required or included.
