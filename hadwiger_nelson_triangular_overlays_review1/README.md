# Independent review of two triangular-lattice overlays

This directory records an independent review of contribution
`bafkreihgxz4xvtbbztmx5cswx7ur3kkk43zm2hxbczm4ibzlbk24yfv7mi`, source
commit `dd26ed334c602a5814c31e01a98bdbc5e881ba1b`.  The reviewed contribution
proves that the strict unit-distance graph on the union of any two unit
triangular lattices sharing a vertex is four-colourable, gives a sharp
four-chromatic angle, and tabulates every exceptional rotation of the
radius-67 patch (253 vertices per copy, at most 505 after identifying the
common origin).  This is a structural theorem and a finite census, not a
sub-509 five-chromatic construction.

## Verdict

Accepted.  I re-derived the algebraic proof, replayed the submitted exact
producer/verifier from a clean directory, exercised its negative controls,
and wrote the independent checker here.  The independent checker does not
import any submitted code or catalog.  It reproduces the 253/702 patch, all
1,542 primitive contact lines, 624 nonsquare-discriminant lines, 498 rational
rotations, 1,746 exceptional rotations, the complete graph census, and the
1,350/396 split between chromatic numbers 3 and 4.

## Proof audit

Write `R=Z[omega]`, where `omega=(1+i sqrt(3))/2`, and define
`rho(a+b omega)=a-b (mod 3)`.  Since
`N(z)=rho(z)^2 (mod 3)`, every unit edge inside one lattice changes `rho`.

If the rotation `alpha` belongs to `Q(sqrt(-3))`, write it primitively as an
Eisenstein numerator divided by an integer `d`.  The norm equation shows
`3` cannot divide `d`: reducing modulo 3 first forces the two numerator
coefficients to agree, and reducing the resulting equation modulo 9 then
forces both and `d` to be divisible by 3.  Thus `rho` extends over `R[1/d]`
and gives a consistent proper three-colouring of both copies.

Now suppose `alpha` is outside that quadratic field and put
`ell(t)=alpha*t+conjugate(alpha*t)`.  The rational subspace
`W={t in Q(sqrt(-3)): ell(t) in Q}` has dimension at most one; otherwise
evaluating on `1` and `omega` recovers both Cartesian coefficients of
`alpha` as rational.  Hence `R intersect W=Z gamma` for a primitive `gamma`.
Every cross contact `z--alpha*w` satisfies

    ell(w*conjugate(z)) = N(z)+N(w)-1.

Writing `ell(gamma)=p/q` in lowest terms and
`w*conjugate(z)=m gamma`, reduction modulo 3 shows that whenever both
endpoint residues are nonzero their product has one fixed sign.  This gives
the submitted four-colouring: use one colour on residue zero in the first
copy, a second colour on residue zero in the second copy, and swap the two
nonzero residue colours according to that fixed sign.  The common origin is
assigned the first zero colour.  If there is no zero-to-zero cross contact,
the two zero colours merge and the graph is three-colourable.

The patch has a triangle whose palette forces the other 250 vertices, so its
three-colouring is unique up to permutation.  Consequently a zero-to-zero
cross contact makes an irrational overlay four-chromatic.  At Moser's angle
`alpha=(5+i sqrt(11))/6`, the vector `z=w=1+omega` has residue zero and norm
3, while `|1-alpha|^2=1/3`; this supplies such a unit contact and proves the
four-colour bound is sharp.

For the finite census, use Cartesian coordinates
`z=(X+i sqrt(3)Y)/2`.  A nonzero ordered pair `(z,w)` gives the rational line

    (2A+B)x - 3B y = N(z)+N(w)-1,

where `w*conjugate(z)=A+B omega` and
`alpha=x+i sqrt(3)y`.  Its intersection discriminant with
`x^2+3y^2=1` is `3u^2+v^2-3k^2`.  A nonsquare positive discriminant gives
two irrational roots.  Two distinct rational lines cannot share an
irrational root, because that would make both Cartesian coordinates of the
root rational.  Rational roots and the separate equal-norm coincidence
rotations exhaust all exceptional events.  The checker constructs every
rational union graph over a common integer denominator; for irrational roots
it counts the contact pairs attached to the unique line and applies the
proved residue criterion.

## Reproduction

From this directory:

```bash
python3 -B independent_check.py
```

The review run used CPython 3 with no third-party packages.  It emitted
`"verified": true` and reproduced the claimed aggregate counts.  Separately,
the submitted commands were run from a fresh scratch directory:

```bash
python3 -B produce.py --work /scratch/research-team-v2/tmp/reviewer-1/triangular-overlays-run
python3 -B verify.py --work /scratch/research-team-v2/tmp/reviewer-1/triangular-overlays-run
python3 -O -B verify.py --work /scratch/research-team-v2/tmp/reviewer-1/triangular-overlays-run
python3 -B controls.py --work /scratch/research-team-v2/tmp/reviewer-1/triangular-overlays-run
```

Both verifier modes performed 71,818,098 exact Cartesian norm evaluations
and reproduced catalog SHA-256
`92b06d19628c1da21472875ee22103888cdd01af4655258fb20e98219324a66b`.
The control suite rejected all 18 corruptions and exhaustively confirmed that
the seven-vertex Moser benchmark has no proper three-colouring and 384 proper
four-colourings.

## Trust boundary

The general all-rotation result is justified by the algebraic argument above,
not by finite sampling.  The exact census still trusts the CPython integer
and rational arithmetic implementation, OS/process execution, and this
reviewer's transcription of the definitions.  The clean replay additionally
trusts the submitted source commit and its SHA-256 manifest.  No SAT solver,
floating-point geometry, external database, or unpublished witness was used.
