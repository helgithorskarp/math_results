# Provenance

- Campaign: Hadwiger--Nelson, strict sub-509 record objective.
- Lane: researcher 3, exact globally coupled plane geometry.
- Frozen on: 2026-09-16 UTC.
- Entry theorem/package:
  `hadwiger_nelson_polygon_difference_spectra`, source commit
  `883ef03fd8550d5ee4f34ef26a7ea1539048aa97`.
- Entry package hashes used during selection:
  - `README.md`: `0ae26cfde59fcf68dfcc0fb26494cc7116f6f6f4fd3b64cfb11f61a48691e4ae`
  - `verify.py`: `8d8ba582167793038cab8ab43120dc238eebd477249fe8c69d12992a0b44b3aa`
  - `certificate.json`: `45a928f317553fd80ea95e992cf38105a50ad12da8e3e4f22bec69f74a33926e`
- Selection rule: normalize and pointwise identify the canonical first
  nonbipartite-shell oriented edge from each of the fixed full clouds `P13`
  and `P14`; then close every private cross unit edge by both equilateral
  apices. Geometry and cap were fixed before querying colourability.
- Fast proposal arithmetic: python-flint 0.7.0 exact rational polynomial
  arithmetic in `Q(zeta_546)`.
- Exploratory chromatic proposal: python-sat 1.9.dev15 / CaDiCaL 1.9.5.
- Published proof boundary: neither dependency is trusted. The standard-
  library checker reconstructs the geometry, verifies the literal positive
  three-colour word, and checks an explicit odd cycle.
- Record status: no record improvement; exact scoped stop.
