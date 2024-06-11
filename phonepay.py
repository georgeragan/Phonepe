import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px
import requests
import json

#Dataframecreatiion

#sql connection
mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data", 
                      password="Sravan@1234")
cursor=mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurance_df=pd.DataFrame(table1,columns=("States","Years","Quater","Transaction_Type","Transaction_count","Transaction_amount"))

#sql connection

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data", 
                      password="Sravan@1234")
cursor=mydb.cursor()

#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggre_transaction_df=pd.DataFrame(table2,columns=("States","Years","Quater","Transaction_Type","Transaction_count","Transaction_amount"))

#sql connection

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data", 
                      password="Sravan@1234")
cursor=mydb.cursor()

#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States","Years","Quater","Brands","Transaction_count","Percentage"))

#sql connection

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data", 
                      password="Sravan@1234")
cursor=mydb.cursor()

#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

map_insurance_df=pd.DataFrame(table4,columns=("States","Years","Quater","District","Transaction_count","Transaction_amount"))


#sql connection

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data", 
                      password="Sravan@1234")
cursor=mydb.cursor()

#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

map_transaction_df=pd.DataFrame(table5,columns=("States","Years","Quater","Transaction_Type","Transaction_count","Transaction_amount"))

#sql connection

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data", 
                      password="Sravan@1234")
cursor=mydb.cursor()

#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

map_user_df=pd.DataFrame(table6,columns=("States","Years","Quater","Disctrict","RegisteredUser","AppOpens"))


#sql connection

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data", 
                      password="Sravan@1234")
cursor=mydb.cursor()

#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

Top_insurance_df=pd.DataFrame(table7,columns=("States","Years","Quater","Pincodes","Transaction_count","Transaction_amount"))


#sql connection

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data", 
                      password="Sravan@1234")
cursor=mydb.cursor()

#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

Top_transaction_df=pd.DataFrame(table8,columns=("States","Years","Quater","Pincodes","Transaction_count","Transaction_amount"))


#sql connection

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data", 
                      password="Sravan@1234")
cursor=mydb.cursor()

#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

Top_user_df=pd.DataFrame(table9,columns=("States","Years","Quater","Pincodes","RegisteredUsers"))

# Transaction_Year_Based

def Transaction_amount_count_Y(df,year):
    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:


        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Agsunset_r,height=650,width=600)

        st.plotly_chart(fig_amount)
    
    with col2:

        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.amp_r,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
        fig_india_1=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

#Transaction_Quater_Base

def Transaction_amount_count_Y_Q(df,quater):
    tacy=df[df["Quater"]==quater]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:


        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{tacy['Years'].unique()} YEAR {quater} QUATER TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_amount)
    with col2:


        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{tacy['Years'].unique()} YEAR {quater} QUATER TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.amp_r)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
        fig_india_1=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States",title=f"{tacy['Years'].unique()} YEAR {quater} QUATER TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States",title=f"{tacy['Years'].unique()} YEAR {quater} QUATER TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

#Transaction_type

