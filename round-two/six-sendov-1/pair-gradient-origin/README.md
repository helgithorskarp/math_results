# A sharp real pair-gradient bound and a larger complex origin box

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author proof with finite exact checks; unformalized;
independent review pending. See [PROOF.md](PROOF.md).

For real r in[1/2,3/2]^8 with sum r=8, put

    Phi(r)=9 integral_0^1 product(r_j^(-1)-t) dt.

The continuous divided-gradient kernel satisfies

    partial_i Phi - partial_j Phi = (r_i-r_j) Gamma_ij,
    Gamma_ij >= kappa = 492694/984375 > 1/2,
    Phi(r) >=1+(kappa/2)sum(r_j-1)^2 >=1+sum(r_j-1)^2/4.

The kernel constant is sharp at paired radii3/2 and six others5/6, approached
also by distinct pairs. Sharpness of the global deviation coefficient and
ordinary strong convexity are not asserted. Nineteen full minimizing-profile
charts have149 Bernstein controls,148 positive and one zero. Two complete
power/tensor routes and every inverse reconstruct the certificate.

For eight complex q with sum|q|<=8, m=mean q, Re m>=a, and

    1-3*10^(-5)<=a<1, |Re(q_j/m-1)|<=1/2,
    eta=q/m-1=u+i v, U=sum u^2, V=sum v^2,

then

    N_a(q)=|9 integral_0^1 product(1-atq_j)dt|^2/product|q_j|^2
          >=1+(1-a)+U/4+V/16>1.

There is no imposed imaginary bound or second-moment premise. The abstract
proof uses direct real pair-gradient control, an elementary imaginary-Taylor
bound on the large box, and retained mixed energies in the inner box. It
requires no preceding radial/polar/phase theorem. The earlier normalization
and mixed-energy mechanism are credited and rederived.

The joint polar/origin/individual-critical-disk system is consequently
excluded for1-2*10^(-5)<=a<1. Every degree-nine disk-root polynomial has
strict critical reciprocal sum greater than eight at marked roots in this
annulus. This consequence explicitly uses published radial8656, mean8533
and adaptive phase8707. Multiplicities are counted; collisions give infinity.
No optimal annulus, unconditional linear surplus or full first-power endpoint
is claimed. [LITERATURE.md](LITERATURE.md) records exact dependency/review scope.

From the repository root, use CPython3.10+ standard library:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-sendov-1/pair-gradient-origin/verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-1/pair-gradient-origin/verify.py

Expected PASS: all149 curvature coefficients in two routes with19 full
inverses; three all-endpoint charts; exact sharp kernel/direct gradient
controls; six full component identities in14 real variables and six Newton
components;90 primitive coefficients;42 support counts;35 rational comparisons;
ten Gaussian-rational controls. An increased sharp constant, four damaged
symbolic identities and ten damaged fixtures are rejected, including-O.
Canonical record SHA256:

    48ddab405370597d5d221357659892c0e3d66b9026430e4da6db1a3f36c90d2a

Default runs read [expected.json](expected.json); --emit explicitly writes
regeneration. No floating-point proof input, solver, external code/data,
omitted large certificate or formal kernel is required. The minimizer,
pair-gradient integration, complex Taylor/modulus, reciprocal denominator,
mean payment, flatness and inherited annulus arguments remain written
mathematics. Author checks are not independent review.
