# Four-active-weight two-level missing walls

This directory classifies every positive candidate wall for four active
normalized weights taking at most two distinct values. Up to permutation and
common scaling, the strata are

\[
(1,1,1,a),\quad(1,1,a,a),\quad(1,a,a,a)\quad(0<a<1),
\quad\text{and}\quad(1,1,1,1).
\]

Exactly three wall orbits disappear:

\[
\begin{array}{c|c|c}
\text{weights}&B&\text{missing wall}\\ \hline
(1,1,1,a_1)&4a_1/(1-a_1)&4\\
(1,1,1,1/\sqrt2)&2\sqrt2&4\\
(1,1,a_2,a_2)&2a_2^2/(1-a_2)&2(1+a_2),
\end{array}
\]

where

\[
4a_1^6-3a_1^2+6a_1-3=0,\qquad
a_2^6+a_2^5+2a_2-2=0
\]

have their unique roots in \((0,1)\). There are no missing positive walls on
the \((1,a,a,a)\) or diagonal strata.

The proof also gives an arbitrary-dimensional obstruction. For weights
\(1^p a^r\), a row supplied by weight \(1\), with \(k\) unit and \(\ell\)
\(a\)-tails, can cancel a row supplied by \(a\), with \(i\) unit and \(j\)
\(a\)-tails, only if

\[
r+k=p+j.
\]

This residual-multiplicity rule reduces the dimension-four classification to
12 exact candidates. See [PROOF.md](PROOF.md) for the theorem and proof, and
[SOURCES.md](SOURCES.md) for dependencies and the trust boundary.

## Reproduce

The independent verifier uses CPython 3.11 or later and only the standard
library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual-verification.json
diff -u EXPECTED_VERIFICATION.json actual-verification.json
~~~

The symbolic derivation pins SymPy 1.13.3:

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python derive.py > actual-derivation.json
diff -u EXPECTED_DERIVATION.json actual-derivation.json
sha256sum -c SHA256SUMS
~~~

Expected statuses are Q4_TWO_LEVEL_MISSING_WALLS_VERIFIED and
Q4_TWO_LEVEL_MISSING_WALLS_DERIVED.

The canonical output hashes are respectively
`c91eecbe4b13c4f53f6af6e5588e45c636b91c716859df8bf8d6c53b7b6c25ec`
and
`addf7084c114fd38ffbdcee1671307f890368cfe1f06daf679035e1a3f200c6a`.