def Aggre_Tran_Transaction_type(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Transaction_Type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_pie_1=px.pie(data_frame=tacyg,names="Transaction_Type",values="Transaction_amount",
                        width=600,title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.5)
        
        st.plotly_chart(fig_pie_1)
    
    with col2:

        fig_pie_2=px.pie(data_frame=tacyg,names="Transaction_Type",values="Transaction_count",
                        width=600,title=f"{state.upper()} TRANSACTION COUNT",hole=0.5)
        
        st.plotly_chart(fig_pie_2)

#Aggre_User_analysis_1

def Aggre_user_plot(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True,inplace= True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)
    fig_bar_1=px.bar(aguyg,x="Brands",y="Transaction_count",title=f"{year}BRANDS AND TRANSACTION COUNT",width=800,
                     color_discrete_sequence=px.colors.sequential.haline_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    return aguy

#Aggre_user_Analysis_2
def Aggre_user_plot2(df,quater):
    aguyq=df[df["Quater"]==quater]
    aguyq.reset_index(drop=True,inplace= True)
    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)
    fig_bar_2=px.bar(aguyqg,x="Brands",y="Transaction_count",title=f"{quater} QUATER, BRANDS AND TRANSACTION COUNT",width=800,
                        color_discrete_sequence=px.colors.sequential.haline_r,hover_name="Brands")
    st.plotly_chart(fig_bar_2)

    return aguyq

#Aggre_user_alalysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers= True)
    st.plotly_chart(fig_line_1)


#Map_insurance_district
def Map_insur_District(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "District", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(tacyg, x= "Transaction_count", y= "District", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

# map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{year} REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

# map_user_plot_2
def map_user_plot_2(df, quater):
    muyq= df[df["Quater"]== quater]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{df['Years'].min()} YEARS {quater} QUARTER REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUser", y= "District", orientation= "h",
                                title= f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:

        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "District", orientation= "h",
                                title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

# top_insurance_plot_1
def Top_insurance_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quater", y= "Transaction_amount", hover_data= "Pincodes",
                                title= "TRANSACTION AMOUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2= px.bar(tiy, x= "Quater", y= "Transaction_count", hover_data= "Pincodes",
                                title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)

def top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States", "Quater"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quater", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


# top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_pot_2= px.bar(tuys, x= "Quater", y= "RegisteredUsers", title= "REGISTEREDUSERS, PINCODES, QUARTER",
                        width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_top_pot_2)


#sql connection

def top_chart_transaction_amount(table_name):

    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data", 
                        password="Sravan@1234")
    cursor=mydb.cursor()

    #PLOT_1

    query1=f'''SELECT states,SUM(transaction_amount) as transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount desc
                limit 10''' 

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=("states","transaction_amount"))

    col1,col2=st.columns()
    with col1:

        fig_amount1=px.bar(df_1,x="states",y="transaction_amount",title="TRANSACTION AMOUNT",hover_name="states",color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_amount1)

    #PLOT_2

    query2=f'''SELECT states,SUM(transaction_amount) as transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount 
                limit 10''' 

    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=("states","transaction_amount"))

    
    with col2:

        fig_amount2=px.bar(df_2,x="states",y="transaction_amount",title="TRANSACTION AMOUNT",hover_name="states",color_discrete_sequence=px.colors.sequential.Blackbody_r)
        st.plotly_chart(fig_amount2)

    #PLOT_3

    query3=f'''SELECT states,AVG(transaction_amount) as transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount 
                ''' 

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=("states","transaction_amount"))
    fig_amount3=px.bar(df_3,x="transaction_amount",y="states",title="TRANSACTION AMOUNT",hover_name="states",orientation="h",color_discrete_sequence=px.colors.sequential.Jet_r)
    st.plotly_chart(fig_amount3)


#sql connection

def top_chart_transaction_count(table_name):

    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data", 
                        password="Sravan@1234")
    cursor=mydb.cursor()

    #PLOT_1

    query1=f'''SELECT states,SUM(transaction_count) as transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count desc
                limit 10''' 

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=("states","transaction_count"))

    col1,col2=st.columns()
    with col1:

        fig_amount=px.bar(df_1,x="states",y="transaction_count",title="TRANSACTION COUNT",hover_name="states",color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_amount)

    #PLOT_2

    query2=f'''SELECT states,SUM(transaction_count) as transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count 
                limit 10''' 

    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=("states","transaction_count"))
    with col2:

        fig_amount=px.bar(df_2,x="states",y="transaction_count",title="TRANSACTION COUNT",hover_name="states",color_discrete_sequence=px.colors.sequential.Blackbody_r)
        st.plotly_chart(fig_amount)

    #PLOT_3

    query3=f'''SELECT states,AVG(transaction_count) as transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count 
                ''' 

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=("states","transaction_count"))

    fig_amount=px.bar(df_3,x="transaction_count",y="states",title="TRANSACTION COUNT",hover_name="states",orientation="h",color_discrete_sequence=px.colors.sequential.Jet_r)
    st.plotly_chart(fig_amount)



#Streamlit Part

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALISATION AND EXPLORATION")

with st.sidebar:
    select =option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":
    pass
