import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import base64

st.set_page_config(page_title="Crime Radar",page_icon="🚔",layout="wide",initial_sidebar_state="expanded")
st.sidebar.markdown("## 🚔 Crime Radar")
menu = st.sidebar.radio("Navigation",["🏠 Overview","📁 Upload & Preview","🧹 Data Cleaning","📊 Crime Analytics","🗺️ Hotspot Map","👮 Arrest Analysis","⏰ Time Analysis","📝 Conclusion"],label_visibility="collapsed")

try:
    df = pd.read_csv("chicago_crime_sample.csv")
except FileNotFoundError:
    st.error("❌ Dataset file 'chicago_crime_sample.csv' not found.")
    st.stop()

if menu == "🏠 Overview":

    st.title("🚔 Crime Radar Dashboard")
    st.caption("Interactive Data Science Dashboard for Crime Analysis")

    st.write("### 🚔 About Crime Radar")
    st.write("""
Crime Radar is a Data Science-based crime analysis and visualization dashboard.
It analyzes historical crime records to identify crime patterns, major crime categories,
crime trends, locations, and arrest information. The dashboard uses data cleaning,
processing, and visualization techniques to present crime information through
interactive charts and graphs, helping users better understand crime behavior and trends.
""")

    # ===================== Metrics =====================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Crimes", len(df))
    col2.metric("Crime Types", df["Primary Type"].nunique())
    col3.metric("Districts", df["District"].nunique())
    col4.metric("Arrests", df["Arrest"].sum())

    # ===================== Row 1 =====================
    col1, col2 = st.columns(2)

    with col1:
        crime = df["Primary Type"].value_counts().head(10).sort_values()

        fig, ax = plt.subplots(figsize=(8,5))
        fig.patch.set_facecolor("#121212")
        ax.set_facecolor("#121212")

        ax.barh(crime.index, crime.values, color="deepskyblue")

        ax.set_title("🚔 Top 10 Crime Types", color="white")
        ax.set_xlabel("Number of Crimes", color="white")

        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("white")

        st.pyplot(fig)

    with col2:

        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.month_name()

        month_order = [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
        ]

        monthly = (
            df["Month"]
            .value_counts()
            .reindex(month_order, fill_value=0)
        )

        fig, ax = plt.subplots(figsize=(8,5))
        fig.patch.set_facecolor("#121212")
        ax.set_facecolor("#121212")

        ax.plot(monthly.index, monthly.values,
                marker="o",
                color="cyan",
                linewidth=2)

        ax.set_title("📅 Monthly Crime Trend", color="white")
        ax.set_xlabel("Month", color="white")
        ax.set_ylabel("Crime Count", color="white")

        plt.xticks(rotation=45)

        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("white")

        st.pyplot(fig)

    # ===================== Row 2 =====================
    col3, col4 = st.columns(2)

    with col3:

        arrest = df["Arrest"].value_counts()

        fig, ax = plt.subplots(figsize=(6,6))
        fig.patch.set_facecolor("#121212")
        ax.set_facecolor("#121212")

        ax.pie(
            arrest,
            labels=arrest.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#00BFFF","#FF4B4B"],
            textprops={"color":"white"}
        )

        ax.set_title("Arrest Status", color="white")

        st.pyplot(fig)

    with col4:

        fig, ax = plt.subplots(figsize=(6,6))
        fig.patch.set_facecolor("#121212")
        ax.set_facecolor("#121212")

        ax.scatter(
            df["Longitude"],
            df["Latitude"],
            color="cyan",
            alpha=0.3,
            s=8
        )

        ax.set_title("Crime Hotspots", color="white")
        ax.set_xlabel("Longitude", color="white")
        ax.set_ylabel("Latitude", color="white")

        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("white")

        st.pyplot(fig)

elif menu == "📁 Upload & Preview":
        st.title("📁 Upload & Preview")
        st.subheader("📋 Chicago Crime Dataset")
        st.dataframe(df, width="stretch")
        st.subheader("📋 Crime Dataset Preview")
        st.subheader("First 10 Records")
        st.dataframe(df.head(10), use_container_width=True)
        st.subheader("📊 Dataset Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("📄 Rows", f"{df.shape[0]:,}")
        col2.metric("📑 Columns", df.shape[1])
        col3.metric("❌ Missing Values", int(df.isnull().sum().sum()))
        col4.metric("🗂️ Duplicate Rows", int(df.duplicated().sum()))
        
        # st.subheader("Column Names")
        # st.write(df.columns.tolist())
        # ===== CHANGE: Better Column Display =====
        st.subheader("📝 Dataset Columns")
        st.dataframe(pd.DataFrame({"Columns": df.columns}), use_container_width=True)
        
        # st.subheader("Data Types")
        # st.dataframe(df.dtypes)
        # ===== CHANGE: Better Data Types Table =====
        st.subheader("📌 Data Types")
        st.dataframe(
        df.dtypes.reset_index().rename(
        columns={"index": "Column", 0: "Data Type"}),use_container_width=True)
        
        # st.subheader("Missing Values")
        # st.dataframe(df.isnull().sum())
        # ===== CHANGE: Better Missing Values Report =====
        st.subheader("🔍 Missing Values")

        missing = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values
})

        st.dataframe(missing, use_container_width=True)

