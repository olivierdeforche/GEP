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

data = YAML.load_file(joinpath(@__DIR__, "data_gep_update_2.yaml"))
demand = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"), "Demand"))
countries = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"),"Countries"))
imp = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"), "Import"))
# exp = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"), "Export"))

Clusters_to_countries_wind = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Asigned_To_Countries/",method,"_",no_clusters,"_",data_used,"_df_wind.xlsx")),"Sheet1"))
Clusters_to_countries_wind_offshore = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Asigned_To_Countries/",method,"_",no_clusters,"_",data_used,"_df_wind_offshore.xlsx")),"Sheet1"))
Clusters_to_countries_solar = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Asigned_To_Countries/",method,"_",no_clusters,"_",data_used,"_df_solar.xlsx")),"Sheet1"))

Time_series_wind = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Timeseries/",method,"_",no_clusters,"_",data_used,"_clustered_on_wind.xlsx")),"Sheet1"))
Time_series_wind_offshore = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Timeseries/",method,"_",no_clusters,"_",data_used,"_clustered_on_wind_offshore.xlsx")),"Sheet1"))
Time_series_solar = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Timeseries/",method,"_",no_clusters,"_",data_used,"_clustered_on_solar.xlsx")),"Sheet1"))

## Step 2: create model & pass data to model
using JuMP
using Gurobi
m = Model(optimizer_with_attributes(Gurobi.Optimizer))
set_optimizer_attribute(m, "Method", 2)
set_optimizer_attribute(m, "BarHomogeneous", 1)
set_optimizer_attribute(m, "Threads", 12)
# set_optimizer_attribute(m, "NodefileDir", "C:\\Users\\defor\\Desktop\\Thesis\\GEP\\GEP")
# set_optimizer_attribute(m, "NodefileStart", 0.5)

# Step 2a: create sets
function define_sets!(m::Model, data::Dict, Time_series_wind::DataFrame, Time_series_wind_offshore::DataFrame, Time_series_solar::DataFrame)
    
    # create dictionary to store sets
    m.ext[:sets] = Dict()

    # define the sets
    m.ext[:sets][:JH] = 1:data["nTimesteps"] # Timesteps (24)
    m.ext[:sets][:JD] = 1:data["nDays"] # Number of days days (365)
    m.ext[:sets][:ID] = [id for id in keys(data["dispatchableGenerators"])] # dispatchable generators
    m.ext[:sets][:IV] = [iv for iv in keys(data["variableGenerators"])] # variable generators
    m.ext[:sets][:I] = union(m.ext[:sets][:ID], m.ext[:sets][:IV]) # all generators
    m.ext[:sets][:CWon] = 1:ncol(Time_series_wind)
    m.ext[:sets][:CWof] = 1:ncol(Time_series_wind_offshore)
    m.ext[:sets][:CSon] = 1:ncol(Time_series_solar)
    m.ext[:sets][:C] = [c for c in countries[!,"Countries"]] 
    m.ext[:sets][:K] = 1:nrow(countries)
    
    # return model
    return m
end


define_sets!(m, data, Time_series_wind, Time_series_wind_offshore, Time_series_solar)

# Step 2b: add time series
function process_time_series_data!(m::Model, data::Dict, demand::DataFrame, Time_series_wind::DataFrame, Time_series_wind_offshore::DataFrame, Time_series_solar::DataFrame)
    # extract the relevant sets
    IV = m.ext[:sets][:IV] # Variable generators
    JH = m.ext[:sets][:JH] # Time steps
    JD = m.ext[:sets][:JD] # Days
    C = m.ext[:sets][:C]
    CWon = m.ext[:sets][:CWon]
    CWof = m.ext[:sets][:CWof]
    CSon = m.ext[:sets][:CSon]

    # create dictionary to store time series
    m.ext[:timeseries] = Dict()
    m.ext[:timeseries][:AF] = Dict()

    m.ext[:timeseries][:D] = [demand[!,country][jh+data["nTimesteps"]*(jd-1)] for country in C, jh in JH, jd in JD]
    m.ext[:timeseries][:AF][IV[2]] = [Time_series_wind[!,cluster][jh+data["nTimesteps"]*(jd-1)] for cluster in CWon, jh in JH, jd in JD]
    m.ext[:timeseries][:AF][IV[1]] = [Time_series_wind_offshore[!,cluster][jh+data["nTimesteps"]*(jd-1)] for cluster in CWof, jh in JH, jd in JD]
    m.ext[:timeseries][:AF][IV[3]] = [Time_series_solar[!,cluster][jh+data["nTimesteps"]*(jd-1)] for cluster in CSon, jh in JH, jd in JD]

    # return model
    return m
