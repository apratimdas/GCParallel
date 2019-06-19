// GCParallel.cpp : Defines the entry point for the application.
//

#define DIRECTED false
#define SIGNED true

#include<fstream>
#include<iostream>
#include<algorithm>
#include<iterator>
#include<vector>
#include<unordered_map>
#include<utility>
#include<chrono>
#include<omp.h>
#include "GCParallel.h"
#include<thread>
#include<cassert>

using namespace std;
using namespace std::chrono;

// Helper types
using uint = unsigned int;
using int64 = long long;
using intpair = pair<int, int>;

// For directed orbit values
struct uvworbit
{
	int vorbit, uorbit, worbit;
};

// Custom pair a<b
struct mpair
{
	int a, b;

	mpair() : a(0), b(0) {}
	mpair(int a0, int b0) : a(std::min(a0, b0)), b(std::max(a0, b0)) {}
};

fstream fin;
uint n;	// Number of Nodes
uint m;	// Number of Edges
uint dmax; // Maximum degree in Graph

// A hash function used to hash a pair of any kind 
struct hash_pair {
	template <class T1, class T2>
	size_t operator()(const pair<T1, T2>& p) const
	{
		auto hash1 = hash<T1>{}(p.first);
		auto hash2 = hash<T2>{}(p.second);
		return hash1 ^ hash2;
	}
};

vector<mpair> edges;
vector<pair<uint, uint>> diredges;
unordered_map<pair<uint, uint>, int, hash_pair> signedmap;
//vector<pair<uint, uint>> signededges;
vector<uint> deg;
vector<uint> posdeg;
vector<uint> negdeg;
vector<pair<uint,uint>> inoutdeg;

int **adj; // adj[x] - adjacency list of node x
int **adjd; // adjd[x] - adjacency list directed of node x
int **adjs; // adjs[x] - adjacency list signed of node x
intpair **inc; // inc[x] - incidence list of node x: (y, edge id)
intpair **incd; // inc[x] - incidence list directed of node x: (y, edge id)
bool adjacent_list(int x, int y) { return binary_search(adj[x], adj[x] + deg[x], y); }
bool directed_adjacent_list(int x, int y) { return binary_search(adjd[x], adjd[x] + inoutdeg[x].first, y); }
//bool signed_adjacent_list(int x, int y) { return binary_search(adjd[x], adjd[x] + inoutdeg[x].first, y); }
int edgesign(int a, int b) { return signedmap.find(make_pair(min(a, b), max(a, b))) != signedmap.end() ? signedmap[make_pair(min(a, b), max(a, b))] : 0; }
int *adj_matrix; // compressed adjacency matrix
const int adj_chunk = 8 * sizeof(int);
bool adjacent_matrix(int x, int y) { return adj_matrix[(x*n + y) / adj_chunk] & (1 << ((x*n + y) % adj_chunk)); }
bool(*adjacent)(int, int);
bool(*diradjacent)(int, int);
bool(*sinadjacent)(int, int);

int64 **orbit; // orbit[x][o] - how many times does node x participate in orbit o
vector<int> wflag;

int threads;

bool operator<(const mpair &x, const mpair &y)
{
	if (x.a == y.a) return x.b < y.b;
	else return x.a < y.a;
}
bool operator==(const mpair &x, const mpair &y)
{
	return x.a == y.a && x.b == y.b;
}

void printorbit3();
void rageTriangleCount();
void triGraphletCount();
void twoStarCount();
void triadcensus();
void hybridgraphlet();
void brutegraphlet();


