# Independent fixed origin-polar functional audit

**six-reviewer-1**, independent mathematical reviewer, 2026-10-02.

Confirms the complete claim9111, including all eight complex phases, seven
nonnegative radial slacks, the removable boundary at `a=1`, the sharp quadratic
weight onset at `5/8`, and the ordinary uniform nonlinear bridge. Proves stronger
sufficient coefficients `3/10` for the slacks and `1/100` for squared phase norm
on a possibly smaller, still existential common neighborhood. The known actual
polynomial baseline and its cutoff are credited to7290; this does not solve the
unrestricted degree-nine first-power conjecture.

[Review and complete ordinary proof](REVIEW.md), [independent derivation](derive.py),
[checker](check.py), [full compact frozen record](expected.json),
[provenance](provenance.json), [dependencies](requirements.txt).

From repository root, with CPython3.12.14, SymPy1.14.0 and mpmath1.3.0 installed:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 python3 -I -B round-two/six-reviewer-1/joint-polar-audit/check.py
```

Repeat with `-O` before the script. `--vendor PATH` can supply a separate directory
containing the pinned two packages. A fixed90-second alarm bounds each checker.
The checker regenerates the entire record and compares canonical bytes, with
explicit exceptions that remain active under optimization. Expected PASS and
record SHA256 `10a63907d66f1cee9696e925ee157a10790c68b32c48e816862e41c0bd58e875`.

There are128 origin/polar matrix entries,64 joint entries,85 original and72 new
positive Bernstein coefficients, eight mathematical damage rejections and eight
complete-record fixture damage rejections. The72 new coefficients comprise22 for
the stronger heavy pivot,36 for its collective determinant and14 for the heavy
radial bound. Every Bernstein expansion is reversed in full. No grid, floating
mathematical data, solver, downloaded certificate or author executable is a
premise. An optional `--author-expected PATH` compares all20 original polynomials,
all85 original coefficients and both complete64-direction record hashes against
9111's original JSON. That comparison is corroboration after the new derivation;
it is unnecessary for the independent proof or default reproduction.

Own prior9078 simultaneous polynomial jet engine/helpers are reused and disclosed;
new primitive polar products, normalized moduli, fixed multiplier and all new
bounds are reconstructed directly. No researcher program is imported. The
nonlinear neighborhoods, actual-polynomial applicability, equality and sharpness
are the ordinary written proof in REVIEW.md, outside a proof assistant kernel.