end

process_time_series_data!(m, data, demand, Time_series_wind, Time_series_wind_offshore, Time_series_solar)

# step 2c: process input parameters
function process_parameters!(m::Model, data::Dict)

    # extract the sets you need
    I = m.ext[:sets][:I]
    IV = m.ext[:sets][:IV]
    CWon = m.ext[:sets][:CWon]
    CWof = m.ext[:sets][:CWof]
    CSon = m.ext[:sets][:CSon]
    C = m.ext[:sets][:C]
    K = m.ext[:sets][:K]

    # generate a dictonary "parameters"
    m.ext[:parameters] = Dict()

    # input parameters
    αCO2 = m.ext[:parameters][:αCO2] = data["CO2Price"] #euro/ton
    m.ext[:parameters][:VOLL] = data["VOLL"] #VOLL
    r = m.ext[:parameters][:discountrate] = data["discountrate"] #discountrate

   
    d = merge(data["dispatchableGenerators"],data["variableGenerators"])
    # variable costs
    β = m.ext[:parameters][:β] = Dict(i => d[i]["fuelCosts"] for i in I) #EUR/MWh
    δ = m.ext[:parameters][:δ] = Dict(i => d[i]["emissions"] for i in I) #ton/MWh
    m.ext[:parameters][:VC] = Dict(i => β[i]+αCO2*δ[i] for i in I) # variable costs - EUR/MWh
    
    # Investment costs
    OC = m.ext[:parameters][:OC] = Dict(i => d[i]["OC"] for i in I) # EUR/MW
    LifeTime = m.ext[:parameters][:LT] = Dict(i => d[i]["lifetime"] for i in I) # years
    m.ext[:parameters][:IC] = Dict(i => r*OC[i]/(1-(1+r).^(-LifeTime[i])) for i in I) # EUR/MW/y

    # legacy capacity
    m.ext[:parameters][:LC] = Dict(i => d[i]["legcap"] for i in I) # MW

    # Totals
    m.ext[:parameters][:totals] = Dict()
    m.ext[:parameters][:totals][IV[2]] = [Clusters_to_countries_wind.total[cluster] for cluster in CWon]
    m.ext[:parameters][:totals][IV[1]] = [Clusters_to_countries_wind_offshore.total[cluster] for cluster in CWof]
    m.ext[:parameters][:totals][IV[3]] = [Clusters_to_countries_solar.total[cluster] for cluster in CSon]

    # Percentages
    m.ext[:parameters][:perc] = Dict()
    m.ext[:parameters][:perc][IV[2]] = [Clusters_to_countries_wind[!,country][cluster] for country in C, cluster in CWon]
    m.ext[:parameters][:perc][IV[1]] = [Clusters_to_countries_wind_offshore[!,country][cluster] for country in C, cluster in CWof]
    m.ext[:parameters][:perc][IV[3]] = [Clusters_to_countries_solar[!,country][cluster] for country in C, cluster in CSon]

    # Import
    m.ext[:parameters][:max_import] = [imp[!,country][k] for country in C, k in K]
    m.ext[:parameters][:max_export] = transpose(m.ext[:parameters][:max_import])
    # Export    
    # m.ext[:parameters][:max_export] = [exp[!,country][k] for country in C, k in K]
    return m
end

