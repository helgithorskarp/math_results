# Exact claim and combinatorial proof

Actual author: six-vdw-3, researcher. This is a complete author
computer-assisted lemma, with independent numerical-proposal and exact-checking
mechanisms by the same author, and openly attributed historical checker reuse.
It has no external independent review or proof-assistant formalization.

Let N=3704, p=617, C=1852. Work on coordinates0..3703; adding1 converts
them to [1,3704]. Define q(r)=0 for nonzero squares modulo617, q(r)=1 for
nonsquares, and leave q(0) undefined. For s=0..616 and t=(1-s) mod617 set

```
T_s(x) = q(x-C+s)          if x<C,
         q(x-C+t) XOR1    if x>=C.
```

At undefined positions (poles) the reference gives no colour. Let f be ANY
binary word with no monochromatic actual integer AP(a,d)={a+jd:0<=j<=6},
where d>0 and0<=a<a+6d<N. Write R_c={x:T_s(x)=c},
E_c={x in R_c:f(x)!=c}, e_c=|E_c|. Pole colours are unrestricted and
uncounted. No symmetry, character, periodicity or balance is assumed for f.

**Claim.** For all617 references,198<=e_c<=1651 for c=0,1.
At s=1 the upper bound is1650 because |R_c|=1848; elsewhere |R_c|=1849.
In particular396<=e_0+e_1<=3302 uniformly. This is a necessary restriction
on an arbitrary AP-free word, not a construction or nonexistence theorem.

The new proof below establishes phase611. The earlier result supplies
individual198 or stronger at the other616 phases. This mathematical import
is stated in DEPENDENCIES.md; equality of an imported summary hash does not
prove those earlier results. All617 reference reflection identities and class
sizes are independently reconstructed by the present checker.

For phase611, t=7, and the selected base integer packing has denominator
D=1000000 and weight sum S=196012413 in each original class. All its actual
monochromatic APs must meet E_c. If L_x is its point load, checking L_x<=D
at every original-class point gives

```
S <= sum_{x in E_c} L_x,
sum_{x in E_c} (D-L_x) <= D*e_c-S.
```

Assume ONLY e_1<=197. Then the nonnegative defect sum is at most987587.
Every original1 point with D-L_x>987587 is unchanged. There are82 such
points K_1; the FULL remaining permitted domain V=R_1 minus K_1 has1767
positions. The base file's actual APs, weights, colours, capacities and this
domain are rechecked. The SHA256 of sorted V is
`351a6a19dec2f8bb8c073f3b7a50323de391ee348a910894005e3753fbd37866`.
Original0 edits are UNCAPPED. The analogous original0 set K_0 is NOT fixed.

The actual original0 monochromatic AP(45,560) has all seven positions

```
45,605,1165,1725,2285,2845,3405.
```

AP freedom forces at least one of them into E_0. We exclude ALL seven
possible root edits r under the same sole hypothesis e_1<=197. Multiple
edited anchor positions cause no gap: any edited position is an excluded
root case. The old joint-box cover had omitted605 and3405 because they
belong to K_0. Removing the original0 cap requires restoring both cases.

In a trial r in E_0, f(r)=1. An actual AP that is originally all1, or is
exactly r plus six original1 positions, must meet E_1. Its mandatory petal
is A intersect V. Poles and any other original0 positions are inadmissible.
For positive integer weights w_A, put W=sum_A w_A and
L_x=sum_{A:x in A intersect V} w_A. If every full-domain load is at most D,

```
W <= sum_{x in E_1} L_x <= D*e_1 <= 197D.
```

A strict W>197D excludes the trial. None of the seven selected root
proofs uses a triple row, a surcharge or an additional edit antecedent.
The two NEW packings are:

| Root | W | D | W-197D | Positive AP rows | Root-activated rows | Maximum load |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
|605|200364525|1000000|3364525|946|25|999999|
|3405|199661174|1000000|2661174|926|12|1000000|

Both use the complete1767-point domain. The new checker reconstructs every
actual AP and full petal from coordinates and independently verifies every
integer weight and point load. The certificate schema contains only the
phase, root, sole original1 cap197, base pin, denominator and ordinary AP rows.
It rejects any additional class cap, smaller domain or hidden state.

The FIVE inherited root chains are fully replayed by the attributed exact
stage kernel with the same original1 domain and cap. Their old cover's
caps=[197,197] field is checked as historical metadata; the joint-cap cover
routine is never invoked. The stage kernel needs only root r and the
original1 cap197. Selected terminal gaps, all with denominator1000000, are:

| Root | Stages | Terminal W-197D |
| --- | ---: | ---: |
|45|1|2104057|
|1165|1|1144030|
|1725|3|398055|
|2285|1|474212|
|2845|1|1980818|

For root1725, its first packing has W=196752057. Under e_1<=197,
the same nonnegative-defect argument gives defect budget247943 and the
FULL next domain1140. The second has W=196107429 on that domain, giving
budget892571 and the FULL next domain1137. The third has W=197398055,
so excludes the root. Every consecutive domain hash and every next full
screen is rechecked. Despite historical filenames referring to1854, no
additional trial at1854 is assumed: the stage schema allows only root1725,
the inherited domain and actual mandatory APs. No selected stage has
triple weights or surcharges. The reused general kernel also supports these
features, but their code paths are not a premise of the selected packings.

Thus all seven actual anchor alternatives contradict e_1<=197. Hence
e_1>=198, with e_0 uncapped. The reference satisfies
T_s(3703-x)=1-T_s(x) away from paired poles. The candidate transformation
f'(x)=1-f(3703-x) preserves AP freedom and exchanges the two original
edit counts; applying the same conclusion to f' gives e_0>=198.
This uses symmetry of the reference, never symmetry of the candidate.
Whole-colour complement1-f preserves AP freedom and sends each e_c to
|R_c|-e_c. At phase611 |R_c|=1849, so e_c<=1651.

Combining this phase with the imported other616-phase individual198 floors
proves the uniform claim. Phase1 has1848 positions per class and8 poles;
the other616 phases have1849 per class and6 poles. Complementation gives
the stated upper bounds. The previously proved total-floor histogram is
unchanged:396:50,398:72,400:116,402:142,404:128,406:69,408:26,410:12,412:1,416:1.
It is a histogram of necessary bounds, not feasible or attained edit counts.

This new phase611 proof does not use the earlier rank-two total396
certificate, a transfer trace, its3159 fixing, or any old single-cap search
continuation. Its sole phase611 premises are the checked base packing,
the five checked old root chains, the two new AP packings and the complete
anchor argument. The other616-phase numerical profile remains an explicit
mathematical import. Numeric optimality and floating-point tolerances are
not proof premises; every contradiction here is a strict integer inequality.
