import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import base64

st.set_page_config(page_title="Crime Radar",page_icon="🚔",layout="wide")
st.sidebar.markdown("## 🚔 Crime Radar")
menu = st.sidebar.radio("Navigation",["🏠 Overview","📁 Upload & Preview","🧹 Data Cleaning","📊 Crime Analytics","🗺️ Hotspot Map","👮 Arrest Analysis","⏰ Time Analysis","📝 Summary & Conclusion"],label_visibility="collapsed")

try:
    df = pd.read_csv("chicago_crime_sample.csv")
except FileNotFoundError:
    st.error("❌ Dataset file 'chicago_crime_sample.csv' not found.")
    st.stop()

if menu == "🏠 Overview":

    st.title("🚔 Crime Radar Dashboard")

    st.write("🚔 About Crime Radar")

    st.write("""Crime Radar is a Data Science-based crime analysis and visualization dashboard.It analyzes historical crime records to identify crime patterns, major crime categories, crime trends, locations, and arrest information.The dashboard uses data cleaning, processing, and visualization techniques to 
            present crime information through interactive charts and graphs, helping users 
            better understand crime behavior and trends.""")
    ### 📌 About Crime Radar



    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Crimes", len(df))
    col2.metric("Crime Types", df["Primary Type"].nunique())
    col3.metric("Districts", df["District"].nunique())
    col4.metric("Arrests", df["Arrest"].sum())


    col1, col2 = st.columns(2)

    with col1:

        crime = df["Primary Type"].value_counts().head(10).sort_values()

        plt.figure(figsize=(8,5))

        plt.barh(
            crime.index,
            crime.values
        )

        plt.title("🚔 Top 10 Crime Types")
        plt.xlabel("Number of Crimes")

        st.pyplot(plt)

    with col2:

        df["Date"] = pd.to_datetime(df["Date"])

        df["Month"] = df["Date"].dt.month_name()

        month_order = [
            "January","February","March","April",
            "May","June","July","August",
            "September","October","November","December"
        ]

        monthly = (
            df["Month"]
            .value_counts()
            .reindex(month_order, fill_value=0)
        )


        plt.figure(figsize=(8,5))

        plt.plot(
            monthly.index,
            monthly.values,
            marker="o"
        )

        plt.title("📅 Monthly Crime Trend")
        plt.xlabel("Month")
        plt.ylabel("Crime Count")

        plt.xticks(rotation=45)

        st.pyplot(plt)

        st.subheader("👮 Arrest Status")

        arrest = df["Arrest"].value_counts()

        plt.figure(figsize=(6,6))

        plt.pie(arrest,labels=arrest.index,autopct="%1.1f%%",startangle=90)

        plt.title("Arrest Status")

        st.pyplot(plt)


        st.subheader("🗺️ Crime Hotspot Overview")

        plt.figure(figsize=(10,6))

        plt.scatter(
        df["Longitude"],
        df["Latitude"],
        alpha=0.3,
        s=8)

        plt.title("Crime Hotspots")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")

        st.pyplot(plt)

elif menu == "📁 Upload & Preview":
        st.title("📁 Upload & Preview")
        st.subheader("📋 Chicago Crime Dataset")
        st.dataframe(df, use_container_width=True)
        st.subheader("📋 Crime Dataset Preview")
        df = pd.read_csv("chicago_crime_sample.csv")
        st.subheader("First 10 Records")
        st.dataframe(df.head(10), use_container_width=True)
        st.subheader("Dataset Shape")
        st.write("Rows :", df.shape[0])
        st.write("Columns :", df.shape[1])
        
        st.subheader("Column Names")
        st.write(df.columns.tolist())
        
        st.subheader("Data Types")
        st.dataframe(df.dtypes)
        
        st.subheader("Missing Values")
        st.dataframe(df.isnull().sum())