elif menu == "🧹 Data Cleaning":
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
    
elif menu == "🗺️ Hotspot Map":

    st.title("🗺️ Crime Hotspots")

    col1, col2 = st.columns(2)

    with col1:
        location = df["Location Description"].value_counts().head(10).sort_values()

        fig, ax = plt.subplots(figsize=(8, 5), facecolor="black")
        ax.set_facecolor("black")

        ax.barh(location.index, location.values,
                color="cyan", edgecolor="white")

        ax.set_title("📍 Top Crime Locations", color="white")
        ax.set_xlabel("Number of Crimes", color="white")

        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("white")

        st.pyplot(fig)

    with col2:
        community = df["Community Area"].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(8, 5), facecolor="black")
        ax.set_facecolor("black")

        ax.bar(
            community.index.astype(str),
            community.values,
            color="purple",
            edgecolor="white"
        )

        ax.set_title("🏙️ Top Community Areas", color="white")
        ax.set_xlabel("Community Area", color="white")
        ax.set_ylabel("Crime Count", color="white")

        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("white")

        plt.xticks(rotation=45)

        st.pyplot(fig)

        # Scatter Plot
        fig, ax = plt.subplots(figsize=(8, 6), facecolor="black")
        ax.set_facecolor("black")

        ax.scatter(
            df["Longitude"],
            df["Latitude"],
            alpha=0.3,
            s=8,
            color="red"
        )

        ax.set_title("🔥 Crime Hotspots", color="white")
        ax.set_xlabel("Longitude", color="white")
        ax.set_ylabel("Latitude", color="white")

        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("white")

        st.pyplot(fig)


# ================= CRIME ANALYTICS =================
elif menu == "📊 Crime Analytics":

    st.title("📊 Crime Analysis")

    col1, col2 = st.columns(2)

    with col1:

        crime = df["Primary Type"].value_counts().head(10).sort_values()

        fig, ax = plt.subplots(figsize=(10, 6), facecolor="black")
        ax.set_facecolor("black")

        ax.barh(
            crime.index,
            crime.values,
            color="tomato",
            edgecolor="white"
        )

        ax.set_title(
            "🚔 Top 10 Crime Types",
            fontsize=16,
            fontweight="bold",
            color="white"
        )

        ax.set_xlabel("Number of Crimes", color="white")
        ax.tick_params(colors="white")

        ax.grid(axis="x", linestyle="--",
                alpha=0.4, color="white")

        for spine in ax.spines.values():
            spine.set_color("white")

        st.pyplot(fig)

    with col2:

        crime = df["Primary Type"].value_counts().head(6)

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="black")
        ax.set_facecolor("black")

        ax.pie(
            crime.values,
            labels=crime.index,
            autopct="%1.1f%%",
            wedgeprops={"width": 0.4},
            textprops={"color": "white"}
        )

        ax.set_title("🚨 Crime Distribution", color="white")

        st.pyplot(fig)

        # Crime vs Arrest
        crime_arrest = pd.crosstab(
            df["Primary Type"],
            df["Arrest"]
        ).head(10)

        fig, ax = plt.subplots(figsize=(12, 6), facecolor="black")
        ax.set_facecolor("black")

        crime_arrest.plot(
            kind="bar",
            stacked=True,
            color=["#FF4D4D", "#00E676"],
            edgecolor="white",
            ax=ax
        )

        ax.set_title(
            "👮 Crime Type vs Arrest",
            color="white",
            fontsize=16
        )

        ax.set_xlabel("Crime Type", color="white")
        ax.set_ylabel("Number of Crimes", color="white")

        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("white")

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.4,
            color="white"
        )

        legend = ax.legend(
            title="Arrest",
            facecolor="black",
            edgecolor="white"
        )

        plt.setp(legend.get_texts(), color="white")
        plt.setp(legend.get_title(), color="white")

        plt.xticks(rotation=45)

        st.pyplot(fig)


