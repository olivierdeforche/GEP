## Backbone to structure your code
# author: Olivier Deforche, Louis Maes
# last update: April 17, 2023
# reference: This model is build upon the backbone code from Kenneth Bruninx for the course: Optimization problems in Engergy systems 
# description: TBD

using Pkg
## Step 0: Activate environment - ensure consistency accross computers
Pkg.activate(@__DIR__) # @__DIR__ = directory this script is in
Pkg.instantiate() # If a Manifest.toml file exist in the current project, download all the packages declared in that manifest. Else, resolve a set of feasible packages from the Project.toml files and install them.

using CSV
using DataFrames
using YAML
using XLSX

##  Step 1: Choose the correct data and load every input data
method = "kmeans"
no_clusters = "10"
data_used = "af"

data = YAML.load_file(joinpath(@__DIR__, "data_gep_update.yaml"))
imp = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"), "Import"))
exp = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"), "Export"))
demand = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"), "Demand"))
countries = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"),"Countries"))

Clusters_to_countries_wind = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Asigned_To_Countries/",method,"_",no_clusters,"_",data_used,"_df_wind.xlsx")),"Sheet1"))
Clusters_to_countries_wind_offshore = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Asigned_To_Countries/",method,"_",no_clusters,"_",data_used,"_df_wind_offshore.xlsx")),"Sheet1"))
Clusters_to_countries_solar = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Asigned_To_Countries/",method,"_",no_clusters,"_",data_used,"_df_solar.xlsx")),"Sheet1"))
Clusters_to_countries_solar_offshore = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Asigned_To_Countries/",method,"_",no_clusters,"_",data_used,"_df_solar_offshore.xlsx")),"Sheet1"))

Time_series_wind = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Timeseries/",method,"_",no_clusters,"_",data_used,"_clustered_on_wind.xlsx")),"Sheet1"))
Time_series_wind_offshore = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Timeseries/",method,"_",no_clusters,"_",data_used,"_clustered_on_wind_offshore.xlsx")),"Sheet1"))
Time_series_solar = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Timeseries/",method,"_",no_clusters,"_",data_used,"_clustered_on_solar.xlsx")),"Sheet1"))
Time_series_solar_offshore = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Timeseries/",method,"_",no_clusters,"_",data_used,"_clustered_on_solar_offshore.xlsx")),"Sheet1"))

## Step 2: create model & pass data to model
using JuMP
using Gurobi
m = Model(optimizer_with_attributes(Gurobi.Optimizer))


# Step 2a: create sets
function define_sets!(m::Model, data::Dict, Clusters_to_countries_wind::DataFrame, Clusters_to_countries_wind_offshore::DataFrame, Clusters_to_countries_solar::DataFrame, Clusters_to_countries_solar_offshore::DataFrame)
    
    # create dictionary to store sets
    m.ext[:sets] = Dict()

    # define the sets
    m.ext[:sets][:JH] = 1:data["nTimesteps"] # Timesteps (24)
    m.ext[:sets][:JD] = 1:data["nDays"] # Number of days days (365)
    m.ext[:sets][:ID] = [id for id in keys(data["dispatchableGenerators"])] # dispatchable generators
    m.ext[:sets][:IV] = [iv for iv in keys(data["variableGenerators"])] # variable generators
    m.ext[:sets][:I] = union(m.ext[:sets][:ID], m.ext[:sets][:IV]) # all generators
    m.ext[:sets][:C] = [c for c in countries[!,"Countries"]] 
    m.ext[:sets][:K] = 1:nrow(imp)
    m.ext[:sets][:CWon] = 1:nrow(Clusters_to_countries_wind)
    m.ext[:sets][:CWof] = 1:nrow(Clusters_to_countries_wind_offshore)
    m.ext[:sets][:CSon] = 1:nrow(Clusters_to_countries_solar)
    m.ext[:sets][:CSof] = 1:nrow(Clusters_to_countries_solar_offshore)
    
    # return model
    return m
