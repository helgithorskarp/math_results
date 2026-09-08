// Strict RUP-only ASCII LRAT checker. No RAT fallback, including for empty clauses.
#include <charconv>
#include <climits>
#include <cstdlib>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include <chrono>
struct Clause { bool active=false; std::vector<int> literals; };
void need(bool x,const std::string& message){if(!x)throw std::runtime_error(message);}
std::vector<std::string> tokens(const std::string& line){
 std::vector<std::string> out;std::size_t i=0;
 while(i<line.size()){
  while(i<line.size()&&(line[i]==' '||line[i]=='\t'||line[i]=='\r'))++i;
  auto j=i;while(i<line.size()&&line[i]!=' '&&line[i]!='\t'&&line[i]!='\r')++i;
  if(i>j)out.push_back(line.substr(j,i-j));
 }return out;
}
int number(const std::string& s){
 long long x=0;auto r=std::from_chars(s.data(),s.data()+s.size(),x);
 need(r.ec==std::errc()&&r.ptr==s.data()+s.size()&&x>=-INT_MAX&&x<=INT_MAX,"integer syntax/range");return static_cast<int>(x);
}
int main(int argc,char** argv){
 try{
  need(argc==3,"usage: strict_lrat formula.cnf proof.lrat");
  auto start=std::chrono::steady_clock::now();std::ifstream cnf(argv[1]);need(bool(cnf),"CNF open");
  std::string line;int n=0,m=0;bool header=false;std::vector<Clause> db(1);std::vector<int> pending;
  while(std::getline(cnf,line)){
   auto t=tokens(line);if(t.empty()||t[0]=="c")continue;
   if(t[0]=="p"){
    need(!header&&t.size()==4&&t[1]=="cnf","CNF header");n=number(t[2]);m=number(t[3]);need(n>0&&m>=0,"CNF dimensions");header=true;continue;
   }
   need(header,"CNF data before header");
   for(const auto& word:t){int x=number(word);
    if(x){need(std::abs(x)<=n,"CNF variable");pending.push_back(x);}
    else{db.push_back({true,std::move(pending)});pending.clear();}
   }
  }
  need(header&&cnf.eof()&&pending.empty()&&db.size()==static_cast<std::size_t>(m)+1,"CNF clause count");
  std::vector<std::uint64_t> stamp(static_cast<std::size_t>(n)+1,0);
  std::vector<signed char> value(static_cast<std::size_t>(n)+1,0);
  std::uint64_t epoch=0,adds=0,dels=0,hints_used=0,proof_lines=0;
  int last=m;bool empty_proved=false;
  std::ifstream proof(argv[2]);need(bool(proof),"LRAT open");
  while(std::getline(proof,line)){
   ++proof_lines;auto t=tokens(line);if(t.empty()||t[0]=="c")continue;
   need(t.size()>=3,"short LRAT line");int id=number(t[0]);need(id>=0,"negative step label");
   if(t[1]=="d"){
    need(t.back()=="0","deletion terminator");
    for(std::size_t k=2;k+1<t.size();++k){int h=number(t[k]);need(h>0&&h<static_cast<int>(db.size())&&db[h].active,"invalid deletion");db[h].active=false;std::vector<int>().swap(db[h].literals);++dels;}
    continue;
   }
   need(id>last,"nonincreasing or reused addition label");last=id;
   std::size_t k=1;std::vector<int> clause;
   for(;k<t.size();++k){int x=number(t[k]);if(!x){++k;break;}need(std::abs(x)<=n,"LRAT variable");clause.push_back(x);}
   need(k<t.size()&&t.back()=="0","addition/hint terminators");
   ++epoch;need(epoch!=0,"assignment stamp overflow");bool conflict=false;
   for(int x:clause){int v=std::abs(x);signed char a=x>0?-1:1;
    if(stamp[v]==epoch&&value[v]!=a){conflict=true;break;}
    stamp[v]=epoch;value[v]=a;
   }
   for(;k+1<t.size();++k){
    int h=number(t[k]);need(h>0,"only positive RUP hints supported");
    need(h<static_cast<int>(db.size())&&db[h].active,"missing/deleted hint clause");
    if(conflict)continue;
    ++hints_used;bool satisfied=false;int unit=0;bool multiple=false;
    for(int x:db[h].literals){int v=std::abs(x);
     if(stamp[v]==epoch){if(value[v]==(x>0?1:-1)){satisfied=true;break;}}
     else if(unit==0)unit=x;else if(unit!=x)multiple=true;
    }
    if(satisfied)continue; // Redundant already-satisfied hints make no inference.
    need(!multiple,"hint is neither unit nor conflicting at line "+std::to_string(proof_lines));
    if(unit==0){conflict=true;continue;}
    int v=std::abs(unit);stamp[v]=epoch;value[v]=unit>0?1:-1;
   }
   need(conflict,"RUP hints ended without contradiction at line "+std::to_string(proof_lines));
   if(db.size()<=static_cast<std::size_t>(id))db.resize(static_cast<std::size_t>(id)+1);
   db[id]={true,std::move(clause)};++adds;if(db[id].literals.empty())empty_proved=true;
  }
  need(proof.eof()&&empty_proved,"no checked empty clause");
  double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout<<"VERIFIED_STRICT_RUP_LRAT\n";
  std::cout<<"{\"variables\":"<<n<<",\"original_clauses\":"<<m<<",\"additions\":"<<adds<<",\"deletions\":"<<dels<<",\"hints_used\":"<<hints_used<<",\"proof_lines\":"<<proof_lines<<",\"seconds\":"<<seconds<<"}\n";
 }catch(const std::exception& e){std::cerr<<"REJECTED: "<<e.what()<<'\n';return 1;}
}
