# Provenance and independence

## Reviewed target

- Branch path:
  <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_parts503_double_triangle_stop>
- Exact revision: `05f007b2fd745420c57b8e55d7f5a59609e01b6b`.
- Target certificate SHA-256:
  `1deac6dde026da4415c3363fe5a2941e0024aedf1e989caa6861aebefee45781`.
- Target expected-output SHA-256:
  `cdec2392b0ea19d7686cf63f17c115c48d455551eea15ea5793f446a3e873ad3`.
- Target manifest SHA-256:
  `f7f721dbaf0f8f826a122182be4a596021545a104e1224fc6d8ceeff3d73b0ce`.
- Target checker SHA-256:
  `c693092b6c6121b444d2f34093c2e676aa73cb8cc05a2e340ece2c22d2ebc559`.

Normal, optimized and emitted target runs produced identical theorem output.
The emitted selected geometry is 43,937 bytes and is not needed by this
review package.

## Public inputs

| Repository path | SHA-256 | Last modifying revision |
|---|---|---|
| `hadwiger_nelson_parts509_fold264_438_stop/points.tsv` | `f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50` | `bdfebeb0ac5c0c8e64066f414164b07084d6618b` |
| `hadwiger_nelson_parts509_swap_closure/completion_points.json` | `b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6` | `1f68cef24f305fb6058768c277a3323652a22028` |
| `hadwiger_nelson_parts509_degree4_list_kernel/certificate.json` | `d0d88c667525589539926efbec124fc697059a6606cde110e7cd53c0b7dbb4e6` | `f5868a47bbe580dff68dcb374de560e53b21c84d` |
| `hadwiger_nelson_parts509_pair_closure/ambient_w3_edges.json` | `960d32618cf5afd013f29b3f6e2e85cb6a35e7d6b8884a6680a657f8e6c46f92` | `50d4b7e186cd4bd8588762eae984e24da49b0858` |

The review checks these bytes before use. It does not duplicate the roughly
744 KB of raw public inputs; reproduction therefore requires a full repository
checkout. No completeness theorem beyond the finite coordinate lists is
imported.

## Algorithmic independence

The target public checker rejects most candidate pairs through a homomorphism
to a finite field, then applies generic gcd/squarefree-radicand products. It
enumerates double triangles by shared centres and tests list extension with a
static-order recursive search. The original author selector used the cached
ambient edge table and a dynamic list search.

The reviewer applies no modular filter. It scans every pair using direct
multiquadratic coefficient formulas, enumerates all pool triangles before
pairing them, and tests extension by filtering the literal `4^5` word set.
Complete ambient edges agree entry for entry; two independently expressed
family enumerators agree; and the full case-relation histogram matches the
target. The review also supplies new hashes for the complete family relation
and positive witnesses and a fresh 508-symbol word.

No private source, Discovery ledger, generated geometry dump, SAT solver,
binary, or large unpublished artifact is required.