end

define_sets!(m, data, Clusters_to_countries_wind, Clusters_to_countries_wind_offshore, Clusters_to_countries_solar, Clusters_to_countries_solar_offshore)

# Step 2b: add time series
function process_time_series_data!(m::Model, data::Dict, demand::DataFrame, Time_series_wind::DataFrame, Time_series_wind_offshore::DataFrame, Time_series_solar::DataFrame, Time_series_solar_offshore::DataFrame)
    # extract the relevant sets
    IV = m.ext[:sets][:IV] # Variable generators
    JH = m.ext[:sets][:JH] # Time steps
    JD = m.ext[:sets][:JD] # Days

    # create dictionary to store time series
    m.ext[:timeseries] = Dict()
    m.ext[:timeseries][:D] = Dict()
    m.ext[:timeseries][:AF] = Dict()
    
    m.ext[:timeseries][:AF][IV[1]] = Dict()
    m.ext[:timeseries][:AF][IV[2]] = Dict()
    m.ext[:timeseries][:AF][IV[3]] = Dict()
    m.ext[:timeseries][:AF][IV[4]] = Dict()

    # example: add time series to dictionary
    l = 1
    for country in m.ext[:sets][:C]
        m.ext[:timeseries][:D][l] = [demand[!,country][jh+data["nTimesteps"]*(jd-1)] for jh in JH, jd in JD]  # This will need to be fixed in terms of days and hours I think? Might not actually!
        l += 1
    end

    for cluster in m.ext[:sets][:CWon]
        m.ext[:timeseries][:AF][IV[2]][cluster] = [Time_series_wind[!,cluster][jh+data["nTimesteps"]*(jd-1)] for jh in JH, jd in JD]
    end

    for cluster in m.ext[:sets][:CWof]
        m.ext[:timeseries][:AF][IV[1]][cluster] = [Time_series_wind_offshore[!,cluster][jh+data["nTimesteps"]*(jd-1)] for jh in JH, jd in JD]
    end

    for cluster in m.ext[:sets][:CSon]
        m.ext[:timeseries][:AF][IV[3]][cluster] = [Time_series_solar[!,cluster][jh+data["nTimesteps"]*(jd-1)] for jh in JH, jd in JD]
    end

    for cluster in m.ext[:sets][:CSof]
        m.ext[:timeseries][:AF][IV[4]][cluster] = [Time_series_solar_offshore[!,cluster][jh+data["nTimesteps"]*(jd-1)] for jh in JH, jd in JD]
    end

    # return model
    return m
end

process_time_series_data!(m, data, demand, Time_series_wind, Time_series_wind_offshore, Time_series_solar, Time_series_solar_offshore)