int main(int argc, char** argv)
{
	//if (argc < 2) 
	//{
	//	std::cerr << "Incorrect number of arguments.\n";
	//	std::cerr << "Usage: GCParallel [graph - input file] [(opt)threads - number of threads to use]\n";
	//	return 0;
	//}
	//bool issigned = false;
	//signed
	//fin.open("signededgelisttest.txt", fstream::in); //
	//fin.open("signededgelist.txt", fstream::in); //
	//fin.open("signedgenerated10_1.txt", fstream::in); //
	//fin.open("signedgenerated10_2.txt", fstream::in); //
	//fin.open("signedgenerated50.txt", fstream::in); //
	//fin.open("testdirected.txt", fstream::in); //
	//fin.open("watershed-s-directedgraph.txt", fstream::in); //
	//fin.open("watershed-k-directedgraph.txt", fstream::in); //
	fin.open("tumor-cardia-signed-00111.txt", fstream::in); //

	// dense
	//fin.open("soc-pokec-relationships.txt", fstream::in); //1.6m v, 30.6m e
	//fin.open("C2000-9.mtx", fstream::in); //
	//fin.open("C4000-5.mtx", fstream::in); //
	//fin.open("scc_reality.mtx", fstream::in); //
	//fin.open("frb100-40.mtx", fstream::in); //4k v, 7m e
	//fin.open("MANN-a81.mtx", fstream::in); //4k v, 7m e
	//fin.open("frb59-26-5.mtx", fstream::in); //1.5k v, 1m e
	//fin.open("co-papers-citeseer.mtx", fstream::in); //434kk v, 16m e


	// sparse
	//fin.open("dbpedia-country.edges", fstream::in); // 500k v,e
	//fin.open("ca-IMDB.edges", fstream::in); //896k v, 3.7m e
	//fin.open("netherlands_osm.mtx", fstream::in); // 2.5m v,e
	// test
	//fin.open("5test.mtx", fstream::in);


	if (fin.fail())
	{
		cerr << "Failed to open file " << argv[2] << endl;
		return 0;
	}
	fin >> n >> m;
	edges.resize(m);
	diredges.resize(m);
	deg.resize(n);
	posdeg.resize(n);
	negdeg.resize(n);
	inoutdeg.resize(n);
	wflag.resize(n);

	threads = 8;// atoi(argv[2]); // Thread count change here (testing)

	if (m < 100)
		threads = 1;	// force single thread for small graphs

	bool flag = true;
	for (uint i = 0; i < m; i++)
	{
		int a, b, c;
		if (SIGNED)
			fin >> a >> b >> c;
		else
			fin >> a >> b;
		if (!(0 <= a && a < n) || !(0 <= b && b < n)) {
			cerr << "Node ids should be between 0 and n-1." << endl;
			cerr << a <<" "<< b<< endl;
			return 0;
		}
		if (a == b) {
			if (flag)
			{
				cerr << "Data contains Self loops which are not allowed. Omitting self loops." << endl;
				flag = false;
			}
			continue;
		}
		deg[a]++; deg[b]++;
		if (SIGNED)
		{
			if (c == 1)
			{
				posdeg[a]++;
				posdeg[b]++;
			}
			if (c == -1)
			{
				negdeg[a]++;
				negdeg[b]++;
			}
		}
		inoutdeg[a].first++; inoutdeg[b].second++;
		edges[i] = mpair(a, b);
		int vsmall = min(a, b);
		int vbig = max(a, b);

		if(SIGNED)
			signedmap[{vsmall, vbig}] = c;
		if(DIRECTED)
			diredges[i] = make_pair(a, b);

	}
	//cout <<"1505,1503: " << edgesign(1505,1503) << endl;
	for (int i = 0; i < n; i++)
		dmax = max(dmax, deg[i]);

	printf("nodes: %d\n", n);
	printf("edges: %d\n", m);
	printf("max degree: %d\n", dmax);
	fin.close();

	// set up adjacency matrix if it's smaller than 100MB
	if (false)//(int64)n*n < 100LL * 1024 * 1024 * 8)
	{
		adjacent = adjacent_matrix;
		adj_matrix = (int*)calloc((n*n) / adj_chunk + 1, sizeof(int));
		for (int i = 0; i < m; i++)
		{
			int a = edges[i].a, b = edges[i].b;
			adj_matrix[(a*n + b) / adj_chunk] |= (1 << ((a*n + b) % adj_chunk));
			adj_matrix[(b*n + a) / adj_chunk] |= (1 << ((b*n + a) % adj_chunk));
		}
	}
	else
		adjacent = adjacent_list;

	// set up adjacency, incidence lists
	adj = (int**)malloc(n * sizeof(int*));
	for (int i = 0; i < n; i++)
		adj[i] = (int*)malloc(deg[i] * sizeof(int));

	inc = (intpair **)malloc(n * sizeof(intpair*));
	for (int i = 0; i < n; i++)
		inc[i] = (intpair*)malloc(deg[i] * sizeof(intpair));

	int *d = (int*)calloc(n, sizeof(int));
	for (int i = 0; i < m; i++)
	{
		int a = edges[i].a, b = edges[i].b;
		adj[a][d[a]] = b; adj[b][d[b]] = a;
		inc[a][d[a]] = intpair(b, i); inc[b][d[b]] = intpair(a, i);
		d[a]++; d[b]++;
	}

	for (int i = 0; i < n; i++)
	{
		sort(adj[i], adj[i] + deg[i]);
		sort(inc[i], inc[i] + deg[i]);
	}
	delete d;
	if (DIRECTED)
	{
		// set up adjacency, incidence lists for directed
		int* dir = (int*)calloc(n, sizeof(int));
		adjd = (int**)malloc(n * sizeof(int*));
		for (int i = 0; i < n; i++)
			adjd[i] = (int*)malloc(inoutdeg[i].first * sizeof(int));
		incd = (intpair **)malloc(n * sizeof(intpair*));
		for (int i = 0; i < n; i++)
			incd[i] = (intpair*)malloc(deg[i] * sizeof(intpair));

		for (int i = 0; i < m; i++)
		{
			int a = diredges[i].first, b = diredges[i].second;
			adjd[a][dir[a]] = b;
			incd[a][dir[a]] = intpair(b, i);
			dir[a]++;
		}

		for (int i = 0; i < n; i++)
		{
			sort(adjd[i], adjd[i] + inoutdeg[i].first);
			sort(incd[i], incd[i] + inoutdeg[i].first);
		}
		delete dir;
		diradjacent = directed_adjacent_list;
	}

	// initialize orbit counts
	orbit = (int64**)malloc(n * sizeof(int64*));
	for (int i = 0; i < n; i++)
		orbit[i] = (int64*)calloc(73, sizeof(int64));

	cout << "Using " << threads << " threads\n";

	// Begin Algorithm

	//cout << "\nRage\n";
	//rageTriangleCount();
	//cout << "\ntwo stars only\n";
	//twoStarCount();
	//cout << "\nthree cycles only\n";
	//triGraphletCount();	
	//cout << "\nhybrid\n";
	//hybridgraphlet();	
	cout << "\nnaiive\n";
	brutegraphlet();
	//cout << "\ntwo star + three cycle\n";
	//twoStarCount();
	//triGraphletCount();

	//cout << "\nTriad census\n";
	//triadcensus();

	printorbit3();

	system("pause");
	return 0;
}

