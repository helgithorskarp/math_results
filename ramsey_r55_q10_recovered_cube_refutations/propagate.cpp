// Two-watched-literal unit propagation only: no decisions, learning or RAT.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
struct Propagator {
 int n; std::vector<std::vector<int>> clauses,watch;
 std::vector<std::int8_t> value;std::vector<int> trail;std::size_t next=0,base=0;
 std::uint64_t visits=0;
 explicit Propagator(int variables):n(variables),watch(2U*std::size_t(n)+2U),value(std::size_t(n)+1U,0){}
 static std::size_t key(int x){return 2U*std::size_t(std::abs(x))+(x<0?1U:0U);}
 int val(int x)const{return (x<0?-1:1)*value[std::size_t(std::abs(x))];}
 bool set(int x){if(val(x)>0)return true;if(val(x)<0)return false;value[std::size_t(std::abs(x))]=static_cast<std::int8_t>(x>0?1:-1);trail.push_back(x);return true;}
 void add(std::vector<int> c){
  std::sort(c.begin(),c.end());c.erase(std::unique(c.begin(),c.end()),c.end());
  for(int x:c)if(std::binary_search(c.begin(),c.end(),-x))return;
  int id=static_cast<int>(clauses.size());clauses.push_back(c);
  if(c.empty())throw std::runtime_error("empty initial clause");
  if(c.size()==1){if(!set(c[0]))throw std::runtime_error("inconsistent initial units");}
  else{watch[key(c[0])].push_back(id);watch[key(c[1])].push_back(id);}
 }
 bool propagate(){
  while(next<trail.size()){
   int false_lit=-trail[next++];auto& list=watch[key(false_lit)];std::size_t i=0;
   while(i<list.size()){
    ++visits;int id=list[i];auto& c=clauses[std::size_t(id)];
    if(c[0]==false_lit)std::swap(c[0],c[1]);
    if(c[1]!=false_lit)throw std::runtime_error("watch invariant");
    if(val(c[0])>0){++i;continue;}
    std::size_t j=2;while(j<c.size()&&val(c[j])<0)++j;
    if(j<c.size()){
     std::swap(c[1],c[j]);list[i]=list.back();list.pop_back();watch[key(c[1])].push_back(id);continue;
    }
    if(val(c[0])<0)return false;
    if(!set(c[0]))throw std::runtime_error("unit assign");
    ++i;
   }
  }
  return true;
 }
 void reset(){for(std::size_t i=base;i<trail.size();++i)value[std::size_t(std::abs(trail[i]))]=0;trail.resize(base);next=base;}
 bool rup(const std::vector<int>& c){reset();for(int x:c)if(!set(-x))return true;return !propagate();}
};
int main(int argc,char**argv){try{
 if(argc!=3&&!(argc==4&&(std::string(argv[3])=="--physical"||std::string(argv[3])=="--all")))throw std::runtime_error("usage: propagate input.cnf candidates.txt [--physical|--all]");
 std::ifstream in(argv[1]),tests(argv[2]);if(!in||!tests)throw std::runtime_error("open");
 std::string p,cnf;int n;std::size_t count;if(!(in>>p>>cnf>>n>>count)||p!="p"||cnf!="cnf"||n<1||n>1000000||count>10000000)throw std::runtime_error("header");
 Propagator db(n);std::vector<int> c;long long raw;std::size_t actual=0;
 while(in>>raw){if(raw < -n || raw > n)throw std::runtime_error("literal range");int x=static_cast<int>(raw);if(x)c.push_back(x);else{db.add(c);c.clear();++actual;}}
 if(!in.eof()||!c.empty()||actual!=count)throw std::runtime_error("clause count/parser");
 if(!db.propagate())throw std::runtime_error("baseline conflict");
 db.base=db.trail.size();
 std::cout<<"{\"baseline_fixed_variables\":"<<db.base<<",\"tests\":[";bool sep=false;
 std::size_t index=0,rups=0;c.clear();while(tests>>raw){if(raw < -n || raw > n)throw std::runtime_error("candidate range");int x=static_cast<int>(raw);if(x){c.push_back(x);continue;}
  bool r=db.rup(c);if(r)++rups;if(sep)std::cout<<',';sep=true;
  std::cout<<"{\"index\":"<<index++<<",\"rup\":"<<(r?"true":"false")<<",\"assigned\":"<<db.trail.size();
  if(argc==4){std::cout<<",\"physical_values\":[";bool valsep=false;for(int v=2;v<=std::min(841,n);++v)if(db.value[std::size_t(v)]){if(valsep)std::cout<<',';valsep=true;std::cout<<(db.value[std::size_t(v)]>0?v:-v);}std::cout<<']';}
  if(argc==4&&std::string(argv[3])=="--all"){std::cout<<",\"assigned_literals\":[";bool valsep=false;for(int v=1;v<=n;++v)if(db.value[std::size_t(v)]){if(valsep)std::cout<<',';valsep=true;std::cout<<(db.value[std::size_t(v)]>0?v:-v);}std::cout<<']';}
  std::cout<<'}';c.clear();
 }
 if(!tests.eof()||!c.empty())throw std::runtime_error("candidate parser");
 std::cout<<"],\"rup\":"<<rups<<",\"not_rup\":"<<index-rups<<",\"watch_visits\":"<<db.visits<<"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
