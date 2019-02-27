//input ed output su stdin
//info su stderr
//risultati uguali alla soluzione in python

#include<bits/stdc++.h>
#define pb push_back
#define mp make_pair
#define x first
#define y second
#define all(v) v.begin(), v.end()

using namespace std;

typedef pair<int, int> ii;
typedef vector<int> vi;
typedef vector<vi> vvi;

int R, C, L, H;
bool pizza[1000][1000];
bool used[1000][1000];

vector<ii> genera_rettangoli_validi(int h) {
    vector<ii> res;
    for(int i=1;i<=h;i++) for(int j=1;j<=h;j++) if(i*j <= h && i*j != 1) res.pb(mp(i,j));
    return res;
}

vector<ii> rettangoli;

bool cmp(ii a, ii b) {
    return a.y > b.y; 
    //return a.x > b.x; 
    //return a.x * a.y < b.x * b.y;
}

int main() {

    int area = 0;

    cin>>R>>C>>L>>H;

    //pomodoro true, fungo false
    for(int i=0;i<R;i++) {
        for(int j=0;j<C;j++) {
            char a; cin>>a;
            if(a == 'T') pizza[i][j] = true;
            else pizza[i][j] = false;
        }
    }

    rettangoli = genera_rettangoli_validi(H);
    //magic pseudo random
    mt19937 g(static_cast<uint32_t>(time(0)));
    sort(all(rettangoli), cmp);
    int max_area = 0;
    //se shuffle disattivato settare NITER = 1
    //attiva shuffle per example e small, NITER ~2000
    int NITER = 1;
    vvi slices;
    for(int iter = 1; iter <= NITER; iter++) {
        vvi tmp_slices;
        area = 0;
        for(int i=0;i<R;i++) for(int j=0;j<C;j++) used[i][j] = false;
        for(int i=0;i<R;i++) {
            for(int j=0;j<C;j++) {
                if(!used[i][j]) {
                    //shuffle(rettangoli.begin(), rettangoli.end(), g); //decommentare per shuffle casuale
                    for(auto r : rettangoli) {
                        if(i + r.x - 1 < R && j + r.y - 1 < C) {
                            bool ok = true;
                            int t = 0, f = 0;
                            for(int z=i;z<i+r.x;z++) {
                                for(int k=j;k<j+r.y;k++) {
                                    if(pizza[z][k]) t++;
                                    else f++;
                                    if(used[z][k]) { ok = false; break; }
                                }
                                if(!ok) break;
                            }

                            if(ok && t >= L && f >= L) {
                                vi v;
                                area += (r.x * r.y);
                                v.pb(i);
                                v.pb(i+r.x-1);
                                v.pb(j);
                                v.pb(j+r.y-1);
                                tmp_slices.pb(v);
                                for(int z=i;z<i+r.x;z++) {
                                    for(int k=j;k<j+r.y;k++) {
                                        used[z][k] = true;
                                    }
                                }
                                break;
                            }
                        }

                    }
                }
            }
        }

        if(iter % 10 == 0) {
            cerr<<"ITER: "<<iter<<endl;
            cerr<<max_area<<endl;
        }
        if(area > max_area) {
            max_area = area;
            slices = tmp_slices;
        }
    }
    cerr<<max_area<<endl;
    cout<<slices.size()<<endl;
    for(auto s: slices) {
        cout<<s[0]<<" "<<s[2]<<" "<<s[1]<<" "<<s[3]<<endl;
    }

    return 0;
}