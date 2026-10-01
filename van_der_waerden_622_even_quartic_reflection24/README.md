# A24-AP reflection certificate for even quartics over F311

Author: **six-vdw-1**, role **researcher**.

For every P(x)=alpha*((x-v)^4+A*(x-v)^2+B), alpha!=0, define phi to be1 on
nonzero square values and0 on nonsquares; each root bit is independently
arbitrary. The parity lift c(t+1)=(t mod2) XOR phi(t mod311) has24 root-free
monochromatic seven-term APs with pairwise disjoint field supports in[1,2171].
Any AP-free repair within this period622 template therefore changes at least
**24 nonroot field bits**, hence **264 nonroot coordinates on[1,3704]**.
An unrestricted AP-free word has only the stated24-coordinate consequence.

This strengthens the [same-family20/220 result](../van_der_waerden_622_even_quartic_character_repair).
It supplies no new W(2,7) bound or3704-point coloring. General quartics with a
nonzero linear coefficient after cubic cancellation are outside its scope.
The finite-field reduction and repair proof are in [PROOF.md](PROOF.md).

## Check the supplied certificate

The independent checker needs only Python3.11+ and its standard library:

```sh
python3 check_reflection622_packings.py --scope all --certificate packings.json --output /tmp/quartic24-check.json
python3 -O check_reflection622_packings.py --scope all --certificate packings.json --output /tmp/quartic24-check-O.json
```

Each check verifies625 canonical cases,15,000 APs and105,000 actual term colors.
The compact179,102-byte certificate has SHA256
`74c7fc5307762c76b5f11001cdd1d876edb1b68ae47bac6a30ac8f44a83cce88`.
The checker imports no generator or solver and checks both APs explicitly.

## Regenerate from source

Run from this directory. Use a fresh output directory outside the repository:

```sh
python3 -m venv /tmp/quartic24-venv
/tmp/quartic24-venv/bin/python -m pip install -r requirements.txt
/tmp/quartic24-venv/bin/python reproduce.py --output-dir /tmp/quartic24-reproduction
```

The native proposal dependency is pinned to python-sat1.8.dev24. Reproduction
starts with no private seeds or numerical proof corpus. It constructs the
12-case pilot, then all625 cases, requiring the regenerated certificate to
match the supplied bytes. Greedy pairing is followed by at most one capped
SAT matching query for each missing case. All positive native witnesses get
separate actual-term checks. Both cohorts run22 mathematical corruption
controls in normal and optimized Python, and all arithmetic reduction audits
are rerun. The complete sequence has1,044 serial child jobs.

Every child is guarded at30 seconds and200,000 declared cases; solver, BLAS
and OpenMP threads are one. The native query requests9,500 conflicts within a
10,000 bound. UNKNOWN, unchecked UNSAT, timeout or an over-cap model stops
without a mathematical exclusion. Generated CNFs, assignments and journals
stay in the chosen output directory. Completed stages with identical pins
can be reused with explicit `--resume`; incomplete or failed stages cannot
be silently retried. [VALIDATION.md](VALIDATION.md), [expected.json](expected.json)
and [evidence.json](evidence.json) record the checked outcome and its limits.

The independent proof input is the complete compact AP certificate plus the
written625-case coverage and transport argument. This is independent code
by the same researcher, without external review or formalization.
