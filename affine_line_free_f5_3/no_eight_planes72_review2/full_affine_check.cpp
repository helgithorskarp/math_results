#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 3) throw std::runtime_error("usage: full_affine_check CATALOGUE ORBITS");
    std::ifstream catalogue_input(argv[1]);
    std::set<std::string> catalogue;
    for (std::string word; catalogue_input >> word;) catalogue.insert(word);
    if (catalogue.size() != 5428) throw std::runtime_error("incomplete catalogue");

    std::ifstream orbit_input(argv[2]);
    std::ostringstream buffer;
    buffer << orbit_input.rdbuf();
    const std::string contents = buffer.str();
    const std::regex word_pattern("[0-4]{25}");
    const std::regex size_pattern("\\\"orbit_size\\\"[[:space:]]*:[[:space:]]*([0-9]+)");
    std::vector<std::string> representatives;
    std::vector<int> published_sizes;
    for (std::sregex_iterator it(contents.begin(), contents.end(), word_pattern), end; it != end; ++it)
        representatives.push_back(it->str());
    for (std::sregex_iterator it(contents.begin(), contents.end(), size_pattern), end; it != end; ++it)
        published_sizes.push_back(std::stoi((*it)[1].str()));
    if (representatives.size() != 1252 || published_sizes.size() != representatives.size())
        throw std::runtime_error("failed to parse orbit catalogue");

    std::map<std::string, int> coverage;
    bool sizes_match = true;
    int affine_maps = 0;
    for (std::size_t index = 0; index < representatives.size(); ++index) {
        const std::string& word = representatives[index];
        std::set<std::string> normalized_images;
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
                    image[static_cast<std::size_t>(5*new_x+new_y)] = word[static_cast<std::size_t>(5*x+y)];
                }
                std::array<int, 5> rows{}, columns{};
                for (int x = 0; x < 5; ++x)
                for (int y = 0; y < 5; ++y) {
                    const int weight = image[static_cast<std::size_t>(5*x+y)]-'0';
                    rows[static_cast<std::size_t>(x)] += weight;
                    columns[static_cast<std::size_t>(y)] += weight;
                }
                if (rows == std::array<int,5>{8,16,16,16,16}
                    && columns == std::array<int,5>{9,15,16,16,16})
                    normalized_images.insert(image);
            }
        }
        if (static_cast<int>(normalized_images.size()) != published_sizes[index]) sizes_match = false;
        for (const std::string& image : normalized_images) {
            if (!catalogue.contains(image)) throw std::runtime_error("orbit image absent from catalogue");
            ++coverage[image];
        }
    }
    int overlaps = 0;
    for (const auto& [word, multiplicity] : coverage)
        if (multiplicity != 1) ++overlaps;
    std::cout << "{\n"
              << "  \"affine_maps\": " << affine_maps << ",\n"
              << "  \"representatives\": " << representatives.size() << ",\n"
              << "  \"normalized_images\": " << coverage.size() << ",\n"
              << "  \"overlaps\": " << overlaps << ",\n"
              << "  \"published_orbit_sizes_match\": " << (sizes_match ? "true" : "false") << "\n"
              << "}\n";
}
