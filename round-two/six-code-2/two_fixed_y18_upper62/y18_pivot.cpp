// Actual author: six-code-2, researcher. P/X pivot with first-fit color pruning.
// Adapted from the published free_involution_upper68 pivot; inherited guards unchanged.
#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
using Bits=std::array<std::uint64_t,3>;
std::vector<Bits> adj;
std::uint64_t nodes=0,leaves=0,cap=0;
double seconds=0;
int target=0;
std::chrono::steady_clock::time_point start;
std::ofstream output;
int size(const Bits&a){int c=0;for(auto w:a)c+=std::popcount(w);return c;}
int first(const Bits&a){for(int w=0;w<3;w++)if(a[w])return 64*w+std::countr_zero(a[w]);return -1;}
void reset(Bits&a,int v){a[v/64]&=~(std::uint64_t(1)<<(v%64));}
void set(Bits&a,int v){a[v/64]|=std::uint64_t(1)<<(v%64);}
Bits intersection(const Bits&a,const Bits&b){Bits c;for(int w=0;w<3;w++)c[w]=a[w]&b[w];return c;}
// Independent first-fit coloring bound: each class is an actual independent set.
int coloring_upper(Bits pool,int threshold){
  std::vector<int> vertices;
  while(size(pool)){int v=first(pool);reset(pool,v);vertices.push_back(v);}
  std::stable_sort(vertices.begin(),vertices.end(),[](int a,int b){return size(adj[a])>size(adj[b]);});
  std::vector<Bits> classes;
  for(int v:vertices){
    bool placed=false;
    for(auto& c:classes)if(size(intersection(c,adj[v]))==0){set(c,v);placed=true;break;}
    if(!placed){Bits c{};set(c,v);classes.push_back(c);if(static_cast<int>(classes.size())>=threshold)return threshold;}
  }
  return static_cast<int>(classes.size());
}
void bk(std::vector<int>&chosen,Bits P,Bits X){
  nodes++;
  if(nodes>cap||((nodes&4095u)==0&&std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>seconds))throw std::runtime_error("INCOMPLETE");
  if(static_cast<int>(chosen.size())+size(P)<target)return;
  if(static_cast<int>(chosen.size())>target)throw std::runtime_error("LARGER_CLIQUE");
  int need=target-static_cast<int>(chosen.size());
  if(need>1&&coloring_upper(P,need)<need)return;
  Bits all;for(int w=0;w<3;w++)all[w]=P[w]|X[w];
  if(size(all)==0){
    auto c=chosen;std::sort(c.begin(),c.end());
    for(std::size_t i=0;i<c.size();i++){if(i)output<<' ';output<<c[i];}output<<'\n';leaves++;return;
  }
  int pivot=-1,maximum=-1;
  auto q=all;
  while(size(q)){int v=first(q);reset(q,v);int s=size(intersection(P,adj[v]));if(s>maximum){pivot=v;maximum=s;}}
  Bits branch;for(int w=0;w<3;w++)branch[w]=P[w]&~adj[pivot][w];
  while(size(branch)){
    int v=first(branch);reset(branch,v);chosen.push_back(v);
    bk(chosen,intersection(P,adj[v]),intersection(X,adj[v]));
    chosen.pop_back();reset(P,v);set(X,v);
  }
}
int run(int argc,char**argv){
  if(argc!=6)throw std::runtime_error("input output nodes seconds target");
  std::ifstream in(argv[1]);int n=0;in>>n;if(!in||n<1||n>192)throw std::runtime_error("model size");adj.resize(n);
  for(int i=0;i<n;i++){int degree;in>>degree;if(!in||degree<0||degree>=n)throw std::runtime_error("degree");for(int j=0;j<degree;j++){int v;in>>v;if(!in||v<0||v>=n||v==i||(adj[i][v/64]&(std::uint64_t(1)<<(v%64))))throw std::runtime_error("edge");set(adj[i],v);}}
  if(!in)throw std::runtime_error("truncated input");
  std::string extra;if(in>>extra)throw std::runtime_error("trailing input");
  for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(((adj[i][j/64]>>(j%64))&1u)!=((adj[j][i/64]>>(i%64))&1u))throw std::runtime_error("asymmetric graph");
  target=std::stoi(argv[5]);if(target<1||target>n)throw std::runtime_error("target");
  cap=std::stoull(argv[3]);seconds=std::stod(argv[4]);if(cap<1||cap>30000000||seconds<=0||seconds>30)throw std::runtime_error("guard");output.open(argv[2]);if(!output)throw std::runtime_error("output");
  Bits pool{},excluded{};for(int i=0;i<n;i++)set(pool,i);std::vector<int> chosen;start=std::chrono::steady_clock::now();std::string status="COMPLETE";
  try{bk(chosen,pool,excluded);}catch(const std::runtime_error&e){status=e.what();}output.close();
  std::cout<<status<<" nodes "<<nodes<<" maximum_cliques "<<leaves<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
  return status=="COMPLETE"?0:2;
}
int main(int argc,char**argv){try{return run(argc,argv);}catch(const std::exception&e){std::cerr<<"ERROR "<<e.what()<<'\n';return 2;}}
