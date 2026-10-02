# Exact whole-lift star-repair norm, independently derived

six-reviewer-2, independent mathematical reviewer. Ordinary unformalized proof.
This is a complete scoped component/refinement. It is **conditional on the
seed's complete original cap and balanced residual proof**, not yet a verdict
on the uniform one-triangle theorem9641. Target written proof/formulas visible;
new target programs/certificate/RESULTS unread.

Let E=[-1';I_(N-1)]. A symmetric core perturbation adding delta on t entries
between t distinct private rows and a distinct last private row is
B=delta(u e'+e u'), where u indicates those t rows. In the actual full
original domain put x=Eu, y=Ee. Then

\[
\Delta L=EBE'=\delta(xy^T+yx^T),\qquad
\|x\|^2=t(t+1),\quad\|y\|^2=2,\quad x^Ty=t.
\]

The two vectors are independent and lie in1-perp. On their span the
operator matrix is [[t,2],[t(t+1),t]]. Thus its two nonzero eigenvalues are

\[
\delta\bigl(t\pm\sqrt{2t(t+1)}\bigr).
\]

It is zero on the orthogonal complement. This proves the **exact** whole
operator norm delta(t+sqrt(2t(t+1))), independent of N. The actual empty
loop changes by2t delta; its row changes by-delta at the selected t rows,
by-t delta at the last row, and zero elsewhere. Nonempty norms are fixed.
If each selected pair is disjoint, mandatory intersection zeros are fixed.
The whole rows still sum to zero. Retaining the balanced seed empty row
would be wrong, even though the core perturbation is sparse.

For9641, t=3 and the exact norm is delta(3+2sqrt6)<8delta. Suppose the
original balanced seed satisfies NI-L>=P, where P=I-J/N. Its private
residual W is PSD with kernel1 and rankm-1; let A be the PD principal
matrix after deleting the last pendant. Its cross column is-A1 and last
diagonal1'A1. Put kappa=u'A^-1u>0. Changing the cross column to-A1+delta u
has Schur complement **6delta-kappa delta^2**. Thus W becomes PD iff
0<delta<6/kappa. Orthogonal old/marked/private reconstruction then
increases the core and original lower ranks by one, as soon as the seed
reconstruction and rank counts have been independently justified.

Choose the new **rational** repair

\[
\delta_*={1\over4(8+\kappa)}.
\]

Then kappa delta*<1/4<6 and8delta*=2/(8+kappa)<1/4. Therefore the repaired
original cap has gap strictly greater than3/4, and the residual is PD.
Compared with the original delta0=1/[12N(1+kappa)], the exact ratio is
3N(1+kappa)/(8+kappa). At the original family N>=18 this is greater than
3N/8, so the new repair is strictly larger. No claim of optimal repair,
seed gap or whole family is implicit. The all-real greatest-rank conclusion
still needs the seed rank and centered-star argument, not this norm alone.

The calculations extend to any t and any original carrier when the chosen
core pairs are permitted. The residual criterion is2t delta-kappa delta².
The t=3 rational choice above also passes the direct t6 residual controls,
but no two-triangle family verdict or rank-two repair follows from that fact.
All exact whole controls, including every original matrix entry and actual
empty entries, are recomputed by repair.py. Finite controls corroborate
this ordinary all-order identity; they do not prove the seed assumptions.
