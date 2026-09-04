// Rebuild pair orbits by union/find under the actual 43-vertex permutation.
// Reconstruct both projected five-set clauses, then compare the complete
// clause multiset. This file does not invoke/import the Python generator.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using Clause=std::vector<int>;
using Formula=std::vector<Clause>;
void require(bool ok,const std::string& msg){if(!ok)throw std::runtime_error(msg);}
struct DSU{
 std::vector<int> p;
 explicit DSU(int n):p(n){std::iota(p.begin(),p.end(),0);}
 int root(int a){return p[a]==a?a:p[a]=root(p[a]);}
 void join(int a,int b){p[root(a)]=root(b);}
};
int main(int argc,char**argv){try{
 require(argc==4,"usage: independent_formula H SYMMETRY(0|1) INPUT.cnf");
 const int h=std::stoi(argv[1]), sym=std::stoi(argv[2]);
 require((h==0||h==1)&&sym==h,"use symmetry=0 for h=0 and symmetry=1 for h=1");
 std::array<int,8> cols=h?std::array<int,8>{0,1,2,3,4,5,6,7}:std::array<int,8>{0,1,2,3,5,5,6,6};
 std::array<std::array<int,43>,43> index{};
 std::vector<std::pair<int,int>> pairs;
 for(int a=0;a<43;++a)for(int b=a+1;b<43;++b){index[a][b]=index[b][a]=pairs.size();pairs.emplace_back(a,b);}
 auto perm=[](int v){return v<3?v:3+5*((v-3)/5)+(v-3+1)%5;};
 DSU dsu(pairs.size());
 for(auto [a,b]:pairs)dsu.join(index[a][b],index[perm(a)][perm(b)]);
 std::map<int,std::vector<int>> orbits;
 for(int e=0;e<(int)pairs.size();++e)orbits[dsu.root(e)].push_back(e);
 require(orbits.size()==183,"incorrect number of actual edge orbits");
 int singleton=0;
 for(const auto& [r,es]:orbits){require(es.size()==1||es.size()==5,"bad orbit length");singleton+=es.size()==1;}
 require(singleton==3,"bad fixed-pair count");
 std::map<int,int> labels;
 auto assign=[&](int a,int b,int value){int r=dsu.root(index[a][b]);require(!labels.count(r),"orbit labeled twice");labels[r]=value;};
 const int yes=1000;
 assign(0,1,yes);assign(0,2,-yes);assign(1,2,-yes);
 for(int f=0;f<3;++f)for(int c=0;c<8;++c)assign(f,3+5*c,(cols[c]&(1<<f))?yes:-yes);
 for(int c=0;c<8;++c){assign(3+5*c,4+5*c,c+1);assign(3+5*c,5+5*c,-c-1);}
 std::array<std::array<std::array<int,5>,8>,8> cross{};
 int next=9;
 for(int a=0;a<8;++a)for(int b=a+1;b<8;++b)for(int k=0;k<5;++k){cross[a][b][k]=next;assign(3+5*a,3+5*b+k,next++);}
 require(next==149&&labels.size()==183,"incomplete semantic orbit assignment");
 std::vector<int> values;
 for(auto [a,b]:pairs)values.push_back(labels.at(dsu.root(index[a][b])));
 std::set<Clause> base;
 long five_sets=0;
 for(int a=0;a<39;++a)for(int b=a+1;b<40;++b)for(int c=b+1;c<41;++c)
 for(int d=c+1;d<42;++d)for(int e=d+1;e<43;++e){
  ++five_sets;std::array<int,5> vertices{a,b,c,d,e};
  for(int color=0;color<2;++color){
   Clause clause;bool tautology=false;
   for(int i=0;i<5;++i)for(int j=i+1;j<5;++j){
    int lit=values[index[vertices[i]][vertices[j]]];if(color)lit=-lit;
    if(lit==yes)tautology=true;else if(lit!=-yes)clause.push_back(lit);
   }
   std::sort(clause.begin(),clause.end());clause.erase(std::unique(clause.begin(),clause.end()),clause.end());
   for(int lit:clause)if(std::binary_search(clause.begin(),clause.end(),-lit))tautology=true;
   if(!tautology)base.insert(clause);
  }
 }
 require(five_sets==962598,"five-set count");
 Formula expected(base.begin(),base.end());const auto base_count=expected.size();
 if(sym){
  expected.push_back({1});
  for(int b=1;b<8;++b)for(int number=0;number<32;++number){
   std::array<int,5> word{};for(int k=0;k<5;++k)word[k]=(number>>k)&1;
   bool minimal=true;
   for(int shift=1;shift<5;++shift){std::array<int,5> rotated{};for(int k=0;k<5;++k)rotated[k]=word[(k+shift)%5];if(rotated<word)minimal=false;}
   if(!minimal){Clause clause;for(int k=0;k<5;++k)clause.push_back(word[k]?-cross[0][b][k]:cross[0][b][k]);expected.push_back(clause);}
  }
 }
 std::ifstream input(argv[3]);require(bool(input),"cannot read CNF");
 std::string p,cnf;int vars;size_t declared;
 require(bool(input>>p>>cnf>>vars>>declared)&&p=="p"&&cnf=="cnf"&&vars==148,"bad DIMACS header");
 Formula actual;Clause row;int lit;
 while(input>>lit){if(lit==0){actual.push_back(row);row.clear();}else{require(std::abs(lit)<=148,"out-of-range literal");row.push_back(lit);}}
 require(input.eof()&&row.empty()&&actual.size()==declared,"malformed DIMACS tail/count");
 auto normalize=[](Formula& formula){for(auto& clause:formula){std::sort(clause.begin(),clause.end());require(std::adjacent_find(clause.begin(),clause.end())==clause.end(),"duplicate literal");}std::sort(formula.begin(),formula.end());};
 normalize(actual);normalize(expected);
 require(actual==expected,"complete clause multiset mismatch");
 std::cout<<"VERIFIED h="<<h<<" symmetry="<<sym<<" edge_orbits="<<orbits.size()<<" variables=148 five_sets="<<five_sets<<" base_clauses="<<base_count<<" total_clauses="<<expected.size()<<"\n";
 return 0;
 }catch(const std::exception& error){std::cerr<<"ERROR: "<<error.what()<<"\n";return 1;}}
