#define NONMONO_EMIT_LIBRARY
#include "../hadwiger_nelson_nonmono159_overlap10/emit_graphs.cpp"
#undef NONMONO_EMIT_LIBRARY

struct Witness {
    std::size_t order{}, edges{};
    std::string colors;
};

static std::vector<Witness> read_witnesses(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open witness file");
    std::map<int, Witness> indexed;
    std::string line;
    while (std::getline(input, line)) {
        if (!line.starts_with("graph=")) continue;
        std::map<std::string, std::string> row;
        for (const std::string& item : split_any(line, ';')) {
            const auto equals = item.find('=');
            row[item.substr(0, equals)] = item.substr(equals + 1);
        }
        if (row.at("status") != "SAT") throw std::runtime_error("non-SAT witness row");
        const int graph = std::stoi(row.at("graph"));
        if (!indexed.emplace(graph, Witness{std::stoul(row.at("order")),
                                            std::stoul(row.at("edges")),
                                            row.at("colors")}).second) {
            throw std::runtime_error("duplicate graph witness");
        }
    }
    std::vector<Witness> result;
    for (int graph = 0; graph < static_cast<int>(indexed.size()); ++graph) {
        result.push_back(indexed.at(graph));
    }
    return result;
}

int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr << "usage: verify_colorings POINTS.tsv TRANSFORMS.txt COLORINGS.txt\n";
        return 2;
    }
    i64 source_scale = 0;
    const auto source = read_points_any(argv[1], source_scale);
    const auto transforms = read_transforms_any(argv[2]);
    const auto witnesses = read_witnesses(argv[3]);
    if (transforms.size() != witnesses.size()) throw std::runtime_error("transform/witness count differs");

    std::size_t min_order = std::numeric_limits<std::size_t>::max(), max_order = 0;
    std::size_t min_edges = std::numeric_limits<std::size_t>::max(), max_edges = 0;
    for (std::size_t graph = 0; graph < transforms.size(); ++graph) {
        const Transform& transformation = transforms[graph];
        const Witness& witness = witnesses[graph];
        std::vector<Point> labelled;
        for (const Point& point : source) {
            labelled.push_back(Point{scale_field(point.x, transformation.denominator),
                                     scale_field(point.y, transformation.denominator)});
        }
        for (const Point& point : source) labelled.push_back(transform_any(point, transformation));

        std::map<Point, std::uint16_t> point_index;
        for (const Point& point : labelled) point_index.emplace(point, point_index.size());
        std::vector<Point> points(point_index.size());
        for (const auto& [point, vertex] : point_index) points[vertex] = point;
        if (points.size() != 318 - transformation.overlaps || witness.order != points.size()
            || witness.colors.size() != points.size()) {
            throw std::runtime_error("order/overlap mismatch at graph " + std::to_string(graph));
        }
        for (const char color : witness.colors) {
            if (color < '0' || color > '3') throw std::runtime_error("bad color digit");
        }

        const i64 transformed_scale = narrow(
            static_cast<i128>(source_scale) * transformation.denominator);
        std::size_t edges = 0;
        for (std::uint16_t u = 0; u < points.size(); ++u) {
            for (std::uint16_t v = u + 1; v < points.size(); ++v) {
                if (is_unit_any(points[u], points[v], transformed_scale)) {
                    ++edges;
                    if (witness.colors[u] == witness.colors[v]) {
                        throw std::runtime_error("monochromatic unit edge at graph "
                                                 + std::to_string(graph));
                    }
                }
            }
        }
        if (edges != witness.edges) {
            throw std::runtime_error("edge-count mismatch at graph " + std::to_string(graph));
        }
        min_order = std::min(min_order, points.size());
        max_order = std::max(max_order, points.size());
        min_edges = std::min(min_edges, edges);
        max_edges = std::max(max_edges, edges);
        if ((graph + 1) % 1000 == 0) std::cerr << "verified=" << graph + 1 << '\n';
    }
    std::cout << "graphs=" << transforms.size() << '\n';
    std::cout << "unsat=0\n";
    std::cout << "order_range=" << min_order << '-' << max_order << '\n';
    std::cout << "edge_range=" << min_edges << '-' << max_edges << '\n';
    std::cout << "exact_geometry=true\n";
    std::cout << "direct_witness_verification=true\n";
}
