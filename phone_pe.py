import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px
import requests
import json


#data frame creation
mydb = psycopg2.connect(host="localhost",
                    user="postgres",
                    password="jainthiyuva",
                    database= "phonepe_data",
                    port=5432
                    )
mycursor = mydb.cursor()
#aggregated insurance
mycursor.execute("select * from aggregated_insurance")
mydb.commit()
table1=mycursor.fetchall()

Aggregated_insurance=pd.DataFrame(table1,columns=("States","Year","Quarter","Transaction_Type","Transaction_Count","Transaction_Amount"))

#aggregated transaction
mycursor.execute("select * from aggregated_transaction")
mydb.commit()
table2=mycursor.fetchall()

Aggregated_transation=pd.DataFrame(table2,columns=("States","Year","Quarter","Transaction_Type","Transaction_Count","Transaction_Amount"))

#aggregated user
mycursor.execute("select * from aggregated_user")
mydb.commit()
table3=mycursor.fetchall()

Aggregated_user=pd.DataFrame(table3,columns=("States","Year","Quarter","Brands","Transaction_Count","Transaction_Percent"))

#map insurance
mycursor.execute("select * from map_insurance")
mydb.commit()
table4=mycursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns=("States","Year","Quarter","Transaction_Type","Transaction_Count","Transaction_Amount"))

#map transaction
mycursor.execute("select * from map_transaction")
mydb.commit()
table5=mycursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns=("States","Year","Quarter","Districts","Transaction_Count","Transaction_Amount"))

#map user
mycursor.execute("select * from map_user")
mydb.commit()
table6=mycursor.fetchall()

Map_user=pd.DataFrame(table6,columns=("States","Year","Quarter","Districts","Registered_User","Appopens"))

#top insurance
mycursor.execute("select * from top_insurance")
mydb.commit()
table7=mycursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns=("States","Year","Quarter","Pincodes","Transaction_Count","Transaction_Amount"))

#top transaction
mycursor.execute("select * from top_transaction")
mydb.commit()
table8=mycursor.fetchall()

Top_transaction=pd.DataFrame(table8,columns=("States","Year","Quarter","Pincodes","Transaction_Count","Transaction_Amount"))

#top user
mycursor.execute("select * from top_user")
mydb.commit()
table9=mycursor.fetchall()

Top_user=pd.DataFrame(table9,columns=("States","Year","Quarter","Pincodes","Registered_User"))

def Transaction_amount_count_Y(df, year):
    tacy=df[df["Year"] == year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg, x="States", y="Transaction_Amount", title=f"{year} TRANSACTION AMOUT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(tacyg, x="States", y="Transaction_Count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_count)

    #geo visualization 
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append((feature["properties"]["ST_NM"]))
    states_name.sort()
    col1,col2=st.columns(2)
    with col1:
        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM", color="Transaction_Amount", 
                                color_continuous_scale="twilight", 
                                range_color=(tacyg["Transaction_Amount"].min(), tacyg["Transaction_Amount"].max()),
                                    hover_name="States", title=f"{year} TRANSACTION AMOUNT", 
                                    fitbounds="locations", height=600, width=600  )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM", color="Transaction_Count",
                                color_continuous_scale="Rainbow", 
                                range_color=(tacyg["Transaction_Count"].min(), tacyg["Transaction_Count"].max()),
                                    hover_name="States", title=f"{year} TRANSACTION COUNT", 
                                    fitbounds="locations", height=600, width=600  )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df, quarter):
    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg, x="States", y="Transaction_Amount", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(tacyg, x="States", y="Transaction_Count", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_count)

