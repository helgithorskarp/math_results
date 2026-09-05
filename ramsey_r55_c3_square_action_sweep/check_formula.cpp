// Independent unordered-pair DSU and complete literal five-set reconstruction.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <vector>
using Pair=std::pair<int,int>;
using Clause=std::vector<int>;
void require(bool ok,const char* why){if(!ok)throw std::runtime_error(why);}
int main(int argc,char** argv){try{
  require(argc==8,"usage: check_formula a b0 b1 b2 b3 c FILE");
  int a=std::stoi(argv[1]),c=std::stoi(argv[6]);
  std::array<int,4> b{};
  for(int i=0;i<4;++i)b[i]=std::stoi(argv[i+2]);
  require(a>=0 && c>=0 && std::all_of(b.begin(),b.end(),[](int x){return x>=0;}),"negative multiplicity");
  require(a+3*std::accumulate(b.begin(),b.end(),0)+9*c==43,"vertex count");
  require(std::is_sorted(b.begin(),b.end()),"unordered multiplicities");
  for(int x:b)require(a+3*x<=10,"fixed-point bound");
  std::array<int,43> g{},h{};
  std::iota(g.begin(),g.end(),0);std::iota(h.begin(),h.end(),0);
  int offset=a;
  const std::array<Pair,4> coefficients{Pair{1,0},Pair{0,1},Pair{1,1},Pair{1,2}};
  for(int line=0;line<4;++line)for(int copy=0;copy<b[line];++copy){
    for(int t=0;t<3;++t){g[offset+t]=offset+(t+coefficients[line].first)%3;
      h[offset+t]=offset+(t+coefficients[line].second)%3;}
    offset+=3;
  }
  for(int copy=0;copy<c;++copy){
    for(int u=0;u<3;++u)for(int v=0;v<3;++v){
      g[offset+3*u+v]=offset+3*((u+1)%3)+v;
      h[offset+3*u+v]=offset+3*u+(v+1)%3;
    }offset+=9;
  }
  require(offset==43,"action coverage");
  for(int i=0;i<43;++i)require(g[g[g[i]]]==i && h[h[h[i]]]==i && g[h[i]]==h[g[i]],"group relations");
  int index[43][43]{};
  std::vector<Pair> pairs;
  for(int u=0;u<43;++u)for(int v=u+1;v<43;++v){
    index[u][v]=index[v][u]=int(pairs.size());pairs.emplace_back(u,v);
  }
  std::vector<int> parent(903);std::iota(parent.begin(),parent.end(),0);
  auto root=[&](int i){while(parent[i]!=i)i=parent[i];return i;};
  for(int i=0;i<903;++i){auto [u,v]=pairs[i];
    parent[root(index[g[u]][g[v]])]=root(i);
    parent[root(index[h[u]][h[v]])]=root(i);
  }
  std::map<int,Pair> least;
  for(int i=0;i<903;++i){int r=root(i);if(!least.count(r)||pairs[i]<least.at(r))least[r]=pairs[i];}
  std::vector<Pair> representatives;for(auto const& row:least)representatives.push_back(row.second);
  std::sort(representatives.begin(),representatives.end());
  std::map<Pair,int> names;int nv=0;for(Pair p:representatives)names[p]=++nv;
  int edge[43][43]{};
  for(int i=0;i<903;++i){auto [u,v]=pairs[i];edge[u][v]=edge[v][u]=names.at(least.at(root(i)));}
  std::set<Clause> clauses;
  int count=0;
  for(int u=0;u<43;++u)for(int v=u+1;v<43;++v)for(int w=v+1;w<43;++w)
  for(int x=w+1;x<43;++x)for(int y=x+1;y<43;++y){
    ++count;std::array<int,5> vs{u,v,w,x,y};
    for(int sign:{-1,1}){Clause q;for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)q.push_back(sign*edge[vs[i]][vs[j]]);
      std::sort(q.begin(),q.end());q.erase(std::unique(q.begin(),q.end()),q.end());clauses.insert(q);}
  }
  require(count==962598,"five-set coverage");
  size_t ramsey=clauses.size();clauses.insert({1});
  std::vector<Clause> canonical(clauses.begin(),clauses.end());
  std::sort(canonical.begin(),canonical.end(),[](Clause const& x,Clause const& y){return x.size()==y.size()?x<y:x.size()<y.size();});
  std::ifstream input(argv[7]);require(bool(input),"open CNF");std::string line;
  require(bool(std::getline(input,line)) && line=="p cnf "+std::to_string(nv)+" "+std::to_string(canonical.size()),"header mismatch");
  for(Clause const& q:canonical){std::ostringstream expected;for(size_t i=0;i<q.size();++i){if(i)expected<<' ';expected<<q[i];}expected<<" 0";
    require(bool(std::getline(input,line)) && line==expected.str(),"complete clause mismatch");}
  require(!std::getline(input,line),"trailing content");
  std::cout<<"FORMULA_AUDIT variables="<<nv<<" clauses="<<canonical.size()<<" ramsey_clauses="<<ramsey<<" five_sets="<<count<<" PASS\n";
}catch(std::exception const& e){std::cerr<<e.what()<<'\n';return 1;}}
