// Independent direct-K5 audit of the Cyclic(43) exact-q=13 closure.
//
// Unlike both target programs, this checker enumerates every 5-subset.  Its
// red-edge count determines both whether the subset is monochromatic and
// whether one edge flip creates or destroys it.  Thus all 903 flip deltas
// are accumulated definition-first, without common-neighbour triangles.

#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

constexpr int N = 43;
constexpr int EDGE_COUNT = N * (N - 1) / 2;
constexpr int WORD_COUNT = 15;
constexpr int FIVE_SET_COUNT = 962598;

struct State {
    std::array<std::uint64_t, WORD_COUNT> words{};
    bool operator==(const State&) const = default;
};

struct StateLess {
    bool operator()(const State& left, const State& right) const {
        return left.words < right.words;
    }
};

struct StateHash {
    std::size_t operator()(const State& state) const {
        std::size_t value = 0x9e3779b97f4a7c15ULL;
        for (std::uint64_t word : state.words) {
            value ^= std::hash<std::uint64_t>{}(word) + 0x9e3779b97f4a7c15ULL
                + (value << 6) + (value >> 2);
        }
        return value;
    }
};

using FiveSet = std::array<std::uint16_t, 10>;

std::array<std::pair<int, int>, EDGE_COUNT> edges;
int edge_id[N][N];
std::array<unsigned char, EDGE_COUNT> seed_red{};

void require(bool condition, const std::string& message) {
    if (!condition) throw std::runtime_error(message);
}

std::string read_file(const std::string& path) {
    std::ifstream input(path);
    require(static_cast<bool>(input), "cannot open " + path);
    return std::string(
        std::istreambuf_iterator<char>(input),
        std::istreambuf_iterator<char>()
    );
}

std::size_t locate_key(const std::string& text, const std::string& key,
                       std::size_t start = 0) {
    const std::string quoted = "\"" + key + "\"";
    const std::size_t position = text.find(quoted, start);
    require(position != std::string::npos, "missing JSON key " + key);
    return position + quoted.size();
}

std::vector<std::vector<int>> parse_integer_matrix(
    const std::string& text, const std::string& key, std::size_t start = 0
) {
    std::size_t position = locate_key(text, key, start);
    position = text.find('[', position);
    require(position != std::string::npos, "missing array for " + key);
    int depth = 0;
    std::vector<int> row;
    std::vector<std::vector<int>> result;
    for (; position < text.size(); ++position) {
        const char symbol = text[position];
        if (symbol == '[') {
            ++depth;
            if (depth == 2) row.clear();
        } else if (symbol == ']') {
            if (depth == 2) result.push_back(row);
            --depth;
            if (depth == 0) return result;
            require(depth >= 0, "malformed array for " + key);
        } else if (depth == 2 && symbol >= '0' && symbol <= '9') {
            int value = 0;
            while (position < text.size() && text[position] >= '0'
                   && text[position] <= '9') {
                value = 10 * value + (text[position] - '0');
                ++position;
            }
            row.push_back(value);
            --position;
        }
    }
    throw std::runtime_error("unterminated array for " + key);
}

bool test_bit(const State& state, int edge) {
    return (state.words[edge / 64] >> (edge % 64)) & 1ULL;
}

void flip_bit(State& state, int edge) {
    state.words[edge / 64] ^= 1ULL << (edge % 64);
}

State make_state(const std::vector<int>& list) {
    State state;
    int previous = -1;
    for (int edge : list) {
        require(edge > previous && edge < EDGE_COUNT, "malformed edge list");
        flip_bit(state, edge);
        previous = edge;
    }
    return state;
}

std::vector<State> make_states(const std::vector<std::vector<int>>& rows) {
    std::vector<State> result;
    result.reserve(rows.size());
    for (const auto& row : rows) result.push_back(make_state(row));
    return result;
}

