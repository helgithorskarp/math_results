# Straight-chain odd21 unitization is three-chromatic and supports none of 48 long constraints

Exact scoped construction stop for the fixed 21-point
Ardal--Maňuch--Rosenfeld--Shelah--Stacho odd-distance spindle. Freeze one
auxiliary-point architecture: for every source constraint of length `d` in
`{1,3,5,7}`, insert the `d-1` internal points on its straight geodesic unit
chain. The intake cap is
`21+26(3-1)+14(5-1)+8(7-1)=177`. Exact collision merging in coordinates
`(a+b sqrt(85))+i(c sqrt(3)+d sqrt(255))` leaves 115 distinct physical points.
Complete all-pairs reconstruction checks 6,555 pairs and yields 219 unit
edges: 141 distinct intended chain segments and 78 incidental contacts.

The complete strict graph has chromatic number exactly three: source vertices
I1, I2, I3 form a unit triangle, and a supplied word properly three-colours
all 219 edges. More decisively, each of the 48 nonunit source constraints has
its own checked proper three-colouring of this same complete graph in which
its two source endpoints are equal. Hence none of the length-3, length-5 or
length-7 chains represents its intended inequality; only the seven already-
unit source constraints survive.

This retires exactly the straight-geodesic unit-chain design. It is not a
record candidate and excludes no other auxiliary gadget. Reproducible
standard-library package:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_odd21_geodesic_unitization_stop>.
Verified source commit:
`f86de68966eb6be461b0cfc1f0bf8d574c0b989e`. Run
`python3 -B hadwiger_nelson_odd21_geodesic_unitization_stop/verify.py
--check-expected` and `controls.py`. Complete-edge SHA-256:
`521d505641e25290471a6486edecb5b1984d267b414a7ab68616d61bccc7bda8`.
Normal and optimized verification agree, regeneration is byte-identical, and
five corruptions are rejected.
