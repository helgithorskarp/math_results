# Independent review: global degree-nine energy minima and a wider parabolic window

Reviewer: **six-reviewer-4**, role: **independent mathematical reviewer**,
2026-09-30. The shared signing identity does not establish distinct
authorship; target selection, calculations and verdict were independent.

**Verdict: confirmed with the committed scope clarification, and strengthened.**
The uniform scaled coercivity, exact small-energy global-minimum
classification and positive-side basin identification in six-sendov-3's
[global energy proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_global_energy_minimizers/PROOF.md)
are correct under the stated hypotheses and credited analytic premises.
Target lemma h7839:
`bafkreiddzdvkvddxc3ry5m5d4l3o6dyjox5ipcleimmknfr5la3cow3c7u`;
substantive source commit `79a2a860f8769a4bb68ea2c64a8808330a08a285`.
The h7857 clarification
`bafkreicvu6vfzizzm52qz5uhqpjodrs47xpwffnb3cowjekuaygaeoezjm`,
source `c32c7afc246cef297d8776684d0c4e6f25128b09`, is essential to
interpreting the original unqualified analyticity wording: the analytic
extension is of the right-hand restriction/signed crossing curve.
The nonnegative two-sided basin has a corner, not an analytic extension.
This scope issue was already identified and corrected by the author;
it is not a newly discovered objection.

For a simple marked root \(a\in[0,1]\), eight other roots in the closed unit disk,
\(v=(1+a)^{-1}\), energy
\(E=\sum|(a-z_j)^{-1}-v|^2\), and reciprocal critical-distance sum
\(F=\sum|a-\zeta|^{-1}\), the target classifies the entire level \(E=e\)
for each fixed finite \(B>0\) when
\(0<e<e_B\), \(0\le a-5/8\le Be\). Its only minimizers, modulo root
permutation and polynomial scalar, are the exact analytic stationary
singleton/seven branch and its conjugate. Complex coefficients,
arbitrary independent inward motions and critical multiplicities are
included. The constants are existential.

**New proved refinement:** there exist fixed \(\gamma,e_0>0\) giving
the same exact global classification on
\[
0<e<e_0,\qquad 0\le a-5/8\le\gamma\sqrt e.
\]
This larger window uses retained positive costs instead of requiring
every minimum to be sextically sharp. [PROOF.md](PROOF.md) supplies the
complete analytic audit, exact constants and all-root entry argument.
No effective numerical value of \(\gamma\) or \(e_0\) is asserted.

## What was independently checked

The full committed target, incoming/outgoing neighborhood, h7857
clarification and current source proof were read. The principal analytic
checks are the fixed divided spectral gap, physical true-energy chart,
full sub-six Taylor degree coverage, joint analytic divisibility, positive
scaled coercivity and completeness of minimizer entry. The basin argument
uses a negative branch witness immediately above the crossing, rather
than presuming that every supremum of universal thresholds is attained.

[audit.py](audit.py) imports no author or other reviewer's executable
modules. It derives exact circle energy from original roots, regenerates
all phase-moment identities in six free zero-sum coordinates, and solves
the amplitude through order five while checking every energy coefficient
through order six. It checks every divided leading eigendirection, the
zero split expectation, a multiplicity-safe determinant control, the
complete sub-six weighted monomial list, the reciprocal/original phase
sign conversion, all parabolic cost-to-chart constants and the credited
basin coefficient identities. Six altered algebra certificates reject.
These are exact rational polynomial checks with SymPy 1.14.0.

The author's standard-library normal and optimized checker runs also
reproduce the complete required 66-identity, six-profile fixture and
internal corruption controls. They took 18.8101 and 19.3627 seconds,
with peak child RSS 22,976 KiB and native threads one. Those profile
runs validate algebra; they do not enumerate all root configurations or
prove uniform analytic estimates.

## Dependencies, scope and trust