# ================= ARREST ANALYSIS =================
elif menu == "👮 Arrest Analysis":

    st.title("👮 Arrest Analysis")

    col1, col2 = st.columns(2)

    with col1:
        arrest = df["Arrest"].value_counts()

        fig, ax = plt.subplots(figsize=(6,6), facecolor="black")
        ax.set_facecolor("black")

        colors = ["#00E676", "#FF5252"]   # Green = Arrest, Red = No Arrest

        ax.pie(
        arrest.values,
        labels=arrest.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        explode=[0.05, 0.05],
        shadow=True,
        textprops={"color":"white","fontsize":12},
        wedgeprops={"edgecolor":"white","linewidth":2}
    )

        ax.set_title("👮 Arrest Status", color="white", fontsize=16)
        st.pyplot(fig)

    with col2:
        domestic = df["Domestic"].value_counts()

        fig, ax = plt.subplots(figsize=(6,6), facecolor="black")
        ax.set_facecolor("black")

        colors = ["#FFD54F", "#42A5F5"]   # Yellow & Blue
 
        ax.pie(
         domestic.values,
        labels=domestic.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        explode=[0.05, 0.05],
        shadow=True,
        textprops={"color":"white","fontsize":12},
        wedgeprops={"edgecolor":"white","linewidth":2}
    )

        ax.set_title("🏠 Domestic Crimes", color="white", fontsize=16)
        st.pyplot(fig)

    col3, col4 = st.columns(2)

    with col3:

        corr = df[
            ["Latitude", "Longitude", "District", "Ward"]
        ].corr(numeric_only=True)

        fig, ax = plt.subplots(figsize=(6, 5), facecolor="black")
        ax.set_facecolor("black")

        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            ax=ax
        )

        ax.set_title("Correlation Heatmap", color="white")

        st.pyplot(fig)

    with col4:

        categories = [
            "Theft",
            "Assault",
            "Burglary",
            "Robbery",
            "Fraud"
        ]

        values = [80, 60, 70, 50, 90]

        radar_fig = go.Figure()

        radar_fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself"
            )
        )

        radar_fig.update_layout(
            title="Crime Radar Chart",
            paper_bgcolor="black",
            plot_bgcolor="black",
            font=dict(color="white"),
            polar=dict(
                bgcolor="black",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False
        )

        st.plotly_chart(
            radar_fig,
            use_container_width=True
        )

        st.subheader("🌳 Crime Type & Arrest Status")

        sunburst_df = df.dropna(
            subset=["Primary Type", "Arrest"]
        )

        sunburst_fig = px.sunburst(
            sunburst_df,
            path=["Primary Type", "Arrest"],
            color="Primary Type"
        )

        sunburst_fig.update_layout(
            paper_bgcolor="black",
            font=dict(color="white"),
            height=650
        )

        st.plotly_chart(
            sunburst_fig,
            use_container_width=True
        )

elif menu == "⏰ Time Analysis":

    st.title("⏰ Time Analysis")
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

        st.plotly_chart(fig1, width="stretch")


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

        st.plotly_chart(fig2,width="stretch")


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

            st.plotly_chart(fig3,width="stretch")
elif menu == "📝 Conclusion":
    st.subheader("✅ Conclusion")

    st.markdown("""
1. **Crime Radar effectively applies Data Science techniques** to collect, clean, process, and analyze crime data for meaningful insights.

2. **The project converts raw crime records into clear visualizations** such as charts, graphs, and maps, making crime trends and patterns easier to understand.

3. **Data analysis helps identify crime frequency, hotspot locations, and time-based trends**, supporting a better understanding of historical crime data.

4. **The use of Python, Pandas, Matplotlib, Plotly, and Streamlit** demonstrates how Data Science can be used to build an interactive and informative crime analysis dashboard.

5. **The project provides a simple, accurate, and efficient Data Science solution** for crime analysis, enabling users to explore data and make informed decisions based on historical crime records.
""") 
    st.subheader("🚀 Future Scope")

    st.markdown("""
1. **Integrate Artificial Intelligence (AI) and Machine Learning (ML)** models to predict future crime trends based on historical crime data.

2. **Implement real-time crime data integration** from police or government sources to provide up-to-date analysis and visualizations.

3. **Enhance hotspot detection** using advanced geospatial analysis and AI-based clustering techniques for more accurate crime mapping.

4. **Develop mobile and web-based applications** with personalized dashboards, alerts, and role-based access for different users.

5. **Expand the system with advanced analytics** such as crime forecasting, anomaly detection, and intelligent decision-support tools using AI and ML.
""")

    st.markdown("""
    <style>
    .director-box {
        background-color: #2f2f2f;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        color: white;
        border: 1px solid #555;
        margin-top: 40px;
    }
    .director-box h3 {
        color: #00c6ff;
    }
    </style>

    <div class="director-box">
        <h3>🚔 Crime Radar</h3>
        <p>📌 Directed By</p>
        <h4>Navjot Sharma</h4>
        <p>📊 Data Science Project</p>
        <p>🗓️ 45 Days Training</p>
    </div>
    """, unsafe_allow_html=True)


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

def add_bg_from_local(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.72), rgba(0,0,0,0.72)),
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background: rgba(15,15,20,0.92);
            backdrop-filter: blur(8px);
        }}

        /* Metric cards */
        div[data-testid="metric-container"] {{
            background: rgba(40,0,0,0.70);
            border: 1px solid red;
            border-radius: 12px;
            padding: 15px;
        }}

        div[data-testid="metric-container"] * {{
            color: white !important;
        }}

        h1,h2,h3,p,label,span {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
add_bg_from_local("bg1.jpg")