if menu == "🧹 Data Cleaning":
    st.subheader("📄 Original Dataset Information")

    # Dataset Info
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Rows", df.shape[0])

    with col2:
        st.metric("Total Columns", df.shape[1])

    st.markdown("---")

    # Missing Values and Duplicate Records
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🔍 Missing Values")
        missing = df.isnull().sum()
        st.dataframe(missing[missing > 0], use_container_width=True)

    with col4:
        st.subheader("🧹 Duplicate Records")
        duplicates = df.duplicated().sum()
        st.metric("Duplicate Rows", duplicates)

    st.markdown("---")

    # Data Cleaning
    st.subheader("🔧 Handling Missing Values")
    df = df.drop_duplicates()
    df = df.dropna()
    st.success("Missing values removed successfully")

    st.subheader("✏️ Column Name Cleaning")
    df.columns = df.columns.str.strip()
    st.success("Extra spaces removed from column names")

    if "Month" in df.columns:
        df["Month"] = pd.to_datetime(df["Month"], errors="coerce")
        st.success("Month column converted into date format")
    
# if menu=="📊 Crime Analytics":
#     col1,col2=st.columns(2)
#     with col1:    
#         crime = df["Primary Type"].value_counts().head(10).sort_values()
#     plt.figure(figsize=(10,6))
#     plt.barh(crime.index, crime.values, color="tomato", edgecolor="black")
#     plt.title("🚔 Top 10 Crime Types", fontsize=16, fontweight="bold")
#     plt.xlabel("Number of Crimes")
#     plt.grid(axis="x", linestyle="--", alpha=0.5)
#     plt.tight_layout()
#     plt.show()           

#     with col2:
#         crime = df["Primary Type"].value_counts().head(6)
#         plt.figure(figsize=(7,7))
#         plt.pie(crime.values, labels=crime.index, autopct="%1.1f%%", wedgeprops={"width":0.4})
#         plt.title("🚨 Crime Distribution")
#         crime_arrest = pd.crosstab(df["Primary Type"], df["Arrest"]).head(10)
#         crime_arrest.plot(kind="bar",stacked=True,figsize=(12,6))
#         plt.title("👮 Crime Type vs Arrest")
#         plt.xlabel("Crime Type")
#         plt.ylabel("Number of Crimes")
#         plt.xticks(rotation=45)
#         plt.tight_layout()
#         plt.show()           


if menu == "🗺️ Hotspot Map":
    st.title("🗺️ Crime Hotspots")
    col1, col2 = st.columns(2)

    with col1:
        location = df["Location Description"].value_counts().head(10)

        plt.figure(figsize=(8,5))
        location.sort_values().plot(kind="barh")
        plt.title("Top Crime Locations")
        plt.xlabel("Number of Crimes")
        st.pyplot(plt)
        


    with col2:
        community = df["Community Area"].value_counts().head(10)

        plt.figure(figsize=(8,5))
        community.plot(kind="bar", color="purple")
        plt.title("🏙️ Top Community Areas with Crimes")
        plt.xlabel("Community Area")
        plt.ylabel("Crime Count")
        plt.tight_layout()
        st.pyplot(plt)

        plt.figure(figsize=(8,6))
        plt.scatter(df["Longitude"], df["Latitude"], alpha=0.3, s=8)
        plt.title("Crime Hotspots")
        plt.xlabel("Longitude") 
        plt.ylabel("Latitude")
        st.pyplot(plt)
    

if menu == "📊 Crime Analytics":

    st.title("📊 Crime Analysis")

    col1, col2 = st.columns(2)
    

    with col1:

        crime = df["Primary Type"].value_counts().head(10).sort_values()

        plt.figure(figsize=(10,6))
        plt.barh(crime.index, crime.values,
                 color="tomato",
                 edgecolor="black")
        plt.title("🚔 Top 10 Crime Types",
                  fontsize=16,
                  fontweight="bold")
        plt.xlabel("Number of Crimes")
        plt.grid(axis="x", linestyle="--", alpha=0.5)
        plt.tight_layout()

        st.pyplot(plt)
        

    with col2:

        crime = df["Primary Type"].value_counts().head(6)

        plt.figure(figsize=(7,7))

        plt.pie(
            crime.values,
            labels=crime.index,
            autopct="%1.1f%%",
            wedgeprops={"width":0.4})

        plt.title("🚨 Crime Distribution")

        st.pyplot(plt)
        crime_arrest = pd.crosstab(df["Primary Type"], df["Arrest"]).head(10)
        crime_arrest.plot(
        kind="bar",
        stacked=True,
        figsize=(12,6)
    )
        plt.title("👮 Crime Type vs Arrest")
        plt.xlabel("Crime Type")
        plt.ylabel("Number of Crimes")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)
    

