# Independent actual low-energy entry audit

Actual reviewer six-reviewer-3, independent mathematical reviewer.
[REVIEW.md](REVIEW.md) confirms LEMMA9588 and proves the wider energy threshold36.
All actual original roots lie in the closed unit disk; p(1-eta)=0 and
0<eta<=2^-16. H<=36eta and F<=8+3eta imply all |c1..c8|<31eta/4<8eta.
The imported9533/9572 cap8 corollaries are explicitly separated in the review.
No unrestricted first-power or all-competitor concentration theorem is claimed.

CPython3.10+ standard library; tested3.12.14. From the repository root:

~~~bash
python3 -I -B round-two/six-reviewer-3/low-energy-entry-audit/verify.py
python3 -I -B -O round-two/six-reviewer-3/low-energy-entry-audit/verify.py
python3 -I -B round-two/six-reviewer-3/low-energy-entry-audit/refine.py
python3 -I -B -O round-two/six-reviewer-3/low-energy-entry-audit/refine.py
python3 -I -B round-two/six-reviewer-3/low-energy-entry-audit/validate.py
python3 -I -B round-two/six-reviewer-3/low-energy-entry-audit/validate_refinement.py
~~~

Serial children, native threads1, fixed45-second guards.
Default commands compare the complete typed fixtures; they reject coefficient,
field, integer/bool, duplicate and nonfinite changes in both Python modes.
First whole record: bccbff984160d4a45bff596722abd391b79d16cb1d5d3df88de3f680a6061214.
H36 whole record: cf5c32e1e4d0b4b7fadfbb9b3698f3ecccaa01287b85c6a6a8668aa7a82c9fd9.
The first83 checks include47 full polynomial identities and36 literal
root/point controls. The later refinement supplies6 additional full identities.
Base validation rejects14 bad fixtures; refinement validation rejects8.
Ten baseline identity alterations are detected; some deliberately weakened
bounds remain valid inequalities and are not claimed to refute a theorem.

[PROVENANCE.json](PROVENANCE.json) separates the original pre-author seal,
author replay, asynchronous reviewer overlap and the later H36 refinement.
The original first seal includes H30/H32 only; H36 was developed after author
replay and consumes no author code/fixture or peer proof.
[INPUTS.json](INPUTS.json) pins every actual external input used for replay,
written corollaries and owned kernel reuse. The proof does not import any
author executable. [VALIDATION.json](VALIDATION.json) contains compact actual
receipts; large raw records, logs and exploratory state remain private.

Optional late comparison (git has the pinned source commit available):

~~~bash
python3 -I -B round-two/six-reviewer-3/low-energy-entry-audit/verify.py --emit > /tmp/entry-own.json
git show 6d1322d6e781746c45264966ecc257fa0dfcc067:round-two/six-sendov-1/low-energy-entry/verify.py > /tmp/entry-author.py
python3 -I -B /tmp/entry-author.py --emit /tmp/entry-native.json
python3 -I -B round-two/six-reviewer-3/low-energy-entry-audit/compare_author.py /tmp/entry-own.json /tmp/entry-native.json
~~~

The adapter matches33 full polynomial digests/559 coefficient positions
including repeated rows, all six lower bounds and both complete original
quadratic costs, mean absorption, lower sum and final cap. Native finite
replay is late corroboration. Analytic convergence, disk-root positivity,
Fourier/norm/Maclaurin inequalities and endpoint monotonicity remain ordinary
written proof bridges. This is not a formal proof-assistant certificate.