void rageParallelBreak(int tnum)
{
	int u, w;
	for (int v = 0; v < n; v += threads + tnum)
	{
		for (int i = 0; i < deg[v]; i++)
		{
			u = adj[v][i];
			if (v < u)
			{
				for (int u_i = 0; u_i < deg[u]; u_i++)
				{
					w = adj[u][u_i];

					if (w <= v)
						continue;

					if (adjacent(v, w))		// constant time or log(n) depending on matrix or list
					{
						if (w <= u)
						{
							orbit[v][3]++;
							orbit[u][3]++;
							orbit[w][3]++;
						}
					}
					else
					{
						orbit[v][1]++;
						orbit[u][2]++;
						orbit[w][1]++;
					}
				}
			}
		}
	}
}

void rageTriangleCount()
{
	auto start = high_resolution_clock::now();


	//#pragma omp parallel for

	vector<thread> tvec;
	tvec.reserve(threads);

	for (int i = 0; i < threads; i++)
		tvec.push_back(thread(rageParallelBreak, i));
	for (int i = 0; i < threads; i++)
		tvec[i].join();

	auto stop = high_resolution_clock::now();

	duration<float> secs = stop - start;

	cout << "Time taken: " << secs.count() << "\n";
}

void calcorbit(int v, int u, int w, uvworbit& uvw, bool triangle)
{
	if (triangle)
	{
		if (diradjacent(v, u) && diradjacent(u, w) && diradjacent(w, v))
		{
			orbit[u][9]++;
			orbit[v][9]++;
			orbit[w][9]++;
		}
		else
		{
			if (diradjacent(v, u) && diradjacent(v, w))
			{
				// v 11
				orbit[v][11]++;
				if (diradjacent(u, w))
				{
					orbit[u][12]++;
					orbit[w][10]++;
				}
				else
				{
					orbit[u][10]++;
					orbit[w][12]++;
				}
			}
			else if (diradjacent(u, v) && diradjacent(u, w))
			{
				// u 11
				orbit[u][11]++;
				if (diradjacent(v, w))
				{
					orbit[v][12]++;
					orbit[w][10]++;
				}
				else
				{
					orbit[v][10]++;
					orbit[w][12]++;
				}
			}
			else if (diradjacent(w, v) && diradjacent(w, u))
			{
				// w 11
				orbit[w][11]++;
				if (diradjacent(v, u))
				{
					orbit[v][12]++;
					orbit[u][10]++;
				}
				else
				{
					orbit[v][10]++;
					orbit[u][12]++;
				}
			}
		}
	}
	else
	{
		// u is always center
		if (diradjacent(v, u) && diradjacent(u, w))
		{
			orbit[v][2]++;
			orbit[u][3]++;
			orbit[w][4]++;
		}
		else if (diradjacent(w, u) && diradjacent(u, v))
		{
			orbit[v][4]++;
			orbit[u][3]++;
			orbit[w][2]++;
		}
		else if (diradjacent(u, v) && diradjacent(u, w))
		{
			orbit[v][5]++;
			orbit[u][6]++;
			orbit[w][5]++;
		}
		else if (diradjacent(v, u) && diradjacent(w, u))
		{
			orbit[v][7]++;
			orbit[u][8]++;
			orbit[w][7]++;
		}
	}
}


