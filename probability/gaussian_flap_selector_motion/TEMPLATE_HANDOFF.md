# Closure of the two R7 template obligations

Both templates in [R7's reduction](../gaussian_flap_tournament_reduction/PROOF.md)
are closed by the [selector-motion proof](PROOF.md), for every allowed
orthocentric shape, every nonnegative weight vector, every variance s>0
and every Gaussian hinge. [R7's independent review](../gaussian_flap_selector_review_r7/REVIEW.md)
accepts that theorem and both arbitrary-radius ball-volume consequences.
The original proof and its checker are unchanged by this handoff. The
reviewer's upstream authorship and the remaining limits are recorded in
[REVIEW_STATUS.md](REVIEW_STATUS.md). No additional family is introduced.

## Exact labels and the only distances requiring a new sign

Use R7's edge order (01,02,03,12,13,23), where bit one selects the smaller
vertex as tail. In both templates choose i=0, which has exactly one outgoing arc.

| R7 template | Mask | Sole arc i->k | Complementary plane | Exceptional selected pairs |
| --- | --- | --- | --- | --- |
| source_cycle | 2 | 0->2 | span(v_1,v_3) | (0->2, 2->1) |
| strong | 4 | 0->3 | span(v_1,v_2) | (0->3, 3->1), (0->3, 3->2) |

Every other pair distance has fixed moving Gram entry and is already
nonincreasing by the coefficient signs in PROOF.md (16)-(17). For a
relabelling of a template, relabel its geometry and all weights too; one
cannot replace the 32 labelled cases at a fixed asymmetric shape by two
unchanged coordinate arrays. The universal construction applies directly
to every labelled case, as the original checker verifies.

## The independently checked certificate for the exceptional sign

For the common projection p and opposite normal components in PROOF.md,
write L=|p|^2, v_i=p+A n, v_k=p-B n. Then A,B,L>0, AB=L+c and
h_k=B(A+B). Put d=asinh(A/sqrt L)+asinh(B/sqrt L),
epsilon=exp(-d), q=tanh(d), and delta=AB(cosh(d)-1)>0.
In the increasing clock t=tanh(w-V), the exceptional squared distance
is constant minus twice

    K(t)=delta sqrt(1-q^2)(1-t^2)/(1+q t)+h_k t.

R7's review, Section 4, independently verifies the exact factorization

    K'(t)=B^2+AB epsilon(2-epsilon)
          +delta epsilon(1-q)(1-t)[2+q(1+t)]/(1+q t)^2
          >B^2>0.

Here -1<=t<=1 and 0<epsilon,q<1. Every displayed factor has a controlled
sign, and the denominator stays positive. This certifies every pair in
the table throughout its motion, without inferring a universal sign from
sampled times. The review also reconstructs the Gram realization and
checks the analytic endpoints; the positive derivative alone would not
supply those obligations. This handoff uses the review's certificate
rather than introducing another author checker for the same sign.

## Exact asymmetric positive controls

For R7's shared rational fixture

    v_0=(0,0,1), v_1=(2,0,-1), v_2=(-1,3,-1), v_3=(-1,-1,-1),

the projection and margin data are:

| Template | p | L | A^2 | B^2 | AB | h_k |
| --- | --- | --- | --- | --- | --- | --- |
| source_cycle | (-1,3,5)/7 | 5/7 | 2/7 | 72/7 | 12/7 | 12 |
| strong | (-1,-1,1)/3 | 1/3 | 2/3 | 8/3 | 4/3 | 4 |

Thus the clock derivatives of the exceptional squared distances are
strictly below -144/7 and -16/3, respectively. These bounds are in clock
t, not in the compact analytic time parameter, whose speed vanishes at
the endpoints. They do not assert a uniform quantitative Gaussian hinge
margin. The controls use an asymmetric tetrahedron and all weights are
allowed; neither balanced weights nor a numerical integration is needed.

Reproduce the independent motion checks from the repository root:

```sh
python3 probability/gaussian_flap_selector_review_r7/verify.py
```

The review's [checker](../gaussian_flap_selector_review_r7/verify.py)
reconstructs the geometry using rational coordinates and exact quadratic
extensions. Its [expected record](../gaussian_flap_selector_review_r7/EXPECTED.json)
includes the two fixture margins above, all 72 eligible tail choices over
the 32 sinkless selectors, and 2,025 coordinate derivative identities.
Its universal sign comes from the factored polynomial identity, not its
finite time checks. The review did not use the author's checker or output.

## The precise R4--R7 chain

| Source | Quantifiers and role | What it does not supply |
| --- | --- | --- |
| [R4 shallow theorem](../gaussian_flap_depth_boundary/SUPPORT_SIGN.md) | Arbitrary tetrahedra and inward normal lengths; all hinges at sufficiently small depth for each fixed law and variance | A common depth for all weights and variances, or a deduction at depth one |
| [R7 tournament reduction](../gaussian_flap_tournament_reduction/PROOF.md) | Orthocentric depth one; any negative hinge survives in one of the two displayed templates | The template sign by itself |
| [R4 selector motions](PROOF.md) | Every selector contracts in R5; common-target convexity signs all hinges for the entire depth-one family, at all weights and variances | Arbitrary tetrahedra at depth one or the unrestricted conjecture |

The shallow theorem is preserved as a separate analytic result. It is not
a premise of the finite-depth proof. The latter settles the exact template
obligation through a different mechanism; no limiting-depth inference is
being used. Its arbitrary-radius union and intersection consequences use
the larger-radius and smaller-radius selectors, respectively, as proved
in PROOF.md Section 7.

The full sixteen-label path remains invalid: a common-head pair i->r,k->r
has no contraction reserve and would decrease then increase. Keep that
failure control alongside the two positive controls above. The common-target
mixture remains essential. The recorded independent team-agent acceptance
is distinct from graph commitment, external peer review and historical
priority. The unrestricted dimension-three problem remains open.
