## Backbone to structure your code
# author: Olivier Deforche, Louis Maes
# last update: April 17, 2023
# reference: This model is build upon the backbone code from Kenneth Bruninx for the course: Optimization problems in Engergy systems 
# description: TBD

using Pkg
## Step 0: Activate environment - ensure consistency accross computers
Pkg.activate(@__DIR__) # @__DIR__ = directory this script is in
Pkg.instantiate() # If a Manifest.toml file exist in the current project, download all the packages declared in that manifest. Else, resolve a set of feasible packages from the Project.toml files and install them.

Pkg.add("CSV")
Pkg.add("DataFrames")
Pkg.add("YAML")
Pkg.add("XLSX")
Pkg.add("JuMP")
Pkg.add("Gurobi")
using CSV
using DataFrames
using YAML
using XLSX
using JuMP
using Gurobi

function GEP(method, no_clusters, data_used)

    ##  Step 1: Choose the correct data and load every input data
    data = YAML.load_file(joinpath(@__DIR__, "data_gep_update_3.yaml"))
    demand = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"), "Demand"))
    countries = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"),"Countries"))
    imp = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"), "Import"))
    # exp = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"), "Export"))
    Max_cap_nuclear = DataFrame(XLSX.readtable(joinpath(@__DIR__,"Data/Data_GEP.xlsx"), "Max_cap_nuclear"))

    Clusters_to_countries_wind = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Asigned_To_Countries/",method,"_",no_clusters,"_",data_used,"_df_wind.xlsx")),"Sheet1"))
    Clusters_to_countries_wind_offshore = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Asigned_To_Countries/",method,"_",no_clusters,"_",data_used,"_df_wind_offshore.xlsx")),"Sheet1"))
    Clusters_to_countries_solar = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Asigned_To_Countries/",method,"_",no_clusters,"_",data_used,"_df_solar.xlsx")),"Sheet1"))

    Time_series_wind = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Timeseries/",method,"_",no_clusters,"_",data_used,"_clustered_on_wind.xlsx")),"Sheet1"))
    Time_series_wind_offshore = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Timeseries/",method,"_",no_clusters,"_",data_used,"_clustered_on_wind_offshore.xlsx")),"Sheet1"))
    Time_series_solar = DataFrame(XLSX.readtable(joinpath(@__DIR__,string("Output_Clusters_Timeseries/",method,"_",no_clusters,"_",data_used,"_clustered_on_solar.xlsx")),"Sheet1"))

    ## Step 2: create model & pass data to model
    m = Model(optimizer_with_attributes(Gurobi.Optimizer))
    set_optimizer_attribute(m, "Method", 2)
    set_optimizer_attribute(m, "BarHomogeneous", 1)
    # set_optimizer_attribute(m, "Threads", 12)
    # set_optimizer_attribute(m, "NodefileDir", "C:\\Users\\defor\\Desktop\\Thesis\\GEP\\GEP")
    # set_optimizer_attribute(m, "NodefileStart", 0.5)

    # Step 2a: create sets
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


    ## Step 2b: add time series
    display("Start Timeseries")
    # Extract sets
    I = m.ext[:sets][:I]
    ID = m.ext[:sets][:ID]
    IV = m.ext[:sets][:IV]
    JH = m.ext[:sets][:JH]
    JD = m.ext[:sets][:JD]
    CWon = m.ext[:sets][:CWon]
    CWof = m.ext[:sets][:CWof]
    CSon = m.ext[:sets][:CSon]
    C = m.ext[:sets][:C]
    K = m.ext[:sets][:K]

    # create dictionary to store time series
    m.ext[:timeseries] = Dict()
    m.ext[:timeseries][:AF] = Dict()

    m.ext[:timeseries][:D] = [demand[!,country][jh+data["nTimesteps"]*(jd-1)] for country in C, jh in JH, jd in JD]
    m.ext[:timeseries][:AF][IV[2]] = [Time_series_wind[!,cluster][jh+data["nTimesteps"]*(jd-1)] for cluster in CWon, jh in JH, jd in JD]
    m.ext[:timeseries][:AF][IV[1]] = [Time_series_wind_offshore[!,cluster][jh+data["nTimesteps"]*(jd-1)] for cluster in CWof, jh in JH, jd in JD]
    m.ext[:timeseries][:AF][IV[3]] = [Time_series_solar[!,cluster][jh+data["nTimesteps"]*(jd-1)] for cluster in CSon, jh in JH, jd in JD]

    ## Add parameters
    display("Start Paramaters")
    # generate a dictonary "parameters"
    m.ext[:parameters] = Dict()

    # input parameters
    αCO2 = m.ext[:parameters][:αCO2] = data["CO2Price"] #euro/ton
    m.ext[:parameters][:VOLL] = data["VOLL"] #VOLL
    r = m.ext[:parameters][:discountrate] = data["discountrate"] #discountrate
    m.ext[:parameters][:TRANSFER] = data["TRANSFER"] #Cost of transfering energy


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

    # Export
    m.ext[:parameters][:max_export] = transpose(m.ext[:parameters][:max_import])   
    
    # Max Capacity Nuclear
    m.ext[:parameters][:max_cap_nuclear] = [Max_cap_nuclear[!,"MaxCapNuclear"][k] for k in K]


    ## Step 3: construct your model
    display("Start Model construction")
    # Greenfield GEP - single year (Lecture 3 - slide 25, but based on representative days instead of full year)
    # Clear m.ext entries "variables", "expressions" and "constraints"
    m.ext[:variables] = Dict()
    m.ext[:expressions] = Dict()
    m.ext[:constraints] = Dict()

    display("extracting timeseries")
    # Extract time series data
    D = m.ext[:timeseries][:D] # demand | per country
    AF = m.ext[:timeseries][:AF] # availability factors | per technology IV per cluster Z

    display("extracting parameters")
    # Extract parameters
    VOLL = m.ext[:parameters][:VOLL] # VOLL | -
    TRANSFER = m.ext[:parameters][:TRANSFER] # Cost for transfering engergy (improt/export) | -
    VC = m.ext[:parameters][:VC] # variable cost | per technology
    IC = m.ext[:parameters][:IC] # investment cost | per technology
    total = m.ext[:parameters][:totals] # Total percentage of clusterd relevant | per technology per cluster
    max_imp = m.ext[:parameters][:max_import] # max import | per country per country
    max_exp = m.ext[:parameters][:max_export] # max import | per country per country
    perc = m.ext[:parameters][:perc] # percentage from cluster assigned to country | technology per country per cluster
    max_cap_nuclear = m.ext[:parameters][:max_cap_nuclear] # max capacity nucelear | per country
    
    display("starting variables now")
    # Create variables
    cap_conv = m.ext[:variables][:capc] = @variable(m, [c=K,i=ID], lower_bound=0, base_name="capacity conventional") # Capacity must be per cluster, but also need a capacity per country
    cap_ren_Won = m.ext[:variables][:cap_r_won] = @variable(m, [z=CWon], lower_bound=0, base_name="capacity renewables wind onshore")
    cap_ren_Wof = m.ext[:variables][:cap_r_wof] = @variable(m, [z=CWof], lower_bound=0, base_name="capacity renewables wind offshore")
    cap_ren_Son = m.ext[:variables][:cap_r_son] = @variable(m, [z=CSon], lower_bound=0, base_name="capacity renewables solar onshore")
    g = m.ext[:variables][:g] = @variable(m, [c=K,i=I,jh=JH,jd=JD], lower_bound=0, base_name="generation") # Generation per country
    ens = m.ext[:variables][:ens] = @variable(m, [c=K,jh=JH,jd=JD], lower_bound=0, base_name="load_shedding")
    display("starting import and export now")
    imp = m.ext[:variables][:imp] = @variable(m,[c=K,k=K,jh=JH,jd=JD], lower_bound=0, base_name="Import")
    exp = m.ext[:variables][:exp] = @variable(m,[c=K,k=K,jh=JH,jd=JD], upper_bound=0, base_name="Export")


    # # Create affine expressions (= linear combinations of variables)
    # curt = m.ext[:expressions][:curt] = @expression(m, [i=IV,jh=JH,jd=JD],
    #     AF[i][Z][jh,jd]*cap[i] - g[i,jh,jd]
    # )

    display("formulating objective")
    # Formulate objective 1a
    m.ext[:objective] = @objective(m, Min,
        + sum(IC[i]*cap_conv[c,i] for c in K, i in ID)
        + sum(IC["On-Wind"]*cap_ren_Won[z]*total["On-Wind"][z] for z in CWon)
        + sum(IC["Off-Wind"]*cap_ren_Wof[z]*total["Off-Wind"][z] for z in CWof)
        + sum(IC["Solar"]*cap_ren_Son[z]*total["Solar"][z] for z in CSon)
        + sum(VC[i]*g[c,i,jh,jd] for c in K, i in I, jh in JH, jd in JD)
        + sum(ens[c,jh,jd]*VOLL for c in K, jh in JH, jd in JD)
        + sum(imp[c,k,jh,jd]*TRANSFER for c in K, k in K, jh in JH, jd in JD)
    )

    display("pre power balance")
    # 2a - power balance
    m.ext[:constraints][:con2a] = @constraint(m, [c=K,jh=JH,jd=JD],
    + sum(g[c,i,jh,jd] for i in I) + sum(imp[c,k,jh,jd] for k in K) + sum(exp[c,k,jh,jd] for k in K) == D[c,jh,jd] - ens[c,jh,jd]
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
    # 4a1 - Max import
    m.ext[:constraints][:con4a1] = @constraint(m, [c=K,k=K,jh=JH,jd=JD],
        imp[c,k,jh,jd] <= max_imp[c,k]
    )

    # 4a2 - Max export
    m.ext[:constraints][:con4a2] = @constraint(m, [c=K,k=K,jh=JH,jd=JD],
        -max_exp[c,k] <= exp[c,k,jh,jd]
    )

    display("improt and export done, link the two")
    # 4b - Import should equal Export other country
    m.ext[:constraints][:con4b] = @constraint(m, [c=K,k=K,jh=JH,jd=JD],
        -exp[c,k,jh,jd] == imp[k,c,jh,jd] 
    )

    display("Start max cap nuclear per country")
    # 5 - Max capacity nuclear per country
    m.ext[:constraints][:con5] = @constraint(m, [c=K],
        cap_conv[c,"Nuclear"] <= max_cap_nuclear[c]
    )

    # Build your model
    display("Start Optimization")
    # build_brownfield_1Y_GEP_model!(m)

    ## Step 4: solve
    optimize!(m)
    # check termination status
    print(
    """

    Termination status: $(termination_status(m))

    """
    )


    ## Extract solution
    display("begin data writing")
    
    str = string("Output_GEP/",method,"_",no_clusters,"_",data_used,".xlsx")
    
    # 1) Cost (objective)
    total_cost = value.(m.ext[:objective])

    # 2) Capacity
    cap_conv = value.(m.ext[:variables][:capc][:,:]);
    cap_convvec = [cap_conv[c,i] for c in K, i in ID]
    cap_res_won = value.(m.ext[:variables][:cap_r_won][:]);
    cap_res_wonvec = [cap_res_won[z] for z in CWon] 
    cap_res_wof = value.(m.ext[:variables][:cap_r_wof][:]);
    cap_res_wofvec = [cap_res_wof[z] for z in CWof] 
    cap_res_son = value.(m.ext[:variables][:cap_r_son][:]);
    cap_res_sonvec = [cap_res_son[z] for z in CSon] 

    # 3) Energy not served
    ens = value.(m.ext[:variables][:ens][:,:,:]);
    ensvec = sum(ens[c,:,:] for c in K)
    ensvec = [ensvec[jh,jd] for jh in JH, jd in JD]



    # 4) Lambda
    λ = dual.(m.ext[:constraints][:con2a][:,:,:]);
    λvec = [λ[c,jh,jd] for c in K, jh in JH, jd in JD]
    λvecmean = (sum(λvec[:,jh,jd] for jh in JH, jd in JD)/8760)
    # λvecmedian = λvec[:,12,182]
    λvecmedian = λvec[:,12,1]

    # 5) Import/Export
    imp = value.(m.ext[:variables][:imp][:,:,:,:]);
    impvec = [imp[c,k,jh,jd] for c in K, k in K, jh in JH, jd in JD]
    impvecsum = sum(impvec[:,:,jh,jd] for jh in JH, jd in JD)

    # XLSX.writetable(str, overwrite=true,
    #     Total_Cost=(collect(DataFrames.eachcol(df1)), DataFrames.names(df1)),
    #     Capacity=(collect(DataFrames.eachcol(df2)), DataFrames.names(df2)),
    #     Off_Wind=(collect(DataFrames.eachcol(df21)), DataFrames.names(df21)),
    #     On_Wind=(collect(DataFrames.eachcol(df22)), DataFrames.names(df22)),
    #     Solar=(collect(DataFrames.eachcol(df23)), DataFrames.names(df23)),
    #     Energy_Not_Served=(collect(DataFrames.eachcol(df3)), DataFrames.names(df3)),
    #     Lambda=(collect(DataFrames.eachcol(df4)), DataFrames.names(df4)),
    #     Import=(collect(DataFrames.eachcol(df5)), DataFrames.names(df5))
    # )
    XLSX.openxlsx(str, mode="w") do xf
        for sheetname in ["Capacity", "Energy Not Served", "Lambda", "Import Export"]
            XLSX.addsheet!(xf, sheetname)
        end

        # 1) Cost
        sheet1 = xf[1]
        XLSX.rename!(sheet1, "Cost")
        sheet1["A1"] = total_cost 

        # 2) Capacity
        sheet2 = xf[2]
        sheet2["B1"] = ["CCGT", "Coal", "Nuclear", "OCGT"]
        countries = ["Albania",	"Austria",	"Bosnia and Herzegovina",	"Belgium",	"Bulgaria",	"Switzerland",	"Czech Republic",	"Germany",	"Denmark",	"Estonia",	"Spain", "Finland",	"France",	"Greece",	"Croatia",	"Hungary",	"Ireland",	"Italy",	"Lithuania",	"Luxembourg",	"Latvia",	"Montenegro",	"The former Yugoslav Republic of Macedonia",	"Netherlands",	"Norway",	"Poland",	"Portugal",	"Romania",	"Serbia",	"Sweden",	"Slovenia",	"Slovakia",	"United Kingdom"]
        for i in 1:length(countries)
            sheet2[string("A",i+1)] = countries[i]
        end
        sheet2["B2"] = cap_convvec
        sheet2["G1"] = "Wind On-Shore"
        sheet2["H1"] = cap_res_wonvec
        sheet2["G2"] = "Wind Off-Shore"
        sheet2["H2"] = cap_res_wofvec
        sheet2["G3"] = "Solar"
        sheet2["H3"] = cap_res_sonvec
        
        # 3) Energy not served
        sheet3 = xf[3]
        sheet3["A1"] = ensvec
        

        # 4) Lambda
        sheet4 = xf[4]
        sheet4["B1"] = ["Albania",	"Austria",	"Bosnia and Herzegovina",	"Belgium",	"Bulgaria",	"Switzerland",	"Czech Republic",	"Germany",	"Denmark",	"Estonia",	"Spain", "Finland",	"France",	"Greece",	"Croatia",	"Hungary",	"Ireland",	"Italy",	"Lithuania",	"Luxembourg",	"Latvia",	"Montenegro",	"The former Yugoslav Republic of Macedonia",	"Netherlands",	"Norway",	"Poland",	"Portugal",	"Romania",	"Serbia",	"Sweden",	"Slovenia",	"Slovakia",	"United Kingdom"]
        sheet4["A2"] = "λ mean"
        sheet4["B2"] = λvecmean
        sheet4["A3"] = "λ median"
        sheet4["B3"] = λvecmedian

        # 5) Import/Export
        sheet5 = xf[5]
        sheet5["B1"] = ["Albania",	"Austria",	"Bosnia and Herzegovina",	"Belgium",	"Bulgaria",	"Switzerland",	"Czech Republic",	"Germany",	"Denmark",	"Estonia",	"Spain", "Finland",	"France",	"Greece",	"Croatia",	"Hungary",	"Ireland",	"Italy",	"Lithuania",	"Luxembourg",	"Latvia",	"Montenegro",	"The former Yugoslav Republic of Macedonia",	"Netherlands",	"Norway",	"Poland",	"Portugal",	"Romania",	"Serbia",	"Sweden",	"Slovenia",	"Slovakia",	"United Kingdom"]
        for i in 1:length(countries)
            sheet5[string("A",i+1)] = countries[i]
        end
        sheet5["B2"] = impvecsum
    end
    
    display("saved and done")
end 

display("start kmeans 10 af")
GEP(string("kmeans"), string("10"), string("af"))