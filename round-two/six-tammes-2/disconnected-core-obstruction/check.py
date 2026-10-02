"""Check the literal core bookkeeping, not the geometric reduction."""
from itertools import combinations
import json
from pathlib import Path


def check():
    data = json.loads(Path(__file__).with_name("CORE.json").read_text())
    labels = data["labels"]
    if len(labels) != 12 or len(set(labels)) != 12:
        raise ValueError("twelve distinct labels required")
    contacts = [tuple(e) for e in data["contacts"]]
    if len(contacts) != 20 or len(set(contacts)) != 20:
        raise ValueError("twenty distinct contacts required")
    if any(len(e) != 2 or e[0] >= e[1] or not set(e) <= set(labels)
           for e in contacts):
        raise ValueError("invalid contact pair")
    triangles = {k: tuple(v) for k, v in data["triangles"].items()}
    if len(triangles) != 8 or len(set(triangles.values())) != 8:
        raise ValueError("eight distinct triangles required")
    if any(len(t) != 3 or tuple(sorted(set(t))) != t for t in triangles.values()):
        raise ValueError("invalid triangle")
    triangle_edges = {e for t in triangles.values() for e in combinations(t, 2)}
    if not triangle_edges <= set(contacts):
        raise ValueError("missing prescribed triangle contact")
    support = sorted({v for t in triangles.values() for v in t})
    if support != labels:
        raise ValueError("triangle support differs from twelve-point labels")
    adjacency = {k: [] for k in triangles}
    for a, b in combinations(triangles, 2):
        if len(set(triangles[a]) & set(triangles[b])) == 2:
            adjacency[a].append(b)
            adjacency[b].append(a)
    if any(not neighbors for neighbors in adjacency.values()):
        raise ValueError("isolated selected triangle")
    if len(triangle_edges) != 18:
        raise ValueError("eighteen intracluster contacts required")
    return {
        "kind": "finite_bookkeeping_only",
        "distinct_labels": len(labels),
        "distinct_contacts": len(contacts),
        "distinct_triangles": len(triangles),
        "triangle_contact_count": len(triangle_edges),
        "triangle_vertex_support": support,
        "selected_face_edge_adjacency": adjacency,
        "unused_cross_contacts": sorted(set(contacts) - triangle_edges),
        "geometric_proof_checked_by_code": False,
        "parent_certificate_executed": False,
    }


if __name__ == "__main__":
    print(json.dumps(check(), sort_keys=True, indent=2))
