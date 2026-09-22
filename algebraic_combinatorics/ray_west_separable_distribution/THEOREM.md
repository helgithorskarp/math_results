# The Ray--West correction on separable permutations

Let `Sep_n=Av_n(2413,3142)`.  For a permutation `pi` of length `n`, let
`j(pi)` be the Ray--West codimension-two correction, normalized by

```text
g_2(pi)=(n^4+2n^3+n^2+4n+4-2j(pi))/2.
```

Define the bivariate ordinary generating function

```text
J(z,u) = sum_{n>=1} sum_{pi in Sep_n} z^n u^{j(pi)}.
```

Put

```text
H=(1-uz)(1+z-2uz),        C=(1-u)z^2.
```

## Theorem

`J` is the unique formal series in `z Z[u][[z]]` satisfying

```text
H J^2 + ((z-1)H-2C)J + zH-2C = 0.                    (1)
```

In particular, the first coefficients are

```text
J = z + 2u z^2 + 6u^2 z^3
      + (8u^2+14u^3)z^4
      + (20u^2+40u^3+30u^4)z^5 + ... .
```

If `Pi_n` is uniformly random in `Sep_n`, then

```text
E[j(Pi_n)] = n/2 + O(1).                              (2)
```

More precisely, with `Delta=1-6z+z^2`, the total first-moment series is

```text
M(z) = d/du J(z,u) at u=1
     = z^2(3-z-sqrt(Delta)) / ((1-z)^2 sqrt(Delta)).  (3)
```

## Signed-Schroeder-tree marking lemma

Every separable permutation has a unique signed Schroeder decomposition tree:
internal nodes have at least two ordered children, signs are direct sum `+` or
skew sum `-`, and signs alternate down every branch.

In this tree, `j(pi)` is the number of the following local marked junctions,
summed recursively over all internal nodes:

- at a `+` node, two adjacent children are both decreasing permutations;
- at a `-` node, two adjacent children are both increasing permutations.

Indeed, iterate the committed direct-sum locality formula.  At a canonical
direct-sum node every child is sum-indecomposable.  Such a child has the right
or left descending endpoint anchor exactly when it is wholly decreasing: a
proper descending terminal or initial interval would itself be a nontrivial
direct-sum component.  Hence the junction term is one exactly for two adjacent
decreasing children.  Complementation gives the skew statement.

## Generating-function proof

Let `F` count trees whose root has a fixed sign.  Complementation exchanges the
two signs and preserves `j`, so both root signs have generating function `F`,
and

```text
J=z+2F.
```

At a `+` root, an allowed child is a leaf or a `-`-rooted tree.  Its generating
function is

```text
A=z+F.
```

The decreasing allowed children form the class consisting of exactly one
decreasing permutation in every positive size.  Its size-`r` member has
`j=r-1`, so

```text
D=z/(1-uz),             N=A-D.
```

The root is a sequence of at least two allowed children, with an extra factor
`u` for every adjacent `DD` pair.  If `E_D,E_N` count nonempty sequences ending
in the indicated type, then

```text
E_D = D(1+u E_D+E_N),
E_N = N(1+E_D+E_N).
```

Therefore their sum is

```text
T = (D+N+(1-u)DN)/(1-N-uD-(1-u)DN),
```

and `F=T-A`, because root arity one must be removed.  Substituting
`A=z+F`, `D=z/(1-uz)`, and `J=z+2F`, then clearing denominators, gives (1).
The coefficient of `J` at `z=0` is `-1`, proving uniqueness recursively.

## First moment and asymptotics

At `u=1`, equation (1) reduces to

```text
J^2+(z-1)J+z=0,
J(z,1)=(1-z-sqrt(Delta))/2,
```

the usual nonempty large-Schroeder generating function.  Differentiating (1)
with respect to `u` and then setting `u=1` gives (3).

Let `rho=3-2sqrt(2)`.  Standard square-root singularity transfer gives

```text
[z^n]J(z,1)
  ~ sqrt(1-rho^2)/(4sqrt(pi)) rho^{-n} n^{-3/2},

[z^n]M(z)
  ~ rho^2(3-rho)/((1-rho)^2 sqrt(1-rho^2)sqrt(pi))
     rho^{-n} n^{-1/2}.
```

Their ratio is `(1/2)n+O(1)`, since

```text
4rho^2(3-rho)/((1-rho)^2(1-rho^2)) = 1/2.
```

This proves (2).

## Evidence and scope

The verifier solves (1) through degree 30 and checks (3) coefficientwise.  An
independent definition-level audit enumerates every separable permutation
through length seven and recomputes `j` from the original active-insertion
definition; all 2,321 objects agree with the tree statistic and with (1).

The universal result rests on the displayed combinatorial proof.  The audit
uses exact Python integers and no solver, randomness, floating point, or
external data.  The theorem is restricted to separable permutations; it is not
a new intrinsic formula for arbitrary permutations and does not address
codimension three.