# step 2c: process input parameters
function process_parameters!(m::Model, data::Dict)

    # extract the sets you need
    I = m.ext[:sets][:I]
    ID = m.ext[:sets][:ID]
    IV = m.ext[:sets][:IV]
    C = m.ext[:sets][:C]
    K = m.ext[:sets][:K]
    CWon = m.ext[:sets][:CWon]
    CWof = m.ext[:sets][:CWof]
    CSon = m.ext[:sets][:CSon]
    CSof = m.ext[:sets][:CSof]

    # generate a dictonary "parameters"
    m.ext[:parameters] = Dict()

    # input parameters
    αCO2 = m.ext[:parameters][:αCO2] = data["CO2Price"] #euro/ton
    m.ext[:parameters][:VOLL] = data["VOLL"] #VOLL
    r = m.ext[:parameters][:discountrate] = data["discountrate"] #discountrate

   
    d = merge(data["dispatchableGenerators"],data["variableGenerators"])
    # variable costs
    β = m.ext[:parameters][:β] = Dict(i => d[i]["fuelCosts"] for i in ID) #EUR/MWh
    δ = m.ext[:parameters][:δ] = Dict(i => d[i]["emissions"] for i in ID) #ton/MWh
    m.ext[:parameters][:VC] = Dict(i => β[i]+αCO2*δ[i] for i in ID) # variable costs - EUR/MWh
    
    # Investment costs
    OC = m.ext[:parameters][:OC] = Dict(i => d[i]["OC"] for i in I) # EUR/MW
    LifeTime = m.ext[:parameters][:LT] = Dict(i => d[i]["lifetime"] for i in I) # years
    m.ext[:parameters][:IC] = Dict(i => r*OC[i]/(1-(1+r).^(-LifeTime[i])) for i in I) # EUR/MW/y

    # legacy capacity
    m.ext[:parameters][:LC] = Dict(i => d[i]["legcap"] for i in I) # MW


    # Percentages
    m.ext[:parameters][:perc] = Dict()
    m.ext[:parameters][:perc][IV[2]] = Dict()
    l = 1
    for c in C
        m.ext[:parameters][:perc][IV[2]][l] = Dict()
        for cluster in CWon
            m.ext[:parameters][:perc][IV[2]][l][cluster] = Clusters_to_countries_wind[!,c][cluster]
        end
        l += 1
    end

    m.ext[:parameters][:perc][IV[1]] = Dict()
    l = 1
    for c in C
        m.ext[:parameters][:perc][IV[1]][l] = Dict()
        for cluster in CWof
            m.ext[:parameters][:perc][IV[1]][l][cluster] = Clusters_to_countries_wind_offshore[!,c][cluster]
        end
        l += 1
    end

    m.ext[:parameters][:perc][IV[3]] = Dict()
    l = 1
    for c in C
        m.ext[:parameters][:perc][IV[3]][l] = Dict()
        for cluster in CSon
            m.ext[:parameters][:perc][IV[3]][l][cluster] = Clusters_to_countries_solar[!,c][cluster]
        end
        l += 1
    end

    m.ext[:parameters][:perc][IV[4]] = Dict()
    l = 1
    for c in C
        m.ext[:parameters][:perc][IV[4]][l] = Dict()
        for cluster in CSof
            m.ext[:parameters][:perc][IV[4]][l][cluster] = Clusters_to_countries_solar_offshore[!,c][cluster]
        end
        l += 1
    end

    # Import
    m.ext[:parameters][:max_import] = Dict()
    l = 1
    for c in C
        m.ext[:parameters][:max_import][l] = Dict()
        for k in K
            m.ext[:parameters][:max_import][l][k] = imp[!,c][k]
        end
        l += 1
    end 
    
    # Export
    m.ext[:parameters][:max_export] = Dict()
    l = 1
    for c in C        
        m.ext[:parameters][:max_export][l] = Dict()
        for k in K
            m.ext[:parameters][:max_export][l][k] = exp[!,c][k]
        end
        l += 1
    end 

    # Totals
    m.ext[:parameters][:totals] = Dict()

    total = 0
    m.ext[:parameters][:totals][IV[2]] = Dict()
    for cluster in m.ext[:sets][:CWon]
        for country in C
            total += Clusters_to_countries_wind[!,country][cluster]
        end
        m.ext[:parameters][:totals][IV[2]][cluster] = total
    end

    total = 0
    m.ext[:parameters][:totals][IV[1]] = Dict()
    for cluster in m.ext[:sets][:CWof]
        for country in C
            total += Clusters_to_countries_wind_offshore[!,country][cluster]
        end
        m.ext[:parameters][:totals][IV[1]][cluster] = total
    end

    total = 0
    m.ext[:parameters][:totals][IV[3]] = Dict()
    for cluster in m.ext[:sets][:CSon]
        for country in C
            total += Clusters_to_countries_solar[!,country][cluster]
        end
        m.ext[:parameters][:totals][IV[3]][cluster] = total
    end

    total = 0
    m.ext[:parameters][:totals][IV[4]] = Dict()
    for cluster in m.ext[:sets][:CSof]
        for country in C
            total += Clusters_to_countries_solar_offshore[!,country][cluster]
        end
        m.ext[:parameters][:totals][IV[4]][cluster] = total
    end

    return m
