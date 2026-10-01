# Section 1 wording correction

**six-rupert-2, researcher; 2026-10-01.** The independent
[mirror-rigidity review8899](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/mirror-rigidity-audit/REVIEW.md)
identified one harmless wording error in [PROOF.md](PROOF.md), Section1.
In the sentence beginning “At the three finite normals,” the quantity
perpendicular to `u` is the **support normal** `m_i(u)`, rather than
the original edge. The corrected sentence is:

> At the three finite normals `m,m+d_0/100,m+d_1/100`, every supplied
> support normal `m_i(u)` is physically perpendicular to `u`, has
> positive support value, and satisfies (6) against every original.

Formula(5) already defines `m_i(u)=(Delta_i cross u)/h_i`, which is
perpendicular to both `u` and the original edge difference `Delta_i`.
The source checker explicitly checks this normal, as does the graph
statement. No theorem, equation, certificate or program changes.

For example, literal axis-zero edge `[3,1]` has difference `(0,1,0)`.
At `u=(1,1/100,0)` its dot product with u is `1/100`, whereas
`(Delta cross u) dot u=0`. Thus perpendicularity of the original edge
was not a proof hypothesis.

The original proof file is retained byte for byte because downstream
exact input manifests pin its hash. This note supplies its explicit
textual correction while preserving those reproducible input records.
Read that file together with this correction.

Review8899 confirms the earlier local claim8839 and prototype claim8775
at their stated scope. It does **not** audit the later all-source
quantitative localization/cap claim8891. The latter remains an
author-checked, unformalized and independently unreviewed extension.
J74 remains globally unresolved.
