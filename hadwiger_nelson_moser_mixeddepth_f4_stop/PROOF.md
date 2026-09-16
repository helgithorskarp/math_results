# Proof and certificate outline

## Exact geometry

Represent a field element by four integer coefficients in the basis
`(1,sqrt(3),sqrt(11),sqrt(33))`; coordinates have common denominator 12.
The independent checker instead groups these as
`(a+b*sqrt(3))+(c+d*sqrt(3))*sqrt(11)` and implements the two nested quadratic
multiplications directly.

For a unit two-path `p-r-q`, the reflected point `z=p+q-r` satisfies

```text
z-p = q-r,       z-q = p-r.
```

Thus both generating contacts are unit. The checker nevertheless verifies
them algebraically for every route, collision-merges exact coordinate tuples,
and measures all contacts between each candidate and the old support. `F4`
keeps precisely the candidates with at least four such contacts. After each
step the checker discards route ownership and reconstructs all unordered unit
pairs from squared distances.

The two steps respectively inspect 283 and 430 distinct new candidates and
keep 99 and 168. This gives 115/447, 214/1,019 and 382/2,026 as the successive
point/edge counts. Exact set comparison with the accepted 398-point full stage
gives intersection 342, 40 final points outside it, and 56 full-stage points
absent from the final support.

## Chromatic decision

Let `Col4(A0)` be the full set of proper named four-colourings of the accepted
115-point source. The pass's success condition was

```text
no c in Col4(A0) extends to a proper four-colouring of A2.
```

The certificate supplies one proper word on all 382 vertices. Direct checking
against every one of the 2,026 reconstructed edges proves it proper; its first
115 symbols are checked against all 447 source edges. Hence that source word
extends and the universal zero-extension assertion is false. This witness is
a complete decision of the required zero-versus-nonzero predicate; no count
or enumeration of the remaining source relation is inferred.

For the lower chromatic bound, the original seven Moser points occur in `A0`
at the certificate's listed indices. Their induced graph has 11 edges, and
exhaustion of all `3^7=2,187` named three-colour words finds none proper.
Together with the four-word, this proves `chi(A2)=4`.

## Trust boundary

The proof trusts the hash-pinned accepted source coordinates, linear
independence of the multiquadratic basis, Python arbitrary-precision integer
arithmetic, complete finite loops, SHA-256 for stream identity, and ordinary
hardware. It uses no floating predicate, hidden graph file, SAT verdict, or
unverified non-four claim. It is an exact computational proof at its stated
scope, not a proof-assistant formalization or independent review.
