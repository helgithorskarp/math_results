# Failure of the legal-gap-set state

Status: explicit obstruction to one proposed compression, awaiting team review with the kernel packet. It is not an obstruction to an exponential bound, a lower-bound construction, or the agreed growth target.

Proposed state: at a fixed size n, remember only the set G(p) of legal maximum-insertion gaps. Proposed transition: G(p) plus a chosen gap g determines G(insert_max(p,g)).

This transition claim fails already at size 2. The parents 12 and 21 both avoid boxed 2143. Each has legal gaps {0,1,2}, since every child has only three entries. Choose gap 2 in both parents. Their children are respectively 123 and 213, both avoiding.

Inserting 4 in the four gaps of 123 gives 4123, 1423, 1243, 1234. None is 2143, so G(123)={0,1,2,3}. Inserting 4 in the four gaps of 213 gives 4213, 2413, 2143, 2134. Only gap 2 is forbidden, so G(213)={0,1,3}. At length 4, containing boxed 2143 is exactly being the permutation 2143, making every check explicit from the definition.

Thus identical current states and the same insertion gap yield different next states. There can be no deterministic transition on this proposed state alone. Sizes 0 and 1 each contain only one parent permutation, so size 2 is minimal for a same-size collision. The claim about minimality concerns this proposed state, not a larger family of compressed states.

state_obstruction.json preserves the exact parents, child permutations and legal-gap sets. The independent definition-based argument above supplies the mathematical certificate without trusting the nearest-greater implementation. The state may need to retain additional order/tree boundary information; no sufficient replacement or asymptotic entropy bound is asserted yet.