end

process_parameters!(m, data)

# perc = m.ext[:parameters][:perc] # Percentage of cluster asigned to country | per technology per country per cluster
# total = m.ext[:parameters][:totals] # Total percentage of clusterd relevant | per technology per cluster
# max_imp = m.ext[:parameters][:max_import] # max import | per country per country
# max_exp = m.ext[:parameters][:max_export] # max import | per country per country
# D = m.ext[:timeseries][:D] # demand | per country
# AF = m.ext[:timeseries][:AF] # availability factors | per technology IV per cluster Z



# imp[!,1][1,1,1]
# exp[!,1][1,1,1]
# typeof(imp[!,1][1,1,1])
# typeof(exp[!,1][1,1,1])
# typeof(perc["On-Wind"][1][2])
# typeof(total["On-Wind"][1])
# typeof(AF["On-Wind"][1][1,1])
# typeof(D[1][1,1])


## Step 3: construct your model
# Greenfield GEP - single year (Lecture 3 - slide 25, but based on representative days instead of full year)
function build_greenfield_1Y_GEP_model!(m::Model)
    # Clear m.ext entries "variables", "expressions" and "constraints"
    m.ext[:variables] = Dict()
    m.ext[:expressions] = Dict()
    m.ext[:constraints] = Dict()

    # Extract sets
    I = m.ext[:sets][:I]
    ID = m.ext[:sets][:ID]
    IV = m.ext[:sets][:IV]
    JH = m.ext[:sets][:JH]
    JD = m.ext[:sets][:JD]
    C = m.ext[:sets][:C]
    K = m.ext[:sets][:K]
    CWon = m.ext[:sets][:CWon]
    CWof = m.ext[:sets][:CWof]
    CSon = m.ext[:sets][:CSon]
    CSof = m.ext[:sets][:CSof]


    # Extract time series data
    D = m.ext[:timeseries][:D] # demand | per country
    AF = m.ext[:timeseries][:AF] # availability factors | per technology IV per cluster Z

    # Extract parameters
    VOLL = m.ext[:parameters][:VOLL] # VOLL | -
    VC = m.ext[:parameters][:VC] # variable cost | per technology
    IC = m.ext[:parameters][:IC] # investment cost | per technology
    perc = m.ext[:parameters][:perc] # Percentage of cluster asigned to country | per technology per country per cluster
    total = m.ext[:parameters][:totals] # Total percentage of clusterd relevant | per technology per cluster
    max_imp = m.ext[:parameters][:max_import] # max import | per country per country
    max_exp = m.ext[:parameters][:max_export] # max import | per country per country
    

    # Create variables
    cap = m.ext[:variables][:cap] = @variable(m, [i=I,c=K], lower_bound=0, base_name="capacity") # Capacity must be per cluster, but also need a capacity per country
    g = m.ext[:variables][:g] = @variable(m, [i=I,c=K,jh=JH,jd=JD], lower_bound=0, base_name="generation") # Generation per country
    ens = m.ext[:variables][:ens] = @variable(m, [c=K,jh=JH,jd=JD], lower_bound=0, base_name="load_shedding")
    imp = m.ext[:variables][:inp] = @variable(m, [c=K,k=K,jh=JH,jd=JD], lower_bound=0, base_name="Import")
    exp = m.ext[:variables][:exp] = @variable(m, [c=K,k=K,jh=JH,jd=JD], lower_bound=0, base_name="Export")

    # # Create affine expressions (= linear combinations of variables)
    # curt = m.ext[:expressions][:curt] = @expression(m, [i=IV,jh=JH,jd=JD],
    #     AF[i][Z][jh,jd]*cap[i] - g[i,jh,jd]
    # )

    # Formulate objective 1a
    m.ext[:objective] = @objective(m, Min,
        + sum(IC[i]*cap[i,c] for i in I, c in K)
        + sum(VC[i]*g[i,c,jh,jd] for i in ID, c in K, jh in JH, jd in JD)
        + sum(ens[c,jh,jd]*VOLL for c in K, jh in JH, jd in JD)
    )

    display("pre power balance")
    # 2a - power balance
    m.ext[:constraints][:con2a] = @constraint(m, [c=K,jh=JH,jd=JD],
    + sum(g[i,c,jh,jd] for i in I) 
    - sum(imp[c,k,jh,jd] for k in K) 
    - sum(exp[c,k,jh,jd] for k in K) 
    + sum(perc["On-Wind"][c][z]*total["On-Wind"][z]*AF["On-Wind"][z][jh,jd]*cap[] for z in CWon) 
    + sum(perc["Off-Wind"][c][z]*total["Off-Wind"][z]*AF["Off-Wind"][z][jh,jd] for z in CWof) 
    + sum(perc["On-Solar"][c][z]*total["On-Solar"][z]*AF["On-Solar"][z][jh,jd] for z in CSon) 
    + sum(perc["Off-Solar"][c][z]*total["Off-Solar"][z]*AF["Off-Solar"][z][jh,jd] for z in CSof)
    == D[c][jh,jd] - ens[c,jh,jd]
    )

    display("post power balance")
    # 2c2 - load shedding
    m.ext[:constraints][:con2c] = @constraint(m, [c=K,jh=JH,jd=JD],
        ens[c,jh,jd] <= D[c][jh,jd]
    )
    

    display("Start constraints max generation")
    # 3a - renewables
    # 3a1 - Onshore wind 
    m.ext[:constraints][:con3a1] = @constraint(m, [c=K,z=CWon,jh=JH,jd=JD],
    g["On-Wind",c,jh,jd] <= perc["On-Wind"][c][z]*total["On-Wind"][z]*AF["On-Wind"][z][jh,jd]*cap["On-Wind",c]
    )

    # 3a2 - Offshore wind 
    m.ext[:constraints][:con3a2] = @constraint(m, [c=K,z=CWof,jh=JH,jd=JD],
    g["Off-Wind",c,jh,jd] <= perc["Off-Wind"][c][z]*total["Off-Wind"][z]*AF["Off-Wind"][z][jh,jd]*cap["On-Wind",c]
    )

    # 3a3 - Onshore solar 
    m.ext[:constraints][:con3a3] = @constraint(m, [c=K,z=CSon,jh=JH,jd=JD],
    g["On-Solar",c,jh,jd] <= perc["On-Solar"][c][z]*total["On-Solar"][z]*AF["On-Solar"][z][jh,jd]*cap["On-Wind",c]
    )

    # 3a4 - Offshore solar
    m.ext[:constraints][:con3a4] = @constraint(m, [c=K,z=CSof,jh=JH,jd=JD],
    g["Off-Solar",c,jh,jd] <= perc["Off-Solar"][c][z]*total["Off-Solar"][z]*AF["Off-Solar"][z][jh,jd]*cap["On-Wind",c]
    )

    # 3b - conventional
    m.ext[:constraints][:con3b] = @constraint(m, [c=K,i=ID,jh=JH,jd=JD],
        g[i,c,jh,jd] <= cap[i,c]
    )

    
    display("Start import/export")
    # 4a - Max import
    m.ext[:constraints][:con4a] = @constraint(m, [c=K,k=K,jh=JH,jd=JD],
        imp[c,k,jh,jd] <= max_imp[c][k]
    )

    # 4b - Max export
    m.ext[:constraints][:con4b] = @constraint(m, [c=K,k=K,jh=JH,jd=JD],
        exp[c,k,jh,jd] <= max_exp[c][k]
    )

    return m
