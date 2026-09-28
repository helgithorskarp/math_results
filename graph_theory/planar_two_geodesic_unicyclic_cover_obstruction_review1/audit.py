#!/usr/bin/env python3
"""Independent geodesic-pair audit of the isometric lollipop obstruction.

This script imports no research code. It enumerates every simple path, filters
by fresh BFS distances, and checks every pair of geodesic vertex sets.
"""

from collections import deque


def graphs(h):
    assert h >= 3
    m = 2*h + 3
    t, x, y = m, m+1, m+2
    full = [set() for _ in range(m+3)]

    def edge(u, v):
        assert u != v and v not in full[u]
        full[u].add(v)
        full[v].add(u)

    for i in range(m):
        edge(i, (i+1) % m)
    for u, v in ((0,t), (0,x), (2,x), (1,y), (3,y)):
        edge(u, v)
    deleted = [set(row) for row in full]
    deleted[1].remove(2)
    deleted[2].remove(1)
    assert sum(map(len, full))//2 == m+5
    return full, deleted, m


def distances(graph, start):
    values = [-1]*len(graph)
    values[start] = 0
    todo = deque([start])
    while todo:
        u = todo.popleft()
        for v in graph[u]:
            if values[v] < 0:
                values[v] = values[u]+1
                todo.append(v)
    return values


def geodesic_masks(graph):
    masks = set()
    simple_paths = 0
    for source in range(len(graph)):
        d = distances(graph, source)

        def visit(last, visited, length):
            nonlocal simple_paths
            simple_paths += 1
            if length == d[last]:
                masks.add(visited)
            for v in graph[last]:
                bit = 1 << v
                if not visited & bit:
                    visit(v, visited | bit, length+1)

        visit(source, 1 << source, 0)
    return masks, simple_paths


def components(graph, removed):
    unseen = {u for u in range(len(graph)) if not removed >> u & 1}
    answer = []
    while unseen:
        part = {unseen.pop()}
        todo = list(part)
        while todo:
            new = graph[todo.pop()] & unseen
            unseen -= new
            part |= new
            todo.extend(new)
        answer.append(part)
    return answer


def explicit_witness(h, m, deleted):
    t, x = m, m+1
    long = [0]+[m-i for i in range(1,2*h+1)]
    assert long[-1] == 3
    first = [long[i] for i in range(h,-1,-1)]+[1]
    second = [t,0,x,2,3]+[long[i] for i in range(2*h-1,h+1,-1)]
    for path in (first, second):
        assert len(path)==len(set(path))
        assert all(v in deleted[u] for u,v in zip(path,path[1:]))
        assert len(path)-1 == distances(deleted,path[0])[path[-1]]
    covered = (set(first)|set(second)) & set(range(m+1))
    assert covered == set(range(m+1))-{long[h+1]}
    return len(covered)


def main():
    total_pairs = 0
    for h in range(3,9):
        full, deleted, m = graphs(h)
        fragment = [row & set(range(m+1)) for row in full]
        for u in range(m+1):
            df, dc = distances(full,u), distances(fragment,u)
            assert df[:m+1] == dc[:m+1]
        assert len(components(deleted,(1<<(m+1))-1)) == 2
        assert len(components(deleted,(1<<(m+3))-1 ^ ((1<<(m+1))-1))) == 1
        masks, simple_count = geodesic_masks(deleted)
        target = (1<<(m+1))-1
        ordered = sorted(masks)
        optimum = max(((a|b)&target).bit_count()
                      for i,a in enumerate(ordered) for b in ordered[i:])
        assert optimum == explicit_witness(h,m,deleted) == m
        total_pairs += len(ordered)*(len(ordered)+1)//2
        if h == 3:
            assert simple_count == 452 and len(masks) == 85
            assert any(max((len(c) for c in components(deleted,a|b)),default=0)
                       <=len(deleted)//2 for a in masks for b in masks)
            full_masks,_ = geodesic_masks(full)
            assert any(max((len(c) for c in components(full,a|b)),default=0)
                       <=len(full)//2 for a in full_masks for b in full_masks)
        print(f'h={h} fragment={m+1} maximum_covered={optimum} '
              f'geodesic_masks={len(masks)}')
    print(f'pair_certificates_checked={total_pairs} PASS')


if __name__ == '__main__':
    main()