void initialize_edges() {
    int number = 0;
    for (int u = 0; u < N; ++u) {
        for (int v = u + 1; v < N; ++v) {
            edges[number] = {u, v};
            edge_id[u][v] = edge_id[v][u] = number;
            const int distance = std::min(v - u, N - (v - u));
            const std::set<int> red_distances = {
                1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21
            };
            seed_red[number] = red_distances.contains(distance);
            ++number;
        }
    }
    require(number == EDGE_COUNT, "edge table size mismatch");
}

std::vector<FiveSet> initialize_five_sets() {
    std::vector<FiveSet> result;
    result.reserve(FIVE_SET_COUNT);
    for (int a = 0; a < N; ++a)
    for (int b = a + 1; b < N; ++b)
    for (int c = b + 1; c < N; ++c)
    for (int d = c + 1; d < N; ++d)
    for (int e = d + 1; e < N; ++e) {
        result.push_back({
            static_cast<std::uint16_t>(edge_id[a][b]),
            static_cast<std::uint16_t>(edge_id[a][c]),
            static_cast<std::uint16_t>(edge_id[a][d]),
            static_cast<std::uint16_t>(edge_id[a][e]),
            static_cast<std::uint16_t>(edge_id[b][c]),
            static_cast<std::uint16_t>(edge_id[b][d]),
            static_cast<std::uint16_t>(edge_id[b][e]),
            static_cast<std::uint16_t>(edge_id[c][d]),
            static_cast<std::uint16_t>(edge_id[c][e]),
            static_cast<std::uint16_t>(edge_id[d][e]),
        });
    }
    require(static_cast<int>(result.size()) == FIVE_SET_COUNT,
            "five-set table size mismatch");
    return result;
}

State rotated(const State& state, int amount) {
    State result;
    for (int edge = 0; edge < EDGE_COUNT; ++edge) {
        if (!test_bit(state, edge)) continue;
        auto [u, v] = edges[edge];
        u = (u + amount) % N;
        v = (v + amount) % N;
        flip_bit(result, edge_id[u][v]);
    }
    return result;
}

State canonical(const State& state) {
    State answer = state;
    for (int amount = 1; amount < N; ++amount) {
        State candidate = rotated(state, amount);
        if (StateLess{}(candidate, answer)) answer = candidate;
    }
    return answer;
}

State reflected(const State& state) {
    State answer;
    for (int edge = 0; edge < EDGE_COUNT; ++edge) {
        if (!test_bit(state, edge)) continue;
        auto [u, v] = edges[edge];
        u = (N - u) % N;
        v = (N - v) % N;
        flip_bit(answer, edge_id[u][v]);
    }
    return canonical(answer);
}

std::vector<int> support_signature(const State& state) {
    std::vector<int> answer;
    for (int edge = 0; edge < EDGE_COUNT; ++edge) {
        if (!test_bit(state, edge)) continue;
        auto [u, v] = edges[edge];
        const int distance = std::min(v - u, N - (v - u));
        if (distance != 1) answer.push_back(distance);
    }
    std::sort(answer.begin(), answer.end());
    return answer;
}

std::string signature_name(const State& state) {
    const std::vector<int> signature = support_signature(state);
    if (signature.empty()) return "cycle_only";
    std::string answer;
    for (std::size_t i = 0; i < signature.size(); ++i) {
        if (i) answer += ',';
        answer += std::to_string(signature[i]);
    }
    return answer;
}

struct Audit {
    int objective = 0;
    std::array<int, EDGE_COUNT> delta{};
};

Audit audit_state(const State& state, const std::vector<FiveSet>& five_sets) {
    std::array<unsigned char, EDGE_COUNT> red{};
    for (int edge = 0; edge < EDGE_COUNT; ++edge)
        red[edge] = seed_red[edge] ^ test_bit(state, edge);

    Audit audit;
    for (const FiveSet& five : five_sets) {
        int red_count = 0;
        for (std::uint16_t edge : five) red_count += red[edge];
        if (red_count == 0 || red_count == 10) {
            ++audit.objective;
            for (std::uint16_t edge : five) --audit.delta[edge];
        } else if (red_count == 1) {
            for (std::uint16_t edge : five)
                if (red[edge]) ++audit.delta[edge];
        } else if (red_count == 9) {
            for (std::uint16_t edge : five)
                if (!red[edge]) ++audit.delta[edge];
        }
    }
    return audit;
}

