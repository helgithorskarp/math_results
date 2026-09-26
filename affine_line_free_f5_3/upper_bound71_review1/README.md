# Independent review of the 72-point exclusion in AG(3,5)

This directory records an independent review of the computer-assisted theorem
in [`upper_bound71`](../upper_bound71/) at exact source commit
`e81f511a02ac5ef43f1005408ba370df110b7007`.

**Verdict:** accept with high confidence the scoped theorem that no 72-point
subset of \(\mathbb F_5^3\) is line-free. Together with the published
70-point construction this proves

\[
70\le r_5(\mathbb F_5^3)\le71.
\]

It does **not** determine the exact value: existence of a 71-point line-free
set remains open. The proof audit and precise trust boundary are in
[`REVIEW.md`](REVIEW.md).

A separate accepting review, published at repository commit
`5265b38b915aeb6701f42f8dbfa8699366b60609`, landed while this full replay
was running. It replays the submitted selected-point formulas in full. This
package is retained as strengthened independent evidence because every SAT
instance instead uses complemented hole variables and a different gauge; it
closes a distinct encoding-and-search trust boundary and is not presented as
the first accepting review.

## Independent method

[`independent_check.py`](independent_check.py) imports none of the reviewed
Python or C++ modules. It:

1. rebuilds the exact low-plane dual inequality that forces at least five
   plane sections of size eight or nine;
2. enumerates all AA, AB and BB quotient matrices as multisets of deficit
   units, recovering 4,442, 5,428 and 6,322 matrices and the published hash;
3. calls [`full_affine_check.cpp`](full_affine_check.cpp), which applies all
   12,000 elements of \(\operatorname{AGL}(2,5)\) to every published
   representative and verifies a disjoint 4,332-orbit cover of all 16,192
   typed matrices; and
4. builds 4,332 fresh formulas with complemented hole variables, reversed
   line order, and the last available noncollinear gauge triple. DRAT-trim
   verifies every UNSAT proof.

The independent traces total 523,609,215 bytes and are temporary outputs, not
repository artifacts. The native structural checker also passed an
address/undefined-behavior sanitizer build.

## Reproduce

The review used Python 3.12.14, `python-sat==1.9.dev15`, GCC 12.2.0, and
DRAT-trim built at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, with executable SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
Install [`requirements.txt`](requirements.txt), build that checker, and run:

```sh
python3 independent_check.py \
  --out /tmp/upper-bound71-independent \
  --drat-trim /path/to/drat-trim \
  | cmp - EXPECTED.json
```

The output directory retains only compact structural inputs and `result.json`
by default. Add `--keep-proofs` to retain generated CNFs and traces. The full
review run took about 22 minutes, including the affine audit. A structural-only
sanitizer replay is available with `--structure-only --sanitize`.

Verify the compact evidence with:

```sh
sha256sum -c SHA256SUMS
```
