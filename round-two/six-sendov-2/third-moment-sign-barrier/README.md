# Zero-third-moment sign barrier

Actual author **six-sendov-2**, role **researcher**, 2026-10-03.

For every balanced norm-one real eight-coordinate original-slope profile
with zero third moment and at most three coordinates of either sign,
\(X=\sum u_i^4\ge1/6\). Equality is exactly the normalized3+3+two-zero
orbit. The actual full-eigenspace angular functional satisfies
\(C<144/7\), including all original and critical collisions. Thus higher
angular candidates on this moment locus have exactly four coordinates of
each sign. The fifth moment is not required.

The full ordinary proof and scope are in [PROOF.md](PROOF.md); attribution
and primary status are in [LITERATURE.md](LITERATURE.md). This is an
unformalized, independently unreviewed lemma, not the complex first-power
endpoint or a sharp angular maximum.

Portable exact checks, from this directory:

```sh
python3 -I -B verify.py --self-test
python3 -I -B -O verify.py --self-test
```

Python3.11+ standard library only. All arithmetic is in QQ and QQ[r],
with ascending polynomial coefficients. The checker reconstructs six
complete multiplicity cases, their whole sign certificates, equality
moments and all five full ambient8x8 spectral projectors. It compares
every record, key, scalar type and coefficient with expected.json;
no assertion is needed and optimization cannot disable a check.
The self-test rejects an altered cubic coefficient, equality profile
and projector node. `--fixture PATH` accepts an explicit canonical
fixture for independent damaged-fixture tests. `--emit-record PATH`
bootstraps evidence after all mathematical checks and does not report a
fixture verification.

Optional dense symbolic comparison requires SymPy1.14.0:

```sh
python3 -B compare_cas.py
```

It imports no portable checker code, expands the polynomials with SymPy,
evaluates dense projector polynomials and independently computes the
ambient characteristic polynomial. Its entire record must equal the
same canonical fixture. This supplies arithmetic-method validation by
the same author, not independent review or formalization.

The canonical record is14408 bytes, SHA256
`e663c6bb0d0d6fd74ac5063368f5bb9a16c28f260c6138e450db552c29102c1c`.
Normal and optimized portable checks took0.122s/0.291s; cold-copy checks
took0.120s/0.294s. The dense CAS comparison took1.683s. Core/fixture
children peaked at21196KiB; all children including CAS peaked at53916KiB.
Four external fixture damages (last coefficient, missing case, extra
claim and changed scalar type) were each rejected in both modes. The
three semantic damages were also rejected in both local/cold modes.
Six native numerical thread variables were set to1; all mathematical
children were serial with fixed45-second internal/50-second outer guards,
under the unchanged1CPU/2GiB scope. No large data, private checkpoint,
ledger, credential, or historical incomplete search is distributed.

The finite code certifies the stated algebra and control. Compactness,
constraint regularity, existence of constrained curves, Hessian necessity,
full block-invariant mass count and the universal angular transfer remain
the ordinary proof's trust boundary. There is no exhaustive search over
the sphere.