void calcorbitsigned(int v, int u, int w, uvworbit& uvw, bool triangle)
{
	if (triangle)
	{
		if (edgesign(v, u) == 1 && edgesign(u, w) == 1 && edgesign(w, v) == 1)
		{
			orbit[u][9]++;
			orbit[v][9]++;
			orbit[w][9]++;
		}
		else if (edgesign(v, u) == -1 && edgesign(u, w) == -1 && edgesign(w, v) == -1)
		{
			orbit[u][14]++;
			orbit[v][14]++;
			orbit[w][14]++;
		}
		else if (edgesign(v, u) + edgesign(u, w) + edgesign(w, v) == 1)
		{
			int n1, n2, p;

			if (edgesign(v, u) == -1)
			{
				p = w;
				n1 = u;
				n2 = v;
			}
			else if(edgesign(u, w) == -1)
			{
				n1 = w;
				n2 = u;
				p = v;
			}
			else if(edgesign(v, w) == -1)
			{
				n1 = w;
				p = u;
				n2 = v;
			}
			orbit[p][10]++;
			orbit[n1][11]++;
			orbit[n2][11]++;
		}
		else if (edgesign(v, u) + edgesign(u, w) + edgesign(w, v) == -1)
		{
			int p1, p2, n;

			if (edgesign(v, u) == 1)
			{
				n = w;
				p1 = u;
				p2 = v;
			}
			else if (edgesign(u, w) == 1)
			{
				p1 = w;
				p2 = u;
				n = v;
			}
			else if (edgesign(v, w) == 1)
			{
				p1 = w;
				n = u;
				p2 = v;
			}
			orbit[n][13]++;
			orbit[p1][12]++;
			orbit[p2][12]++;
		}
		else
		{
			assert(true && "SG Triangle should only have 4 structures");
		}
	}
	else
	{
		// u is always center
		if (edgesign(v, u) + edgesign(u, w) == 2)
		{
			orbit[u][3]++;
			orbit[v][2]++;
			orbit[w][2]++;
		}
		else if (edgesign(v, u) + edgesign(u, w) == -2)
		{
			orbit[u][8]++;
			orbit[v][7]++;
			orbit[w][7]++;
		}
		else if (edgesign(v, u) + edgesign(u, w) == 0)
		{
			int neg, pos;
			if (edgesign(v, u) == 1)
			{
				pos = v;
				neg = w;
			}
			else
			{
				pos = w;
				neg = v;
			}

			orbit[u][6]++;
			orbit[neg][5]++;
			orbit[pos][4]++;
		}
		else
		{
			assert(true && "SG 2-star has only 3 possible structures");
		}
	}
}


