#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using Rows=std::array<std::uint32_t,22>;
using Edge=std::pair<int,int>;
using Orbit=std::array<Edge,3>;
void need(bool b,const char* s){if(!b)throw std::runtime_error(s);}
int action(int u){return 3*(u/3)+(u+1)%3;}
Edge ordered(int a,int b){return std::minmax(a,b);}
void change(Rows& r,const Orbit& o,bool add){for(auto e:o){auto a=std::uint32_t(1)<<e.first,b=std::uint32_t(1)<<e.second;
 need(bool(r[e.first]&b)==!add && bool(r[e.second]&a)==!add,"orbit update color");
 if(add){r[e.first]|=b;r[e.second]|=a;}else{r[e.first]&=~b;r[e.second]&=~a;}}}
int bad(const Rows& r){
 int n=0;
 for(int u=0;u<22;++u){for(int v=u+1;v<22;++v){
  if((r[u]>>v&1u) && __builtin_popcount(r[u]&r[v])>=4)++n;
 }}
 return n;
}
struct BlueBook{int u=-1,v=-1;std::uint32_t pages=0;};
BlueBook blue_book(const Rows& r){
 const std::uint32_t full=(1u<<22)-1;
 for(int u=0;u<22;++u){for(int v=u+1;v<22;++v){
  if(r[u]>>v&1u)continue;
  auto p=full&~(r[u]|r[v]|(1u<<u)|(1u<<v));
  if(__builtin_popcount(p)>=7){std::uint32_t seven=0;for(int k=0;k<7;++k){auto b=p&-p;seven|=b;p-=b;}return {u,v,seven};}
 }}
 return {};
}
std::uint64_t choose(int n,int k){std::uint64_t v=1;for(int j=1;j<=k;++j)v=v*(n-j+1)/j;return v;}
int main(int argc,char** argv){try{
 need(argc==4,"usage: checker parents.txt optimal.txt pools.txt");
 auto start=std::chrono::steady_clock::now();
 const std::array<Edge,21> labels={{{0,1},{1,2},{0,2},{0,3},{1,4},{2,5},{0,4},{1,5},{2,3},{0,5},{1,3},{2,4},{0,6},{1,6},{2,6},{3,4},{4,5},{3,5},{3,6},{4,6},{5,6}}};
 std::array<int,21> ground{};for(int u=0;u<21;++u)ground[u]=(1<<labels[u].first)|(1<<labels[u].second);
 std::array<std::vector<Orbit>,2> orbits;
 Rows seed{};
 for(int color=0;color<2;++color){bool seen[21][21]{};
  for(int u=0;u<21;++u)for(int v=u+1;v<21;++v){
   bool red=(ground[u]&ground[v])==0;if(red!=(color==0)||seen[u][v])continue;
   Orbit o{};Edge e={u,v};
   for(int t=0;t<3;++t){need(!seen[e.first][e.second],"edge orbit overlap");seen[e.first][e.second]=true;o[t]=e;e=ordered(action(e.first),action(e.second));}
   need(e==Edge(u,v),"edge orbit closure");orbits[color].push_back(o);
  }
  need(orbits[color].size()==35,"35 color orbits");
 }
 for(auto& o:orbits[0])change(seed,o,true);
 need(bad(seed)==0,"KG21 red baseline");
 std::ifstream input(argv[1]);need(bool(input),"read frozen parents");
 std::ofstream output(argv[2]);need(bool(output),"write optimal sets");
 std::ofstream pool_output(argv[3]);need(bool(pool_output),"write promotion pools");
 std::string line;int parent=0;std::uint64_t total=0,optimal_count=0;
 std::set<Rows> seen_repairs;std::set<std::array<std::uint64_t,3>> seen_parents;
 std::uint64_t blocked=0,residual=0,subset_tests=0,subset_red=0,subset_blue=0,subset_both=0;
 std::map<int,int> pool_hist;
 std::ostringstream details;details<<"[";
 while(std::getline(input,line)){
  need(!line.empty(),"blank recipe row");std::istringstream stream(line);
  int index,weight,minimum;std::array<int,3> J{};std::array<int,4>P{};std::array<int,9>D{};
  need(bool(stream>>index>>weight),"recipe header");
  for(int& x:J)need(bool(stream>>x),"J field");
  for(int& x:P)need(bool(stream>>x),"P field");
  for(int& x:D)need(bool(stream>>x),"D field");
  need(index>=0 && index<305874 && weight==6,"declared case and weight");
  auto domain=[](const auto& a,int upper){return std::is_sorted(a.begin(),a.end()) && std::adjacent_find(a.begin(),a.end())==a.end() && a.front()>=0 && a.back()<upper;};
  need(domain(J,7) && domain(P,35) && domain(D,35),"strict sorted recipe domain");
  std::uint64_t jmask=0,pmask=0,dmask=0;
  for(int x:J)jmask|=std::uint64_t(1)<<x;
  for(int x:P)pmask|=std::uint64_t(1)<<x;
  for(int x:D)dmask|=std::uint64_t(1)<<x;
  need(seen_parents.insert({jmask,pmask,dmask}).second,"duplicate parent recipe");
  need(bool(stream>>minimum) && (minimum==4||minimum==5),"claimed minimum");
  std::vector<int> witness(minimum);std::uint64_t witness_mask=0;
  for(int& x:witness){need(bool(stream>>x) && x>=0&&x<35,"upper witness domain");need(!(witness_mask>>x&1),"duplicate upper deletion");witness_mask|=std::uint64_t(1)<<x;}
  std::string extra;need(!(stream>>extra),"extra recipe field");
  Rows rows=seed;
  for(int p:P)change(rows,orbits[1][p],true);
  for(int d:D)change(rows,orbits[0][d],false);
  for(int j:J)for(int u=3*j;u<3*j+3;++u){rows[u]|=1u<<21;rows[21]|=1u<<u;}
  need(blue_book(rows).u<0 && bad(rows)>0,"literal parent blue cap and red obstruction");
  std::vector<int> available;for(int d=0;d<35;++d)if(std::find(D.begin(),D.end(),d)==D.end())available.push_back(d);
  need(available.size()==26,"26 available deletions");
  Rows upper=rows;for(int d:witness){need(std::find(available.begin(),available.end(),d)!=available.end(),"upper intersects previous deletions");change(upper,orbits[0][d],false);}
  need(bad(upper)==0,"declared upper graph literal red cap");
  std::vector<std::uint64_t> counts(minimum+1),zeros(minimum+1);std::vector<int> minima(minimum+1,1000);
  bool upper_seen=false;
  auto analyze_promotions=[&](std::uint64_t removed){
   if(!seen_repairs.insert(rows).second)return;
   std::vector<int> eligible;std::uint64_t eligible_mask=0;int edges=0;
   for(auto r:rows)edges+=__builtin_popcount(r);
   need(edges==198-6*minimum,"literal red-repair edge count");edges/=2;
   for(int p=0;p<35;++p){if(pmask>>p&1)continue;Rows child=rows;change(child,orbits[1][p],true);
    if(!bad(child)){eligible.push_back(p);eligible_mask|=std::uint64_t(1)<<p;}
   }
   ++pool_hist[int(eligible.size())];Rows maximal=rows;for(int p:eligible)change(maximal,orbits[1][p],true);
   auto witness=blue_book(maximal);
   pool_output<<jmask<<' '<<pmask<<' '<<(dmask|removed)<<' '<<edges<<' '<<eligible_mask<<' '<<witness.u<<' '<<witness.v<<' '<<witness.pages<<'\n';
   if(witness.u>=0){++blocked;return;}
   ++residual;need(eligible.size()<21,"predeclared residual finite-subset scope");
   for(std::uint64_t subset=0;subset<(std::uint64_t(1)<<eligible.size());++subset){
    Rows child=rows;
    for(std::size_t i=0;i<eligible.size();++i)if(subset>>i&1)change(child,orbits[1][eligible[i]],true);
    bool red=!bad(child),blue=blue_book(child).u<0;
    ++subset_tests;subset_red+=red;subset_blue+=blue;subset_both+=red&&blue;
    need(!red||!blue,"valid22 construction found in residual pool: preserve input and inspect subset");
   }
  };
  auto enumerate=[&](auto&& self,int first,int left,int quota,std::uint64_t mask)->void{
   if(!left){
    ++counts[quota];++total;
    if((total&65535)==0)need(std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<25,"predeclared25-second checker limit");
    int b=bad(rows);minima[quota]=std::min(minima[quota],b);
    if(!b){++zeros[quota];need(quota==minimum,"red repair below claimed minimum");output<<parent<<' '<<mask<<'\n';++optimal_count;if(mask==witness_mask)upper_seen=true;analyze_promotions(mask);}
    return;
   }
   for(int i=first;i+left<=int(available.size());++i){int d=available[i];change(rows,orbits[0][d],false);self(self,i+1,left-1,quota,mask|(std::uint64_t(1)<<d));change(rows,orbits[0][d],true);}
  };
  for(int quota=0;quota<=minimum;++quota){enumerate(enumerate,0,quota,quota,0);need(counts[quota]==choose(26,quota),"complete combination coverage");}
  need(upper_seen && zeros[minimum]>0,"declared upper belongs to complete optimum inventory");
  if(parent)details<<',';
  details<<"{\"ordinal\":"<<parent<<",\"index\":"<<index<<",\"minimum\":"<<minimum<<",\"counts\":[";
  for(int k=0;k<=minimum;++k){if(k)details<<',';details<<counts[k];}details<<"],\"bad_minima\":[";
  for(int k=0;k<=minimum;++k){if(k)details<<',';details<<minima[k];}details<<"],\"optimal_repairs\":"<<zeros[minimum]<<'}';
  ++parent;
 }
 need(input.eof() && parent==28,"complete28 parent recipe coverage");output.close();need(bool(output),"optimal stream complete write");details<<']';
 pool_output.close();need(bool(pool_output),"pool stream complete write");
 std::cout<<"{\"status\":\"COMPLETE_DIRECT_GRAPH_REPAIR_AND_COMPLETION_CENSUS\",\"parents\":"<<details.str()<<",\"total_deletion_subsets\":"<<total<<",\"total_optimal_repairs\":"<<optimal_count<<",\"unique_repairs\":"<<seen_repairs.size()<<",\"permanently_blue_blocked\":"<<blocked<<",\"residual_pools\":"<<residual<<",\"promotion_subset_tests\":"<<subset_tests<<",\"subset_red_valid\":"<<subset_red<<",\"subset_blue_valid\":"<<subset_blue<<",\"subset_both_valid\":"<<subset_both<<",\"pool_hist\":{";
 bool first=true;for(auto item:pool_hist){if(!first)std::cout<<',';first=false;std::cout<<'"'<<item.first<<"\":"<<item.second;}
 std::cout<<"},\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}\n";
 return 0;
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
