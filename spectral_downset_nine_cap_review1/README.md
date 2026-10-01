# Order-nine capped H: independent review and a stronger signed bound

Actual agent **six-reviewer-1**, independent mathematical reviewer. The dual
vector/matrix originate with six-downset-3's committed claim 8354; this package
provides a separate exact audit and a new strict uniform surplus of 17.

For real symmetric normalized supported H matrices on subsets of [9] of size at
most seven, additionally assume `0 <= 255M+247I <= 502I` in PSD order. The
original ordered signed-sum bound is confirmed and improved from
`6693928918269/25371875000` to **`7125250793269/25371875000`**, strictly. Its
coefficients are unchanged. The complement-plus-disjoint-two-set architecture
is excluded for arbitrary individual signed entries. The best extra surplus in
the necessary six-dimensional PSD pair is strictly between 17 and 18.

[REVIEW.md](REVIEW.md) supplies the exact scope, written real proof, independent
methodology, strengthening and improvement opportunities, primary literature
and limitations. Positive cap constructions at orders 6/7/8 are outside this
fresh review. General H/I and unrestricted capped feasibility at nine are not
settled. The proof is ordinary mathematics with exact checked arithmetic,
**unformalized**.

Use Python 3.10+ standard library only, executed on CPython 3.11.2. From this
directory:

```bash
python3 verify.py --output /tmp/order9-independent.json
cmp RESULTS.json /tmp/order9-independent.json
python3 -O verify.py --output /tmp/order9-independent-O.json
cmp RESULTS.json /tmp/order9-independent-O.json
sha256sum -c SHA256SUMS
```

The standalone verifier imports no author code and uses permutation determinants
and cofactor inverses. It reconstructs the shift certificates from exact inputs,
checks all 7,071 middle disjoint edges, 624 individual cancellations, all layer
and full affine identities, twelve corrupt inputs and six determinant controls.
No optimization or floating-point premise is used. The full synthetic matrix is
an affine identity control with negative dual functional, not a PSD witness.

Files: `CERTIFICATE.json` contains the credited input dual and the independent
compact shifted-PD certificate; `RESULTS.json` records deterministic exact
output; `verify.py` checks it; `REVIEW.md` proves the real bridges. No private
ledger, key, controller checkpoint, search dump or large corpus is required.
The original unmodified verifier was separately replayed byte-identically,
normally and with `-O`; that is reproducibility evidence separate from the
independent method.

Expected RESULTS SHA256: `1865f8fcbaac5a02bbb1e9e08b2e3729053b8f3cefc1d37bf3e60ef61b5d0b53`.
Certificate SHA256: `6b7f08d9d99663e7ee8c3e2f5de3ca0c46e973edc3e793cdf7279166cbdff06b`.
