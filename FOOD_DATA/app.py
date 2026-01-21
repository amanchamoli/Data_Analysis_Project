import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import json

st.set_page_config(page_title="Indian Cuisine Map", layout="wide")

df = pd.read_csv("indian_food_final2.csv")

df["time_category"] = pd.cut(
    df['total_time'],
    bins=[-1, 30, 60, float('inf')],
    labels=['Under 30 min', '1 hour', 'More than 1 hour']
)

region = set(df['region'])
state = set(df['state'])
diet = set(df['diet'])
time = set(df['time_category'])
flavour = set(df['flavour'])
health = set(df['health_status'])

st.sidebar.title("Welcome")

def load_overall():
    st.title("INDIAN Cuisine ")
    st.image("Map.jpg")

def load_map():
    st.title("Indian Cuisine Distribution Map")

    df_map = pd.read_csv("food_map.csv")
    df_map["state"] = df_map["state"].str.strip().str.title()

    replace_dict = {
        "Odisha": "Orissa",
        "Uttarakhand": "Uttaranchal",
        "Nct Of Delhi": "Delhi",
        "Jammu & Kashmir": "Jammu and Kashmir"
    }
    df_map["state"] = df_map["state"].replace(replace_dict)

    with open("india_states.geojson", "r", encoding="utf-8-sig") as f:
        geojson = json.load(f)

    df_map["dominance_score"] = df_map["veg_percent"] - df_map["nonveg_percent"]

    fig = px.choropleth(
        df_map,
        geojson=geojson,
        featureidkey="properties.NAME_1",
        locations="state",
        color="dominance_score",
        color_continuous_scale="RdBu",
        range_color=(df_map["dominance_score"].min(), df_map["dominance_score"].max()),
        hover_name="state",
        hover_data={
            "veg_percent": ':.1f',
            "nonveg_percent": ':.1f'
        },
    )

    fig.update_geos(
        fitbounds="locations",
        visible=True,
        resolution=110,
        projection_type="mercator"
    )

    fig.update_layout(
        margin=dict(r=0, t=40, l=0, b=0),
        coloraxis_colorbar=dict(title="Veg → Blue | Non-Veg → Red"),
        geo=dict(bgcolor='rgba(0,0,0,0)')
    )

    st.plotly_chart(fig, use_container_width=True)

def load_Region():
    Select_region = st.sidebar.selectbox('Select Region', region)
    st.write(df[df["region"] == Select_region])
    

def load_state():
    Select_state = st.sidebar.selectbox('Select State', state)
    st.write(df[df["state"] == Select_state])
     
def load_diet():
    Select_diet = st.sidebar.selectbox('Select Diet', diet)
    st.write(df[df["diet"] == Select_diet])

def load_time():
    Select_time = st.sidebar.selectbox('Select time', time)
    st.write(df[df["time_category"] == Select_time])

def load_flavour():
    Select_flavour = st.sidebar.selectbox('Select flavour', flavour)
    st.write(df[df["flavour"] == Select_flavour])
    
def load_health():
    Select_health = st.sidebar.selectbox('Select Type', ['Overall Analysis'] + sorted(list(health)))
    if Select_health != "Overall Analysis":
        st.write(df[df["health_status"] == Select_health])
    else:
        col1,col2 = st.columns(2)
        
        with col1:
            region_status = df.groupby(["region", "health_status"]).size().unstack()

            fig, ax = plt.subplots()
            region_status.plot(kind="bar", ax=ax)

            ax.set_xlabel("Region")
            ax.set_ylabel("Number of Dishes")
            ax.set_title("Region vs Health Status")

            st.pyplot(fig)
        with col2:
            flavour_health = df.groupby(["flavour", "health_status"]).size().unstack()

            fig, ax = plt.subplots()
            flavour_health.plot(kind="bar", ax=ax)

            ax.set_title("Flavour vs Health Status")
            ax.set_xlabel("Flavour")
            ax.set_ylabel("Number of Dishes")

            st.pyplot(fig)
            
        col3,col4 = st.columns(2)
        
        with col3:
            region_status = df.groupby(["dish_type", "health_status"]).size().unstack()


            fig, ax = plt.subplots()
            region_status.plot(kind="bar", ax=ax)

            ax.set_title("Dish type vs Health Status")
            ax.set_xlabel("Dish Type")
            ax.set_ylabel("Number of Dishes")

            st.pyplot(fig)
        with col4:
            diet_status = df.groupby(["diet", "health_status"]).size().unstack()

            fig, ax = plt.subplots()
            diet_status.plot(kind="bar", ax=ax)

            ax.set_xlabel("Diet Type")
            ax.set_ylabel("Number of Dishes")
            ax.set_title("Diet vs Health Status")    

            st.pyplot(fig)



def load_comptime():
    st.subheader("Compare Cooking Time Between Two Dishes")

    dish1 = st.text_input("Enter name of First Dish")
    dish2 = st.text_input("Enter name of Second Dish")
    
    if st.button("Compare"):
        if dish1 in df["name"].values and dish2 in df["name"].values:
            d1 = df.loc[df["name"] == dish1, "total_time"].iloc[0]
            d2 = df.loc[df["name"] == dish2, "total_time"].iloc[0]

            st.write(f"**{dish1}:** {d1} minutes")
            st.write(f"**{dish2}:** {d2} minutes")

            if d1 < d2:
                st.success(f"{dish1} is faster to cook")
            elif d2 < d1:
                st.success(f"{dish2} is faster to cook")
            else:
                st.info("Both dishes take the same time")
        else:
            st.error("One or both dish names were not found in the dataset.")

def load_comppro():
    st.subheader("Check if a Dish is Healthy")

    dish = st.text_input("Enter dish name", key="dish1")

    if st.button("Check health", key="btn1"):
        if dish in df["name"].values:
            status = df.loc[df["name"] == dish, "health_status"].iloc[0]

            if status == "Healthy":
                st.success(status)
            elif status == "Unhealthy":
                st.error(status)
            else:
                st.info(status)
        else:
            st.error("Dish name was not found in the dataset.")


    st.subheader("Compare Health Score of Two Dishes")

    dish3 = st.text_input("First dish", key="dish3")
    dish4 = st.text_input("Second dish", key="dish4")

    if st.button("Compare health score", key="btn2"):
        if dish3 in df["name"].values and dish4 in df["name"].values:
            d3 = df.loc[df["name"] == dish3, "health_score"].iloc[0]
            d4 = df.loc[df["name"] == dish4, "health_score"].iloc[0]

            if d3 > d4:
                st.success(f"{dish3} is more healthy")
            elif d4 > d3:
                st.success(f"{dish4} is more healthy")
            else:
                st.info("Both dishes have the same health score")
        else:
            st.error("One or both dish names were not found in the dataset.")

        

step = st.sidebar.selectbox('Select One', ['Overall', 'Indivisual', 'Comparision','Map Distripution'])

if step == "Overall":
    load_overall()

elif step == "Indivisual":
    option = st.sidebar.selectbox('Select One', ['Region', 'State', 'Diet', 'Time', 'Flavour','Health'])

    if option == "Region":
        load_Region()
    elif option == "State":
        load_state()
    elif option == "Diet":
        load_diet()
    elif option == "Time":
        load_time()
    elif option == "Flavour":
        load_flavour()
    else:
        load_health()

elif step == "Comparision":
    comparison = st.sidebar.selectbox('Select Comparison Factor', ['Time', 'Health'])
    
    if comparison == "Time":
        load_comptime()
    else:
        load_comppro()
        
else:
    load_map()
