import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import json
from PIL import Image

st.set_page_config(page_title="Indian Cuisine Map", layout="wide", page_icon="🍛")

@st.cache_data
def load_data():
    df = pd.read_csv("D:/CampusX/Project-World/food_Analysis/Data/indian_food_final2.csv")
    df["time_category"] = pd.cut(
        df['total_time'],
        bins=[-1, 30, 60, float('inf')],
        labels=['Under 30 min', '1 hour', 'More than 1 hour']
    )
    return df

@st.cache_data
def load_map_data():
    df_map = pd.read_csv("D:/CampusX/Project-World/food_Analysis/Data/food_map.csv")
    df_map["state"] = df_map["state"].str.strip().str.title()
    replace_dict = {
        "Odisha": "Orissa",
        "Uttarakhand": "Uttaranchal",
        "Nct Of Delhi": "Delhi",
        "Jammu & Kashmir": "Jammu and Kashmir"
    }
    df_map["state"] = df_map["state"].replace(replace_dict)
    
    with open("D:/CampusX/Project-World/food_Analysis/india_states.geojson", "r", encoding="utf-8-sig") as f:
        geojson = json.load(f)
        
    df_map["dominance_score"] = df_map["veg_percent"] - df_map["nonveg_percent"]
    return df_map, geojson

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Extracted categories for filters
region = sorted([str(x) for x in set(df['region'].dropna())])
state = sorted([str(x) for x in set(df['state'].dropna())])
diet = sorted([str(x) for x in set(df['diet'].dropna())])
time = sorted([str(x) for x in set(df['time_category'].dropna())])
flavour = sorted([str(x) for x in set(df['flavour'].dropna())])
health = sorted([str(x) for x in set(df['health_status'].dropna())])

st.sidebar.title("Welcome to Indian Cuisine Insights 🍛")

def load_overall():
    st.title("Indian Cuisine Overview")
    st.markdown("Explore the rich diversity, flavors, and nutritional characteristics of Indian dishes.")
    try:
        img = Image.open("Map.jpg")
        st.image(img, use_column_width=True)
    except Exception as e:
        st.error(f"Error loading image: {e}")

def load_map():
    st.title("Vegetarian vs Non-Vegetarian Distribution")
    st.markdown("This map shows the prevalence of Vegetarian diet vs Non-Vegetarian diets across India. Blue regions tilt towards Vegetarian, while Red states tilt towards Non-Vegetarian.")
    try:
        df_map, geojson = load_map_data()

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
                "nonveg_percent": ':.1f',
                "dominance_score": False,
                "state": False
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
            coloraxis_colorbar=dict(title="Veg (Blue) → Non-Veg (Red)"),
            geo=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not load mapping resources: {e}")

