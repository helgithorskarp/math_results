// Literal clause audit with a separate coordinate implementation. Completeness
// is checked against algebraic counts, not another five-clique traversal.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
using namespace std;
static void need(bool ok,const string&s){if(!ok)throw runtime_error(s);}
static int pair_color(int u,int v){int x=0;for(int j=0;j<4;j++)x^=(((u>>j)&1)*((v>>(4+j))&1))^(((v>>j)&1)*((u>>(4+j))&1));return x;}
int main(int argc,char**argv){try{
  need(argc==3,"usage: audit full.cnf counter.cnf");
  array<uint64_t,5> dp{};dp[0]=1;
  for(int k=0;k<5;k++){
    array<uint64_t,5> next{};
    for(int d=0;d<=4;d++)if(dp[d]){
      int inside=(1<<d)-1-k;need(inside>=0,"span state");next[d]+=dp[d]*inside;
      if(d<4)next[d+1]+=dp[d]*((1<<(8-d))-(1<<d));
    }dp=next;
  }
  uint64_t blue=0;for(auto v:dp)blue+=v;need(blue%120==0,"blue division");blue/=120;
  uint64_t red=uint64_t(255)*128*63*32*16/120;
  ifstream in(argv[1]),counter(argv[2]);need(bool(in)&&bool(counter),"input open");
  string p,f;int nv,cv,cc;uint64_t clauses;
  in>>p>>f>>nv>>clauses;need(p=="p"&&f=="cnf","full header");
  counter>>p>>f>>cv>>cc;need(p=="p"&&f=="cnf"&&nv==cv&&clauses==blue+red+cc,"counter/full sizes");
  array<array<int,256>,256> colors{};
  for(int u=1;u<=255;u++)for(int v=1;v<=255;v++)colors[u][v]=pair_color(u,v);
  for(int col=0;col<2;col++){
    array<int,5> previous{};uint64_t count=col?red:blue;
    for(uint64_t t=0;t<count;t++){
      array<int,5> tuple{};int end;
      for(int j=0;j<5;j++){int lit;need(bool(in>>lit)&&lit<=-1&&lit>=-255,"five-set literal");tuple[j]=-lit;if(j)need(tuple[j]>tuple[j-1],"five-set order");}
      need(bool(in>>end)&&end==0,"five-set terminator");need(tuple>previous,"duplicate or unordered five-set");previous=tuple;
      for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)need(colors[tuple[i]][tuple[j]]==col,"non-monochromatic clause");
    }
  }
  int actual,wanted;while(counter>>wanted){need(bool(in>>actual)&&actual==wanted,"counter payload mismatch");}
  need(!(in>>actual),"extra payload");
  cout<<"{\"blue_fives\":"<<blue<<",\"red_fives\":"<<red<<",\"counter_clauses\":"<<cc<<",\"variables\":"<<nv<<",\"algebraic_counts_and_all_literal_clauses_verified\":true}\n";
}catch(const exception&e){cerr<<"REJECT: "<<e.what()<<'\n';return 1;}}
