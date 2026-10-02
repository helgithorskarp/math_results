# Independent actual low-energy review

Reviewer six-reviewer-1, independent mathematical reviewer. Read
[REVIEW.md](REVIEW.md) for the full ordinary analytic argument and scope.

Confirms committed9588: actual complex monic degree9, p(1-eta)=0, all
originals in the closed unit disk, 0<eta<=2^-16, H<=30eta and F<=8+3eta
imply all |c1..c8|<(31/4)eta. Critical and original multiplicities retained.

Proves a distinct wider H<=40eta entry on the same interval/objective,
with all coefficients<127eta/16<8eta; c7<7eta and lower six sum<9eta/16.
Original cap8 REVIEW9572 is imported only AFTER entry for F>8+9eta/4
and low-objective H<271eta/10. General first-power and high-energy
coverage remain open. The wider entry does not claim the tighter31/4 cap.

CPython3.12.14 and standard library, no packages. From this directory:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -I -B check.py
python3 -I -B -O check.py
python3 -I -B refine.py
python3 -I -B -O refine.py
```

Initial expected output: PASS; nine complete cyclic rows,24 literal
division-free weight controls, energy profiles30/32; entire record SHA256
`08eb89594e88a723ee0ffc01f76d158733162814653897a7362de18103bf0906`.
Later expected output: PASS; energy profiles36/40 and a literal nondisk
hypothesis control; entire record SHA256
`f9f43a66b3521eaf490fd6167626d29235572f67d800fe51952a96d3864b71bc`.

Both entry points regenerate and compare the entire typed fixture, not
only counts or hashes; explicit guards remain active under -O. A supplied
fixture path is accepted as a single argument for read-only damage checks.
The mathematical argument proves full parameter coverage. The finite
Gaussian unit-point controls do not assert entry hypotheses or prove the
universal positivity argument by enumeration.

The initial sparse formal-complex core and its whole fixture were sealed
BEFORE reading target executable/expected/provenance. The written proof
was visible. The later36/40 scalar layer was developed AFTER author replay
and independent-review overlap, importing only own frozen core. This
phase is explicitly distinguished in independence.json. No author program
is imported by either public entry point. author-replay.json reports later
whole native replay and full change-of-basis coefficient comparison.

All local jobs serial, all native threads1, fixed45/50second guards,
unchanged1CPU2GiB. Positive independent checks take about0.1--0.23seconds;
initial child peak19,236KiB. Ordinary all-index tails, actual-root
positivity, Maclaurin/norm/monotonicity bridges and imported cap8 theorem
remain unformalized. No large omitted certificate or external data is
needed; all seven source/fixture/evidence files accompany this review.
