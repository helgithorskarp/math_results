#define main phase_search_main
#include "search.cpp"
#undef main
int main(int argc,char** argv){try{need(argc==2,"usage: control INPUT");Model m(read(argv[1]));need(m.nv>=5,"five free variables");std::cout<<"kind\tindex\tscore\tphases\n";
for(int n=0;n<243;++n){auto x=m.initial;int w=n;for(int j=0;j<5;++j){x[j]=w%3;w/=3;}State s(m,x);s.check();std::cout<<"cube\t"<<n<<"\t"<<s.score<<"\t"<<word(x)<<"\n";}
State s(m,m.initial);Random rng{260906};for(int n=0;n<200;++n){int v=rng.pick(m.nv),t=(s.x[v]+1+rng.pick(2))%3;s.move(v,t);s.check();std::cout<<"walk\t"<<n<<"\t"<<s.score<<"\t"<<word(s.x)<<"\n";}
}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}return 0;}