def render_filtered_view(filtered_df, title):
    st.subheader(title)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Dishes", len(filtered_df))
    veg_count = len(filtered_df[filtered_df['diet'] == 'vegetarian'])
    col2.metric("Vegetarian Dishes", veg_count)
    non_veg_count = len(filtered_df[filtered_df['diet'] == 'non vegetarian'])
    col3.metric("Non-Vegetarian Dishes", non_veg_count)
    
    c1, c2 = st.columns(2)
    with c1:
        if len(filtered_df) > 0:
            fig = px.pie(filtered_df, names='diet', title="Diet Type Breakdown", hole=0.4, 
                         color='diet',
                         color_discrete_map={'vegetarian':'green', 'non vegetarian':'red'})
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        if len(filtered_df) > 0:
            fig = px.pie(filtered_df, names='flavour', title="Flavor Profiles Breakdown", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Interactive Dataset View")
    st.dataframe(filtered_df, use_container_width=True)

def load_Region():
    Select_region = st.sidebar.selectbox('Select Region', region)
    filtered = df[df["region"] == Select_region]
    render_filtered_view(filtered, f"Cuisine of `{Select_region}` Region")

def load_state():
    Select_state = st.sidebar.selectbox('Select State', state)
    filtered = df[df["state"] == Select_state]
    render_filtered_view(filtered, f"Cuisine of `{Select_state}`")

def load_diet():
    Select_diet = st.sidebar.selectbox('Select Diet', diet)
    filtered = df[df["diet"] == Select_diet]
    st.subheader(f"Dishes that are `{Select_diet.title()}`")
    st.metric("Total Dishes Found", len(filtered))
    st.dataframe(filtered, use_container_width=True)

def load_time():
    Select_time = st.sidebar.selectbox('Select Prep Time', time)
    filtered = df[df["time_category"] == Select_time]
    render_filtered_view(filtered, f"Dishes taking `{Select_time}` to cook")

def load_flavour():
    Select_flavour = st.sidebar.selectbox('Select Flavour Profile', flavour)
    filtered = df[df["flavour"] == Select_flavour]
    render_filtered_view(filtered, f"Dishes with `{Select_flavour.title()}` flavor")
    
def load_health():
    Select_health = st.sidebar.selectbox('Select Analysis Type', ['Overall Analysis'] + health)
    if Select_health != "Overall Analysis":
        filtered = df[df["health_status"] == Select_health]
        st.subheader(f"Dishes considered `{Select_health}`")
        st.metric("Total Dishes Found", len(filtered))
        st.dataframe(filtered, use_container_width=True)
    else:
        st.header("Health Status Dashboard")
        st.markdown("Compare the representation of *Healthy* vs *Unhealthy* choices across different segments.")
        
        c1, c2 = st.columns(2)
        with c1:
            region_status = df.groupby(["region", "health_status"]).size().reset_index(name='count')
            fig = px.bar(region_status, x="region", y="count", color="health_status", 
                         barmode="group", title="Health Status by Region")
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            flavour_health = df.groupby(["flavour", "health_status"]).size().reset_index(name='count')
            fig = px.bar(flavour_health, x="flavour", y="count", color="health_status", 
                         barmode="group", title="Health Status by Flavor Profile")
            st.plotly_chart(fig, use_container_width=True)
            
        c3, c4 = st.columns(2)
        with c3:
            dish_col = "dish_type" if "dish_type" in df.columns else ("course" if "course" in df.columns else None)
            if dish_col:
                dish_status = df.groupby([dish_col, "health_status"]).size().reset_index(name='count')
                fig = px.bar(dish_status, x=dish_col, y="count", color="health_status", 
                             barmode="group", title="Health Status by Dish Type")
                st.plotly_chart(fig, use_container_width=True)
                
        with c4:
            diet_status = df.groupby(["diet", "health_status"]).size().reset_index(name='count')
            fig = px.bar(diet_status, x="diet", y="count", color="health_status", 
                         barmode="group", title="Health Status by Dietary Preferences")
            st.plotly_chart(fig, use_container_width=True)

def load_comptime():
    st.subheader("⏱️ Compare Cooking Time Between Two Dishes")
    st.markdown("Enter two dish names to see which one cooks faster. (Case-Insensitive)")

    col1, col2 = st.columns(2)
    with col1:
        dish1 = st.text_input("First Dish Name", placeholder="e.g. Samosa")
    with col2:
        dish2 = st.text_input("Second Dish Name", placeholder="e.g. Dosa")
    
    if st.button("Compare Times", type="primary"):
        if not dish1 or not dish2:
            st.warning("Please enter two dish names to compare.")
            return
         
        matches1 = df[df["name"].str.contains(dish1, case=False, na=False)]
        matches2 = df[df["name"].str.contains(dish2, case=False, na=False)]
        
        if len(matches1) == 0:
            st.error(f"❌ '{dish1}' not found in the dataset.")
        if len(matches2) == 0:
            st.error(f"❌ '{dish2}' not found in the dataset.")
            
        if len(matches1) > 0 and len(matches2) > 0:
            d1 = matches1["total_time"].iloc[0]
            d2 = matches2["total_time"].iloc[0]
            name1 = matches1["name"].iloc[0]
            name2 = matches2["name"].iloc[0]
            
            mc1, mc2 = st.columns(2)
            mc1.metric(f"Time for {name1}", f"{d1} mins")
            mc2.metric(f"Time for {name2}", f"{d2} mins")

            if d1 < d2:
                st.success(f"🏆 **{name1}** is faster to cook!")
            elif d2 < d1:
                st.success(f"🏆 **{name2}** is faster to cook!")
            else:
                st.info("⏱️ Both dishes take the exact same time.")

def load_comppro():
    st.subheader("🩺 Check a Dish's Health Status")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        dish = st.text_input("Enter a dish name", key="dish1", placeholder="e.g. Jalebi")
    with col2:
        st.write("")
        st.write("")
        btn1 = st.button("Check health", key="btn1")
        
    if btn1:
        if dish:
            matches = df[df["name"].str.contains(dish, case=False, na=False)]
            if len(matches) > 0:
                name = matches["name"].iloc[0]
                status = matches["health_status"].iloc[0]
                if str(status).lower() == "healthy":
                    st.success(f"🥗 **{name}** is **{status.title()}**")
                elif str(status).lower() == "unhealthy":
                    st.error(f"🍔 **{name}** is **{status.title()}**")
                else:
                    st.info(f"**{name}**: {str(status).title()}")
            else:
                st.error("❌ Dish not found.")
        else:
            st.warning("Please enter a dish name.")

    st.divider()
    st.subheader("⚖️ Compare Health Score of Two Dishes")

    c1, c2 = st.columns(2)
    with c1:
        dish3 = st.text_input("First dish name", key="dish3", placeholder="e.g. Poha")
    with c2:
        dish4 = st.text_input("Second dish name", key="dish4", placeholder="e.g. Vada Pao")

    if st.button("Compare health scores", key="btn2", type="primary"):
        if not dish3 or not dish4:
            st.warning("Please enter two dishes.")
            return
            
        matches3 = df[df["name"].str.contains(dish3, case=False, na=False)]
        matches4 = df[df["name"].str.contains(dish4, case=False, na=False)]
        
        if len(matches3) == 0:
             st.error(f"❌ '{dish3}' not found.")
        if len(matches4) == 0:
             st.error(f"❌ '{dish4}' not found.")
             
        if len(matches3) > 0 and len(matches4) > 0:
            if "health_score" not in df.columns:
                st.warning("Health score computation missing from dataset format.")
                return
            
            d3 = matches3["health_score"].iloc[0]
            d4 = matches4["health_score"].iloc[0]
            n1 = matches3["name"].iloc[0]
            n2 = matches4["name"].iloc[0]

            mc1, mc2 = st.columns(2)
            mc1.metric(f"Health Score of {n1}", round(d3, 2))
            mc2.metric(f"Health Score of {n2}", round(d4, 2))

            if d3 > d4:
                st.success(f"🌟 **{n1}** is relatively healthier!")
            elif d4 > d3:
                st.success(f"🌟 **{n2}** is relatively healthier!")
            else:
                st.info("⚖️ Both dishes have the exact same health score.")
        
# Navigation Setup
step = st.sidebar.radio("Navigation", ['Overall', 'Individual Analysis', 'Comparison', 'Map Distribution'])

if step == "Overall":
    load_overall()

elif step == "Individual Analysis":
    option = st.sidebar.selectbox('Filter By Category', ['Region', 'State', 'Diet', 'Time', 'Flavour','Health'])

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

elif step == "Comparison":
    comparison = st.sidebar.radio('Select Comparison Dimension', ['Time', 'Health'], horizontal=True)
    if comparison == "Time":
        load_comptime()
    else:
        load_comppro()
        
elif step == "Map Distribution":
    load_map()

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Data Analysis Portfolio - Streamlit App")
