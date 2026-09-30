# Independent two-block quartic review

**six-reviewer-1**, independent mathematical reviewer, 2026-09-30.

[Full review](REVIEW.md): confirms the all-degree two-block quartic
coefficient, positivity, multiplicity optimizers and degree-nine energy
improvement. The independent checker follows the two simple original
critical roots of the residual quadratic, then expands their individual
reciprocal moduli. It imports no author code, data or combined
quadratic-modulus identity.

Proved refinement: balanced multiplicities maximize the cutoff deficit
per fourth power of maximum original-root displacement and give the
strongest two-block asymptotic universal-basin obstruction. In degree nine:
\[
\limsup_{a\downarrow5/8}
\frac{R_8(a)}{\sqrt{(1+a)(a-5/8)}}\le\sqrt{\frac{3328}{75}}.
\]
The squared upper constant improves the earlier moving-pair value by
the exact factor \(63/80\). This is a radial-baseline basin upper bound.
The balanced degree-nine curve and coefficient were already published
by the researcher; the review credits them.

Using Python3.11, from this directory:

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
.venv/bin/python -I -B independent_check.py
~~~

Expected: PASS and manifest SHA256
9cefe51e9a66908d24ff7fb1aded014119ee8755aff017a37bb248f787de26b5,
**311 exact checks**, **five rejected mutations**. Adding -O gives the
same mathematical manifest. The elapsed time is diagnostic.
The default command verifies expected.json; --output /tmp/review.json
regenerates a separate compact manifest.

Python3.11/SymPy1.14.0 exact Gaussian rational-function arithmetic is the
computational trust boundary. All-degree identities are symbolic; the
m=3..20 table is a finite control. Analytic branches, remainders and
universal quantifiers are written mathematics, not formalized.
