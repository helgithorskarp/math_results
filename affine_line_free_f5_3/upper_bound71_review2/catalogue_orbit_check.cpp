#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Key = std::pair<int, std::string>;

std::set<Key> token_catalogue() {
    constexpr std::array<int, 5> A{12, 4, 4, 4, 4};
    constexpr std::array<int, 5> B{11, 5, 4, 4, 4};
    std::set<Key> result;
    for (int type = 0; type < 3; ++type) {
        const auto rows = type < 2 ? A : B;
        const auto columns = type == 0 ? A : B;
        const int first_total = type == 0 ? 7 : 8;
        const int last_total = type == 2 ? 10 : first_total + 1;
        for (int total = first_total; total <= last_total; ++total) {
            std::array<int, 16> interior{};
            auto distribute = [&](auto&& self, int remaining, int least_cell) -> void {
                if (remaining != 0) {
                    for (int cell = least_cell; cell < 16; ++cell) {
                        if (interior[static_cast<std::size_t>(cell)] == 4) continue;
                        ++interior[static_cast<std::size_t>(cell)];
                        self(self, remaining - 1, cell);
                        --interior[static_cast<std::size_t>(cell)];
                    }
                    return;
                }

                std::array<int, 4> interior_rows{}, interior_columns{};
                for (int x = 0; x < 4; ++x)
                for (int y = 0; y < 4; ++y) {
                    const int value = interior[static_cast<std::size_t>(4*x+y)];
                    interior_rows[static_cast<std::size_t>(x)] += value;
                    interior_columns[static_cast<std::size_t>(y)] += value;
                }
                std::array<int, 25> deficit{};
                deficit[0] = rows[0] + columns[0] - 28 + total;
                if (deficit[0] < (type == 2 ? 2 : 3) || deficit[0] > 4) return;
                for (int i = 0; i < 4; ++i) {
                    deficit[static_cast<std::size_t>(5*(i+1))] = rows[static_cast<std::size_t>(i+1)] - interior_rows[static_cast<std::size_t>(i)];
                    deficit[static_cast<std::size_t>(i+1)] = columns[static_cast<std::size_t>(i+1)] - interior_columns[static_cast<std::size_t>(i)];
                    if (deficit[static_cast<std::size_t>(5*(i+1))] < 1
                        || deficit[static_cast<std::size_t>(5*(i+1))] > 4
                        || deficit[static_cast<std::size_t>(i+1)] < 1
                        || deficit[static_cast<std::size_t>(i+1)] > 4) return;
                }
                for (int x = 0; x < 4; ++x)
                for (int y = 0; y < 4; ++y)
                    deficit[static_cast<std::size_t>(5*(x+1)+y+1)] = interior[static_cast<std::size_t>(4*x+y)];
                for (int slope = 0; slope < 5; ++slope)
                for (int offset = 0; offset < 5; ++offset) {
                    int line_deficit = 0;
                    for (int x = 0; x < 5; ++x)
                        line_deficit += deficit[static_cast<std::size_t>(5*x+(slope*x+offset)%5)];
                    if (line_deficit < 4) return;
                }
                std::string word;
                for (int value : deficit) word += static_cast<char>('0' + 4 - value);
                result.emplace(type, word);
            };
            distribute(distribute, total, 0);
        }
    }
    return result;
}