if menu == "👮 Arrest Analysis":

    st.title("👮 Arrest Analysis")

    col1, col2 = st.columns(2)

    with col1:
        arrest = df["Arrest"].value_counts()

        fig, ax = plt.subplots(figsize=(5,5))
        ax.pie(arrest, labels=arrest.index, autopct="%1.1f%%", startangle=90)
        ax.set_title("Arrest Status")
        st.pyplot(fig)

    with col2:
        domestic = df["Domestic"].value_counts()

        fig, ax = plt.subplots(figsize=(5,5))
        ax.pie(domestic, labels=domestic.index, autopct="%1.1f%%")
        ax.set_title("Domestic Crimes")
        st.pyplot(fig)


        st.subheader("📊 Crime Type vs Arrest")

        crime_arrest = pd.crosstab(df["Primary Type"], df["Arrest"]).head(10)

        fig, ax = plt.subplots(figsize=(10,5))
        crime_arrest.plot(kind="bar", stacked=True, ax=ax)

        ax.set_xlabel("Crime Type")
        ax.set_ylabel("Number of Crimes")
        plt.xticks(rotation=45)
        plt.tight_layout()

    st.pyplot(fig)

    col3, col4 = st.columns(2)

    with col3:

        corr = df[["Latitude","Longitude","District","Ward"]].corr(numeric_only=True)

        fig, ax = plt.subplots(figsize=(6,5))
        sns.heatmap(corr,annot=True,cmap="coolwarm",ax=ax)

        ax.set_title("Correlation Heatmap")
        st.pyplot(fig)

    with col4:

        categories = ['Theft','Assault','Burglary','Robbery','Fraud']
        values = [80,60,70,50,90]

        radar_fig = go.Figure()

        radar_fig.add_trace(go.Scatterpolar(r=values,theta=categories,fill='toself'))

        radar_fig.update_layout(title="Crime Radar Chart",polar=dict(radialaxis=dict(visible=True,range=[0,100])),height=450,showlegend=False)

        st.plotly_chart(radar_fig, use_container_width=True)

        st.subheader("🌳 Crime Type & Arrest Status")

        sunburst_df = df.dropna(subset=["Primary Type","Arrest"])

        sunburst_fig = px.sunburst(sunburst_df,path=["Primary Type","Arrest"],color="Primary Type")

        sunburst_fig.update_layout(height=650)

        st.plotly_chart(sunburst_fig, use_container_width=True)

elif menu == "⏰ Time Analysis":

    st.title("⏰ Time Analysis")

    # Remove spaces from column names
    df.columns = df.columns.str.strip()
    st.write(df.columns.tolist())

    st.write("Dataset Columns:", df.columns.tolist())

    # Find date/month column automatically
    date_col = None

    for col in df.columns:
        if "month" in col.lower() or "date" in col.lower():
            date_col = col
            break

    if date_col is None:
        st.error("❌ No Month/Date column found in dataset")
    
    else:

        # Convert date column
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

        df = df.dropna(subset=[date_col])

        # Graph 1: Monthly Crime Trend
        st.subheader("📈 Monthly Crime Trend")

        monthly_crime = (
            df.groupby(date_col)
            .size()
            .reset_index(name="Crime Count")
        )

        fig1 = px.line(
            monthly_crime,
            x=date_col,
            y="Crime Count",
            markers=True,
            title="Crime Trend Over Time"
        )

        st.plotly_chart(fig1, use_container_width=True)


        # Graph 2: Crime Count by Month
        st.subheader("📊 Crime Count by Month")

        df["Month_Name"] = df[date_col].dt.month_name()

        month_count = (
            df["Month_Name"]
            .value_counts()
            .reset_index()
        )

        month_count.columns = ["Month", "Crime Count"]

        fig2 = px.bar(
            month_count,
            x="Month",
            y="Crime Count",
            title="Crime Count by Month"
        )

        st.plotly_chart(fig2, use_container_width=True)


        # Graph 3: Crime Type Trend
        if "Crime type" in df.columns:

            st.subheader("📉 Crime Type Trend")

            crime_time = (
                df.groupby([date_col, "Crime type"])
                .size()
                .reset_index(name="Crime Count")
            )

            fig3 = px.line(
                crime_time,
                x=date_col,
                y="Crime Count",
                color="Crime type",
                markers=True,
                title="Crime Type Over Time"
            )

            st.plotly_chart(fig3, use_container_width=True)

        else:
            st.warning("Crime type column not found")

