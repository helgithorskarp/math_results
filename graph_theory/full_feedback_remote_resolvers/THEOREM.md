# A remote-resolver theorem for independent substitutions

All graphs below are finite, simple, undirected, and connected.  In the
full-feedback directional localization game, probing `x` against a robber at
`y != x` returns

\[
 D_H(x,y)=\{z\in N_H(x):d_H(z,y)=d_H(x,y)-1\};
\]

probing the robber's vertex returns `{x}`.  After each nonwinning response the
robber may stay or traverse one edge.

For a vertex `p` of a graph `G`, put

\[
 R_p=\{p\}\cup(V(G)\setminus N_G[p])
\]

and define the **remote signature**

\[
 F_p(q)=
 \begin{cases}
 N_G(p),&q=p,\\
 D_G(p,q),&q\in V(G)\setminus N_G[p].
 \end{cases}
\]

Call `p` a **remote resolver** when `F_p` is injective on `R_p`.

Let

\[
 X=G[\overline K_{m_v}:v\in V(G)]
\]

denote the independent substitution in which `v` is replaced by an independent
module `M_v` of size `m_v`, with all edges between `M_u` and `M_v` precisely
when `uv` is an edge of `G`.

## Theorem 1 (exact first-probe criterion)

Suppose every `m_v >= 2`, and fix a clone `x in M_p`.  The response to the
probe at `x` either locates the robber immediately or uniquely identifies the
robber's module for every initial location if and only if `p` is a remote
resolver.

### Proof

There are four possible positions for the robber.

1. At `x`, the response is `{x}` and the robber is located.
2. At another vertex of `M_p`, the distance is two and the response is
   `union(M_s : s in N_G(p))`.
3. At a vertex `y in M_q` with `q in N_G(p)`, the response is the singleton
   `{y}`, so the robber is located.
4. At a vertex of `M_q` with `q` outside `N_G[p]`, the response is
   `union(M_s : s in D_G(p,q))`.

The modules are pairwise disjoint and nonempty, so two union responses are
equal exactly when their sets of quotient indices are equal.  Every such union
has at least two vertices because every module has size at least two, and hence
it cannot equal an adjacent-module singleton response.  Thus injectivity of
`F_p` gives module identification.

Conversely, if two values of `F_p` coincide, select arbitrary clones in the two
corresponding remote modules; when one index is `p`, select a clone distinct
from `x`, which exists because `m_p >= 2`.  Those two targets lie in different
modules and give the same response.  Module identification fails.  This proves
both directions.  QED

## Theorem 2 (one-cop consequence)

If `G` has a remote resolver and every `m_v >= 2`, then

\[
 \zeta_D^*(X)=1.
\]

One cop wins in at most `1 + max_v m_v` rounds.

### Proof

Probe a clone in a remote-resolving module `M_p`.  By Theorem 1 the robber is
located immediately or his module `M_q` is known.  After recontamination, the
territory is contained in `M_q` together with its neighboring modules.

Now probe the vertices of `M_q` one at a time, never repeating one.  A robber
in a neighboring module produces his own vertex as a singleton response and
is located.  A robber at the probed vertex is likewise located.  The only
remaining response is the common response

\[
 \bigcup_{s\in N_G(q)}M_s,
\]

which certifies that the robber occupies some other, as-yet-unprobed vertex of
`M_q`.  On this continuing branch the robber can stay or enter a neighboring
module, but cannot move to another vertex of `M_q`, since `M_q` is independent.
Consequently a cleared vertex of `M_q` never reappears on the continuing
branch.  The next probe either locates a robber who left `M_q` or clears one
more possible clone.  After at most `m_q` scan probes the robber is located.
Including the initial probe gives the stated bound.  Since `X` has more than
one vertex, zero cops cannot locate the robber, so the value is exactly one.
QED

## Proposition 3 (cycle classification)

Every vertex of `C_n` is a remote resolver exactly when `n` is 3 or 5.

### Proof

For `C_3`, the remote domain is just `{p}`.  For `C_5`, label the vertices
cyclically as `0,1,2,3,4` and take `p=0`; the signatures on `{0,2,3}` are,
respectively, `{1,4}`, `{1}`, and `{4}`.

If `n >= 4` is even, the antipode of `p` has both neighbors of `p` as first
steps on shortest paths, so its signature equals `F_p(p)=N(p)`.  If `n >= 7`
is odd, the vertices at clockwise distances two and three from `p` are both
remote and both have the singleton clockwise neighbor as their signature.
These collisions exclude all other cycles.  QED

## Corollary 4 (strict decrease under false-twin replication)

For arbitrary integers `m_0,...,m_4 >= 2`,

\[
 \zeta_D^*\!\left(C_5[\overline K_{m_0},\ldots,
 \overline K_{m_4}]\right)=1,
\]

whereas `zeta_D^*(C_5)=2`.

### Proof

The blow-up value follows from Proposition 3 and Theorem 2.  For completeness,
two simultaneous probes at consecutive vertices `0,1` locate a stationary
target in one round: the five ordered responses are

```text
target 0: ({0}, {0})
target 1: ({1}, {1})
target 2: ({1}, {2})
target 3: ({4}, {2})
target 4: ({4}, {0})
```

so they are pairwise distinct.

For the one-cop lower bound, suppose before a probe that the territory contains
four consecutive vertices.  Directly checking the five possible probe
vertices shows that one response class contains two adjacent vertices among
that block; the table is audited by `verify.py`.  The closed neighborhood of
an adjacent pair in `C_5` is again a block of four consecutive vertices.
Thus the robber can maintain this invariant after every recontamination phase,
and can never be uniquely located.  The full-feedback number of `C_5` is two.
QED

This is a genuine nonmonotonicity phenomenon: replacing every vertex by two or
more false twins can reduce the full-feedback directional localization number.
It also explains why an independent-substitution construction cannot in
general lift a lower bound from its quotient.