void hybridParallel(int tnum)
{
	for (int v = 0; v < n; v += threads + tnum)
	{
		for (int i = 0; i < (int(deg[v]) - 1); i++)
		{
			int u = adj[v][i];
			for (int j = i + 1; j < deg[v]; j++)
			{
				int w = adj[v][j];
				if (adjacent(u,w)) //deg[u] >= deg[v] && deg[w] >= deg[v] && adjacent(u, w))
				{
					if (DIRECTED)
					{
						uvworbit uvw;
						calcorbit(v, u, w, uvw, true);
					}
					else if (SIGNED)
					{
						uvworbit uvw;
						calcorbitsigned(v, u, w, uvw, true);
					}
					else
					{
						orbit[v][3]++;
						orbit[u][3]++;
						orbit[w][3]++;
					}
				}
			}

			if (v < u)
			{
				vector<int> uList(adj[u], adj[u] + deg[u]);
				vector<int> vList(adj[v], adj[v] + deg[v]);
				vector<int> difflist;
				std::set_difference(uList.begin(), uList.end(), vList.begin(), vList.end(),
					std::inserter(difflist, difflist.begin()));
				difflist.erase(std::remove_if(difflist.begin(), difflist.end(), [v](int x) {return x <= v; }), difflist.end());

				for (auto w : difflist)
				{
					if (w > v)
					{
						if (DIRECTED)
						{
							uvworbit uvw;
							calcorbit(v, u, w, uvw, false);
						}
						else if (SIGNED)
						{
							uvworbit uvw;
							calcorbitsigned(v, u, w, uvw, false);
						}
						else 
						{
							orbit[v][1]++;
							orbit[u][2]++;
							orbit[w][1]++;
						}
					}
				}
			}
		}
		int u = adj[v][int(deg[v]) - 1];
		if (v < u)
		{
			vector<int> uList(adj[u], adj[u] + deg[u]);
			vector<int> vList(adj[v], adj[v] + deg[v]);
			vector<int> difflist;
			std::set_difference(uList.begin(), uList.end(), vList.begin(), vList.end(),
				std::inserter(difflist, difflist.begin()));
			difflist.erase(std::remove_if(difflist.begin(), difflist.end(), [v](int x) {return x <= v; }), difflist.end());

			for (auto w : difflist)
			{
				if (w > v)
				{
					if (DIRECTED)
					{
						uvworbit uvw;
						calcorbit(v, u, w, uvw, false);
					}
					else if (SIGNED)
					{
						uvworbit uvw;
						calcorbitsigned(v, u, w, uvw, false);
					}
					else
					{
						orbit[v][1]++;
						orbit[u][2]++;
						orbit[w][1]++;
					}
				}
			}
		}
	}
}

