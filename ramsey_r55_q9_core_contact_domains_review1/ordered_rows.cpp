// Independent h4059 census: ordered row triples, no S4 quotient or column DFS.
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct BitSet128 {
    std::uint64_t low = 0;
    std::uint64_t high = 0;
};

BitSet128 intersect(BitSet128 a, BitSet128 b) {
    return {a.low & b.low, a.high & b.high};
}

void insert(BitSet128& bits, unsigned value) {
    if (value < 64) bits.low |= std::uint64_t{1} << value;
    else bits.high |= std::uint64_t{1} << (value - 64);
}

std::uint64_t cardinality(BitSet128 bits) {
    return std::popcount(bits.low) + std::popcount(bits.high);
}

using Graph = std::array<std::array<unsigned, 7>, 7>;

void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

Graph parse_graph6(const std::string& line) {
    require(line.size() == 5 && line.front() == 'F', "graph6 shape");
    std::array<unsigned, 24> bits{};
    unsigned position = 0;
    for (unsigned k = 1; k < line.size(); ++k) {
        unsigned value = static_cast<unsigned char>(line[k]);
        require(value >= 63 && value <= 126, "graph6 character");
        value -= 63;
        for (int shift = 5; shift >= 0; --shift) bits[position++] = (value >> shift) & 1U;
    }
    require(bits[21] == 0 && bits[22] == 0 && bits[23] == 0, "graph6 padding");
    Graph graph{};
    position = 0;
    for (unsigned v = 1; v < 7; ++v) {
        for (unsigned u = 0; u < v; ++u) {
            graph[u][v] = graph[v][u] = bits[position++];
        }
    }
    for (unsigned a = 0; a < 7; ++a)
        for (unsigned b = a + 1; b < 7; ++b)
            for (unsigned c = b + 1; c < 7; ++c)
                for (unsigned d = c + 1; d < 7; ++d) {
                    unsigned red = graph[a][b] + graph[a][c] + graph[a][d]
                                 + graph[b][c] + graph[b][d] + graph[c][d];
                    require(red != 0 && red != 6, "core is not Ramsey(4,4)");
                }
    return graph;
}

std::array<std::uint64_t, 2> count_contacts(const Graph& graph) {
    std::vector<unsigned> edges;
    std::vector<unsigned> triangles;
    std::array<unsigned, 2> selected{};
    unsigned selected_count = 0;
    unsigned used = 0;
    for (unsigned u = 0; u < 7; ++u) {
        for (unsigned v = u + 1; v < 7; ++v) {
            if (!graph[u][v]) continue;
            unsigned edge = (1U << u) | (1U << v);
            edges.push_back(edge);
            if ((used & edge) == 0) {
                if (selected_count < 2) selected[selected_count] = edge;
                ++selected_count;
                used |= edge;
            }
            for (unsigned w = v + 1; w < 7; ++w) {
                if (graph[u][w] && graph[v][w]) triangles.push_back(edge | (1U << w));
            }
        }
    }
    require(selected_count >= 2, "greedy matching too short");

    std::array<bool, 128> independent{};
    std::array<bool, 128> triangle_free{};
    std::array<BitSet128, 128> pair_allowed{};
    std::array<BitSet128, 128> triple_allowed{};
    std::array<BitSet128, 128> empty_allowed{};
    std::array<unsigned, 128> type{};
    std::array<BitSet128, 4> type_rows{};

    for (unsigned subset = 0; subset < 128; ++subset) {
        independent[subset] = true;
        triangle_free[subset] = true;
        for (unsigned edge : edges) {
            if ((subset & edge) == edge) independent[subset] = false;
        }
        for (unsigned triangle : triangles) {
            if ((subset & triangle) == triangle) triangle_free[subset] = false;
        }
        type[subset] = static_cast<unsigned>((subset & selected[0]) == selected[0])
                     | (static_cast<unsigned>((subset & selected[1]) == selected[1]) << 1);
        insert(type_rows[type[subset]], subset);
    }

    for (unsigned fixed = 0; fixed < 128; ++fixed) {
        for (unsigned row = 0; row < 128; ++row) {
            unsigned common = fixed & row;
            if (triangle_free[common]) insert(pair_allowed[fixed], row);
            if (independent[common]) insert(triple_allowed[fixed], row);
            if (common == 0) insert(empty_allowed[fixed], row);
        }
    }

    std::uint64_t plain = 0;
    std::uint64_t joint = 0;
    for (unsigned x = 0; x < 128; ++x) {
        for (unsigned y = 0; y < 128; ++y) {
            unsigned xy = x & y;
            if (!triangle_free[xy]) continue;
            for (unsigned z = 0; z < 128; ++z) {
                unsigned xz = x & z;
                unsigned yz = y & z;
                unsigned xyz = xy & z;
                if (!triangle_free[xz] || !triangle_free[yz] || !independent[xyz]) continue;
                BitSet128 candidates = intersect(pair_allowed[x], pair_allowed[y]);
                candidates = intersect(candidates, pair_allowed[z]);
                candidates = intersect(candidates, triple_allowed[xy]);
                candidates = intersect(candidates, triple_allowed[xz]);
                candidates = intersect(candidates, triple_allowed[yz]);
                candidates = intersect(candidates, empty_allowed[xyz]);
                std::uint64_t accepted = cardinality(candidates);
                plain += accepted;

                // A selected-edge augmentation needs exactly two e-only rows
                // and two f-only rows. Local validity already bounds each
                // selected edge's common-neighbour set by two block rows.
                std::array<unsigned, 3> first{type[x], type[y], type[z]};
                bool pure = true;
                unsigned e_only = 0;
                for (unsigned value : first) {
                    pure = pure && (value == 1 || value == 2);
                    e_only += value == 1;
                }
                if (pure && e_only == 2) accepted -= cardinality(intersect(candidates, type_rows[2]));
                if (pure && e_only == 1) accepted -= cardinality(intersect(candidates, type_rows[1]));
                joint += accepted;
            }
        }
    }
    require(joint > 0 && joint <= plain && plain <= 170859375ULL, "contact count bounds");
    return {plain, joint};
}

int main(int argc, char** argv) {
    try {
        require(argc == 3, "usage: ordered_rows catalogue.g6 output.tsv");
        std::ifstream input(argv[1]);
        require(static_cast<bool>(input), "catalogue open");
        std::vector<Graph> graphs;
        std::string line;
        while (std::getline(input, line)) graphs.push_back(parse_graph6(line));
        require(graphs.size() == 362, "catalogue record count");
        std::ofstream output(argv[2]);
        require(static_cast<bool>(output), "output open");
        auto start = std::chrono::steady_clock::now();
        for (unsigned index = 0; index < graphs.size(); ++index) {
            auto counts = count_contacts(graphs[index]);
            output << index << '\t' << counts[0] << '\t' << counts[1] << '\n';
        }
        require(static_cast<bool>(output), "output write");
        double seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
        std::cout << "{\"status\":\"ORDERED_ROW_CENSUS_COMPLETE\",\"records\":362,\"ordered_triples\":759169024,\"seconds\":"
                  << seconds << "}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