int direct_objective(const State& state, const std::vector<FiveSet>& five_sets) {
    std::array<unsigned char, EDGE_COUNT> red{};
    for (int edge = 0; edge < EDGE_COUNT; ++edge)
        red[edge] = seed_red[edge] ^ test_bit(state, edge);
    int objective = 0;
    for (const FiveSet& five : five_sets) {
        int red_count = 0;
        for (std::uint16_t edge : five) red_count += red[edge];
        objective += red_count == 0 || red_count == 10;
    }
    return objective;
}

template <class Key>
std::string histogram_text(const std::map<Key, int>& histogram) {
    std::string answer = "{";
    bool first = true;
    for (const auto& [key, count] : histogram) {
        if (!first) answer += ",";
        first = false;
        answer += std::to_string(key) + ":" + std::to_string(count);
    }
    return answer + "}";
}

std::string signature_histogram_text(const std::map<std::string, int>& histogram) {
    std::string answer = "{";
    bool first = true;
    for (const auto& [key, count] : histogram) {
        if (!first) answer += ",";
        first = false;
        answer += key + ":" + std::to_string(count);
    }
    return answer + "}";
}

}  // namespace

int main(int argc, char** argv) try {
    require(argc == 5,
            "usage: verify_direct_k5 BOUNDARY PRIMARY_Q6 PRIMARY_Q8 CERTIFICATE");
    initialize_edges();
    const std::vector<FiveSet> five_sets = initialize_five_sets();
    const std::string boundary_text = read_file(argv[1]);
    const std::string q6_text = read_file(argv[2]);
    const std::string q8_text = read_file(argv[3]);
    const std::string certificate_text = read_file(argv[4]);

    const std::vector<State> boundary = make_states(
        parse_integer_matrix(boundary_text, "target_states")
    );
    const std::vector<State> certificate_seeds = make_states(
        parse_integer_matrix(certificate_text, "seed_states")
    );
    const std::vector<State> states = make_states(
        parse_integer_matrix(certificate_text, "q13_states")
    );
    require(states.size() == 150, "wrong q13 state count");
    require(std::is_sorted(states.begin(), states.end(), StateLess{}),
            "q13 states are not canonically ordered");
    require(std::adjacent_find(states.begin(), states.end()) == states.end(),
            "duplicate q13 state");

    std::set<State, StateLess> expected_seeds;
    for (const State& state : boundary) {
        const std::vector<int> signature = support_signature(state);
        if (signature == std::vector<int>{17, 21}
            || signature == std::vector<int>{17, 17, 21}) {
            expected_seeds.insert(state);
        }
    }
    const std::set<State, StateLess> seeds(
        certificate_seeds.begin(), certificate_seeds.end()
    );
    require(seeds == expected_seeds && seeds.size() == 18,
            "seed selection disagrees with parent boundary");

    std::unordered_map<State, int, StateHash> index;
    for (int i = 0; i < static_cast<int>(states.size()); ++i) {
        require(canonical(states[i]) == states[i], "noncanonical q13 state");
        std::set<State, StateLess> orbit;
        for (int amount = 0; amount < N; ++amount)
            orbit.insert(rotated(states[i], amount));
        require(orbit.size() == N, "nonfree q13 rotation orbit");
        index.emplace(states[i], i);
    }

    std::vector<Audit> audits(states.size());
#pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < static_cast<int>(states.size()); ++i)
        audits[i] = audit_state(states[i], five_sets);

    std::vector<std::set<int>> graph(states.size());
    std::map<std::pair<int, int>, int> directed_multiplicity;
    std::map<int, std::set<State, StateLess>> low_targets;
    std::map<int, int> low_incidences;
    std::map<int, int> minimum_histogram;
    std::map<std::string, int> support_histogram;
    for (int source = 0; source < static_cast<int>(states.size()); ++source) {
        require(audits[source].objective == 13, "listed state does not have q=13");
        ++support_histogram[signature_name(states[source])];
        int minimum = 1'000'000;
        for (int edge = 0; edge < EDGE_COUNT; ++edge) {
            const int after = 13 + audits[source].delta[edge];
            minimum = std::min(minimum, after);
            if (after > 13) continue;
            State target = states[source];
            flip_bit(target, edge);
            target = canonical(target);
            if (after == 13) {
                const auto found = index.find(target);
                require(found != index.end(), "q13 neighbour omitted from closure");
                require(found->second != source, "quotient self-loop");
                ++directed_multiplicity[{source, found->second}];
                graph[source].insert(found->second);
            } else {
                low_targets[after].insert(target);
                ++low_incidences[after];
            }
        }
        ++minimum_histogram[minimum];
    }

    int internal_directed = 0;
    std::set<std::pair<int, int>> undirected;
    for (const auto& [arc, multiplicity] : directed_multiplicity) {
        require(multiplicity == 1, "parallel q13 quotient incidence");
        const auto reverse = directed_multiplicity.find({arc.second, arc.first});
        require(reverse != directed_multiplicity.end()
                && reverse->second == multiplicity,
                "asymmetric q13 quotient incidence");
        internal_directed += multiplicity;
        undirected.insert(std::minmax(arc.first, arc.second));
    }
    require(internal_directed == 456 && undirected.size() == 228,
            "internal edge totals disagree");

    const std::size_t low_object_start = locate_key(
        certificate_text, "sublevel_endpoint_states_by_objective"
    );
    const std::vector<int> objectives = {6, 8, 10, 11, 12};
    const std::vector<int> expected_low_counts = {8, 16, 20, 52, 178};
    for (std::size_t i = 0; i < objectives.size(); ++i) {
        const int objective = objectives[i];
        const std::vector<State> listed = make_states(parse_integer_matrix(
            certificate_text, std::to_string(objective), low_object_start
        ));
        const std::set<State, StateLess> listed_set(listed.begin(), listed.end());
        require(listed.size() == listed_set.size(), "duplicate sublevel endpoint");
        require(listed_set == low_targets[objective],
                "sublevel endpoint payload mismatch");
        require(static_cast<int>(listed_set.size()) == expected_low_counts[i],
                "sublevel endpoint count mismatch");
    }
    require(low_targets.size() == objectives.size(), "unexpected sublevel objective");
    require(low_incidences == std::map<int, int>{{6, 8}, {8, 16}, {10, 20},
                                                 {11, 124}, {12, 238}},
            "sublevel incidence counts disagree");
    require(minimum_histogram == std::map<int, int>{{6, 8}, {8, 16}, {10, 20},
                                                     {11, 36}, {12, 68}, {13, 2}},
            "minimum-neighbour histogram disagrees");
    require(support_histogram == std::map<std::string, int>{
                {"17,17,21", 8}, {"17,21", 118}, {"21", 24}},
            "support histogram disagrees");

    std::set<State, StateLess> primary_q6;
    for (const State& state : make_states(parse_integer_matrix(
             q6_text, "objective_six_rotation_representatives")))
        primary_q6.insert(state);
    std::set<State, StateLess> primary_q8;
    for (const State& state : make_states(parse_integer_matrix(
             q8_text, "objective_eight_component_rotation_representatives")))
        primary_q8.insert(state);
    require(std::includes(primary_q6.begin(), primary_q6.end(),
                          low_targets[6].begin(), low_targets[6].end(), StateLess{}),
            "q6 endpoint outside pinned primary array");
    require(std::includes(primary_q8.begin(), primary_q8.end(),
                          low_targets[8].begin(), low_targets[8].end(), StateLess{}),
            "q8 endpoint outside pinned primary array");

    std::vector<int> component(states.size(), -1);
    std::vector<std::vector<int>> components;
    for (int start = 0; start < static_cast<int>(states.size()); ++start) {
        if (component[start] != -1) continue;
        const int number = static_cast<int>(components.size());
        std::queue<int> queue;
        queue.push(start);
        component[start] = number;
        components.push_back({});
        while (!queue.empty()) {
            const int source = queue.front();
            queue.pop();
            components.back().push_back(source);
            for (int target : graph[source]) {
                if (component[target] == -1) {
                    component[target] = number;
                    queue.push(target);
                }
            }
        }
    }
    std::map<int, int> component_sizes;
    for (const auto& part : components) ++component_sizes[part.size()];
    require(component_sizes == std::map<int, int>{{6, 2}, {10, 2}, {59, 2}},
            "component sizes disagree");
    require(static_cast<int>(undirected.size()) - static_cast<int>(states.size())
                + static_cast<int>(components.size()) == 84,
            "cycle rank disagrees");

    std::set<int> reached;
    std::queue<int> queue;
    for (const State& seed : seeds) {
        const auto found = index.find(seed);
        require(found != index.end(), "seed absent from q13 list");
        if (reached.insert(found->second).second) queue.push(found->second);
    }
    while (!queue.empty()) {
        const int source = queue.front();
        queue.pop();
        for (int target : graph[source])
            if (reached.insert(target).second) queue.push(target);
    }
    require(reached.size() == states.size(), "q13 list contains a seed-unreachable state");

    int reflection_fixed_states = 0;
    int dihedral_orbits = 0;
    std::set<std::pair<int, int>> component_pairs;
    for (int source = 0; source < static_cast<int>(states.size()); ++source) {
        const State image = reflected(states[source]);
        const auto found = index.find(image);
        require(found != index.end(), "reflection leaves closure");
        reflection_fixed_states += image == states[source];
        dihedral_orbits += !StateLess{}(image, states[source]);
        component_pairs.insert(std::minmax(component[source], component[found->second]));
    }
    require(reflection_fixed_states == 0 && dihedral_orbits == 75,
            "reflection orbit count disagrees");
    require(component_pairs == std::set<std::pair<int, int>>{{0, 3}, {1, 4}, {2, 5}},
            "reflection component pairing disagrees");

    std::vector<std::pair<State, int>> endpoint_checks;
    for (int objective : objectives)
        for (const State& state : low_targets[objective])
            endpoint_checks.push_back({state, objective});
    std::vector<int> recounted(endpoint_checks.size());
#pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < static_cast<int>(endpoint_checks.size()); ++i)
        recounted[i] = direct_objective(endpoint_checks[i].first, five_sets);
    for (std::size_t i = 0; i < endpoint_checks.size(); ++i)
        require(recounted[i] == endpoint_checks[i].second,
                "direct endpoint objective recount disagrees");

    std::cout << "PASS direct all-K5 audit of the complete exact-q13 closure\n";
    std::cout << "q13_states=150 five_sets_per_state=" << FIVE_SET_COUNT
              << " flips=135450 endpoint_recounts=" << endpoint_checks.size() << "\n";
    std::cout << "components=6 sizes=" << histogram_text(component_sizes)
              << " edges=228 cycle_rank=84\n";
    std::cout << "internal_directed=456 dihedral_orbits=75 reflection_fixed=0\n";
    std::cout << "support=" << signature_histogram_text(support_histogram) << "\n";
    std::map<int, int> low_counts;
    for (const auto& [objective, targets] : low_targets)
        low_counts[objective] = static_cast<int>(targets.size());
    std::cout << "sublevel=" << histogram_text(low_counts) << "\n";
    return 0;
} catch (const std::exception& error) {
    std::cerr << "FAIL " << error.what() << '\n';
    return 1;
}
