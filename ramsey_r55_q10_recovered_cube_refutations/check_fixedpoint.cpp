// Independent full-clause audit of supplied partial fixed points.
// No watched literals, propagation algorithm, solver, or producer code.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
void need(bool b,const char* message){if(!b)throw std::runtime_error(message);}
std::vector<int> row(const std::string& line,int n){
 std::istringstream s(line);long long x;std::vector<int> r;bool end=false;
 while(s>>x){need(!end,"trailing token");need(x>=-n&&x<=n,"literal range");if(!x)end=true;else r.push_back(static_cast<int>(x));}
 need(s.eof()&&end,"row format");return r;
}
int main(int argc,char**argv){try{
 need(argc==4,"usage: check-fixedpoint formula.cnf negated-cubes.txt fixedpoints.txt");
 std::ifstream f(argv[1]),q(argv[2]),a(argv[3]);need(bool(f)&&bool(q)&&bool(a),"open");
 std::string p,kind;int n;std::size_t m;need(bool(f>>p>>kind>>n>>m),"header");
 need(p=="p"&&kind=="cnf"&&n>0&&n<=1000000&&m<=10000000,"dimensions");
 std::vector<std::vector<int>> clauses;std::vector<int> c;long long x;
 while(f>>x){need(x>=-n&&x<=n,"literal range");if(x)c.push_back(static_cast<int>(x));else{std::sort(c.begin(),c.end());c.erase(std::unique(c.begin(),c.end()),c.end());clauses.push_back(c);c.clear();}}
 need(f.eof()&&c.empty()&&clauses.size()==m,"formula completeness");
 std::size_t checked=0;std::uint64_t scans=0;std::string query,assignment;
 while(std::getline(q,query)){
  need(bool(std::getline(a,assignment)),"missing fixed point");
  std::vector<std::int8_t> value(std::size_t(n)+1U,0);
  for(int v:row(assignment,n)){auto& cell=value[std::size_t(std::abs(v))];need(!cell,"duplicate variable");cell=static_cast<std::int8_t>(v>0?1:-1);}
  for(int v:row(query,n))need(value[std::size_t(std::abs(v))]==(v>0?-1:1),"cube not extended");
  for(const auto& clause:clauses){
   ++scans;int live=0;bool satisfied=false;
   for(int v:clause){int bit=value[std::size_t(std::abs(v))];if(bit&&(bit>0)==(v>0)){satisfied=true;break;}if(!bit&&++live>=2)break;}
   need(satisfied||live>=2,"not a consistent closed partial assignment");
  }
  ++checked;
 }
 need(!std::getline(a,assignment),"extra fixed point");
 std::cout<<"{\"status\":\"VERIFIED_UNIT_CONSISTENT_FIXED_POINTS\",\"cases\":"<<checked<<",\"clauses_scanned\":"<<scans<<"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