def Aggre_Tran_Transaction_type(df, state):
    tacy=df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("Transaction_Type")[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.pie(data_frame=tacyg, names="Transaction_Type", values="Transaction_Amount",
                            width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
        st.plotly_chart(fig_amount_1)
    
    with col2:
        fig_count_1=px.pie(data_frame=tacyg, names="Transaction_Type", values="Transaction_Count",
                            width=600, title=f"{state.upper()} TRANSACTION COUNT", hole=0.5)
        st.plotly_chart(fig_count_1)

def Aggre_Tran_Transaction_amount_count_Y_Q(df, quarter):
    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    
    with col1:
        fig_amount=px.bar(tacyg, x="States", y="Transaction_Amount", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUT", height=650, width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(tacyg, x="States", y="Transaction_Count", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", height=650, width=600)
        st.plotly_chart(fig_count)
    return tacy

def Aggre_user_plot_1(df,year):
    aguy=df[df["Year"]==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_Count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg, x="Brands", y="Transaction_Count", title=f"{year} TRANSACTION COUNT WITH BRANDS", width=550,
                     color_discrete_sequence=px.colors.sequential.Agsunset_r,
                     hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

def Aggre_user_plot_2(df, quarter):
    aguy=df[df["Quarter"] == quarter]
    aguy.reset_index(drop=True, inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_Count"].sum())
    aguyg.reset_index(inplace=True)

    fig_count=px.line(aguyg, x="Brands", y="Transaction_Count", title=f"{aguy['Year'].min()} YEAR {quarter}  QUARTER TRANSACTION COUNT", markers=True, width=500)
    st.plotly_chart(fig_count)

def Aggre_user_plot_3(df,year):
    aguy=df[df["Year"]==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_Percent"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_3=px.bar(aguyg, x="Brands", y="Transaction_Percent", title="TRANSACTION PERCENT WITH BRANDS", width= 550,
                     color_discrete_sequence=px.colors.sequential.Bluered)
    st.plotly_chart(fig_bar_3)
    return aguy

def Aggre_user_plot_4(df,quarter):
    aguy=df[df["Quarter"] == quarter]    
    aguy.reset_index(drop=True, inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_Percent"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_4=px.line(aguyg, x="Brands", y="Transaction_Percent", title="QUARTER TRANSACTION PERCENT WITH BRANDS", width= 500, markers=True)
    st.plotly_chart(fig_bar_4)
    return aguy

def map_trans_district(df, state):
    tacy=df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("Districts")[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace=True)

    fig_amount_1=px.bar(tacyg, x="Transaction_Amount", y="Districts", orientation="h",
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", 
                        color_discrete_sequence=px.colors.sequential.Magenta)
    fig_amount_1.show()

    fig_count_1=px.bar(tacyg, x="Transaction_Count", y="Districts", orientation="h",
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT", 
                        color_discrete_sequence=px.colors.sequential.Darkmint)
    fig_count_1.show()

def Map_insur_Transaction_amount_count_Y_Q(df, quarter):
    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    
    with col1:
        fig_amount=px.bar(tacyg, x="States", y="Transaction_Amount", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUT",
                          height=600,width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(tacyg, x="States", y="Transaction_Count", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                         height=600,width=600)
        st.plotly_chart(fig_count)
    return tacy

def Map_User_plot_1(df, year):

    muy=df[df["Year"]==year]
    muy.reset_index(drop=True, inplace=True)

    muyg=muy.groupby("States")[["Registered_User","Appopens"] ].sum()
    muyg.reset_index(inplace=True)

    fig_state_1=px.line(muyg, x="States", y=["Registered_User","Appopens"],
                        title=f"{year} REGISTERED USER WITH APOPENS", markers=True, width=800, height=600)
    st.plotly_chart(fig_state_1)
    return muy

def Map_User_plot_2(df, quarter):

    muy=df[df["Quarter"]==quarter]
    muy.reset_index(drop=True, inplace=True)

    muyg=muy.groupby("States")[["Registered_User","Appopens"] ].sum()
    muyg.reset_index(inplace=True)

    fig_quarter_1=px.line(muyg, x="States", y=["Registered_User","Appopens"],
                        title=f"{quarter} QUARTER REGISTERED USER WITH APOPENS", markers=True, width=800, height=600,
                        color_discrete_sequence=px.colors.sequential.Pinkyl_r)
    st.plotly_chart(fig_quarter_1)
    return muy

def Map_User_plot_3(df,states):
    muys=df[df["States"]==states]
    muys.reset_index(drop=True, inplace=True)

    fig_map_user_bar_1=px.bar(muys, x="Registered_User",color="Appopens", y="Districts", orientation="h",
                            title=f"{states.upper()} REGISTERED USER", height=800, color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_map_user_bar_1)

def Top_insur_plot_2(df, state):
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_top_ins_plot=px.bar(tiy, x="Quarter", y="Transaction_Amount", title="TRANSACTION AMOUNT", height=600,width=500,
                                color_discrete_sequence=px.colors.sequential.YlOrRd, hover_data="Pincodes")
        st.plotly_chart(fig_top_ins_plot)
    with col2:
        fig_top_ins_plot_1=px.bar(tiy, x="Quarter", y="Transaction_Count", title="TRANSACTION COUNT", height=600, width=500,
                                color_discrete_sequence=px.colors.sequential.Rainbow, hover_data="Pincodes")
        st.plotly_chart(fig_top_ins_plot_1)

def top_user_plot_1(df, year):
    tuy=df[df["Year"] == year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States", "Quarter"])["Registered_User"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuyg, x="States", y="Registered_User", color="Quarter",width=800, height=600,
                        color_discrete_sequence=px.colors.sequential.Burgyl, hover_name="States", title=f"{year} REGISTERED USER")
    st.plotly_chart(fig_top_plot_1)
    return tuy

def top_user_plot_2(df, state):
    tuys=df[df["States"] == state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_1=px.bar(tuys, x="Quarter", y="Registered_User", color="Registered_User",width=800, height=600,
                        color_continuous_scale=px.colors.sequential.Magenta, hover_name="Pincodes", title=f"{state} PINCODE WITH REGISTERED USER")
    st.plotly_chart(fig_top_plot_1)

def ques1():
    brand=Aggregated_user[["Brands","Transaction_Count"]]
    brand1=brand.groupby("Brands")["Transaction_Count"].sum().sort_values(ascending=False)
    brand2=pd.DataFrame(brand1).reset_index()

    fig_brands=px.pie(brand2, values="Transaction_Count", names="Brands",title="Top Mobile Brands of Transaction_Count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt=Aggregated_transation[["States","Transaction_Amount"]]
    lt1=lt.groupby("States")["Transaction_Amount"].sum().sort_values(ascending=True)
    lt2=pd.DataFrame(lt1).reset_index().head(10)

    fig_lts=px.bar(lt2, x="States", y="Transaction_Amount", title="STATES WITH LOWER TRANSACTION AMOUNT",
                color_discrete_sequence=px.colors.sequential.YlOrBr)
    return st.plotly_chart(fig_lts)

def ques3():
    ht=Map_transaction[["Districts","Transaction_Amount"]]
    ht1=ht.groupby("Districts")["Transaction_Amount"].sum().sort_values(ascending=False)
    ht2=pd.DataFrame(ht1).reset_index().head(10)

    fig_hts=px.bar(ht2, x="Districts", y="Transaction_Amount", title="DISTRICTS WITH HIGHER TRANSACTION AMOUNT",
                color_discrete_sequence=px.colors.sequential.Pinkyl_r)
    return st.plotly_chart(fig_hts)

def ques4():
    htd= Map_transaction[["Districts", "Transaction_Amount"]]
    htd1= htd.groupby("Districts")["Transaction_Amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_Amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)

def ques5():
    sa= Map_user[["States", "Appopens"]]
    sa1= sa.groupby("States")["Appopens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "Appopens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_user[["States", "Appopens"]]
    sa1= sa.groupby("States")["Appopens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "Appopens", title="Lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggregated_transation[["Transaction_Type", "Transaction_Count"]]
    stc1= stc.groupby("Transaction_Type")["Transaction_Count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "Transaction_Type", y= "Transaction_Count", title= "TRANSACTION TYPE WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggregated_transation[["States", "Transaction_Count"]]
    stc1= stc.groupby("States")["Transaction_Count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index().head(20)

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_Count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Aggregated_transation[["States", "Transaction_Amount"]]
    ht1= ht.groupby("States")["Transaction_Amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_Amount",title= "STATES WITH HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    hru= Top_user[["States", "Registered_User"]]
    hru1= hru.groupby("States")["Registered_User"].sum().sort_values(ascending= False)
    hru2= pd.DataFrame(hru1).reset_index().head(10)

    fig_lts= px.bar(hru2, x= "States", y= "Registered_User",title= "STATES WITH HIGHEST REGISTERED USERS",
                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
    return st.plotly_chart(fig_lts)
#streamlit part

#page congiguration
st.set_page_config(layout="wide")
st.title("PHONEPE PULSE DATA VISUALIZATION")

st.sidebar.header(":wave: :red[**Hello! Welcome to the dashboard**]")
with st.sidebar:
    selected = option_menu("Menu", ["Home","Explore Data","Top Charts","About"])
                
if selected == "Home":
    st.markdown("# :red[Data Visualization and Exploration]")
    st.markdown("## :red[A User-Friendly Tool Using Streamlit and Plotly]")
    st.write(" ")
    st.write(" ")
    st.markdown("#### :red[Domain :] Fintech")
    st.markdown("##### :red[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
    st.markdown("###### :red[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
   
elif selected == "Explore Data":
    tab1, tab2, tab3= st.tabs(["AGGREGATED ANALYSIS","MAP ANALYSIS","TOP ANALYSIS"])
    #component1=  TabBar(tabs=["Aggregated Analysis","Map Analysis","Top Analysis"],default=0,background = "white",color="black",activeColor="violet",fontSize="20px")
    with tab1:
        method=st.radio("SELECT THE METHOD",["Aggregated Insurance", "Aggregated Transaction", "Aggregated User"])
        if method=="Aggregated Insurance":

            col1,col2= st.columns(2)

            with col1:
                years=st.slider("Select the year",Aggregated_insurance["Year"].min(),Aggregated_insurance["Year"].max(), Aggregated_insurance["Year"].min() )
            tac_Y= Transaction_amount_count_Y(Aggregated_insurance, years)
           
            col1,col2=st.columns(2)
            
            with col1:
                quarters=st.slider("Select the quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(), tac_Y["Quarter"].min() )
            Transaction_amount_count_Y_Q(tac_Y, quarters)
        
        elif method== "Aggregated Transaction":
            col1,col2= st.columns(2)

            with col1:
                years=st.slider("Select the year",Aggregated_transation["Year"].min(),Aggregated_transation["Year"].max(), Aggregated_transation["Year"].min() )
            Aggre_trans_tac_Y= Transaction_amount_count_Y(Aggregated_transation, years)
            
            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("Select the states", Aggre_trans_tac_Y["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_trans_tac_Y, states)

            col1,col2= st.columns(2)

            with col1:
                quarters=st.slider("Select the quarter",Aggre_trans_tac_Y["Quarter"].min(),Aggre_trans_tac_Y["Quarter"].max(), Aggre_trans_tac_Y["Quarter"].min() )
            Aggre_tran_tac_Y_Q=Aggre_Tran_Transaction_amount_count_Y_Q(Aggre_trans_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("Select the states for quarter", Aggre_tran_tac_Y_Q["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)


        elif method== "Aggregated User":
            col1,col2= st.columns(2)
            with col1:
                years=st.slider("Select the year",Aggregated_user["Year"].min(),Aggregated_user["Year"].max(), Aggregated_user["Year"].min() )
                Aggre_user_Y= Aggre_user_plot_1(Aggregated_user, years)
           
            with col2:
                quarters=st.slider("Select the quarter_count",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min() )
                Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                years=st.slider("Select the year_percent",Aggregated_user["Year"].min(),Aggregated_user["Year"].max(), Aggregated_user["Year"].min() )
                Aggre_user_Y_TP= Aggre_user_plot_3(Aggregated_user, years)
            with col2:
                quarters=st.slider("Select the quarter_percent",Aggre_user_Y_TP["Quarter"].min(),Aggre_user_Y_TP["Quarter"].max(), Aggre_user_Y_TP["Quarter"].min() )
                Aggre_user_plot_4(Aggre_user_Y_TP, quarters)
    
    with tab2:
        method2=st.radio("SELECT THE METHOD",["Map Insurance", "Map Transaction", "Map User"])
        if method2=="Map Insurance":
            col1,col2= st.columns(2)

            with col1:
                years=st.slider("Select the year for map_insurance", Map_insurance["Year"].min(), Map_insurance["Year"].max(), Map_insurance["Year"].min() )
            map_insur_plot_1= Transaction_amount_count_Y(Map_insurance, years)
                       
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the quarter for map insurance", map_insur_plot_1["Quarter"].min(), map_insur_plot_1["Quarter"].max(), map_insur_plot_1["Quarter"].min() )
            map_insur_plot_3=Map_insur_Transaction_amount_count_Y_Q(map_insur_plot_1, quarters)
            

        elif method2== "Map Transaction":
            col1,col2= st.columns(2)

            with col1:
                years=st.slider("Select the year for map_transaction", Map_transaction["Year"].min(), Map_insurance["Year"].max(), Map_insurance["Year"].min() )
            map_trans_plot_1= Transaction_amount_count_Y(Map_transaction, years)
                       
            col1,col2= st.columns(2)

            with col1:
                states=st.selectbox("Select the statesfor map_transaction", map_trans_plot_1["States"].unique())
            map_trans_plot_2= map_trans_district(map_trans_plot_1, states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the quarter for map_transaction", map_trans_plot_1["Quarter"].min(), map_trans_plot_1["Quarter"].max(), map_trans_plot_1["Quarter"].min() )
            map_trans_plot_3=Map_insur_Transaction_amount_count_Y_Q(map_trans_plot_1, quarters)
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states for map_transaction", map_trans_plot_3["States"].unique())
            map_trans_district(map_trans_plot_3, states)

        elif method2== "Map User":
            col1,col2= st.columns(2)

            with col1:
                years=st.slider("Select the year for map_user", Map_user["Year"].min(), Map_user["Year"].max(), Map_user["Year"].min() )
            map_user_Y=Map_User_plot_1(Map_user, years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the quarter for map_user", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(), map_user_Y["Quarter"].min() )
            Map_user_Y_Q= Map_User_plot_2(map_user_Y, quarters)

            col1,col2= st.columns(2)

            with col1:
                states=st.selectbox("Select the statesfor map_user", Map_user_Y_Q["States"].unique())
            Map_User_plot_3(Map_user_Y_Q, states)
    with tab3:
        method3=st.radio("SELECT THE METHOD",["Top Insurance", "Top Transaction", "Top User"])
        if method3=="Top Insurance":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select the year for top_insurance", Top_insurance["Year"].min(), Top_insurance["Year"].max(), Top_insurance["Year"].min() )
            Top_insur_plot_1=Transaction_amount_count_Y(Top_insurance, years)
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states for top_insurance", Top_insur_plot_1["States"].unique())
            Top_insur_plot_2(Top_insur_plot_1, states)
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the quarter for top_insurance", Top_insur_plot_1["Quarter"].min(), Top_insur_plot_1["Quarter"].max(), Top_insur_plot_1["Quarter"].min() )
            Map_insur_Transaction_amount_count_Y_Q(Top_insur_plot_1, quarters)

        elif method3== "Top Transaction":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select the year for top_transaction", Top_transaction["Year"].min(), Top_transaction["Year"].max(), Top_transaction["Year"].min() )
            Top_trans_plot_1=Transaction_amount_count_Y(Top_transaction, years)
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states for top_transaction", Top_trans_plot_1["States"].unique())
            Top_insur_plot_2(Top_trans_plot_1, states)
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the quarter for top_transaction", Top_trans_plot_1["Quarter"].min(), Top_trans_plot_1["Quarter"].max(), Top_trans_plot_1["Quarter"].min() )
            Map_insur_Transaction_amount_count_Y_Q(Top_trans_plot_1, quarters)
        elif method3== "Top User":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select the year for top_user", Top_user["Year"].min(), Top_user["Year"].max(), Top_user["Year"].min())
            Top_user_Y=top_user_plot_1(Top_user, years)
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states for top user", Top_user_Y["States"].unique())
            top_user_plot_2(Top_user_Y, states)

elif selected == "Top Charts":
    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','Least Transaction Count with Transaction Type',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top States with Highest Registered Users'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="Least Transaction Count with Transaction Type":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top States with Highest Registered Users":
        ques10()
    
elif selected == "About":
    st.header("PHONEPE")
    st.subheader("INDIA'S BEST TRANSACTION APP")
    st.markdown("PhonePe  is an Indian digital payments and financial technology company")
    st.write("****FEATURES****")
    st.write("****Credit & Debit card linking****")
    st.write("****Bank Balance check****")
    st.write("****Money Storage****")
    st.write("****PIN Authorization****")
    st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    col1,col2=st.columns(2)
    with col1:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")
    with col2:
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")