if menu == "📝 Summary & Conclusion":

    st.title("📝 Project Summary & Conclusion")

    st.subheader("📌 Project Summary")

    st.write("""
    Crime Radar is a Data Science-based crime analysis and visualization project 
    developed to understand crime patterns and trends using historical crime data.

    The project focuses on collecting, cleaning, processing, and analyzing crime 
    datasets to identify important information such as crime frequency, crime 
    categories, locations, and time-based crime trends.

    Using Python libraries like Pandas, Matplotlib, Plotly, and Streamlit, an 
    interactive dashboard is created to visualize crime distribution, hotspots, 
    arrest analysis, and time-based crime patterns.

    The dashboard helps users explore crime data easily through interactive graphs 
    and provides meaningful insights from large datasets.
    """)


    st.subheader("✅ Conclusion")

    st.write("""
    The Crime Radar project successfully demonstrates the use of Data Science 
    techniques for crime data analysis and visualization.

    The project helps in identifying crime patterns, analyzing high-crime areas, 
    and understanding changes in crime trends through graphical representation.

    The interactive dashboard provides a simple and effective way to analyze crime 
    information and supports data-driven decision-making.

    In the future, the project can be improved by adding real-time crime data 
    updates, advanced analytics, and additional visualization features.
    """)


st.markdown("""
<style>

/* Main Background */
.stApp{

    background:
    radial-gradient(circle at center,#400000,#000000);

    overflow:hidden;

}


/* Red Glow */

.stApp::before{

    content:"";

    position:fixed;

    width:450px;
    height:450px;

    top:-120px;
    left:-120px;

    background:red;

    opacity:0.25;

    filter:blur(100px);

    animation:move1 8s infinite alternate;

}


.stApp::after{

    content:"";

    position:fixed;

    width:400px;
    height:400px;

    right:-100px;
    bottom:-100px;

    background:#ff0033;

    opacity:0.20;

    filter:blur(100px);

    animation:move2 10s infinite alternate;

}


/* Animation */

@keyframes move1{

from{
transform:translate(0,0);
}

to{
transform:translate(150px,100px);
}

}


@keyframes move2{

from{
transform:translate(0,0);
}

to{
transform:translate(-120px,-80px);
}

}


/* Grid */

.stApp{

background-image:

linear-gradient(
rgba(255,0,0,.08) 1px,
transparent 1px),

linear-gradient(
90deg,
rgba(255,0,0,.08) 1px,
transparent 1px);

background-size:50px 50px;

}


/* Sidebar */

[data-testid="stSidebar"]{

background:rgba(10,10,10,.85);

backdrop-filter:blur(15px);

border-right:1px solid red;

}


/* Cards */

div[data-testid="stMetric"]{

background:rgba(255,0,0,.12);

border:1px solid red;

border-radius:15px;

padding:15px;

backdrop-filter:blur(10px);

transition:.3s;

}


div[data-testid="stMetric"]:hover{

transform:translateY(-8px);

box-shadow:0 0 25px red;

}


/* Headings */

h1,h2,h3{

color:#ff3333;

text-shadow:0 0 15px red;

}


</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Sidebar Background */
section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #120000,
        #330000,
        #000000
    ) !important;

}


/* Sidebar text */
section[data-testid="stSidebar"] * {

    color: white !important;

}


/* Sidebar menu hover */
section[data-testid="stSidebar"] div:hover {

    color: #ff3333 !important;

}


/* Radio buttons / menu */
section[data-testid="stSidebar"] .stRadio label:hover {

    background: rgba(255,0,0,0.25);

    border-radius:10px;

    padding:8px;

}


/* Sidebar title */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {

    color:#ff3333 !important;

    text-shadow:0 0 15px red;

}


</style>
""", unsafe_allow_html=True)
