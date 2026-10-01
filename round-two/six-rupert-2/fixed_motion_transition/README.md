# Exact J74 fixed-motion support transition

**six-rupert-2, researcher; 2026-10-01.** A new intermediate theorem for
original unit-edge J74; author-checked, unformalized and independently
unreviewed. Global Rupert status remains **OPEN**.

On the entire prior receiving patch
`u=m+t*d+s*(m cross d)`, `3/5<=t<=7/10`, `|s|<=1/50000`, the fixed
proper motion `Q0=M_m Hy` and its three proper companions have unit closed
fits exactly on

    t <= (sqrt5-1)/2 + ((sqrt5-3)/4)*s.

Within relative Cayley norm `1/14400` of any of these four centers,
**every** closed fit with scale at least one and arbitrary physical
translation is that center at scale one and zero translation, and is
feasible only on the stated side. Original source39 against receiving
edge17--32 gives the event. All60 originals and all18 receiving edges
are checked. These source neighborhoods are uniformly separated from
the four prior neighborhoods. This is conditional source coverage.

Any continuous path of scale-at-least-one closed fits staying in this
receiving patch and starting at one new center stays on that same family;
it cannot cross the event into an infeasible region or a strict passage.
The [complete proof](PROOF.md) gives the exact quantifiers, arbitrary
translation chart, nonlinear closure and connectedness argument.

From the repository root, Python3.11+ standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-2/fixed_motion_transition/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O round-two/six-rupert-2/fixed_motion_transition/check.py
```

Both compare every field of [expected.json](expected.json), including4320
exact source-support signs, literal original contact images, properness,
two full quadratic Bernstein separation bounds and eight damaged controls.
The [small certificate](certificate.json) supplies witnesses, not a proof
corpus. Seven direct inputs are hash-pinned in [DEPENDENCIES.json](DEPENDENCIES.json);
the complete parent patch and arc records, including their controls,
are replayed. See [validation evidence](VALIDATION.md).

No private search, numerical solver, network, ledger, credential or omitted
large artifact is needed. The exact Fraction/Q(sqrt5) arithmetic and the
written continuum reasoning remain the trust boundary. The new frontier
is a changed receiving horizon or source motions outside these families.
