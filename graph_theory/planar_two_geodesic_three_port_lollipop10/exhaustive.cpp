#include <algorithm>
#include <array>
#include <cstdint>
#include <functional>
#include <iostream>
#include <vector>

using namespace std;

constexpr int N = 11;
constexpr int INF = 1000;
constexpr int EDGE_COUNT = 11;
using Mask = uint16_t;
using Graph = array<vector<pair<int, int>>, N>;

array<pair<int, int>, EDGE_COUNT> fragment_edges() {
    array<pair<int, int>, EDGE_COUNT> edges{};
    for (int i = 0; i < 10; ++i) edges[i] = {i, (i + 1) % 10};
    edges[10] = {0, 10};
    return edges;
}

void add(Graph& graph, int u, int v, int weight) {
    graph[u].push_back({v, weight});
    graph[v].push_back({u, weight});
}

Graph make_graph(int fragment_mask, int x, int y, int z) {
    Graph graph;
    const auto edges = fragment_edges();
    for (int i = 0; i < EDGE_COUNT; ++i) {
        if (fragment_mask & (1 << i)) add(graph, edges[i].first, edges[i].second, 1);
    }
    if (x < INF) add(graph, 1, 3, x);
    if (y < INF) add(graph, 1, 5, y);
    if (z < INF) add(graph, 3, 5, z);
    return graph;
}

Mask large_component(int fragment_mask) {
    auto graph = make_graph(fragment_mask, INF, INF, INF);
    Mask remaining = (1 << N) - 1;
    while (remaining) {
        const int start = __builtin_ctz(remaining);
        vector<int> stack{start};
        Mask part = 1 << start;
        remaining &= ~(1 << start);
        while (!stack.empty()) {
            const int u = stack.back();
            stack.pop_back();
            for (const auto& [v, weight] : graph[u]) {
                (void)weight;
                if (remaining & (1 << v)) {
                    remaining &= ~(1 << v);
                    part |= 1 << v;
                    stack.push_back(v);
                }
            }
        }
        if (__builtin_popcount(part) >= 6) return part;
    }
    return 0;
}

bool coverable(const Graph& graph, Mask target) {
    if (!target) return true;
    int dist[N][N];
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) dist[i][j] = (i == j ? 0 : INF);
        for (const auto& [v, weight] : graph[i]) dist[i][v] = min(dist[i][v], weight);
    }
    for (int k = 0; k < N; ++k)
        for (int i = 0; i < N; ++i)
            for (int j = 0; j < N; ++j)
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);

    array<bool, 1 << N> seen{};
    vector<Mask> masks;
    for (int source = 0; source < N; ++source) {
        if (!(target & (1 << source))) continue;
        function<void(int, Mask)> visit = [&](int u, Mask mask) {
            if (target & (1 << u)) {
                const Mask trace = mask & target;
                if (!seen[trace]) {
                    seen[trace] = true;
                    masks.push_back(trace);
                }
            }
            for (const auto& [v, weight] : graph[u]) {
                if (dist[source][u] + weight == dist[source][v]) {
                    visit(v, static_cast<Mask>(mask | (1 << v)));
                }
            }
        };
        visit(source, 1 << source);
    }
    for (Mask a : masks)
        for (Mask b : masks)
            if ((a | b) == target) return true;
    return false;
}

int main() {
    const Mask negative_target = large_component(2043);
    if (negative_target != 2047 ||
        coverable(make_graph(2043, 2, 3, INF), negative_target)) {
        cerr << "negative control failed\n";
        return 1;
    }

    array<Mask, 1 << EDGE_COUNT> target{};
    int relevant = 0;
    for (int mask = 0; mask < (1 << EDGE_COUNT); ++mask) {
        target[mask] = large_component(mask);
        relevant += target[mask] != 0;
    }
    uint64_t checked = 0;
    for (int x = 2; x <= 11; ++x)
        for (int y = 4; y <= 11; ++y)
            for (int z = 2; z <= 11; ++z)
                for (int mask = 0; mask < (1 << EDGE_COUNT); ++mask) {
                    if (!target[mask]) continue;
                    const int xx = (x == 11 ? INF : x);
                    const int yy = (y == 11 ? INF : y);
                    const int zz = (z == 11 ? INF : z);
                    if (!coverable(make_graph(mask, xx, yy, zz), target[mask])) {
                        cerr << "FAIL x=" << x << " y=" << y << " z=" << z
                             << " fragment_mask=" << mask << " target=" << target[mask] << '\n';
                        return 2;
                    }
                    ++checked;
                }
    cout << "profiles=800 fragment_masks=2048 relevant_fragment_masks=" << relevant
         << " checked_large_components=" << checked
         << " short_route_control=FAILS_COVER PASS\n";
}