end


# Build your model
build_greenfield_1Y_GEP_model!(m)
# build_brownfield_1Y_GEP_model!(m)

## Step 4: solve
optimize!(m)
# check termination status
print(
    """

    Termination status: $(termination_status(m))

    """
)


# print some output
@show value(m.ext[:objective])
@show value.(m.ext[:variables][:cap])

## Step 5: interpretation
using Plots
using Interact
using StatsPlots

# examples on how to access data

# sets
JH = m.ext[:sets][:JH]
JD = m.ext[:sets][:JD]
I = m.ext[:sets][:I]

# parameters
D = m.ext[:timeseries][:D]
W = m.ext[:parameters][:W]
LC = m.ext[:parameters][:LC]

# variables/expressions
cap = value.(m.ext[:variables][:cap])
g = value.(m.ext[:variables][:g])
ens = value.(m.ext[:variables][:ens])
curt = value.(m.ext[:expressions][:curt])
λ = dual.(m.ext[:constraints][:con2a])

# create arrays for plotting
λvec = [λ[jh,jd]/W[jd] for jh in JH, jd in JD]
gvec = [g[i,jh,jd] for i in I, jh in JH, jd in JD]
capvec = [cap[i] for  i in I]


# Select day for which you'd like to plotting
jd = 1

# Electricity price 
p1 = plot(JH,λvec[:,jd], xlabel="Timesteps [-]", ylabel="λ [EUR/MWh]", label="λ [EUR/MWh]", legend=:outertopright );

