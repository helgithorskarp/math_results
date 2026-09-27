# Positive-loss all-threshold handoff for the R2/R3/R8 spine

The claim is a uniform parameter family, pending independent review. It
uses the already accepted spherical-gap endpoint6032/6048, rather than
trying to reconstruct an entire hinge curve from an enormous beta row.

For centered source radius R and scatter V>0, a martingale coupling to the
dilated target aY, a>1, gives the uniform spherical gap

```
eta=(a-1)V/(96 a R^2)   for every lambda>=1/(2R).
```

The existing endpoint therefore signs every threshold simultaneously at
`s>=4224 a R^4/((a-1)V)`. The class has raw pair loss
`D>=2(1-a^-2)V`: it concerns positive relative loss, not an infinitesimal
near-isometry case. It does not require a lower covariance eigenvalue once
the coupling is given.

The compact producer uses `K(x,y)=1+a x^T Sigma_X^(-1)y`. Positivity on
the cross-support product, both means and Sigma suffice. If Sigma_X>=kappa I
and the target radius about its mean is at most kappa/(aR), K is nonnegative
uniformly. For a=2, any target cF with F 1-Lipschitz and
`c<=kappa/(4R^2)` passes this condition, at every
`s>=2816R^4/kappa`. This includes arbitrary atom counts and diffuse laws.

The source and target clouds need not be planar or have paired rank<=5.
The kernel is an auxiliary coupling of the marginals. The original map
must contract; a times that map need not. Neither a moment-grid positivity
test nor a numerical integration oracle is a premise.

With the original support-wide kernel or radius inequality established,
degree-two same-pair cubature preserves the means, covariance, V and
contracting original sites on at most 19 pairs. It preserves this passing
condition; it does not identify the original and compressed hinge curves.
A kernel passing only on compressed sites does not prove it on discarded
support. No common cubature choice or rational rounding over a parameter
cell is asserted.

The finite certificate costs quadratically many rational operations in n,
and linear storage, with nine extra rational entries beyond the input. Its cost does not grow
with a beta degree or inverse threshold. That is a guarantee for this
sufficient family, not a complexity claim for the remaining majorisation
decision. Outside the kernel condition or below the sufficient variance,
the method honestly returns unresolved.

R3's accepted effective small-loss guard6426/6432, its accepted moving-window
defect6450/6460, the accepted covariance-collapse boundary6442/6448 and R8's
general covariance boundary6454 address other parts of the frontier.
Their conclusions are preserved. The undamped full-rank positive-loss
remainder remains open. The current result adds a complete all-threshold
family with a direct certificate; it does not take a fixed nonzero defect
bound to zero or send a finite beta degree to infinity.
