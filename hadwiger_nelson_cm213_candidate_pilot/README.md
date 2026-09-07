# Capped candidate-discovery pilot in Q(sqrt(-3),sqrt(-71))

**Outcome: no non-four-colourable signal.** All 32 sampled candidates have
508 distinct plane vertices and explicit proper four-colourings. Their
strict unit-distance graphs have 1,217–1,480 edges.

This is a bounded discovery experiment, not a classification of a field,
an infinite lattice, or a complete construction family. No record
improvement is established. The pilot ended at its original 32-query cap;
no larger windows, additional scales, or exhaustive classification followed.

## Exact physical source

Put `omega=(1+i sqrt(3))/2`, `tau=(1+i sqrt(71))/2`, and
`L=Z[omega,tau]`. A vertex label `(a,b,c,d)` means
`z=a+b omega+c tau+d omega*tau` in this physical complex embedding.
For

```
X = 4a+2b+2c+d,  Y = 2b+d,  Z = 2c+d,
A = X^2+213d^2+3Y^2+71Z^2,
B = -2dX+2YZ,
```

the exact coordinates and squared norm are

```
Re(z) = (X-d sqrt(213))/4
Im(z) = (Y sqrt(3)+Z sqrt(71))/4
|z|^2 = (A+B sqrt(213))/16.
```

Distinct integer labels give distinct plane points: equality first forces
`d=0` by irrationality of `sqrt(213)`, then `b=c=0` by irrationality of
`sqrt(71/3)`, and finally `a=0`.

For an observed nonzero squared distance `lambda=(A+B sqrt(213))/16`,
divide every point in the selected window by the **positive real**
`sqrt(lambda)`. Two resulting points have distance one exactly when the
two integer coefficients of their original squared distance equal `(A,B)`.
The verifier checks `A>0` and `A^2>213B^2`, which ensure positivity at both
real embeddings. These are exact algebraic coordinates; no numerical
embedding or distance tolerance is used.

The source follows the finite norm-fibre/window idea in
[Will Sawin, *An explicit lower bound for the unit distance problem*,
Lemmas 2 and 4](https://arxiv.org/html/2605.20579v1).
The specific degree-four field and pilot are our choices. The paper's
high-degree class-field tower and asymptotic density bound are not used
as chromatic evidence. The assigned problem remains the Hadwiger–Nelson
record target; no separate extremal-distance problem is being pursued.

## Frozen sampling protocol

Eight rational centres, with denominator 16, are listed in `CENTRES` in
both scripts. For each centre `h/16`, select the 508 integer labels with
smallest `A(16v-h)`, breaking ties lexicographically on `v`. This is a
trace-norm window in the two complex embeddings.

Enumerate `a,b` from -10 to 10 and `c,d` from -3 to 3. The scripts verify
that no point outside this box can precede the 508th point, using the
dual quadratic-form bounds

```
a^2,b^2 <= (6/71) A(a,b,c,d),
c^2,d^2 <= A(a,b,c,d)/213.
```

Group all pair differences by their exact squared norms. A fibre is
eligible when its observed step vectors span all four rational coordinate
directions. Take the four eligible fibres with most edges, breaking ties
lexicographically on `(A,B)`. The rank filter was fixed after a geometry-only
probe and before the first chromatic query; the 32-query cap was retained.

Each candidate receives one four-colour query, capped at 100,000 CaDiCaL
conflicts. The encoding has one Boolean variable per vertex and colour,
exactly one colour per vertex, and unequal colours on every edge. A
verified triangle is pinned to three distinct colours, which loses no
four-colouring under colour-name permutation. Any UNSAT signal stops the
pilot and requires independent geometry and refutation checking before a
non-four-colourability claim. UNKNOWN at the cap would remain UNKNOWN.

All 32 queries returned SAT. The eight windows selected the same four
squared distances, in varying order:

```
18, (39-sqrt(213))/2, (39+sqrt(213))/2, 20.
```

Every selected candidate had 12 observed oriented step vectors of rational
rank four. The sampling is deliberately biased toward density. Neither
distinct graph isomorphism classes nor a representative sample of all
norm fibres is claimed. No exact lower chromatic number was computed.

## Reproduce and verify

The independent verifier needs only standard-library CPython 3.11.2.
From the repository root:

```sh
python3 hadwiger_nelson_cm213_candidate_pilot/verify.py --certificate hadwiger_nelson_cm213_candidate_pilot/certificate.json
```

It reconstructs all eight windows and every selected edge from the tensor
ring identities `omega^2=omega-1`, `tau^2=tau-18`, with physical conjugation
`omega -> 1-omega`, `tau -> 1-tau`. It imports no producer code or solver.
It checks 1,030,224 pair norms, all 41,452 selected edge occurrences, and
the 32 explicit 508-symbol colour words. One deliberately broken colouring
per candidate is rejected. Small arithmetic controls include a norm with
nonzero `sqrt(213)` coefficient.

To regenerate the discovery run, install `python-sat==1.9.dev15` and run:

```sh
python3 hadwiger_nelson_cm213_candidate_pilot/pilot.py --work /tmp/hn-cm213-pilot
```

This uses `cadical195` (CaDiCaL 1.9.5). Generated point/edge tables, solver
statistics, and any future proof traces belong in the external work
directory. `--generate-only` regenerates the geometry without a SAT
dependency. With generated tables present, add `--work /tmp/hn-cm213-pilot`
to the verifier command for entry-by-entry point and edge comparison.

The published colour words can be checked without trusting the solver.
Solver-generated words and run times may differ across versions; the exact
source selection and independently checked graph definitions determine
the experiment. See [EXPECTED.json](EXPECTED.json) and
[PROVENANCE.json](PROVENANCE.json) for recorded checks and versions.

The whole field and untested norm fibres remain undecided by this pilot.
No new general nonexistence theorem, formalization, or external-review
claim is made. The absence of a positive signal ends this milestone.
