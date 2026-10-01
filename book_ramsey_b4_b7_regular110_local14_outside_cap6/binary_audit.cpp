// Exhaust every free-edge binary word in each fixed local14 alignment.
// Independent implementation by six-books-3, researcher. No Python imports,
// search recursion, orbit representatives, external catalogue or solver.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

struct Configuration {
  int intersection;
  std::array<int,8> target;
  std::array<std::array<int,2>,2> pairs;
};

int main() {
  const std::array<Configuration,3> cases{{
    {2, {{1,1,3,3,3,3,3,3}}, {{{{0,1}},{{0,1}}}}},
    {1, {{1,2,2,3,3,3,3,3}}, {{{{0,1}},{{0,2}}}}},
    {0, {{2,2,2,2,3,3,3,3}}, {{{{0,1}},{{2,3}}}}}
  }};
  std::cout << "{\"agent\":\"six-books-3\",\"role\":\"researcher\",\"alignments\":[";
  bool first_case = true;
  for (const auto &c : cases) {
    std::vector<std::array<int,3>> free_edges;
    int bit = 0;
    for (int i=0;i<8;++i) for (int j=i+1;j<8;++j,++bit) {
      bool forbidden = false;
      for (auto p:c.pairs) if (p[0]==i && p[1]==j) forbidden=true;
      if (!forbidden) free_edges.push_back({i,j,bit});
    }
    const std::uint64_t bound = std::uint64_t{1} << free_edges.size();
    std::array<int,8> degree{};
    std::array<unsigned,8> adjacency{};
    int correct=0;
    for (int i=0;i<8;++i) correct += degree[i]==c.target[i];
    unsigned mask=0;
    std::uint64_t fixed_degree=0;
    std::vector<unsigned> retained;
    for (std::uint64_t word=0;word<bound;++word) {
      if (correct==8) {
        ++fixed_degree;
        std::array<unsigned,10> local{};
        for (int i=0;i<8;++i) local[i+2]=adjacency[i]<<2;
        for (int low=0;low<2;++low) for(int x:c.pairs[low]) {
          local[low] |= 1U << (x+2);
          local[x+2] |= 1U << low;
        }
        bool valid=true;
        for(int i=0;i<10 && valid;++i) for(int j=i+1;j<10;++j) {
          const int h_i=__builtin_popcount(local[i]);
          const int h_j=__builtin_popcount(local[j]);
          const bool red = (local[i]>>j)&1U;
          const int shared=__builtin_popcount(local[i]&local[j]);
          if (h_i+h_j-(red?5:2)-shared<0) {valid=false;break;}
        }
        if (valid) retained.push_back(mask);
      }
      if(word+1<bound) {
        // Consecutive reflected Gray words differ in bit ctz(word+1).
        const auto edge=free_edges[__builtin_ctzll(word+1)];
        const int i=edge[0],j=edge[1];
        const bool old = (adjacency[i]>>j)&1U;
        correct -= degree[i]==c.target[i];
        correct -= degree[j]==c.target[j];
        degree[i] += old?-1:1;
        degree[j] += old?-1:1;
        correct += degree[i]==c.target[i];
        correct += degree[j]==c.target[j];
        adjacency[i] ^= 1U<<j;
        adjacency[j] ^= 1U<<i;
        mask ^= 1U<<edge[2];
      }
    }
    std::sort(retained.begin(),retained.end());
    if(std::adjacent_find(retained.begin(),retained.end())!=retained.end())
      throw std::runtime_error("Gray census repeats a graph");
    if(!first_case)std::cout<<',';
    first_case=false;
    std::cout<<"{\"intersection\":"<<c.intersection
      <<",\"binary_words\":"<<bound<<",\"fixed_degree_graphs\":"<<fixed_degree
      <<",\"retained_count\":"<<retained.size()<<",\"masks\":[";
    for(std::size_t i=0;i<retained.size();++i) {
      if(i)std::cout<<',';
      std::cout<<retained[i];
    }
    std::cout<<"]}"<<std::flush;
  }
  std::cout<<"],\"complete\":true}\n";
}