process_parameters!(m, data)


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
    JH = m.ext[:sets][:JH]
    JD = m.ext[:sets][:JD]
    CWon = m.ext[:sets][:CWon]
    CWof = m.ext[:sets][:CWof]
    CSon = m.ext[:sets][:CSon]
    C = m.ext[:sets][:C]
    K = m.ext[:sets][:K]

    display("extracting timeseries")
    # Extract time series data
    D = m.ext[:timeseries][:D] # demand | per country
    AF = m.ext[:timeseries][:AF] # availability factors | per technology IV per cluster Z

    display("extracting parameters")
    # Extract parameters
    VOLL = m.ext[:parameters][:VOLL] # VOLL | -
    VC = m.ext[:parameters][:VC] # variable cost | per technology
    IC = m.ext[:parameters][:IC] # investment cost | per technology
    total = m.ext[:parameters][:totals] # Total percentage of clusterd relevant | per technology per cluster
    max_imp = m.ext[:parameters][:max_import] # max import | per country per country
    max_exp = m.ext[:parameters][:max_export] # max import | per country per country
    perc = m.ext[:parameters][:perc] # percentage from cluster assigned to country | technology per country per cluster
    
    display("starting variables now")
    # Create variables
    cap_conv = m.ext[:variables][:capc] = @variable(m, [c=K,i=ID], lower_bound=0, base_name="capacity conventional") # Capacity must be per cluster, but also need a capacity per country
    cap_ren_Won = m.ext[:variables][:cap_r_won] = @variable(m, [z=CWon], lower_bound=0, base_name="capacity renewables wind onshore")
    cap_ren_Wof = m.ext[:variables][:cap_r_wof] = @variable(m, [z=CWof], lower_bound=0, base_name="capacity renewables wind offshore")
    cap_ren_Son = m.ext[:variables][:cap_r_son] = @variable(m, [z=CSon], lower_bound=0, base_name="capacity renewables solar onshore")
    g = m.ext[:variables][:g] = @variable(m, [c=K,i=I,jh=JH,jd=JD], lower_bound=0, base_name="generation") # Generation per country
    ens = m.ext[:variables][:ens] = @variable(m, [c=K,jh=JH,jd=JD], lower_bound=0, base_name="load_shedding")
    display("starting import and export now")
    impexp = m.ext[:variables][:imp] = @variable(m,[c=K,k=K,jh=JH,jd=JD], base_name="Import")


    # # Create affine expressions (= linear combinations of variables)
    # curt = m.ext[:expressions][:curt] = @expression(m, [i=IV,jh=JH,jd=JD],
    #     AF[i][Z][jh,jd]*cap[i] - g[i,jh,jd]
    # )

    display("formulating objective")
    # Formulate objective 1a
    m.ext[:objective] = @objective(m, Min,
        + sum(IC[i]*cap_conv[c,i] for c in K, i in ID)
        + sum(IC["On-Wind"]*cap_ren_Won[z]/total["On-Wind"][z] for z in CWon)
        + sum(IC["Off-Wind"]*cap_ren_Wof[z]/total["Off-Wind"][z] for z in CWof)
        + sum(IC["Solar"]*cap_ren_Son[z]/total["Solar"][z] for z in CSon)
        + sum(VC[i]*g[c,i,jh,jd] for c in K, i in I, jh in JH, jd in JD)
        + sum(ens[c,jh,jd]*VOLL for c in K, jh in JH, jd in JD)
    )

    display("pre power balance")
    # 2a - power balance
    m.ext[:constraints][:con2a] = @constraint(m, [c=K,jh=JH,jd=JD],
    + sum(g[c,i,jh,jd] for i in I) + sum(impexp[c,k,jh,jd] for k in K) == D[c,jh,jd] - ens[c,jh,jd]
    )

    display("post power balance")
    # 2c2 - load shedding
    m.ext[:constraints][:con2c] = @constraint(m, [c=K,jh=JH,jd=JD],
        ens[c,jh,jd] <= D[c,jh,jd]
    )
    

    display("Start constraints max generation")
    # 3a - renewables
    # 3a1 - Onshore wind 
    m.ext[:constraints][:con3a1] = @constraint(m, [c=K,jh=JH,jd=JD],
    g[c,"On-Wind",jh,jd] <= sum(perc["On-Wind"][c,z]*AF["On-Wind"][z,jh,jd]*cap_ren_Won[z] for z in CWon)
    )

    # 3a2 - Offshore wind 
    m.ext[:constraints][:con3a2] = @constraint(m, [c=K,jh=JH,jd=JD],
    g[c,"Off-Wind",jh,jd] <= sum(perc["Off-Wind"][c,z]*AF["Off-Wind"][z,jh,jd]*cap_ren_Wof[z] for z in CWof)
    )

    # 3a3 - Onshore solar 
    m.ext[:constraints][:con3a3] = @constraint(m, [c=K,jh=JH,jd=JD],
    g[c,"Solar",jh,jd] <= sum(perc["Solar"][c,z]*AF["Solar"][z,jh,jd]*cap_ren_Son[z] for z in CSon)
    )

    # 3b - conventional
    m.ext[:constraints][:con3b] = @constraint(m, [c=K,i=ID,jh=JH,jd=JD],
        g[c,i,jh,jd] <= cap_conv[c,i]
    )

    display("Start import/export")
    # 4a - Max import
    m.ext[:constraints][:con4a] = @constraint(m, [c=K,k=K,jh=JH,jd=JD],
    -max_exp[c,k] <= impexp[c,k,jh,jd] <= max_imp[c,k]
    )

    # 4b - Import should equal Export other country
    m.ext[:constraints][:con4b] = @constraint(m, [c=K,k=K,jh=JH,jd=JD],
     impexp[c,k,jh,jd] == -impexp[k,c,jh,jd] 
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
@show value.(m.ext[:variables][:capc])
@show value.(m.ext[:variables][:cap_r_won])
@show value.(m.ext[:variables][:cap_r_wof])
@show value.(m.ext[:variables][:cap_r_son])

## Step 5: interpretation
using Plots
using Interact
using StatsPlots

# examples on how to access data
# Warning: insufficient memory, speed may be affected.

# sets
I = m.ext[:sets][:I];
ID = m.ext[:sets][:ID];
IV = m.ext[:sets][:IV];
JH = m.ext[:sets][:JH];
JD = m.ext[:sets][:JD];
CWon = m.ext[:sets][:CWon];
CWof = m.ext[:sets][:CWof];
CSon = m.ext[:sets][:CSon];
K = m.ext[:sets][:K];

# parameters
D = m.ext[:timeseries][:D];
VOLL = m.ext[:parameters][:VOLL] # VOLL | -
VC = m.ext[:parameters][:VC] # variable cost | per technology
IC = m.ext[:parameters][:IC] # investment cost | per technology

# variables/expressions
cap_conv = value.(m.ext[:variables][:capc][:,:]);
cap_res_won = value.(m.ext[:variables][:cap_r_won][:]);
cap_res_wof = value.(m.ext[:variables][:cap_r_wof][:]);
cap_res_son = value.(m.ext[:variables][:cap_r_son][:]);
g = value.(m.ext[:variables][:g][:,:,:,:]);
ens = value.(m.ext[:variables][:ens][:,:,:]);
λ = dual.(m.ext[:constraints][:con2a][:,:,:]);
impexp = value.(m.ext[:variables][:imp][:,:,:,:]);

# # create arrays for plotting
λvec = [λ[c,jh,jd] for c in K, jh in JH, jd in JD];
λvec = sum(λvec[c,:,:] for c in K);
gvec = [g[c,i,jh,jd] for c in K, i in I, jh in JH, jd in JD];
gvec = sum(gvec[c,:,:,:] for c in K);
cap_res_wonvec = sum(cap_res_won[z] for z in CWon)
cap_res_wofvec = sum(cap_res_wof[z] for z in CWof)
cap_res_sonvec = sum(cap_res_son[z] for z in CSon) 
cap_convvec = [cap_conv[c,i] for  c in K, i in ID]
cap_convvec = sum(cap_convvec[c,:] for c in K)
demand = sum(D[c,:,:] for c in K);
impexpvec = [impexp[c,k,jh,jd] for c in K, k in K, jh in JH, jd in JD];
impexpvec = sum(impexpvec[:,:,jh,jd] for jh in JH, jd in JD)


capvec = cap_convvec
push!(capvec,cap_res_wonvec)
push!(capvec,cap_res_wofvec)
push!(capvec,cap_res_sonvec)


# Select day for which you'd like to plotting
jd = 150
# Electricity price 
p1 = plot(JH,λvec[:,jd], xlabel="Timesteps [-]", ylabel="λ [EUR/MWh]", label="λ [EUR/MWh]", legend=:outertopright );
# Dispatch
p2 = groupedbar(transpose(gvec[:,:,jd]), label=["CCGT" "Nuclear" "OCGT" "Off-Wind" "On-Wind" "Solar" "import" "export"], bar_position = :stack,legend=:outertopright);
plot!(p2, JH, demand[:,jd], label ="Demand", xlabel="Timesteps [-]", ylabel="Generation [MWh]", legend=:outertopright, lindewidth=3, lc=:black);# Capacity
p3 = bar(capvec, label="", xticks=(1:length(capvec), ["CCGT" "Nuclear" "OCGT" "On-Wind" "Off-Wind" "Solar"]), xlabel="Technology [-]", ylabel="New capacity [MW]", legend=:outertopright);
p4 = plot(JH,impexpvec[:,jd], xlabel="Timesteps [-]", ylabel="Import/Export [WATT]", label="Import/Export [WATT]", legend=:outertopright );
# combine
plot(p1, p2, p3, p4, layout = (4,1))
plot!(size=(1000,800))


# variables/expressions for Belgium
cap_conv_alb = value.(m.ext[:variables][:capc][9,:])
cap_res_won_alb = value.(m.ext[:variables][:cap_r_won][:])
cap_res_wof_alb = value.(m.ext[:variables][:cap_r_wof][:])
cap_res_son_alb = value.(m.ext[:variables][:cap_r_son][:])
g_alb = value.(m.ext[:variables][:g][9,:,:,:])
ens_alb = value.(m.ext[:variables][:ens][9,:,:])
# curt = value.(m.ext[:expressions][:curt])
λ_alb = dual.(m.ext[:constraints][:con2a][9,:,:])
impexp = value.(m.ext[:variables][:imp][9,:,:,:])
perc = m.ext[:parameters][:perc]

# # create arrays for plotting
λvec_alb = [λ_alb[jh,jd] for jh in JH, jd in JD]
gvec_alb = [g_alb[i,jh,jd] for i in I, jh in JH, jd in JD]
cap_res_wonvec_alb = sum(perc["On-Wind"][9,z]*cap_res_won_alb[z] for z in CWon)
cap_res_wofvec_alb = sum(perc["Off-Wind"][9,z]*cap_res_wof_alb[z] for z in CWof)
cap_res_sonvec_alb = sum(perc["Solar"][9,z]*cap_res_son_alb[z] for z in CSon) 
cap_convvec_alb = [cap_conv_alb[i] for  i in ID]
impexpvec = [impexp[k,jh,jd] for k in K, jh in JH, jd in JD]
impexpvec = sum(impexpvec[k,:,:] for k in K)
capvec_alb = cap_convvec_alb
push!(capvec_alb,cap_res_wonvec_alb)
push!(capvec_alb,cap_res_wofvec_alb)
push!(capvec_alb,cap_res_sonvec_alb)

# Select day for which you'd like to plotting
jd = 12
# Electricity price 
p1 = plot(JH,λvec_alb[:,jd], xlabel="Timesteps [-]", ylabel="λ [EUR/MWh]", label="λ [EUR/MWh]", legend=:outertopright );
# Dispatch
p2 = groupedbar(transpose(gvec_alb[:,:,jd]), label=["CCGT" "Nuclear" "OCGT" "Off-Wind" "On-Wind" "Solar"], bar_position = :stack,legend=:outertopright);
plot!(p2, JH, D[9,:,jd], label ="Demand", xlabel="Timesteps [-]", ylabel="Generation [MWh]", legend=:outertopright, lindewidth=3, lc=:black);# Capacity
p3 = bar(capvec_alb, label="", xticks=(1:length(capvec_alb), ["CCGT" "Nuclear" "OCGT" "On-Wind" "Off-Wind" "Solar"]), xlabel="Technology [-]", ylabel="New capacity [MW]", legend=:outertopright);
p4 = plot(JH,impexpvec[:,jd], xlabel="Timesteps [-]", ylabel="export/import", label="export/import in WATT", legend=:outertopright);
# combine
plot(p1, p2, p3, p4, layout = (4,1))
plot!(size=(1000,800))