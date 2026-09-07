# Identical-block normalization theorem

Fix any of the 60 h3835 branches and distinguish its first red four-clique as
the root. Partition the remaining eleven blocks by their complete fixed atom
type: `R4`, `B4`, `R3`, `B3`, `E3`, or `P3`.

## Block action

Within one type class, any permutation of whole blocks is a physical vertex
relabeling. It preserves every fixed internal edge because the atom types are
identical. Transporting all incident cross edges gives a bijection on the 846
free physical edge assignments. The red/blue condition on every five-set is
invariant under this vertex permutation.

The h3835 root clauses sort vertices inside each child block by their four-bit
adjacency signatures to the root. Permuting whole child blocks transports each
complete root matrix and therefore preserves these per-block inequalities.
Consequently, the base branch formula is invariant under permutations inside
each nonroot identical-type class.

For each child block, form its key by listing its already sorted root
signatures from first vertex to last, with each four-bit integer written most
significant bit first. Permute every identical-type block class so that these
keys are nonincreasing. Every finite list admits such an ordering. Therefore
every orbit of base-formula assignments has at least one representative that
satisfies all adjacent key comparisons.

The converse is immediate because the normalized formula contains every base
clause. Thus the base branch formula is satisfiable if and only if its
identical-block normalized formula is satisfiable. This holds separately for
all 60 h3835 branches and preserves the unconditional target-class cover.

This argument claims an orbit representative, not a free group action or an
exact division of the retained-state count. Equal block keys and other
stabilizers can leave multiple normalized representatives.

## Comparator encoding

For two equal-length bit vectors `x` and `y`, written most significant bit
first, let `e_i` mean that positions before `i` agree. The forced-true h3835
variable is `e_0`. At every position the clause

```text
not e_i or x_i or not y_i
```

forbids the first difference `x_i=0, y_i=1`. Five Tseitin clauses define
`e_(i+1)` exactly as `e_i and (x_i equals y_i)`. Hence the clauses have a unique
auxiliary extension exactly when `x >= y` lexicographically.

`controls.py` exhaustively tests every input and every auxiliary assignment for
bit lengths one through five and separately checks the signature-to-bit order.
`interface_audit.py` integrates the construction with all 60 reviewed branch
types. `audit.py`, importing no h3835 or normalization module, reconstructs the
entire `r7-s4-t3` DIMACS stream literal by literal.

For `r7-s4-t3`, five adjacent comparisons sort six 16-bit `R4` keys and four
comparisons sort five 12-bit `R3` keys. Their block permutation group has order
`6! * 5! = 86400`. The encoding uses 119 auxiliary prefix variables and 723
clauses.
