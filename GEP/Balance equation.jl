# Single Node

sum(g[i,jh,jd]) == D[jh,jd] - ens[jh,jd]

# --> i is generator (base,mid,peak,wind,solar)
# --> jh is hours (1:24)
# --> jd is nr of days (1:12)


# Multi Node

sum(g[j,i,jh,jd] i in I) + sum(inp[j,k,jh,jd] for k in K) - sum(exp[j,k,jh,jd] for k in K) == D[j,jh,jd] -ens[j,jh,jd]

# --> j is at which node we are currently
# --> k is also the node, but to which the current node imports from or exports to
# inp[j,k] = 2d matrix with country j as rows and as columns values that it inports from country k 
# exp[j,k] = 2d matrix with country j as rows and as columns values that it exports from country k 

# Extra restrictions:
# inp[j][k] = exp[k][j]
# inp[j][k] = exp[j][k] = 0 for all j=k


# Our multi node

sum(g[j,i,jh,jd] i in I) + sum(inp[j,k,jh,jd] for k in K) - sum(exp[j,k,jh,jd] for k in K) + sum(perc[j,r,z,jh,jd]*cluster[r,z,jh,jd] for z in Z, r in R) == D[j,jh,jd] -ens[j,jh,jd]

# --> i is now generators (base mid and peak)
# inport and export stays the same
# --> r is which renewable technology (wind and solar)
# --> z is every cluster 
# perc[j,r,z] is a 3d matrix with for each country j, for each renewable technolgy r, a percentage per cluster z that belongs to the respective country
# cluster[r,z] is a 2d matrix that holds the generation of cluster z for renewable technology r
