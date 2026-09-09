// Generate every monochromatic five-set from the defining alternating form.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using Bits=array<uint64_t,4>;
static array<array<Bits,256>,2> adj;
static int form(int u,int v){return __builtin_parity(unsigned(((u&15)&(v>>4))^((v&15)&(u>>4))));}
static Bits meet(const Bits&a,const Bits&b){Bits c{};for(int i=0;i<4;i++)c[i]=a[i]&b[i];return c;}
static uint64_t population(const Bits&a){uint64_t n=0;for(auto x:a)n+=__builtin_popcountll(x);return n;}
static int pop(Bits& a){for(int i=0;i<4;i++)if(a[i]){int j=__builtin_ctzll(a[i]);a[i]&=a[i]-1;return 64*i+j;}return -1;}
static void need(bool ok,const string& msg){if(!ok)throw runtime_error(msg);}
static array<uint64_t,2> count5{};
static void enumerate(int color,int depth,array<int,5>& tuple,Bits choices,ostream& out){
  int v;
  while((v=pop(choices))>=0){tuple[depth]=v;
    if(depth==4){for(int x:tuple)out<<-x<<' ';out<<"0\n";count5[color]++;}
    else enumerate(color,depth+1,tuple,meet(choices,adj[color][v]),out);
  }
}
int main(int argc,char**argv){try{
  need(argc==3,"usage: host counter.cnf output.cnf");
  for(int u=1;u<=255;u++)for(int v=1;v<=255;v++)if(u!=v)adj[form(u,v)][u][v/64]|=uint64_t(1)<<(v%64);
  // Independent double-count: each monochromatic five-set has five four-set
  // faces, and each face extends through its full common neighbor set.
  array<uint64_t,2> faces{};
  for(int a=1;a<=255;a++)for(int b=a+1;b<=255;b++)for(int c=b+1;c<=255;c++){
    int col=form(a,b);if(form(a,c)!=col||form(b,c)!=col)continue;
    Bits abc=meet(meet(adj[col][a],adj[col][b]),adj[col][c]);
    for(int d=c+1;d<=255;d++)if(form(a,d)==col&&form(b,d)==col&&form(c,d)==col)
      faces[col]+=population(meet(abc,adj[col][d]));
  }
  need(faces[0]%5==0&&faces[1]%5==0,"face division");
  ifstream counter(argv[1]);need(bool(counter),"counter input");string p,cnf;int nv,nc;counter>>p>>cnf>>nv>>nc;
  need(p=="p"&&cnf=="cnf"&&nv>255&&nc>0,"counter header");string line;getline(counter,line);
  ofstream out(argv[2]);need(bool(out),"output");out<<"p cnf "<<nv<<' '<<(faces[0]+faces[1])/5+nc<<'\n';
  Bits full{};for(int v=1;v<=255;v++)full[v/64]|=uint64_t(1)<<(v%64);
  array<int,5> tuple{};for(int col=0;col<2;col++)enumerate(col,0,tuple,full,out);
  for(int col=0;col<2;col++)need(count5[col]*5==faces[col],"enumeration versus face double-count");
  int copied=0;while(getline(counter,line)){out<<line<<'\n';copied++;}need(copied==nc,"counter lines");out.close();need(bool(out),"output write");
  cout<<"{\"blue_fives\":"<<count5[0]<<",\"red_fives\":"<<count5[1]<<",\"variables\":"<<nv<<",\"counter_clauses\":"<<nc<<",\"face_double_count_verified\":true}\n";
}catch(const exception&e){cerr<<e.what()<<'\n';return 1;}}
