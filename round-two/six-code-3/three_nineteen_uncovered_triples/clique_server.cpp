// Independent maximal-clique enumeration; no coloring bounds.
#include <algorithm>
#include <bitset>
#include <chrono>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>

using Bits = std::bitset<256>;
using Clock = std::chrono::steady_clock;

struct Graph {
    int n;
    std::vector<Bits> adjacency;
};

struct Search {
    const Graph& graph;
    int target;
    unsigned long long nodes = 0, cap;
    int milliseconds;
    Clock::time_point started = Clock::now();
    std::set<std::vector<int>> solutions;

    void tick() {
        ++nodes;
        if (nodes>cap || Clock::now()-started > std::chrono::milliseconds(milliseconds))
            throw std::runtime_error("INCOMPLETE clique guard");
    }

    void subsets(const std::vector<int>& clique, std::size_t from, std::vector<int>& selected) {
        tick();
        if (static_cast<int>(selected.size()) == target) {
            auto result = selected;
            std::sort(result.begin(), result.end());
            solutions.insert(std::move(result));
            return;
        }
        for (std::size_t i=from; i<clique.size(); ++i) {
            if (clique.size()-i < static_cast<std::size_t>(target)-selected.size()) break;
            selected.push_back(clique[i]);
            subsets(clique,i+1,selected);
            selected.pop_back();
        }
    }

    void visit(std::vector<int>& chosen, Bits possible, Bits previous) {
        tick();
        if (chosen.size()+possible.count() < static_cast<std::size_t>(target)) return;
        if (possible.none()) {
            if (previous.none()) {
                std::vector<int> selected;
                subsets(chosen,0,selected);
            }
            return;
        }
        const auto all = possible | previous;
        int pivot=-1;
        std::size_t best=0;
        for (int v=0; v<graph.n; ++v) if (all[v]) {
            auto count=(graph.adjacency[v]&possible).count();
            if (pivot<0 || count>best) { pivot=v;best=count; }
        }
        const auto branches=possible & ~graph.adjacency[pivot];
        for (int v=0; v<graph.n; ++v) if (branches[v]) {
            chosen.push_back(v);
            visit(chosen,possible & graph.adjacency[v],previous & graph.adjacency[v]);
            chosen.pop_back();
            possible.reset(v); previous.set(v);
        }
    }
};

int main() {
    try {
        int graph_count;
        if (!(std::cin>>graph_count) || graph_count<1 || graph_count>2)
            throw std::runtime_error("invalid graph count");
        std::vector<Graph> graphs;
        for (int g=0; g<graph_count; ++g) {
            int n;
            if (!(std::cin>>n) || n<0 || n>256) throw std::runtime_error("invalid graph size");
            Graph graph{n,std::vector<Bits>(n)};
            for (int i=0; i<n; ++i) {
                int degree;
                if (!(std::cin>>degree) || degree<0 || degree>=n) throw std::runtime_error("invalid degree");
                int last=-1;
                for (int j=0; j<degree; ++j) {
                    int v;
                    if (!(std::cin>>v) || v<0 || v>=n || v<=last || v==i)
                        throw std::runtime_error("invalid neighbor list");
                    graph.adjacency[i].set(v);last=v;
                }
            }
            for (int i=0; i<n; ++i) for (int j=0; j<n; ++j)
                if (graph.adjacency[i][j]!=graph.adjacency[j][i])
                    throw std::runtime_error("asymmetric graph");
            graphs.push_back(std::move(graph));
        }
        int gid,target,count,milliseconds;
        unsigned long long cap;
        while (std::cin>>gid) {
            if (!(std::cin>>target>>cap>>milliseconds>>count) || gid<0 || gid>=graph_count ||
                target<1 || target>256 || cap<1 || cap>2000000 || milliseconds<1 || milliseconds>20000 ||
                count<0 || count>graphs[gid].n)
                throw std::runtime_error("invalid query");
            Bits possible;
            int last=-1;
            for (int i=0; i<count; ++i) {
                int v;
                if (!(std::cin>>v) || v<0 || v>=graphs[gid].n || v<=last)
                    throw std::runtime_error("invalid selected vertex");
                possible.set(v);last=v;
            }
            Search search{graphs[gid],target,0,cap,milliseconds,Clock::now(),{}};
            std::vector<int> chosen;
            search.visit(chosen,possible,Bits());
            std::cout << "{\"status\":\"COMPLETE\",\"nodes\":" << search.nodes << ",\"cliques\":[";
            bool first=true;
            for (const auto& clique:search.solutions) {
                if (!first) std::cout << ',';
                first=false;std::cout << '[';
                for (std::size_t i=0; i<clique.size(); ++i) {
                    if (i) std::cout << ',';
                    std::cout << clique[i];
                }
                std::cout << ']';
            }
            std::cout << "]}" << std::endl;
        }
        if (!std::cin.eof()) throw std::runtime_error("invalid trailing input");
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}
