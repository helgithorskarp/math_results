// Independent literal-page and integer-matrix controls for a written draft.
// Author: six-books-2, role researcher. This is not an order22 enumeration.
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>
using Matrix = std::vector<std::vector<int>>;
void require(bool ok,const char* message){if(!ok)throw std::runtime_error(message);}
Matrix square(const Matrix& a){int n=a.size();Matrix b(n,std::vector<int>(n));for(int i=0;i<n;++i)for(int j=0;j<n;++j)for(int k=0;k<n;++k)b[i][j]+=a[i][k]*a[k][j];return b;}
std::array<unsigned,22> red_graph(int q,const Matrix& kind,unsigned inside){
 std::array<unsigned,22> red{};
 auto add=[&](int a,int b){red[a]|=1u<<b;red[b]|=1u<<a;};
 for(int i=0;i<q;++i)if(inside>>i&1)add(2*i,2*i+1);
 for(int i=0;i<q;++i)for(int j=i+1;j<q;++j)for(int a=0;a<2;++a)for(int b=0;b<2;++b){
  int k=kind[i][j];if(k==3||(k==1&&a==b)||(k==2&&a!=b))add(2*i+a,2*j+b);
 }
 return red;
}
int degree(int k){return k==3?2:(k==0?0:1);}
int sign(int k){return k==1?1:(k==2?-1:0);}
std::uint64_t graphs=0,matching_checks=0,blue_checks=0,full_red_checks=0,matrix_checks=0,general_matching_checks=0,uniform_difference_checks=0;
void literal_controls(int q,const Matrix& kind,unsigned inside){
 auto red=red_graph(q,kind,inside);std::array<unsigned,22> blue{};
 unsigned all=(1u<<(2*q))-1;for(int v=0;v<2*q;++v)blue[v]=all^red[v]^(1u<<v);
 for(int i=0;i<q;++i)for(int j=i+1;j<q;++j){
  int type=kind[i][j],ui=0,uj=0,wdot=0,sdot=0;
  for(int k=0;k<q;++k){
   if(k!=i)ui+=degree(kind[i][k])-1;
   if(k!=j)uj+=degree(kind[j][k])-1;
   if(k!=i&&k!=j){wdot+=(degree(kind[i][k])-1)*(degree(kind[j][k])-1);sdot+=sign(kind[i][k])*sign(kind[j][k]);}
  }
  if(type==1||type==2){
   int rednum=q-2+ui+uj+wdot+sign(type)*sdot;
   int bluenum=q-2-ui-uj+wdot-sign(type)*sdot;
   require(rednum%2==0&&bluenum%2==0,"integer general page counts");
   for(int a=0;a<2;++a)for(int b=0;b<2;++b){int u=2*i+a,v=2*j+b;
    if(red[u]>>v&1)require(__builtin_popcount(red[u]&red[v])==rednum/2,"general red matching formula");
    else require(__builtin_popcount(blue[u]&blue[v])==bluenum/2,"general blue matching formula");
    ++general_matching_checks;
   }
   bool eligible=true;int t=0,z=0;
   for(int k=0;k<q;++k)if(k!=i&&k!=j){
    if(kind[i][k]==3||kind[j][k]==3)eligible=false;
    if(kind[i][k]==0&&kind[j][k]==0)++z;
    int prod=sign(type)*sign(kind[i][k])*sign(kind[j][k]);if(prod==1)++t;
   }
   if(eligible)for(int a=0;a<2;++a)for(int b=0;b<2;++b){int u=2*i+a,v=2*j+b;
    if(red[u]>>v&1)require(__builtin_popcount(red[u]&red[v])==t,"red matching page formula");
    else require(__builtin_popcount(blue[u]&blue[v])==q-2-t+z,"blue matching page formula");
    ++matching_checks;
   }
  }
  if(type==0){
   int predicted=2*(2-int(inside>>i&1)-int(inside>>j&1));
   for(int k=0;k<q;++k)if(k!=i&&k!=j)predicted+=(2-degree(kind[i][k]))*(2-degree(kind[j][k]));
   for(int a=0;a<2;++a){int u=2*i+a;
    int observed=__builtin_popcount(blue[u]&blue[2*j])+__builtin_popcount(blue[u]&blue[2*j+1]);
    require(observed==predicted,"sum of two blue spines");++blue_checks;
    int difference=__builtin_popcount(blue[u]&blue[2*j])-__builtin_popcount(blue[u]&blue[2*j+1]);
    require(difference==(a==0?sdot:-sdot),"blue uniform spine difference");++uniform_difference_checks;
   }
  }
  if(type==3){
   int f=0,predicted=2*(int(inside>>i&1)+int(inside>>j&1));
   for(int k=0;k<q;++k)if(k!=i&&k!=j){
    f+=(kind[i][k]==0||kind[j][k]==0);
    predicted+=degree(kind[i][k])*degree(kind[j][k]);
   }
   for(int a=0;a<2;++a){int u=2*i+a;
    int observed=__builtin_popcount(red[u]&red[2*j])+__builtin_popcount(red[u]&red[2*j+1]);
    require(observed==predicted,"sum of two red spines");
    int difference=__builtin_popcount(red[u]&red[2*j])-__builtin_popcount(red[u]&red[2*j+1]);
    require(difference==(a==0?sdot:-sdot),"red uniform spine difference");++uniform_difference_checks;
    require(observed>=q-2-f+2*(int(inside>>i&1)+int(inside>>j&1)),"red full-pair lower bound");++full_red_checks;
   }
  }
 }
 ++graphs;
}
void matrix_controls(int q,const Matrix& kind){
 // No fully red pairs; only when D is a union of cliques.
 std::vector<int> r(q,1);bool cluster=true;
 for(int i=0;i<q;++i)for(int j=0;j<q;++j)if(i!=j&&kind[i][j]==0)++r[i];
 for(int i=0;i<q;++i)for(int j=i+1;j<q;++j)if(kind[i][j]!=0)
  for(int k=0;k<q;++k)if(k!=i&&k!=j&&kind[i][k]==0&&kind[j][k]==0)cluster=false;
 if(!cluster)return;
 Matrix s(q,std::vector<int>(q));for(int i=0;i<q;++i)for(int j=0;j<q;++j)if(i!=j)s[i][j]=sign(kind[i][j]);
 Matrix s2=square(s);
 for(int a=0;a<=q-2;++a){Matrix x=s;for(int i=0;i<q;++i)for(int j=0;j<q;++j)x[i][j]*=2;
  for(int i=0;i<q;++i)x[i][i]=q-2*a-2*r[i];
  Matrix x2=square(x);
  for(int i=0;i<q;++i){require(x2[i][i]==4*(q-r[i])+(q-2*a-2*r[i])*(q-2*a-2*r[i]),"square diagonal");++matrix_checks;
   for(int j=i+1;j<q;++j){
    if(kind[i][j]==0){require(x2[i][j]==4*s2[i][j],"square inside a clique");++matrix_checks;}
    else{int t=0;for(int k=0;k<q;++k)if(k!=i&&k!=j&&s[i][j]*s[i][k]*s[j][k]==1)++t;
     require(s2[i][j]==(2*t-q+r[i]+r[j])*s[i][j],"sign triangle dot product");
     require(x2[i][j]==8*(t-a)*s[i][j],"square across cliques");matrix_checks+=2;
    }
   }
  }
 }
}
void enumerate(int q,int alphabet,bool matrix){
 std::vector<std::array<int,2>> pairs;for(int i=0;i<q;++i)for(int j=i+1;j<q;++j)pairs.push_back({i,j});
 unsigned total=1;for(auto p:pairs){(void)p;total*=alphabet;}
 for(unsigned word=0;word<total;++word){unsigned value=word;Matrix kind(q,std::vector<int>(q));
  for(auto p:pairs){kind[p[0]][p[1]]=kind[p[1]][p[0]]=value%alphabet;value/=alphabet;}
  if(matrix)matrix_controls(q,kind);
  for(unsigned inside=0;inside<(1u<<q);++inside)literal_controls(q,kind,inside);
 }
}
int main()try{
 for(int q=3;q<=5;++q)enumerate(q,3,true);
 for(int q=3;q<=4;++q)enumerate(q,4,false);
 std::uint64_t commutation=0;
 for(int h=-9;h<=9;h+=2)for(int a:{-2,2})for(int b:{-2,2}){
  bool single=(49*a==37*a+4*h*b)&&(49*b==4*h*a+37*b);
  if(single){require(h==3||h==-3,"singleton-pair h");if(h==3)require(a==b,"singleton active direction");}
  bool triple=(33*a==37*a+4*h*b)&&(33*b==4*h*a+37*b);
  if(triple){require(h==1||h==-1,"triple-pair h");if(h==1)require(a==-b,"triple active direction");}commutation+=2;
 }
 for(int h:{1,3})for(int a:{-2,2})for(int b:{-2,2})for(int c:{-2,2})for(int d:{-2,2}){
  bool commute=(b==c&&a==d); // B C=C B for B=[[37,4h],[4h,37]] below.
  bool direct=(37*a+4*h*c==37*a+4*h*b)&&(37*b+4*h*d==4*h*a+37*b)&&
    (4*h*a+37*c==37*c+4*h*d)&&(4*h*b+37*d==4*h*c+37*d);
  require(commute==direct,"pair block commutation");
  if(direct){require((a-b)%4==0&&(a+b)%4==0,"inactive entries divisible by four");}++commutation;
 }
 require((25-1)%16!=0&&(41-1)%16!=0,"inactive squared-norm contradictions");
 std::cout<<"{\"agent\":\"six-books-2\",\"role\":\"researcher\",\"complete\":true,\"formula_control_graphs\":"<<graphs
 <<",\"matching_spine_checks\":"<<matching_checks<<",\"general_matching_checks\":"<<general_matching_checks<<",\"uniform_difference_checks\":"<<uniform_difference_checks<<",\"blue_pair_sum_checks\":"<<blue_checks<<",\"red_pair_sum_and_lower_bound_checks\":"<<full_red_checks
 <<",\"integer_matrix_entry_checks\":"<<matrix_checks<<",\"commutation_controls\":"<<commutation<<",\"order22_exhaustive_enumeration\":false}\n";
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 2;}
