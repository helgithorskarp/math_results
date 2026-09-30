// Exact quotient page-budget exploration, not a complete signing search.
// Author: six-books-2, role researcher. Threads one; q=11 two-vertex orbits.
#include <array>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
unsigned pop(unsigned v){return __builtin_popcount(v);}
constexpr unsigned Q=11;
using Pair=std::array<unsigned,2>;
using Neighbors=std::array<unsigned,Q>;
struct Budget{unsigned i,j,kind;int outside;};
struct Form{std::string name;std::vector<Pair> red;};
int main(int argc,char**argv)try{
 if(argc!=3)throw std::runtime_error("usage: census 5_or_6 survivors.jsonl");
 std::string input=argv[1];if(input!="5"&&input!="6")throw std::runtime_error("only literal 5 or 6 accepted");
 unsigned uniform=input=="5"?5:6;
 std::ofstream survivors(argv[2]);if(!survivors)throw std::runtime_error("cannot write scratch result");
 std::vector<Pair> pairs;for(unsigned i=0;i<Q;++i)for(unsigned j=i+1;j<Q;++j)pairs.push_back({i,j});
 std::vector<Form> forms={
  {"one",{{0,1}}},{"two_adjacent",{{0,1},{0,2}}},{"two_disjoint",{{0,1},{2,3}}},
  {"3k2",{{0,1},{2,3},{4,5}}},{"p3k2",{{0,1},{1,2},{3,4}}},{"p4",{{0,1},{1,2},{2,3}}},
  {"star",{{0,1},{0,2},{0,3}}},{"triangle",{{0,1},{0,2},{1,2}}}};
 for(auto const&f:forms){if(f.red.size()>uniform-3)continue;
  Neighbors r{};for(auto p:f.red){r[p[0]]|=1u<<p[1];r[p[1]]|=1u<<p[0];}
  std::vector<Pair> available;for(auto p:pairs)if(!(r[p[0]]>>p[1]&1))available.push_back(p);
  unsigned k=uniform-f.red.size();std::vector<unsigned> choice(k);for(unsigned i=0;i<k;++i)choice[i]=i;
  std::uint64_t all=0,neighbors_pass=0,matching_pass=0,flag_calls=0,color_survivors=0,flag_survivors=0;
  bool done=false;
  while(!done){++all;Neighbors b{};std::uint64_t blue_word=0;
   for(auto index:choice){auto p=available[index];b[p[0]]|=1u<<p[1];b[p[1]]|=1u<<p[0];
    auto id=std::find(pairs.begin(),pairs.end(),p)-pairs.begin();blue_word|=1ull<<id;}
   bool good=true;
   for(auto p:f.red)if(pop(b[p[0]]|b[p[1]])<3){good=false;break;}
   if(good){++neighbors_pass;
    for(auto p:pairs){auto i=p[0],j=p[1];if((r[i]|b[i])>>j&1)continue;
     int opposite=pop(r[i]&b[j])+pop(b[i]&r[j]);
     int red_known=int(pop(r[i])+pop(r[j]))-opposite;
     int blue_known=int(pop(b[i])+pop(b[j]))-opposite;
     int both_matching=9-int(pop(r[i]|b[i])+pop(r[j]|b[j]))+int(pop((r[i]|b[i])&(r[j]|b[j])));
     if(std::max(0,both_matching+blue_known-6)>std::min(both_matching,3-red_known)){good=false;break;}
    }
    if(good){++matching_pass;std::vector<Budget> budgets;
     for(auto p:pairs){auto i=p[0],j=p[1];unsigned kind=(r[i]>>j&1)?0:1;if(!((r[i]|b[i])>>j&1))continue;
      int outside=0;for(unsigned t=0;t<Q;++t)if(t!=i&&t!=j){
       int di=(r[i]>>t&1)?2:((b[i]>>t&1)?0:1),dj=(r[j]>>t&1)?2:((b[j]>>t&1)?0:1);
       outside+=(kind==0?di*dj:(2-di)*(2-dj));
      }
      budgets.push_back({i,j,kind,outside});
     }
     std::vector<unsigned> flags;
     for(unsigned word=0;word<(1u<<Q);++word){++flag_calls;bool feasible=true;
      for(unsigned i=0;i<Q;++i){if(word>>i&1){if(2*pop(r[i])>3){feasible=false;break;}}
       else if(2*pop(b[i])>6){feasible=false;break;}}
      if(!feasible)continue;
      for(auto budget:budgets){int sum=(word>>budget.i&1)+(word>>budget.j&1);
       int pages=budget.outside+2*(budget.kind==0?sum:2-sum);
       if(pages>(budget.kind==0?6:12)){feasible=false;break;}}
      if(feasible)flags.push_back(word);
     }
     if(!flags.empty()){++color_survivors;flag_survivors+=flags.size();
      survivors<<"{\"red_form\":\""<<f.name<<"\",\"blue_mask\":"<<blue_word<<",\"flags\":[";
      for(unsigned i=0;i<flags.size();++i){if(i)survivors<<',';survivors<<flags[i];}survivors<<"]}\n";
     }
    }
   }
   int pos=int(k)-1;while(pos>=0 && choice[pos]==available.size()-k+pos)--pos;
   if(pos<0)done=true;else{++choice[pos];for(unsigned t=pos+1;t<k;++t)choice[t]=choice[t-1]+1;}
  }
  std::cout<<"{\"agent\":\"six-books-2\",\"role\":\"researcher\",\"uniform_pairs\":"<<uniform<<",\"red_form\":\""<<f.name<<"\",\"complete\":true,\"all_patterns\":"<<all
   <<",\"three_blue_neighbors_pass\":"<<neighbors_pass<<",\"matching_budget_pass\":"<<matching_pass<<",\"flag_calls\":"<<flag_calls<<",\"color_pattern_survivors\":"<<color_survivors<<",\"flag_survivors\":"<<flag_survivors<<"}\n"<<std::flush;
 }
 survivors.close();if(!survivors)throw std::runtime_error("write failure");
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 2;}
