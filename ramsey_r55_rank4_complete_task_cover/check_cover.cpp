#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using U=std::uint32_t;
using W=std::uint64_t;
using Map=std::array<int,16>;

static U transform(U code,const Map&map,int points){
 U image=0;for(int x=1;x<=points;++x)image|=((code>>(2*(x-1)))&3U)<<(2*(map[x]-1));return image;
}
static int spanrank(const std::vector<int>&xs,int rank){
 std::set<int> span{0};for(int x:xs){auto old=span;for(int y:old)span.insert(x^y);}
 int r=0;while((1U<<r)<span.size())++r;if(r>rank)throw std::runtime_error("span dimension");return r;
}
static void bases(int rank,std::vector<int>&base,std::vector<Map>&maps){
 if(static_cast<int>(base.size())==rank){Map m{};for(int x=1;x<(1<<rank);++x)for(int j=0;j<rank;++j)if((x>>j)&1)m[x]^=base[j];maps.push_back(m);return;}
 for(int x=1;x<(1<<rank);++x){base.push_back(x);if(spanrank(base,rank)==static_cast<int>(base.size()))bases(rank,base,maps);base.pop_back();}
}
static std::vector<int> support(U code,int points){
 std::vector<int> result;for(int x=1;x<=points;++x)if((code>>(2*(x-1)))&3U)result.push_back(x);return result;
}
static int weight(U code,int points){int w=0;for(int x=0;x<points;++x)w+=static_cast<int>((code>>(2*x))&3U);return w;}

int main(int argc,char**argv){
 try{
  if(argc!=5)throw std::runtime_error("usage: check_cover rank lower_weight upper_weight cover.tsv");
  int rank=std::stoi(argv[1]),lo=std::stoi(argv[2]),hi=std::stoi(argv[3]);
  if(rank<2||rank>4||lo<0||hi!=lo+1)throw std::runtime_error("invalid domain");
  int points=(1<<rank)-1;
  std::vector<Map> maps;std::vector<int> base;bases(rank,base,maps);
  W expected_group=1;for(int j=0;j<rank;++j)expected_group*=static_cast<W>((1<<rank)-(1<<j));
  if(maps.size()!=expected_group||std::set<Map>(maps.begin(),maps.end()).size()!=maps.size())throw std::runtime_error("group census");
  W burnside[2]={0,0};std::map<std::vector<int>,W> cycle_types;
  for(const auto&m:maps){
    bool seen[16]={};std::vector<int> cycles;
    for(int x=1;x<=points;++x)if(!seen[x]){int length=0,y=x;do{seen[y]=true;y=m[y];++length;}while(y!=x);cycles.push_back(length);}
    std::sort(cycles.begin(),cycles.end());++cycle_types[cycles];
    std::vector<W> poly(hi+1,0);poly[0]=1;
    for(int len:cycles){std::vector<W> next(hi+1,0);for(int w=0;w<=hi;++w)for(int digit=0;digit<4&&w+digit*len<=hi;++digit)next[w+digit*len]+=poly[w];poly=next;}
    burnside[0]+=poly[lo];burnside[1]+=poly[hi];
  }
  for(W b:burnside)if(b%expected_group)throw std::runtime_error("nonintegral Burnside quotient");
  std::set<U> nonfull;
  // Every nonspanning support lies in at least one proper linear hyperplane.
  for(int normal=1;normal<=points;++normal){
    std::vector<int> hyperplane;
    for(int x=1;x<=points;++x)if(__builtin_popcount(static_cast<unsigned>(normal&x))%2==0)hyperplane.push_back(x);
    U limit=1U<<(2*hyperplane.size());
    for(U small=0;small<limit;++small){
      U large=0;int w=0;
      for(std::size_t i=0;i<hyperplane.size();++i){U digit=(small>>(2*i))&3U;w+=static_cast<int>(digit);large|=digit<<(2*(hyperplane[i]-1));}
      if(w==lo||w==hi)nonfull.insert(large);
    }
  }
  W nonfull_count[2]={0,0};std::set<U> nonfull_canon[2];
  for(U code:nonfull){
    int category=weight(code,points)-lo;++nonfull_count[category];
    U canonical=code;for(const auto&m:maps)canonical=std::min(canonical,transform(code,m,points));
    nonfull_canon[category].insert(canonical);
  }
  std::ifstream in(argv[4]);if(!in)throw std::runtime_error("cannot open cover");
  std::string header;std::getline(in,header);if(header!="code\tzero\torbit_size\tsupport\ttriples")throw std::runtime_error("header");
  W count[2]={0,0},mass[2]={0,0};U previous=0;bool first=true;W checks=0;
  std::map<int,W> stabilizers;
  for(std::string line;std::getline(in,line);){
    std::istringstream s(line);W large_code=0,orbit=0;int zero=0,supp=0,triples=0;std::string extra;
    if(!(s>>large_code>>zero>>orbit>>supp>>triples)||(s>>extra)||large_code>=(W{1}<<(2*points)))throw std::runtime_error("malformed row");
    U code=static_cast<U>(large_code);int w=weight(code,points),category=w-lo;
    if((w!=lo&&w!=hi)||zero!=hi-w||(!first&&code<=previous))throw std::runtime_error("row order/domain");
    first=false;previous=code;
    auto xs=support(code,points);int t=0;for(int x=0;x<points;++x)t+=((code>>(2*x))&3U)==3U;
    if(supp!=static_cast<int>(xs.size())||triples!=t||spanrank(xs,rank)!=rank)throw std::runtime_error("row metadata");
    W stabilizer=0;U minimum=code;
    for(const auto&m:maps){U image=transform(code,m,points);minimum=std::min(minimum,image);stabilizer+=(image==code);++checks;}
    if(minimum!=code||stabilizer==0||expected_group%stabilizer||orbit!=expected_group/stabilizer)throw std::runtime_error("canonicality/stabilizer");
    ++count[category];mass[category]+=orbit;++stabilizers[static_cast<int>(stabilizer)];
  }
  for(int c=0;c<2;++c)if(count[c]!=burnside[c]/expected_group-nonfull_canon[c].size())throw std::runtime_error("incomplete orbit cover");
  // The identity map fixed-count polynomial independently counts all profiles.
  std::vector<W> poly(hi+1,0);poly[0]=1;
  for(int i=0;i<points;++i){std::vector<W> next(hi+1,0);for(int w=0;w<=hi;++w)for(int d=0;d<4&&w+d<=hi;++d)next[w+d]+=poly[w];poly=next;}
  for(int c=0;c<2;++c)if(mass[c]!=poly[lo+c]-nonfull_count[c])throw std::runtime_error("profile mass");
  std::cout<<"{\"status\":\"VERIFIED_COMPLETE_ROW_ORBIT_COVER\",\"rank\":"<<rank<<",\"group_order\":"<<expected_group
    <<",\"raw\":["<<poly[lo]<<','<<poly[hi]<<"],\"nonspanning\":["<<nonfull_count[0]<<','<<nonfull_count[1]
    <<"],\"spanning_orbits\":["<<count[0]<<','<<count[1]<<"],\"canonical_map_checks\":"<<checks<<",\"cycle_types\":"<<cycle_types.size()<<",\"stabilizer_histogram\":{";
  bool comma=false;for(const auto&[size,total]:stabilizers){if(comma)std::cout<<',';comma=true;std::cout<<'\"'<<size<<"\":"<<total;}
  std::cout<<"}}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
