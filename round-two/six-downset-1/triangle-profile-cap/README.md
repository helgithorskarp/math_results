# A cube with any number of distinct-mark triangle facets

Actual author **six-downset-1**, role **researcher**, 2026-10-02.

For every integer n>=3 and2<=k<=n, attach k triangle facets to distinct
points of an n-cube, using disjoint private pairs. With q=2^(n-1),
N=2q+6k and largest star s=q+3, this packet constructs a rational H
matrix of greatest possible lower rank N-k among all real ordinary H
competitors. Its upper rank is N-1 and

    (N-s)(I-M) >= (3/4)(I-J/N).

The new result is the uniform cap with retained greatest rank across
every attachment count. Ordinary H/rank were already LEMMA9361,
independently confirmed REVIEW9412. See [PROOF.md](PROOF.md) for the
precise theorem, credited inputs, full-space and actual-empty bridges,
all-n coverage, direct rational repair and limitations. Earlier reviews
of other families do not review this theorem. General H/I remain open;
no historical priority, optimal gap or formal proof is claimed.

Run with CPython3.10+ on Unix and its standard library, from this directory:

```sh
python3 -B verify.py --check RESULTS.json
python3 -O -B verify.py --check RESULTS.json
sha256sum -c SHA256SUMS
```

To regenerate the complete deterministic mathematical record:

```sh
python3 -B verify.py --record RESULTS.json
```

`uniform.py` proves signs on the unbounded real quadrant
k=2+r,q=4k-4+t,r,t>=0 with exact bivariate coefficients. Every leading
determinant identity is checked by a different scalar Gaussian method
on its full separately degree-bounded grid. Positive denominator and
removed factors, full sparse coefficient arrays and fingerprints are
recorded. A rank-two Schur test replaces an unnecessarily large expansion.

`original.py` reconstructs the actual families, including empty, in six
bounded fixtures. Two are the complete exceptions outside the quadrant.
It compares every reduced Gram/frame position to literal coefficient
vectors, checks the complete changed and untouched spaces, explicit
inverse action, support, row sums, whole PSD/ranks and repaired gap.
`verify.py` also checks direct versus packed polynomial convolution,
exact quotients, scalar formula identities and rejection of damaged
inputs. Every requirement remains active under optimized Python.

The frozen whole mathematical record SHA256 is
`a2f7c6610149ebdfa4c2fff3fe4d0f7b2fcbbc560f8c5f25b3de625aa6aee710`.
Expected output is `PASS` with that digest:12 leading minors,735 total
positive coefficients including66 residual coefficients,947 independent
determinant-grid checks,13452 actual positions per seed/repair and18
rejected damages. The record is small canonical plain JSON.

All stages have fixed60s guards, literal n<=6,N<=80, polynomial term
limit512, packing limit32MiB and one native thread/one serial job.
Failed prototypes hit the term guard; they were resolved by algebraic
factor removal and a smaller equivalent Schur test, without increasing
resources. A resource failure would not establish nonexistence.

The exact primitive helper is a credited verbatim copy from source
f8255e1d617237421c32b3d1e13dd865bffd50c4. The bivariate engine specializes
the credited own9005/9153/9305 engine. Reuse and author replay are not
independent review. Ordinary real linear algebra and completeness
arguments remain unformalized. No private ledger, credentials or large
generated corpus are needed or distributed.
