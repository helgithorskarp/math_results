#include "cadical.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using namespace std; constexpr int N=43,L=21;
int var(int a,int b){if(a>b)swap(a,b);return 1+a*(2*L-a-1)/2+(b-a-1);}
int before(int a,int b){return a<b?var(a,b):-var(b,a);}
struct Outcome{int status=20;long long decisions=0,conflicts=0;array<int,L> order{};};
Outcome local(const array<array<bool,N>,N>&T,const vector<int>&V,bool reverse){CaDiCaL::Solver s;s.set("quiet",1);
 auto add=[&](initializer_list<int> c){for(int x:c)s.add(x);s.add(0);};
 for(int a=0;a<L;a++)for(int b=a+1;b<L;b++)for(int c=b+1;c<L;c++){add({-before(a,b),-before(b,c),before(a,c)});add({before(a,b),before(b,c),-before(a,c)});}
 long clauses4=0,clauses5=0;
 for(int a=0;a<L;a++)for(int b=a+1;b<L;b++)for(int c=b+1;c<L;c++)for(int d=c+1;d<L;d++){
  array<int,4>x{a,b,c,d},deg{};for(int i=0;i<4;i++)for(int j=0;j<4;j++)if(i!=j){bool arc=T[V[x[i]]][V[x[j]]];if(reverse)arc=!arc;deg[i]+=arc;}
  auto sd=deg;sort(sd.begin(),sd.end());if(sd!=array<int,4>{0,1,2,3})continue;array<int,4>q=x;sort(q.begin(),q.end(),[&](int i,int j){int ii=find(x.begin(),x.end(),i)-x.begin(),jj=find(x.begin(),x.end(),j)-x.begin();return deg[ii]>deg[jj];});
  add({-before(q[0],q[1]),-before(q[1],q[2]),-before(q[2],q[3])});clauses4++;
 }
 for(int a=0;a<L;a++)for(int b=a+1;b<L;b++)for(int c=b+1;c<L;c++)for(int d=c+1;d<L;d++)for(int e=d+1;e<L;e++){
  array<int,5>x{a,b,c,d,e},deg{};for(int i=0;i<5;i++)for(int j=0;j<5;j++)if(i!=j){bool arc=T[V[x[i]]][V[x[j]]];if(reverse)arc=!arc;deg[i]+=arc;}
  auto sd=deg;sort(sd.begin(),sd.end());if(sd!=array<int,5>{0,1,2,3,4})continue;array<int,5>q=x;sort(q.begin(),q.end(),[&](int i,int j){int ii=find(x.begin(),x.end(),i)-x.begin(),jj=find(x.begin(),x.end(),j)-x.begin();return deg[ii]>deg[jj];});
  add({-before(q[4],q[3]),-before(q[3],q[2]),-before(q[2],q[1]),-before(q[1],q[0])});clauses5++;
 }
 Outcome o;for(int first=0;first<L;first++){for(int j=0;j<L;j++)if(j!=first)s.assume(before(first,j));if(!s.limit("conflicts",100000)){o.status=0;return o;}int res=s.solve();if(res==10){o.status=10;vector<int>q(L);iota(q.begin(),q.end(),0);sort(q.begin(),q.end(),[&](int i,int j){return s.val(before(i,j))>0;});copy(q.begin(),q.end(),o.order.begin());return o;}if(res!=20){o.status=0;return o;}}
 return o;
}
int main(int argc,char**argv){if(argc!=5){cerr<<"usage data first count max_roots\n";return 2;}ifstream f(argv[1]);vector<string>lines;string z;while(f>>z)lines.push_back(z);int first=stoi(argv[2]),count=stoi(argv[3]),maxroots=stoi(argv[4]);long tested=0,sat=0,unsat=0,unknown=0;
 for(int rec=first;rec<first+count;rec++){array<array<bool,N>,N>T{};int k=0;for(int i=0;i<N;i++)for(int j=i+1;j<N;j++){if(lines[rec][k++]=='1')T[i][j]=1;else T[j][i]=1;}bool record_survives=false;
  for(int root=0;root<min(N,maxroots);root++){vector<int>Q;for(int x=0;x<N;x++)if(T[root][x])Q.push_back(x);if(Q.size()!=L)return 3;auto o=local(T,Q,false);tested++;if(o.status==10){sat++;record_survives=true;cout<<"SAT "<<rec<<' '<<root<<" Q";for(int x:o.order)cout<<' '<<Q[x];cout<<"\n";}else if(o.status==20)unsat++;else unknown++;
  }
  cerr<<"record "<<rec<<" roots "<<min(N,maxroots)<<" survives "<<record_survives<<" cumulative "<<tested<<' '<<sat<<' '<<unsat<<' '<<unknown<<"\n";
 }
cerr<<"FINAL tested "<<tested<<" sat "<<sat<<" unsat "<<unsat<<" unknown "<<unknown<<"\n";
}
