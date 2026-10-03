"""Both-child exact receiving cover; actual antipodal contacts remove lambda and T."""
import geometry as g
Q, a = g.Q, g.a

def record(certificate):
    images = tuple(g.act(g.G, v) for v in g.V)
    seen_nodes, seen_leaves, records = set(), set(), []
    tree = certificate['width_cover']
    def visit(ref, poly):
        kind, index = ref
        if kind == 'node':
            g.require(0 <= index < len(tree['nodes']) and index not in seen_nodes,
                      'no missing, duplicate or ancestor split node')
            seen_nodes.add(index)
            node = tree['nodes'][index]
            w = g.dec(node['line'])
            values = [g.value(w, p) for p in poly]
            g.require(min(values) < 0 < max(values) and len(node['children']) == 2,
                      'nontrivial split with BOTH required closed children')
            left, right = g.clip(poly, w), g.clip(poly, tuple(-v for v in w))
            g.require(g.area(left) > 0 and g.area(right) > 0 and
                      g.area(left)+g.area(right) == g.area(poly), 'exact linear split checksum')
            visit(node['children'][0], left)
            visit(node['children'][1], right)
            return
        g.require(kind == 'leaf' and 0 <= index < len(tree['leaves']) and index not in seen_leaves,
                  'every leaf genuine and used exactly once')
        seen_leaves.add(index)
        leaf = tree['leaves'][index]
        g.require(poly == [g.dec(v) for v in leaf['poly']], 'entire original closed receiving leaf')
        edges, signs = leaf['original_edges'], leaf['signs']
        g.require(len(edges) == len(signs) == 3, 'three actual antipodal supports')
        vectors, contact_rows, stream, sums = [], [], [], []
        for (i, j), sign in zip(edges, signs):
            g.require(sign in (-1, 1) and 0 <= i < 60 and 0 <= j < 60 and i != j,
                      'actual original directed support edge and orientation')
            vectors.append(a.sub(g.V[j], g.V[i]))
            opposite = tuple(-x for x in g.V[i])
            g.require(g.V[i] in images and opposite in g.V and opposite in images,
                      'genuine positive and negative original source contacts')
            contact_rows.append([i, g.V.index(opposite), images.index(g.V[i]), images.index(opposite)])
        det = a.dot(vectors[0], a.cross(vectors[1], vectors[2]))
        g.require(det != 0, 'constant three-dimensional support-edge basis')
        for p in poly:
            heights = []
            for (i, j), sign in zip(edges, signs):
                m = a.scale(sign, a.cross(a.sub(g.V[j], g.V[i]), g.raw(p)))
                h = a.dot(m, g.V[i])
                g.require(a.dot(m, g.raw(p)) == 0 and h >= 0,
                          'physical projection support and nonnegative opposite height')
                for v in g.V:
                    stream.extend((h-a.dot(m, v), h+a.dot(m, v)))
                heights.append(h)
            sums.append(sum(heights, Q()))
        g.require(min(stream) >= 0 and min(sums) > 0,
                  'every actual original opposite support and strictly positive total width')
        records.append({'leaf': index, 'whole_closed_polygon': list(map(g.vec, poly)),
            'original_edges': edges, 'signs': signs, 'actual_spatial_preimages': contact_rows,
            'edge_basis_determinant': g.enc(det), 'original_support_controls': len(stream),
            'minimum_original_gap': g.enc(min(stream)), 'minimum_summed_height': g.enc(min(sums)),
            'complete_actual_support_stream_sha256': g.digest(list(map(g.enc, stream)))})
    visit(tree['root'], g.P)
    g.require(seen_nodes == set(range(len(tree['nodes']))) and
              seen_leaves == set(range(len(tree['leaves']))), 'complete exact tree, no omitted data')
    records.sort(key=lambda r: r['leaf'])
    return {'closed_split_nodes': len(seen_nodes), 'closed_receiving_leaves': len(seen_leaves),
            'actual_original_support_controls': sum(r['original_support_controls'] for r in records),
            'actual_original_spatial_preimages': 6*len(records), 'leaves': records,
            'complete_closed_width_cover_sha256': g.digest(records)}
