# Which quadratic maps obey the universal half-total dimension bound?

For every real polynomial Q(x,y,z) of total degree at most two, we give an
exact coefficient test for

    dim_H Q(A x B x C) >= (dim_H A + dim_H B + dim_H C)/2

for **all nonempty compact** A,B,C in R whose summed dimensions are at most
two. The criterion has two parts: Q is nonconstant on every coordinate
line, and at least one of three explicitly displayed Jacobians is nonzero.
See [the full theorem and proof](PROOF.md).

The two obstructions are different. A constant coordinate line gives an
interval-times-singletons counterexample. If the coordinate condition
holds but all three Jacobians vanish, Q has additive polynomial structure;
a base-27 Cantor construction gives three factors of dimension 2/3 with
image dimension at most log(25)/log(27), strictly below one.

This is a structural clarification of the quantifiers in a quadratic
Falconer-type image bound. The positive-factor bound, coefficient-map rank
principle, sharp planar projection theorem and collapsing example are
credited to the literature in [SOURCES.md](SOURCES.md). In particular,
Pham's later paper already gives Q=x(y+z), A={0}, B=C=[0,1]. We do not claim
that counterexample or a new projection estimate. The specific contribution
is the necessary-and-sufficient test for the universal compact-product
statement, including zero-dimensional factors and additive polynomials.
This does not decide Falconer's Euclidean distance conjecture.

## Reproduce the exact algebra checks

Python 3.11 or later; standard library only; no installation or network:

    python3 discrete_geometry/quadratic_universal_dimension_criterion/verify.py
    python3 -O discrete_geometry/quadratic_universal_dimension_criterion/verify.py

Both commands must print the same JSON as [expected.json](expected.json).
The checker verifies the three Jacobian identities as identities in a
formal polynomial ring; tests rational constant-line witnesses and the
coefficient classification on a bounded coefficient grid; and checks the
Cantor digit addition with integer arithmetic. These are validation of the
algebra and explicit obstructions. The infinite-dimensional theorem relies
on the written proof, Frostman's lemma and Ren--Wang's projection theorem;
no computation proves those inputs. No solver, floating-point inference,
random input, hidden certificate or formal proof assistant is used.

From this directory, source integrity can be checked with:

    sha256sum -c SHA256SUMS

The main theorem is terminal at this scope. No higher-degree classification,
optimal image bound for each particular triple, or historical priority
claim is made. Independent review of this note is not yet available.
