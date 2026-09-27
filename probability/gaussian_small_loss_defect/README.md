# Gaussian defect smaller than every power of mean loss

**New author proof; independent review pending.** The preceding effective
mean-loss theorem is independently accepted. Full three-dimensional
Gaussian majorisation remains open.

For every fixed source radius R and positive covariance floor kappa,
the [proof](PROOF.md) bounds the adverse Gaussian hinge defect by an
explicit constant times exp(-c (log(a/d))^2) as the mean contraction
loss d tends to zero. The estimate is uniform over all bounded laws
in that class, including diffuse laws and disappearing atom weights.

A fully rational sufficient guard is available at centered radius
sqrt(s)/2 and Cov(X)/s>=2^-15 I. For each integer m>=4,

~~~
d<=2^-(44m+208)
  => H(u)>=0 for every u>=exp(-m^2/2),
     Def<=2^20 d exp(-m^2/4).
~~~

Thus relative error 2^-b requires only N=44m+208 loss bits with
m=max(4,ceil(sqrt(3(b+20)))). The cutoff scales as sqrt(b).
These are sufficient bounds, not a proof that the remaining defect is zero.

The new step bounds integrated Gaussian Hessians on the complement
of the actual source top set and cancels common Gaussian factors in
posterior ratios. It retains the low threshold in the earlier accepted
interval comparison. The [handoff](HANDOFF.md) states the exact parameter,
cubature and certification interface; [sources](SOURCES.md) record
dependencies and their status.

From the repository root, standard-library CPython 3.11 or later:

~~~sh
python3 -B probability/gaussian_small_loss_defect/verify.py
python3 -B -O probability/gaussian_small_loss_defect/verify.py
~~~

From this directory, sha256sum -c SHA256SUMS checks all packet files.
The verifier reports SMALL_LOSS_DEFECT_PASS and the canonical record hash
in EXPECTED.json. Its controls are exact algebra, not Gaussian quadrature,
formalization or independent acceptance.

The finite-data API finite_guard(xs,ys,weights,bits,variance=1) accepts
integers and Fraction values. It returns CONTROLLED_DEFECT, ZERO_LOSS,
or UNRESOLVED; invalid inputs raise ValueError. CONTROLLED_DEFECT
includes d, relative error bits and the negative logarithm of the signed
threshold. It does not mean the entire hinge curve is nonnegative.

INPUTS.json pins both commits and bytes. Matching local bytes suffice;
otherwise the verifier uses read-only git show at the recorded commit.
Git history is therefore required when current source headers differ.
There is no network fallback. The previous packet has a separate
[historical replay helper](../gaussian_effective_mean_loss/REPLAY.md);
its original ten files remain frozen.
