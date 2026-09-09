// Independent reverse audit: every clause must identify one physical forbidden
// subset, and every nontrivial forbidden subset must occur exactly once.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
static void need(bool ok,const string& why){if(!ok)throw runtime_error(why);}
static array<array<int,23>,23> pinned;
static vector<pair<int,int>> vars;
static unsigned long long total_clauses=0,total_witnesses=0;
static void setup(const string& row){
  need(row.size()==5&&row[0]=='F',"graph6 format");
  for(auto& r:pinned)r.fill(-1);
  for(int b=0;b<4;b++)for(int i=4*b;i<4*b+4;i++)for(int j=i+1;j<4*b+4;j++)pinned[i][j]=0;
  int bit=0;
  for(int j=1;j<7;j++)for(int i=0;i<j;i++,bit++){
    unsigned c=static_cast<unsigned char>(row[1+bit/6]);
    need(c>=63&&c<=126,"graph6 character");
    pinned[16+i][16+j]=((c-63)>>(5-bit%6))&1;
  }
  need(((static_cast<unsigned char>(row[4])-63)&7)==0,"graph6 padding");
  vars.clear();vars.push_back({-1,-1});
  for(int i=0;i<23;i++)for(int j=i+1;j<23;j++)if(pinned[i][j]<0)vars.push_back({i,j});
  need(vars.size()==209,"physical variable bijection");
}
static bool viable(uint32_t mask,int forbidden){
  for(int i=0;i<23;i++)if(mask>>i&1)for(int j=i+1;j<23;j++)if(mask>>j&1)
    if(pinned[i][j]>=0&&pinned[i][j]!=forbidden)return false;
  return true;
}
static void subsets(int k,int begin,uint32_t mask,int forbidden,set<uint32_t>& out){
  if(k==0){if(viable(mask,forbidden))out.insert(mask);return;}
  for(int i=begin;i<=23-k;i++)subsets(k-1,i+1,mask|(1U<<i),forbidden,out);
}
static void audit(const string& path){
  ifstream in(path);need(bool(in),"missing CNF "+path);
  string p,cnf;int n,count;in>>p>>cnf>>n>>count;
  need(p=="p"&&cnf=="cnf"&&n==208&&count>0,"CNF header");
  array<set<uint32_t>,2> seen,expected;
  subsets(4,0,0,1,expected[1]);subsets(5,0,0,0,expected[0]);
  for(int c=0;c<count;c++){
    set<int> literals;uint32_t vertices=0;int sign=0,lit;bool ended=false;
    while(in>>lit){
      if(lit==0){ended=true;break;}
      need(lit>=-208&&lit<=208,"literal range");
      int s=lit>0?1:-1;need(sign==0||sign==s,"mixed clause colors");sign=s;
      need(literals.insert(lit).second,"duplicate literal");
      auto [i,j]=vars[abs(lit)];vertices|=1U<<i;vertices|=1U<<j;
    }
    need(ended&&sign!=0,"truncated or empty clause");
    int forbidden=sign<0?1:0,k=forbidden?4:5;
    need(__builtin_popcount(vertices)==k,"physical subset order");
    need(viable(vertices,forbidden),"already satisfied physical subset");
    set<int> wanted;
    for(int v=1;v<=208;v++){
      auto [i,j]=vars[v];if((vertices>>i&1)&&(vertices>>j&1))wanted.insert(sign*v);
    }
    need(wanted==literals,"clause omits or changes physical edge");
    need(seen[forbidden].insert(vertices).second,"duplicate physical subset");
  }
  string trailing;need(!(in>>trailing),"extra CNF payload");
  need(seen==expected,"missing physical constraints");total_clauses+=count;
}
static void witness(const string& hex){
  need(hex.size()==64,"witness length");
  array<array<int,23>,23> edge{};int bit=0;
  for(char c:hex)need((c>='0'&&c<='9')||(c>='a'&&c<='f'),"witness hex");
  auto digit=[](char c){return c<='9'?c-'0':c-'a'+10;};
  need(digit(hex[0])<2,"253-bit padding");
  for(int i=0;i<23;i++)for(int j=i+1;j<23;j++,bit++){
    int value=(digit(hex[63-bit/4])>>(bit%4))&1;edge[i][j]=value;
    need(pinned[i][j]<0||pinned[i][j]==value,"witness pinned edge");
  }
  // Literal tuples, independent from the producer's dictionary/combinations.
  for(int a=0;a<23;a++)for(int b=a+1;b<23;b++)for(int c=b+1;c<23;c++)for(int d=c+1;d<23;d++){
    int four=edge[a][b]+edge[a][c]+edge[a][d]+edge[b][c]+edge[b][d]+edge[c][d];
    need(four!=6,"red K4 witness");
    if(four==0)for(int e=d+1;e<23;e++)need(edge[a][e]+edge[b][e]+edge[c][e]+edge[d][e]!=0,"blue K5 witness");
  }
  total_witnesses++;
}
int main(int argc,char** argv){try{
  need(argc==3||argc==4||argc==5,"usage: check catalogue case-directory [witnesses.tsv | --case index]; or check catalogue --models witnesses.tsv");
  ifstream catalog(argv[1]);need(bool(catalog),"catalogue missing");
  vector<string> rows;string row;while(getline(catalog,row))rows.push_back(row);
  need(rows.size()==362,"catalogue count");
  int first=0,last=362;
  if(string(argv[2])=="--models"){need(argc==4,"models argument");last=0;}
  if(argc==5){need(string(argv[3])=="--case","case option");first=stoi(argv[4]);last=first+1;need(first>=0&&last<=362,"case range");}
  for(int index=first;index<last;index++){
    setup(rows[index]);string number=to_string(index);number=string(6-number.size(),'0')+number;
    audit(string(argv[2])+"/"+number+"/input.cnf");
  }
  if(argc==4){ifstream in(argv[3]);need(bool(in),"witness TSV missing");set<int> seen;string line;
    while(getline(in,line)){istringstream fields(line);int index;string hex,extra;
      need(bool(fields>>index>>hex)&&!(fields>>extra),"witness TSV parse");
      need(index>=0&&index<362&&seen.insert(index).second,"witness index");setup(rows[index]);witness(hex);}
    need(in.eof(),"witness TSV read");need(seen.size()==362,"complete witness registry");
  }
  cout<<"{\"audited_formulas\":"<<last-first<<",\"audited_clauses\":"<<total_clauses<<",\"literal_witnesses\":"<<total_witnesses<<"}\n";
}catch(const exception& e){cerr<<"REJECT: "<<e.what()<<'\n';return 1;}}
