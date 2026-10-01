// Exact semantic-profile transport and bounded lookahead for n=13.
// This is a necessary filter. A passing path need not have a sorting completion.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

constexpr int N=13, WORDS=64;
using Gate=std::pair<int,int>;
using Bits=std::array<std::uint64_t,WORDS>;
struct Record {
  std::array<Bits,N> truth{};
  std::array<std::int8_t,N> mark{};
  unsigned deleted=0, redundant=0;
};
struct Family {
  unsigned lo=0, hi=0, words=0;
  std::vector<Record> records;
};
using State=std::array<Family,5>;
const std::array<std::pair<unsigned,unsigned>,5> types{{{1,0},{0,1},{2,0},{0,2},{1,1}}};
const std::array<std::string,5> names{{"one_minimum","one_maximum","two_minima","two_maxima","mixed_pair"}};
const std::array<std::uint64_t,5> limits{{32,32,512,512,512}};

State initial() {
  State state;
  for(std::size_t f=0;f<state.size();++f) {
    auto& family=state[f];
    auto [lo,hi]=types[f]; family.lo=lo;family.hi=hi;
    const unsigned k=N-lo-hi, values=1U<<k;
    family.words=values/64;
    std::array<Bits,N> columns{};
    for(unsigned x=0;x<values;++x) for(unsigned j=0;j<k;++j)
      if((x>>j)&1U) columns[j][x/64]|=std::uint64_t{1}<<(x%64);
    for(unsigned lows=0;lows<(1U<<N);++lows) if(std::popcount(lows)==static_cast<int>(lo))
      for(unsigned highs=0;highs<(1U<<N);++highs)
        if(!(lows&highs) && std::popcount(highs)==static_cast<int>(hi)) {
          Record row;unsigned free=0;
          for(unsigned i=0;i<N;++i) {
            if((lows>>i)&1U)row.mark[i]=-1;
            else if((highs>>i)&1U)row.mark[i]=1;
            else row.truth[i]=columns[free++];
          }
          if(free!=k)throw std::runtime_error("wrong free count");
          family.records.push_back(row);
        }
  }
  return state;
}

void apply(State& state,Gate g) {
  auto a=static_cast<std::size_t>(g.first), b=static_cast<std::size_t>(g.second);
  for(auto& family:state) for(auto& row:family.records) {
    if(row.mark[a] || row.mark[b]) {
      ++row.deleted;
      if(row.mark[a]>row.mark[b]) {
        std::swap(row.mark[a],row.mark[b]);
        std::swap(row.truth[a],row.truth[b]);
      }
    } else {
      bool redundant=true;
      for(unsigned w=0;w<family.words;++w) {
        const auto x=row.truth[a][w],y=row.truth[b][w];
        redundant=redundant && ((x&~y)==0);
        row.truth[a][w]=x&y;row.truth[b][w]=x|y;
      }
      if(redundant)++row.redundant;
    }
  }
}

using Envelope=std::map<std::pair<unsigned,unsigned>,std::pair<unsigned,unsigned>>;
Envelope envelope(const Family& family) {
  Envelope result;
  for(const auto& row:family.records) {
    unsigned lo=0,hi=0;
    for(unsigned i=0;i<N;++i) {
      if(row.mark[i]==-1)lo|=1U<<i;
      else if(row.mark[i]==1)hi|=1U<<i;
    }
    auto& value=result[{lo,hi}];
    value.first=std::max(value.first,row.deleted);
    value.second=std::max(value.second,row.deleted+row.redundant);
  }
  return result;
}

std::pair<std::uint64_t,std::uint64_t> masses(const Family& family) {
  std::uint64_t ordinary=0,semantic=0;
  for(const auto& [ports,p]:envelope(family)) {
    (void)ports;
    if(p.second>=60)throw std::runtime_error("profile overflow");
    ordinary+=std::uint64_t{1}<<p.first;
    semantic+=std::uint64_t{1}<<p.second;
  }
  return {ordinary,semantic};
}

std::uint64_t ceil_power(std::uint64_t x) {
  if(x==0)return 0;
  const auto exponent=std::bit_width(x-1);
  if(exponent>=63)throw std::runtime_error("anchor overflow");
  return std::uint64_t{1}<<exponent;
}

std::array<std::uint64_t,2> anchor_units(const State& state) {
  std::array<Envelope,5> env;
  for(std::size_t f=0;f<state.size();++f)env[f]=envelope(state[f]);
  std::array<std::uint64_t,2> result{};
  for(unsigned side=0;side<2;++side) {
    const auto unary=side,paired=side+2;
    for(const auto& [ports,costs]:env[unary]) {
      const auto port=side?ports.second:ports.first;
      auto units=(std::uint64_t{1}<<costs.second)*16;
      for(auto f:{paired,4U}) {
        std::uint64_t mass=0;
        for(const auto& [z,p]:env[f]) {
          auto marked=side?z.second:z.first;
          if(marked&port)mass+=std::uint64_t{1}<<p.second;
        }
        units=std::max(units,ceil_power(mass));
      }
      result[side]+=units;
    }
  }
  return result;
}

