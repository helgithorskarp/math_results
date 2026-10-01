// Complete deletion-only frontier of supplied 45/46-comparator seeds.
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
constexpr int n=13, words=128;
using Gate=std::pair<int,int>;
using Net=std::vector<Gate>;
using Bits=std::array<std::uint64_t,words>;
using State=std::array<Bits,n>;
void apply(State& s,Gate g) {
 auto& a=s[static_cast<std::size_t>(g.first)]; auto& b=s[static_cast<std::size_t>(g.second)];
 for(int j=0;j<words;++j) { auto k=static_cast<std::size_t>(j),x=a[k],y=b[k];a[k]=x&y;b[k]=x|y; }
}
Bits failures(const State& s) {
 Bits bad{};
 for(int i=0;i<n-1;++i) for(int j=0;j<words;++j) bad[static_cast<std::size_t>(j)]|=s[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)]&~s[static_cast<std::size_t>(i+1)][static_cast<std::size_t>(j)];
 return bad;
}
int count(const Bits& b) {int c=0;for(auto x:b)c+=std::popcount(x);return c;}
void write_net(std::ofstream& out,const Net& net) {out<<"13 "<<net.size()<<'\n';for(auto [a,b]:net)out<<a<<' '<<b<<'\n';}
int main(int argc,char** argv) {
 try {
  if(argc!=4)throw std::runtime_error("usage: deletion_frontier SEEDS SUMMARY_JSON POSITIVE45_NETS");
  std::ifstream in(argv[1]);std::size_t total=0;if(!(in>>total))throw std::runtime_error("missing input");
  State initial{};
  for(unsigned x=0;x<(1U<<n);++x)for(int i=0;i<n;++i)if((x>>i)&1U)initial[static_cast<std::size_t>(i)][x/64]|=std::uint64_t{1}<<(x%64);
  Bits witness_union{};std::vector<unsigned> witness_list;
  const auto cover = [&](const Bits& bad) {
   bool covered=false;
   for(int j=0;j<words;++j)if(bad[static_cast<std::size_t>(j)]&witness_union[static_cast<std::size_t>(j)])covered=true;
   if(!covered)for(int j=0;j<words;++j)if(bad[static_cast<std::size_t>(j)]){
    auto x=static_cast<unsigned>(64*j+std::countr_zero(bad[static_cast<std::size_t>(j)]));
    witness_list.push_back(x);witness_union[static_cast<std::size_t>(j)]|=std::uint64_t{1}<<(x%64);break;
   }
  };
  int minimum=std::numeric_limits<int>::max();Net closest;
  std::uint64_t candidates=0,sorters44=0,sorters45=0;std::ofstream positive(argv[3]);
  for(std::size_t r=0;r<total;++r) {
   int nn=0,m=0;if(!(in>>nn>>m)||nn!=n||(m!=45&&m!=46))throw std::runtime_error("bad seed");
   Net net;for(int j=0;j<m;++j){int a=0,b=0;if(!(in>>a>>b)||a<0||a>=b||b>=n)throw std::runtime_error("bad comparator");net.emplace_back(a,b);}
   std::vector<State> prefix(static_cast<std::size_t>(m+1));prefix[0]=initial;
   for(int j=0;j<m;++j){prefix[static_cast<std::size_t>(j+1)]=prefix[static_cast<std::size_t>(j)];apply(prefix[static_cast<std::size_t>(j+1)],net[static_cast<std::size_t>(j)]);}
   if(count(failures(prefix.back())))throw std::runtime_error("invalid seed");
   if(m==46)for(int a=0;a<m;++a){State s=prefix[static_cast<std::size_t>(a)];for(int j=a+1;j<m;++j)apply(s,net[static_cast<std::size_t>(j)]);auto bad45=failures(s);cover(bad45);if(count(bad45)==0){Net small;for(int j=0;j<m;++j)if(j!=a)small.push_back(net[static_cast<std::size_t>(j)]);write_net(positive,small);++sorters45;}}
   for(int a=0;a<m;++a)for(int b=(m==45?-1:a+1);b<(m==45?0:m);++b) {
    State s=prefix[static_cast<std::size_t>(a)];for(int j=a+1;j<m;++j)if(j!=b)apply(s,net[static_cast<std::size_t>(j)]);
    auto bad=failures(s);auto fc=count(bad);++candidates;
    cover(bad);
    if(fc<minimum){minimum=fc;closest.clear();for(int j=0;j<m;++j)if(j!=a&&j!=b)closest.push_back(net[static_cast<std::size_t>(j)]);}
    if(fc==0)++sorters44;
   }
  }
  std::string extra;if(in>>extra)throw std::runtime_error("trailing data");
  std::ofstream out(argv[2]);out<<"{\n  \"seeds\": "<<total<<", \"candidates44\": "<<candidates<<", \"sorters44\": "<<sorters44<<", \"sorters45\": "<<sorters45<<", \"minimum_failed_inputs\": "<<minimum<<",\n  \"witnesses\": [";
  for(std::size_t i=0;i<witness_list.size();++i)out<<(i?", ":"")<<witness_list[i];
  out<<"],\n  \"closest_gates\": [";
  for(std::size_t i=0;i<closest.size();++i)out<<(i?", ":"")<<'['<<closest[i].first<<", "<<closest[i].second<<']';
  out<<"]\n}\n";
  std::cout<<"COMPLETE seeds="<<total<<" candidates44="<<candidates<<" sorters44="<<sorters44<<" sorters45="<<sorters45<<" minimum_failed_inputs="<<minimum<<" witnesses="<<witness_list.size()<<'\n';
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 2;}
}