void hybridgraphlet()
{
	auto start = high_resolution_clock::now();

	vector<thread> tvec;
	tvec.reserve(threads);

	for (int i = 0; i < threads; i++)
		tvec.push_back(thread(hybridParallel, i));
	for (int i = 0; i < threads; i++)
		tvec[i].join();


	auto stop = high_resolution_clock::now();
	duration<float> secs = stop - start;
	cout << "Time taken: " << secs.count() << "\n";
}


void bruteParallel(int tnum)
{
	for (int v = 0; v < n; v += threads + tnum)
	{
		for (int i = 0; i < deg[v]; i++)
		{
			int u = adj[v][i];

			for (int j = 0; j < deg[u]; j++)
			{
				int w = adj[u][j];
				if (u == w || v == w)
					continue;

				//TODO: Fix repeated counts
				if (adjacent(v,w))
				{
					if (DIRECTED)
					{
						uvworbit uvw;
						calcorbit(v, u, w, uvw, true);
					}
					else if (SIGNED)
					{
						uvworbit uvw;
						calcorbitsigned(v, u, w, uvw, true);
					}
					else
					{
						orbit[v][3]++;
						orbit[u][3]++;
						orbit[w][3]++;
					}
				}
				else
				{
					if (DIRECTED)
					{
						uvworbit uvw;
						calcorbit(v, u, w, uvw, false);
					}
					else if (SIGNED)
					{
						uvworbit uvw;
						calcorbitsigned(v, u, w, uvw, false);
					}
					else
					{
						orbit[v][1]++;
						orbit[u][2]++;
						orbit[w][1]++;
					}
				}

			}
		}
	}
}

void brutegraphlet()
{
	auto start = high_resolution_clock::now();

	vector<thread> tvec;
	tvec.reserve(threads);

	for (int i = 0; i < threads; i++)
		tvec.push_back(thread(bruteParallel, i));
	for (int i = 0; i < threads; i++)
		tvec[i].join();


	auto stop = high_resolution_clock::now();
	duration<float> secs = stop - start;
	cout << "Time taken: " << secs.count() << "\n";
}


void triGraphletParallel(int tnum)
{
	for (int v = 0; v < n; v += threads + tnum)
	{
		for (int i = 0; i < (int(deg[v]) - 1); i++)
		{
			for (int j = i + 1; j < deg[v]; j++)
			{
				int u = adj[v][i];
				int w = adj[v][j];
				if (deg[u] > deg[v] && deg[w] > deg[v] && adjacent(u, w))
				{
					orbit[v][3]++;
					orbit[u][3]++;
					orbit[w][3]++;
				}
			}
		}


	}
}

void triGraphletCount()
{
	auto start = high_resolution_clock::now();

	vector<thread> tvec;
	tvec.reserve(threads);

	for (int i = 0; i < threads; i++)
		tvec.push_back(thread(triGraphletParallel, i));
	for (int i = 0; i < threads; i++)
		tvec[i].join();


	auto stop = high_resolution_clock::now();
	duration<float> secs = stop - start;
	cout << "Time taken: " << secs.count() << "\n";
}

void twoStarParallel(int tnum)
{
	for (int v = 0; v < n; v += threads + tnum)
	{
		for (int i = 0; i < deg[v]; i++)
		{
			int u = adj[v][i];

			if (v < u)
			{
				vector<int> uList(adj[u], adj[u] + deg[u]);
				vector<int> vList(adj[v], adj[v] + deg[v]);
				vector<int> difflist;
				//vector<int> intersectionlist(min(uList.size(), vList.size()));
				std::set_difference(uList.begin(), uList.end(), vList.begin(), vList.end(),
					std::inserter(difflist, difflist.begin()));
				difflist.erase(std::remove_if(difflist.begin(), difflist.end(), [v](int x) {return x <= v; }), difflist.end());

				//auto it = std::set_intersection(uList.begin(), uList.end(), vList.begin(), vList.end(), intersectionlist.begin());
				//intersectionlist.resize(it - intersectionlist.begin());

				for (auto w : difflist)
				{
					if (w > v)
					{
						orbit[v][1]++;
						orbit[u][2]++;
						orbit[w][1]++;
					}
				}
				//for (auto w : intersectionlist)
				//{
				//	if (w <= v || w <= u)
				//		continue;
				//	orbit[v][3]++;
				//	orbit[u][3]++;
				//	orbit[w][3]++;
				//}
			}
		}
	}
}