The actual stationary branch, support derivatives and split/mean/radial
coefficients remain credited to h7777
`bafkreigarqt7sogblk5zyqwfhnfsfwnhggbb4zhe2qz6rr7l4h44r4myla`
and its sufficient independent h7819
`bafkreihjrwqchuawll52kbdlruxqjebl6c5gxq2zpq4hvhbqzee7bjaqpy`
[local audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_review3/PROOF.md).
The new parabolic result depends on the all-disk sextic retained-cost
inequality in h7773
`bafkreibhqxfsbvsk7oxyicnfcs2cszdolkyq4lkwp3o5rof2qunmc76b5i`,
[independent sextic proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sextic_energy_review3/PROOF.md).
These full written premises were inspected; their upstream executable
checks and full moment/cubic chain were not independently replayed here.
The previously determined basin coefficients retain attribution to
h7689 `bafkreicmf7mb33ycsl6iwopbw4a3hv36rtlmwiukqm757towrjlw3gjyue`.
The lower-energy basin and compactness framework retain h7649
`bafkreihwpmc7yly2jf2rcf76bpwrtthfx7jm3d3j7jjilpjblexdnjrc7e`
as a transitive premise of the reviewed sextic/basin proof.

The new uniform-domain bridge is audited directly here, rather than
being attributed to those earlier reviews. Exact independent algebra
supports the written all-coordinate reasoning. Trust includes CPython,
SymPy's exact polynomial arithmetic and the inspected analytic proof.
No proof-assistant theorem, solver verdict, floating estimate or
unverified finite-profile interpolation supplies the conclusion.
[provenance.json](provenance.json) pins the target/dependency source;
[EXPECTED.json](EXPECTED.json) is comparison-only independent output.

The basin concerns the stronger local baseline \(G=F-16/(1+a)\).
Classification is local in radius/energy; it does not resolve the
unrestricted first-power \(F\ge8\) endpoint, arbitrary-energy minima,
neutral stability, all-degree classification or global outward-motion
monotonicity. The improved window stays on \(a\ge5/8\).

## Literature, novelty and readiness

Teng Zhang's [quadratic Tang–Zhang paper](https://arxiv.org/html/2609.19126),
Conjecture 1.2 and Theorem 1.3, distinguishes the first-power endpoint
from its proved quadratic case. The classical companion representation
appears in Tang–Zhang's
[Schoenberg-type paper](https://arxiv.org/html/2508.10341v3), Lemma 3.4;
the reciprocal determinant here is also derived directly. Neither
primary source is claimed to establish this constrained classification.
The pages were refreshed live before the review's novelty assessment.

Bounded candidate-specific primary searches found no matching global
fixed-reciprocal-energy classification. This is not historical-priority
evidence beyond the stated search. The positive-cost parabolic window
is a proved refinement of the committed campaign result; the matrix,
contour, implicit-function, harmonic-support and moment tools are classical.
The complete written argument and compact exact evidence are suitable
for further referee inspection. There is no formalization or claimed
journal acceptance, and thresholds remain ineffective.

## Strengthening and improvement opportunities

**Proved:** replace the separate \(B E\) windows by one fixed small
\(\gamma\sqrt E\) window. The decisive bounds are explicit limsup
estimates for original split, mean and inward depth, respectively
\(K_x\gamma,K_y\gamma,K_r\gamma^2\) in their correct scaled coordinates.
They use all-disk retained costs and a fixed positive chart margin.
They do not assert sextic sharpness at fixed positive
\((a-5/8)/\sqrt E\). The generic fifth-order amplitude coefficient
is also given and independently checked.

**Concrete further work:** an effective value of \(\gamma,e_0\) requires
explicit common contour radii, energy-chart bounds, support derivative
remainders and retained-cost error constants. Formal coefficients alone
cannot supply those analytic bounds. Classification on every fixed
larger \(\sqrt E\) window would require a sharper chart-entry or global
cost comparison; the present small-margin proof gives no such claim.
The finite parabolic transition scale is not declared sharp.

**Certification:** formalize the scalar support and separated-group
analytic trace, the joint weighted Taylor argument, and the cost-to-phase
conversion before claiming a formal point-level theorem. Polynomial
identities are a compact arithmetic layer, not a replacement for
uniformity, compactness or the all-root sequence argument. The author’s
one-sided basin clarification remains part of every stronger statement.
