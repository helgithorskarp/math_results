# Finite-atomic producer and stability consumer

This interface consumes [Theorem 1](PROOF.md). Its inputs are rigorous
bounds for one fixed contraction, reference law, variance and reference
volume. No Gaussian enclosure has been computed by this packet. Written
analysis is the proof; this document is an input/output contract.

## Geometry and reference data

Supply finite sites x_i, target sites y_i, a reference probability vector
sigma, variance s>0 and a level 0<a<max(sigma*gamma_s). Verify all contraction
inequalities and an affine isometry S matching the reference support.
Pull y_i back by S and translate a reference point to zero.

Determine Z using the exact geometric condition

    |y_i-c|^2=|x_i-c|^2 for every reference support point c.

This avoids deciding whether a numerically small Gaussian slack is zero.
Determine U=span(reference support), V=U-perp. If V is nonzero, provide a
positive lower bound b_lo for the finitely many transverse coefficients
alpha(u_i,|w_i|) at sites in Z. If any sites lie outside Z, provide a
positive lower bound q_lo for their reference slacks q_i.

The theorem proves these coefficients are positive in the required cases.
Obtaining certified numerical lower bounds is the producer's task. Small
floating-point values or failed interval attempts are not valid inputs.
No positive q floor is assumed at sites of Z.

Supply L>0 bounding all pair losses d_ij=|x_i-x_j|^2-|y_i-y_j|^2. Any larger
source-diameter bound suffices. For rational arithmetic one may use H=1/s,
since H>=2/(pi s), to replace the squared gradient bound G^2.

With both V nonzero and K\Z nonempty, the consumer may take

    C_bar=max{16/(s b_lo^2), (4H/b_lo^2+2L)/q_lo}.

Use the appropriate simpler branch of Theorem 1 if either set is absent.
Lower coefficient bounds and upper geometric bounds increase C_bar, so
D/C_bar remains a valid lower bound. If s and the supplied bounds are
rational, this step is exact rational arithmetic. The analytic enclosures
are still external premises.

## Two usable lower models

For every nonnegative probability weight vector p, the exact pair loss is

    D(p)=sum_(i,j) p_i p_j d_ij.

The sum is over ordered pairs. Therefore

    J_A(p)>=D(p)/C_bar.

This is uniform over the entire weight simplex. A rigorous lower bound on
D over any specified weight region yields a margin throughout that region.
D is not asserted to be convex in p; the producer must justify such a
regional bound. Existing finite face/strict-pair certificates can supply it.

A second model uses the individual reference data directly. Let

    v_i=P_V grad Psi(y_i),
    Q(p)=sum_i p_i q_i,      zeta(p)=sum_i p_i v_i.

Then

    J_A(p)>=Q(p)+(s/4)|zeta(p)|^2.

For fixed exact coefficients this is a convex quadratic function of p.
It retains the translation term on the zero-slack face. With interval
coefficients, use a certified lower bound for Q and for the norm of zeta;
for Q it is valid to take the maximum of zero and the interval lower bound.
Do not replace a certified norm bound by the norm of interval midpoints.
The target's optimizing set is not an input: all integrations are over the
single reference set A.

## Turning a common-set bound into the requested profile sign

The exact identity is

    C_g(v)-C_f(v)=J_A(p)-R_A(p),
    R_A(p)=C_f(v)-integral_A f >=0.

Thus a common-set margin alone is not the requested comparison. Supply a
rigorous upper bound R_hi, or supply epsilon<a with
||f-sigma*gamma_s||_infinity<=epsilon and an upper bound E_hi for

    integral (epsilon-|sigma*gamma_s-a|)_+.

Then R_hi=E_hi is valid, including critical reference levels. A lower bound
M_lo for either common-set model certifies

    C_g(v)-C_f(v)>=M_lo-R_hi.

Only a nonnegative right side certifies the weak sign; a positive one gives
a strict margin. A regular-level shell estimate can provide a quadratic
remainder, but its uniform constant must be established separately.

The source-density estimate epsilon<= (2 pi s)^(-n/2) TV(p,sigma) is one
available input. It can be weak when a is small or the actual prior differs
substantially from the reference. The theorem does not assert this test
covers every prior or every volume. A finite collection of certified
positive tests still needs interpolation and the two volume ends to give
an all-volume certificate. The existing [bounded-law interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md)
retains those separate endpoint, enclosure and transport obligations.

## Uniform windows and scope

For one fixed finite geometry and reference, common coefficient bounds
exist on compact positive variance and volume windows. The source-shell
remainder is uniformly o(epsilon) there. This is an existence/analysis
statement; the producer still has to enclose the minima for a quantitative
window certificate. No positive reserve for varying geometry, vanishing
weights in the reference itself, limiting volumes or zero variance is
asserted.

The direct consumers are the finite-atomic lane's equality controls and
the all-eight common-set formulation. The general arbitrary-source-set
sign, the evolution lane's contact covariance sign, and the geometric
lanes' Kneser--Poulsen classes are unchanged. No hypothetical certificate
input is represented here as a computed or independently verified value.