void twoStarCount()
{
	auto start = high_resolution_clock::now();

	vector<thread> tvec;
	tvec.reserve(threads);

	for (int i = 0; i < threads; i++)
		tvec.push_back(thread(twoStarParallel, i));
	for (int i = 0; i < threads; i++)
		tvec[i].join();


	auto stop = high_resolution_clock::now();
	duration<float> secs = stop - start;
	cout << "Time taken: " << secs.count() << "\n";
}


void triadparallel(int tnum)
{
	for (int i = 0; i < edges.size(); i += threads + tnum)
	{
		mpair e = edges[i];
		int u = e.a;
		int v = e.b;

		for (int u_i = 0; u_i < deg[u]; u_i++)
		{
			int w = adj[u][u_i];
			if (w == v)
				continue;
			wflag[w] = 1;
		}

		for (int v_i = 0; v_i < deg[v]; v_i++)
		{
			int w = adj[v][v_i];
			if (w == u)
				continue;
			if (wflag[w] == 1)
			{
				// value /3
				// u,v,w triangle
				orbit[u][3]++;
				orbit[v][3]++;
				orbit[w][3]++;
			}
			else
			{
				//TODO: Fix, incorrect values
				// u,v,w two star
				orbit[u][1]++;
				orbit[v][2]++;
				orbit[w][1]++;
			}
			wflag[w] = 0;
		}
	}
}

void triadcensus()
{
	auto start = high_resolution_clock::now();

	vector<thread> tvec;
	tvec.reserve(threads);

	for (int i = 0; i < threads; i++)
		tvec.push_back(thread(triadparallel, i));
	for (int i = 0; i < threads; i++)
		tvec[i].join();


	auto stop = high_resolution_clock::now();
	duration<float> secs = stop - start;
	cout << "Time taken: " << secs.count() << "\n";

}


void printorbit3()
{
	if (SIGNED) // brute print
	{
		for (int i = 0; i < n; i++)
			cout << posdeg[i] << " " << negdeg[i]<< " " << orbit[i][2] / 2 << " " << orbit[i][3]/2 << " " << orbit[i][4]/2 << " " << orbit[i][5]/2 << " "
			<< orbit[i][6]/2 << " " << orbit[i][7]/2 << " " << orbit[i][8]/2 << " " << orbit[i][9]/6 << " "
			<< orbit[i][10]/6 << " " << orbit[i][11]/6 << " " << orbit[i][12]/6 << " " << orbit[i][13]/6 << " " << orbit[i][14]/6 << "\n";
		return;
	}

	if(!DIRECTED)
		for (int i = 0; i < n; i++)
			cout << orbit[i][1] << " " << orbit[i][2] << " " << orbit[i][3] << "\n";

	else // brute print
	{
		for (int i = 0; i < n; i++)
			cout << inoutdeg[i].first << " " << inoutdeg[i].second << " " << orbit[i][2]/2 << " " << orbit[i][3]/2 << " " << orbit[i][4]/2 << " " << orbit[i][5]/2 << " "
			<< orbit[i][6]/2 << " " << orbit[i][7]/2 << " " << orbit[i][8]/2 << " " << orbit[i][9]/3 << " " 
			<< orbit[i][10]/6 << " " << orbit[i][11]/6 << " " << orbit[i][12]/6 << "\n";
	}
}
