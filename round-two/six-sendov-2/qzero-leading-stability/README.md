# Leading-vector regularity at zero cubic moment

Actual **six-sendov-2**, **researcher**. An author-checked ordinary lemma
with a portable rational certificate; unformalized and independently
unreviewed. See [PROOF.md](PROOF.md) for definitions and the whole claim.

The exact module identity proves that the angular stationary pencil's
four E-leading coefficients never vanish simultaneously at q=0,u!=0,
even away from stationary solutions. It also supplies explicit lower
bounds for their complex norm on bounded coefficient sets and a finite
q-neighborhood, plus bounds for all scalar-E secants and derivatives.
A single complex recovery formula `E=-sum(L_i*beta_i)/(u*(1+q*Z))`
also covers every individual zero-leading branch in the certified domain;
all four cleared linear rows and the remaining R0 equation are retained.
This is a strengthening on a precise slice of the previously conditional
[9743](../critical-coefficient-recovery/PROOF.md) regularity result.

From the repository root, using Python 3.12 and only its standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/qzero-leading-stability/verify.py
```

Repeat with `-O` to check that validation remains active under optimization.
The same-author pinned 9743 source and its existing parents must be present
in their repository directories. Every input fixture is regenerated and
compared as a whole typed record. No downloads, CAS, numerical roots,
sampling, floating point or solver soundness are needed for this command.

Expected complete certificate SHA-256:
`890e776a165519a176e8f7fd1cf55e42d314a1c4e40ba8490d920916d8ea454f`.
Output records 15 whole polynomial identities, the complete21-by26 system,
L degrees4/3/5/4 and term counts13/8/19/12, and all35 coefficients of the
degree6 relative q defect. Deliberate coefficient damage controls are exact.

For M,U>=1 and |r|,|x|<=M:

- At q=0, `||alpha|| >= |u|/(400000*M^5)`, without an upper bound on |u|.
- For `0<|u|<=U` and `|q|<=1/(2000000*M^5*U)`,
  `||alpha|| >= |u|/(800000*M^5)`.

The five full scalar equations, simple real critical roots and strict
mass feasibility remain required for an original stationary profile.
The result proves no profile existence, full Jacobian rank, collision
extension, sharp global basin, or degree-nine first-power endpoint.
The existing independent review of the input does not review this lemma.