elif select=="DATA EXPLORATION":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:
        method=st.radio("Select the Method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method=="Insurance Analysis":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_insurance_df["Years"].min(),Aggre_insurance_df["Years"].max(),Aggre_insurance_df["Years"].min())
            tac_Y=Transaction_amount_count_Y(Aggre_insurance_df,years)

            col1,col2=st.columns(2)
            with col1:
                quaters=st.slider("Select The Quater",tac_Y["Quater"].min(),tac_Y["Quater"].max(),tac_Y["Quater"].min())
            Transaction_amount_count_Y_Q(tac_Y,quaters)


        elif method=="Transaction Analysis":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_transaction_df["Years"].min(),Aggre_transaction_df["Years"].max(),Aggre_transaction_df["Years"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction_df,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Aggre_tran_tac_Y["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quaters=st.slider("Select The Quater",Aggre_tran_tac_Y["Quater"].min(),Aggre_tran_tac_Y["Quater"].max(),Aggre_tran_tac_Y["Quater"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quaters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State_Ty",Aggre_tran_tac_Y["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states)


        elif method=="User Analysis":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot(Aggre_user,years)

            col1,col2=st.columns(2)
            with col1:
                quaters=st.slider("Select The Quater",Aggre_user_Y["Quater"].min(),Aggre_user_Y["Quater"].max(),Aggre_user_Y["Quater"].min())
            Aggre_user_Y_Q=Aggre_user_plot2(Aggre_user_Y,quaters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)

    with tab2:
        method_2=st.radio("Select the Method",["Map_Insurance","Map_Transaction","Map_User"])
        
        if method_2 == "Map Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mi",map_insurance_df["Years"].min(), map_insurance_df["Years"].max(),map_insurance_df["Years"].min())
            map_insur_tac_Y= Transaction_amount_count_Y(map_insurance_df, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", map_insur_tac_Y["States"].unique())

            Map_insur_District(map_insur_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quaters= st.slider("Select The Quater_mi",map_insur_tac_Y["Quater"].min(), map_insur_tac_Y["Quater"].max(),map_insur_tac_Y["Quater"].min())
            map_insur_tac_Y_Q= Transaction_amount_count_Y_Q(map_insur_tac_Y, quaters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_Ty", map_insur_tac_Y_Q["States"].unique())

            Map_insur_District(map_insur_tac_Y_Q, states)

        elif method_2 == "Map Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",map_transaction_df["Years"].min(), map_transaction_df["Years"].max(),map_transaction_df["Years"].min())
            map_tran_tac_Y= Transaction_amount_count_Y(map_transaction_df, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", map_tran_tac_Y["States"].unique())

            Map_insur_District(map_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quaters= st.slider("Select The Quater_mt",map_tran_tac_Y["Quater"].min(), map_tran_tac_Y["Quater"].max(),map_tran_tac_Y["Quater"].min())
            map_tran_tac_Y_Q= Transaction_amount_count_Y_Q(map_tran_tac_Y, quaters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_Ty", map_tran_tac_Y_Q["States"].unique())

            Map_insur_District(map_tran_tac_Y_Q, states)


        elif method_2 == "Map User":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mu",map_user_df["Years"].min(), map_user_df["Years"].max(),map_user_df["Years"].min())
            map_user_Y= map_user_plot_1(map_user_df, years)

            col1,col2= st.columns(2)
            with col1:

                quaters= st.slider("Select The Quater_mu",map_user_Y["Quater"].min(), map_user_Y["Quater"].max(),map_user_Y["Quater"].min())
            map_user_Y_Q= map_user_plot_2(map_user_Y, quaters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mu", map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q, states)


    with tab3:
        method_3=st.radio("Select the Method",["Top_Insurance","Top_Transaction","Top_User"])

        if method_3 == "Top Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_ti",Top_insurance_df["Years"].min(), Top_insurance_df["Years"].max(),Top_insurance_df["Years"].min())
            top_insur_tac_Y= Transaction_amount_count_Y(Top_insurance_df, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_ti", top_insur_tac_Y["States"].unique())

            Top_insurance_plot_1(top_insur_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quaters= st.slider("Select The Quater_mu",top_insur_tac_Y["Quater"].min(), top_insur_tac_Y["Quater"].max(),top_insur_tac_Y["Quater"].min())
            top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(top_insur_tac_Y, quaters)

            

        elif method_3 == "Top Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tt",Top_transaction_df["Years"].min(), Top_transaction_df["Years"].max(),Top_transaction_df["Years"].min())
            top_tran_tac_Y= Transaction_amount_count_Y(Top_transaction_df, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tt", top_tran_tac_Y["States"].unique())

            Top_insurance_plot_1(top_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quaters= st.slider("Select The Quater_tt",top_tran_tac_Y["Quater"].min(), top_tran_tac_Y["Quater"].max(),top_tran_tac_Y["Quater"].min())
            top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(top_tran_tac_Y, quaters)


        elif method_3 == "Top User":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tu",Top_user_df["Years"].min(), Top_user_df["Years"].max(),Top_user_df["Years"].min())
            top_user_Y= top_user_plot_1(Top_user_df, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tu", top_user_Y["States"].unique())

            top_user_plot_2(top_user_Y, states)

    

elif select=="TOP_CHARTS":
    question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Registered users of Top User",
                                                    ])

    if question=="1. Transaction Amount and Count of Aggregated Insurance":
        top_chart_transaction_amount("aggregated_insurance")
