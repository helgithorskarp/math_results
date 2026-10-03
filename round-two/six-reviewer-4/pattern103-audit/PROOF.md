# Independent F103 witness audit and shorter integer interval

Actual author: six-reviewer-4, independent mathematical reviewer. This proof
audits LEMMA9886/0; its defining statement and ordinary proof were exposed.
The reviewer's executable code and complete evidence were sealed before
opening the target's executables, positive certificate or expected outputs.
This is an ordinary unformalized computer-assisted proof, not a blind review.

Let \(L(x)\) be zero on nonzero squares and one on nonsquares in
\(\mathbb F_{103}\), undefined at zero. Choose arbitrary \(p\) and nonzero
\(u\). The four original free columns are
\(p,p+u,p+2u,p+4u\), even for a constant Boolean function or an ignored
character input. Outside these columns the pattern is
\[
 T(x)=(L(x-p-u),L(x-p-2u),L(x-p-4u)).
\]
For every positive \(m\) coprime to 103, choose any Boolean rule \(F_s\)
separately in each phase \(s\in\mathbb Z/m\mathbb Z\). The background at
an integer \(n\) is \(F_{n\bmod m}(T(n\bmod103))\). Values at free
columns and edited positions may be arbitrary and nonperiodic.

The finite evidence consists only of positive witnesses: for every nonzero
scale \(v\) and every even truth word \(w\in\{0,2,\ldots,254\}\), it
provides five actual seven-term field progressions, avoiding
\(0,v,2v,4v\), with pairwise disjoint supports and monochromatic colors
under the entire word. Each progression has an oriented step between 1
and **50**, inclusive. There are \(102\cdot128=13056\) ordered cases.
The complete corpus is regenerated privately; compact expected records
pin all individual partition bytes and the complete corpus. No heuristic
failure, optimum, packing upper bound or nonexistence is a premise.

`generate.py` proposes positive packs using Gauss characters, literal set
intersection and bounded increasing-tuple search. `check.py` imports no
proposal kernel. It computes actual character values by an independently
formed square set, checks Euler's criterion, and checks every literal
point, color, original free column, oriented step and pairwise intersection.
It also checks each positive pack's actual cyclic modulus-618 and integer
phase-6 lifts in all six phases. These finite checks do not themselves
enumerate all moduli or all translated packs.

Complementing the output word preserves monochromaticity, so the even
words cover all 256 Boolean functions. This complement is applied within
one homogeneous phase's certificate; it is not a claimed symmetry of the
mixed-phase AP-free coloring problem. Character input permutations and
leading coefficients can likewise be absorbed into its arbitrary rule.

## All poles, scales, and coprime phase moduli

Choose a phase's positive representative \(t\in\{1,\ldots,m\}\) and
write \(n=t+mk\). In the field put
\[
 \alpha=m^{-1}(p-t),\qquad v=m^{-1}u.
\]
For each \(r\in\{1,2,4\}\),
\[
 L(n-p-ur)=L(m)\mathbin{\mathrm{XOR}}L(k-\alpha-vr).
\]
Thus its arbitrary rule becomes another arbitrary rule in ordinal
coordinates. Translate the certified scale-\(v\) pack by \(\alpha\).
This translation preserves field supports, step sizes, disjointness and
all four original free columns. No affine symmetry of the finite integer
interval is being assumed. Choose each translated start's representative
\(a\in\{0,\ldots,102\}\). A witness with certified step \(d\le50\)
lifts to the actual positive integer progression
\[
 t+ma,\ t+m(a+d),\ \ldots,\ t+m(a+6d).
\]
Every endpoint is at most \(t+402m\), because \(a\le102\). Its field
points and original character colors agree exactly with the certificate.
The five supports have 35 distinct field columns; their lifted actual
positions are disjoint. On the cyclic domain \(\mathbb Z/(103m)\),
distinct field columns also ensure seven distinct residues and disjoint
supports, and the nonzero step is \(md\).

Consequently any AP7-free coloring agreeing with this background outside
four free columns and a fixed extra-column set \(H\) must satisfy
\(\lvert H\rvert\ge5\) on the cyclic domain, and on
\([1,N]\) already when **\(N\ge402m+1\)**: use \(t=1\).
If edits are specified as individual actual positions, each phase needs
at least five nonroot/nonpole discrepancies. On the cyclic domain this
gives at least \(5m\) in total. On the integer interval it gives at
least \(5m\) within **\([1,403m]\)**, for \(N\ge403m\).
Different phases' positions cannot coincide. The original weaker
\(408m+1\) and \(409m\) endpoints in9886 therefore follow too.
For \(m=6\), the improved thresholds are **2413** for five extra columns
and **2418** for at least 30 actual discrepancies.

## Separate basic Boolean obstruction and affine-basis coverage

`basis.py` independently enumerates regular normalized points and their
labels \(4b_1+2b_2+b_3\), obtaining
\(11,14,14,11,14,11,11,13\). It searches a four-AP kernel whose label
sets are \(\{1,2\},\{1,4\},\{1,5\},\{2,4,5\}\). If the first
three were nonmonochromatic, labels 2,4,5 would all be opposite to label
1; the fourth would then be monochromatic. All 256 full words are also
checked explicitly. This structural obstruction is independent of the
positive five-pack proof and does not establish five as an optimum.

For all \(103\cdot102=10506\) original pole/unit pairs, the code checks
each entire affine bijection, all four original free columns and all
\(10506\cdot99\cdot3=3120282\) actual character entries using
\(L(p+ux-(p+ur))=L(u)\mathbin{\mathrm{XOR}}L(x-r)\).
It transports all four kernel progressions through every pair and checks
42024 actual cyclic phase-6 APs and their positive integer lifts with
the original2449 endpoint. Translation of the scale-indexed five-packs
and the universal ordinal-coordinate argument remain ordinary proofs.

These are necessary construction-family conditions. They provide no
feasible repair, no optimality assertion, no coloring of length3704 and
no numerical improvement of an unrestricted van der Waerden bound.
Trust includes Python integer arithmetic, ordinary character
multiplicativity, the exhaustive positive domain/certificate checker,
and the written translation, Boolean absorption and integer-lift bridges.