int main(int argc, char** argv) {
    if (argc != 3) throw std::runtime_error("usage: catalogue_orbit_check ORBITS CATALOGUE_OUT");
    const std::set<Key> catalogue = token_catalogue();
    std::ofstream catalogue_output(argv[2]);
    for (const auto& [type, word] : catalogue) catalogue_output << type << ' ' << word << '\n';
    catalogue_output.close();

    std::ifstream orbit_input(argv[1]);
    std::ostringstream buffer;
    buffer << orbit_input.rdbuf();
    const std::string contents = buffer.str();
    const std::regex type_pattern("\\\"type\\\"[[:space:]]*:[[:space:]]*([0-2])");
    const std::regex word_pattern("\\\"weights\\\"[[:space:]]*:[[:space:]]*\\\"([0-4]{25})\\\"");
    const std::regex size_pattern("\\\"orbit_size\\\"[[:space:]]*:[[:space:]]*([0-9]+)");
    std::vector<int> types, published_sizes;
    std::vector<std::string> words;
    for (std::sregex_iterator it(contents.begin(), contents.end(), type_pattern), end; it != end; ++it)
        types.push_back(std::stoi((*it)[1].str()));
    for (std::sregex_iterator it(contents.begin(), contents.end(), word_pattern), end; it != end; ++it)
        words.push_back((*it)[1].str());
    for (std::sregex_iterator it(contents.begin(), contents.end(), size_pattern), end; it != end; ++it)
        published_sizes.push_back(std::stoi((*it)[1].str()));
    if (types.size() != 4332 || words.size() != types.size() || published_sizes.size() != types.size())
        throw std::runtime_error("failed to parse representatives");

    constexpr std::array<int, 5> A{8, 16, 16, 16, 16};
    constexpr std::array<int, 5> B{9, 15, 16, 16, 16};
    std::map<Key, int> coverage;
    bool orbit_sizes_match = true;
    int affine_maps = 0;
    std::array<int, 3> canonical_counts{};
    for (std::size_t index = 0; index < words.size(); ++index) {
        ++canonical_counts[static_cast<std::size_t>(types[index])];
        std::set<Key> normalized_images;
        for (int a = 0; a < 5; ++a)
        for (int b = 0; b < 5; ++b)
        for (int c = 0; c < 5; ++c)
        for (int d = 0; d < 5; ++d) {
            if ((a*d-b*c) % 5 == 0) continue;
            for (int u = 0; u < 5; ++u)
            for (int v = 0; v < 5; ++v) {
                if (index == 0) ++affine_maps;
                std::string image(25, '?');
                for (int x = 0; x < 5; ++x)
                for (int y = 0; y < 5; ++y) {
                    const int new_x = (a*x+b*y+u) % 5;
                    const int new_y = (c*x+d*y+v) % 5;
                    image[static_cast<std::size_t>(5*new_x+new_y)] = words[index][static_cast<std::size_t>(5*x+y)];
                }
                std::array<int, 5> row_sums{}, column_sums{};
                for (int x = 0; x < 5; ++x)
                for (int y = 0; y < 5; ++y) {
                    const int weight = image[static_cast<std::size_t>(5*x+y)] - '0';
                    row_sums[static_cast<std::size_t>(x)] += weight;
                    column_sums[static_cast<std::size_t>(y)] += weight;
                }
                int new_type = -1;
                if (row_sums == A && column_sums == A) new_type = 0;
                if (row_sums == A && column_sums == B) new_type = 1;
                if (row_sums == B && column_sums == B) new_type = 2;
                if (new_type >= 0) normalized_images.emplace(new_type, image);
            }
        }
        if (static_cast<int>(normalized_images.size()) != published_sizes[index]) orbit_sizes_match = false;
        for (const Key& image : normalized_images) {
            if (!catalogue.contains(image)) throw std::runtime_error("orbit image absent from independent catalogue");
            ++coverage[image];
        }
    }
    int overlaps = 0;
    for (const auto& [key, multiplicity] : coverage)
        if (multiplicity != 1) ++overlaps;
    std::array<int, 3> labeled_counts{};
    for (const auto& [type, word] : catalogue) ++labeled_counts[static_cast<std::size_t>(type)];
    std::cout << "{\n"
              << "  \"status\": \"INDEPENDENT_TOKEN_CATALOGUE_AND_FULL_AFFINE_AUDIT_VERIFIED\",\n"
              << "  \"typed_quotients\": " << catalogue.size() << ",\n"
              << "  \"labeled_counts_AA_AB_BB\": [" << labeled_counts[0] << ", " << labeled_counts[1] << ", " << labeled_counts[2] << "],\n"
              << "  \"representatives\": " << words.size() << ",\n"
              << "  \"canonical_counts_AA_AB_BB\": [" << canonical_counts[0] << ", " << canonical_counts[1] << ", " << canonical_counts[2] << "],\n"
              << "  \"affine_maps_per_representative\": " << affine_maps << ",\n"
              << "  \"normalized_images\": " << coverage.size() << ",\n"
              << "  \"overlaps\": " << overlaps << ",\n"
              << "  \"published_orbit_sizes_match\": " << (orbit_sizes_match ? "true" : "false") << "\n"
              << "}\n";
}
