# Proof details

Let the exact source coordinates be `p_i=(x_i,y_i)` and their rational
midpoints be `m_i`.  The imported contraction proof gives

```text
|x_i-m_i,x| <= r,  |y_i-m_i,y| <= r,  r=10^-25
```

coordinatewise.  The source verifier also proves that its complete strict
graph is four-chromatic and that `p_0=(0,0)` exactly.

For a formal address `a=(i,j)`, put `P_a=p_i-p_j` and
`M_a=m_i-m_j`.  Each coordinate of `P_a-M_a` has absolute value at most
`2r`.  Therefore an actual equality `P_a=P_b` implies that both coordinates
of `M_a-M_b` have absolute value at most `4r`.  The verifier takes connected
components of all pairs satisfying that necessary condition.  Thus every
actual collision is inside one component.  It also checks directly that the
squared-distance upper bound of every same-component pair is below one.

For different formal addresses `a,b`, write the rational midpoint difference
as `(dx,dy)`.  Each coordinate of the exact difference varies by at most
`e=4r`.  Expanding both squares gives

```text
| |P_a-P_b|^2 - (dx^2+dy^2) |
  <= 2e(|dx|+|dy|) + 2e^2.
```

Call the right-hand side `E`.  For addresses in different components the
verifier proves `dx^2+dy^2>E`, excluding equality.  If

```text
|dx^2+dy^2-1| <= E,
```

their two components receive a conservative edge.  Otherwise the pair is
rigorously nonunit.  Hence every actual unit pair maps to an edge of the
conservative graph, while an actual collision maps to one vertex.  The stored
word is checked on every conservative edge and so defines a proper
four-colouring of the complete actual unit graph.

The 23 diagonal addresses `(i,i)` are all exactly zero.  Merging only these
gives the physical upper bound `529-22=507`.  The different-component
separation proof gives the lower bound of 433 distinct points.  Finally,
`{p_i-p_0}` is the exact source itself, so the graph is not three-colourable.
Together with the conservative four-colouring, its ordinary chromatic number
is exactly four.

The SAT solver in `produce.py` supplies only the displayed positive word.
`verify.py` checks that word literally and makes no use of a solver answer.