# Dispatch
p2 = groupedbar(transpose(gvec[:,:,jd]), label=["Mid" "Base" "Peak" "Wind" "Solar"], bar_position = :stack,legend=:outertopright,ylims=(0,13_000));
plot!(p2, JH, D[:,jd], label ="Demand", xlabel="Timesteps [-]", ylabel="Generation [MWh]", legend=:outertopright, lindewidth=3, lc=:black);

# Capacity
p3 = bar(capvec, label="", xticks=(1:length(capvec), ["Mid" "Base" "Peak" "Wind" "Solar"]), xlabel="Technology [-]", ylabel="New capacity [MW]", legend=:outertopright);

# combine
plot(p1, p2, p3, layout = (3,1))
plot!(size=(1000,800))












# # Brownfield GEP - single year
# function build_brownfield_1Y_GEP_model!(m::Model)
#     # start from Greenfield
#     m = build_greenfield_1Y_GEP_model!(m::Model)

#     # extract sets
#     ID = m.ext[:sets][:ID]
#     IV = m.ext[:sets][:IV]
#     JH = m.ext[:sets][:JH]
#     JD = m.ext[:sets][:JD]  
    
#     # Extract parameters
#     LC = m.ext[:parameters][:LC]

#     # Extract time series
#     AF = m.ext[:timeseries][:AF] # availability factors

#     # extract variables
#     g = m.ext[:variables][:g]
#     cap = m.ext[:variables][:cap]

#     # remove the constraints that need to be changed:
#     for iv in IV, jh in JH, jd in JD
#         delete(m,m.ext[:constraints][:con3a1res][iv,jh,jd])
#     end
#     for id in ID, jh in JH, jd in JD
#         delete(m,m.ext[:constraints][:con3a1conv][id,jh,jd]) #If there is an error, check here, not 100% sure
#     end

#     # define new constraints
#     # 3a1 - renewables
#     m.ext[:constraints][:con3a1res] = @constraint(m, [i=IV, jh=JH, jd =JD],
#         g[i,jh,jd] <= AF[i][jh,jd]*(cap[i]+LC[i])
#     )

#     # 3a1 - conventional
#     m.ext[:constraints][:con3a1conv] = @constraint(m, [i=ID, jh=JH, jd=JD],
#         g[i,jh,jd] <= (cap[i]+LC[i])
#     )

#     return m
# end