bool passes(const State& state,bool use_anchors=true) {
  // Pair profiles first; all five are enforced before a node is retained.
  for(auto f:{2U,3U,4U,0U,1U}) if(masses(state[f]).second>limits[f])return false;
  if(use_anchors) {
    auto units=anchor_units(state);
    if(units[0]>512 || units[1]>512)return false;
  }
  return true;
}

std::vector<Gate> read_network(const std::string& path) {
  std::ifstream in(path);int n=0,m=0;
  if(!(in>>n>>m) || n!=N || m<0 || m>44)throw std::runtime_error("bad input dimensions");
  std::vector<Gate> gates;
  for(int j=0;j<m;++j) {
    int a=0,b=0;
    if(!(in>>a>>b) || a<0 || a>=b || b>=N)throw std::runtime_error("bad comparator");
    gates.emplace_back(a,b);
  }
  std::string rest;if(in>>rest)throw std::runtime_error("trailing input");
  return gates;
}

struct Search {
  unsigned depth=0;
  std::uint64_t node_limit=0,nodes=0;
  bool complete=true;
  bool use_anchors=true;
  std::vector<std::uint64_t> visited,passing;
  std::vector<Gate> path;
  std::vector<std::vector<Gate>> leaves;
  void visit(const State& state,unsigned level) {
    if(nodes>=node_limit) {complete=false;return;}
    ++nodes;++visited[level];
    if(!passes(state,use_anchors))return;
    ++passing[level];
    if(level==depth) {leaves.push_back(path);return;}
    for(int a=0;a<N;++a)for(int b=a+1;b<N;++b) {
      State child=state;apply(child,{a,b});path.emplace_back(a,b);
      visit(child,level+1);path.pop_back();
      if(!complete)return;
    }
  }
};

void write_numbers(std::ostream& out,const std::vector<std::uint64_t>& xs) {
  out<<'[';for(std::size_t i=0;i<xs.size();++i)out<<(i?",":"")<<xs[i];out<<']';
}

#ifndef SEMANTIC_PROFILE_LIBRARY
int main(int argc,char** argv) {
 try {
  if(argc!=6 && argc!=7)throw std::runtime_error("usage: filter_frontier PREFIX_TXT DEPTH MAX_NODES OUTPUT_JSON INCLUDE_LEAVES_0_OR_1 [USE_ANCHORS_0_OR_1]");
  const auto gates=read_network(argv[1]);const auto depth=static_cast<unsigned>(std::stoul(argv[2]));
  const auto limit=std::stoull(argv[3]);const std::string leaf_flag=argv[5];
  const std::string anchor_flag=argc==7?argv[6]:"1";
  if(depth>10 || gates.size()+depth>44 || limit==0 || (leaf_flag!="0" && leaf_flag!="1") ||
     (anchor_flag!="0" && anchor_flag!="1"))
    throw std::runtime_error("invalid search bounds");
  State state=initial();for(auto g:gates)apply(state,g);
  Search search;search.depth=depth;search.node_limit=limit;search.use_anchors=anchor_flag=="1";
  search.visited.resize(depth+1);search.passing.resize(depth+1);search.visit(state,0);
  std::ofstream out(argv[4]);if(!out)throw std::runtime_error("cannot open output");
  out<<"{\"n\":13,\"budget\":44,\"filter\":\""<<(search.use_anchors?"semantic_anchors":"five_semantic_profiles")
     <<"\",\"prefix_size\":"<<gates.size()
     <<",\"depth\":"<<depth<<",\"status\":\""<<(search.complete?"COMPLETE_NECESSARY_FRONTIER":"INCOMPLETE_NODE_LIMIT")
     <<"\",\"nodes\":"<<search.nodes<<",\"visited\":";write_numbers(out,search.visited);
  out<<",\"passing\":";write_numbers(out,search.passing);
  out<<",\"initial_profiles\":{";
  for(std::size_t f=0;f<state.size();++f) {
    auto [ordinary,semantic]=masses(state[f]);
    out<<(f?",":"")<<'"'<<names[f]<<"\":{\"ordinary_mass\":"<<ordinary<<",\"semantic_mass\":"<<semantic<<'}';
  }
  auto units=anchor_units(state);
  out<<"},\"anchor_units\":{\"low\":"<<units[0]<<",\"high\":"<<units[1]<<"},\"leaf_count\":"<<search.leaves.size();
  if(leaf_flag=="1") {
    out<<",\"leaves\":[";
    for(std::size_t i=0;i<search.leaves.size();++i) {
      out<<(i?",":"")<<'[';
      for(std::size_t j=0;j<search.leaves[i].size();++j) {
        auto [a,b]=search.leaves[i][j];out<<(j?",":"")<<'['<<a<<','<<b<<']';
      }
      out<<']';
    }
    out<<']';
  }
  out<<"}\n";out.close();if(!out)throw std::runtime_error("output failed");
  std::cout<<(search.complete?"COMPLETE":"INCOMPLETE_NODE_LIMIT")<<" nodes="<<search.nodes<<" passing=";
  write_numbers(std::cout,search.passing);std::cout<<'\n';
 }catch(const std::exception& e){std::cerr<<"ERROR "<<e.what()<<'\n';return 2;}
}
#endif
