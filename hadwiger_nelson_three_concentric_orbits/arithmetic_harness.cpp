#define main enumeration_entry_not_called
#include "enumerate.cpp"
#undef main
int main(int argc,char**argv){
 if(argc!=2)return 2;
 ifstream f(argv[1]);int cap;f>>cap>>SCALE;tables.resize(cap+1);
 for(int t=3;t<=cap;t++){tables[t].resize(2*t);for(int j=0;j<2*t;j++){int a,b;I s,c;f>>a>>b>>s.l>>s.h>>c.l>>c.h;if(a!=t||b!=j)return 3;tables[t][j]={c,s};}}
 string op;
 while(cin>>op){
  try{
   I a,b,c;
   if(op=="G"){int factor;cin>>n>>factor>>a.l>>a.h>>b.l>>b.h;auto v=grid({a,b},factor);cout<<v.size();for(int j:v)cout<<' '<<j;cout<<'\n';continue;}
   cin>>a.l>>a.h;
   if(op=="R")c=root(a);
   else{cin>>b.l>>b.h;if(op=="M")c=mul(a,b);else if(op=="D")c=divide(a,b);else if(op=="A")c=add(a,b);else if(op=="S")c=sub(a,b);else throw runtime_error("bad operation");}
   cout<<c.l<<' '<<c.h<<'\n';
  }catch(const exception&){cout<<"REJECT\n";}
 }
 return 0;
}
