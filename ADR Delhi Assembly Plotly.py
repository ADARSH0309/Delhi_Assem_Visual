import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Delhi Assembly 2025 Dashboard", layout="wide")

# Title and description
st.title("🗳️ Delhi Assembly 2025 Candidate Dashboard")
st.markdown("Visualizing insights from the candidate dataset: Criminal cases, assets, gender, education & more.")

# Load data
@st.cache_data
def load_data():
    path = "data/Delhi Assembly 2025 Candidates Data.xls"
    return pd.read_excel(path, engine='openpyxl')

df = load_data()

# Clean column names
df.columns = [col.strip() for col in df.columns]





# Sidebar filters
st.sidebar.header("Filter Options")
parties = st.sidebar.multiselect("Select Parties", options=df['Party'].unique(), default=df['Party'].unique())
genders = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
districts = st.sidebar.multiselect("Select Districts", options=df['District'].unique(), default=df['District'].unique())

filtered_df = df[(df['Party'].isin(parties)) & (df['Gender'].isin(genders)) &  (df['District'].isin(districts))]

# 1. Bar Chart – Candidates by Party
st.subheader("1. Candidates by Party")
fig1 = px.bar(filtered_df['Party'].value_counts().reset_index(),x='index', y='Party',labels={'index': 'Party', 'Party': 'Number of Candidates'},title='Number of Candidates per Party',
              color='index',text_auto=True)
st.plotly_chart(fig1, use_container_width=True)




# 2. Treemap – Cases by Region
st.subheader("2. Treemap – Criminal Cases by Region")
fig2 = px.treemap(filtered_df, path=['District', 'Constituency', 'Candidate'],values='Cases Total', color='Cases Total',title="Treemap of Criminal Cases", template='plotly_dark')
st.plotly_chart(fig2, use_container_width=True)




# 3. Sunburst – Cases by Location
if 'Cases Total' in filtered_df.columns and (filtered_df['Cases Total'] > 0).sum() > 0:
    if (filtered_df['Cases Total'] > 0).sum() > 0:
        sunburst = px.sunburst(filtered_df[filtered_df['Cases Total'] > 0],path=['District', 'Constituency', 'Candidate'],values='Cases Total', color='Cases Total',template="plotly_dark", color_continuous_scale='viridis')    
        st.plotly_chart(sunburst, use_container_width=True)
    else:
        st.warning("No candidates with criminal cases to show in the sunburst chart.")








# 4. Violin Plot – Assets by Gender
fig3 = px.violin(filtered_df, x='Gender', y='Total Assets', box=True, points="all",color='Gender', template="plotly_dark", hover_data=filtered_df.columns)
                 
fig3.update_traces(meanline_visible=True)
st.plotly_chart(fig3, use_container_width=True)






# 5. Pie Chart – Gender Distribution
st.subheader("5. Gender Distribution of Candidates")
fig4 = px.pie(filtered_df, names='Gender', title='Candidate Gender Ratio')
st.plotly_chart(fig4, use_container_width=True)




# 6. Histogram – Age Distribution
st.subheader("6. Age Distribution of Candidates")
fig5 = px.histogram(filtered_df, x='Age', nbins=30, title='Age Distribution', color='Gender')
st.plotly_chart(fig5, use_container_width=True)




# 7. Box Plot – Assets by Party
st.subheader("7. Box Plot – Total Assets by Party")
fig6 = px.box(filtered_df, x='Party', y='Total Assets', color='Party',title='Asset Comparison by Party')
st.plotly_chart(fig6, use_container_width=True)






# 8. Heatmap – District vs Party

st.subheader("8. Heatmap – Candidate Count by District & Party")
heatmap_df = filtered_df.groupby(['District', 'Party']).size().reset_index(name='Counts')
heatmap_pivot = heatmap_df.pivot(index='District', columns='Party', values='Counts').fillna(0)
fig7 = go.Figure(data=go.Heatmap(z=heatmap_pivot.values,x=heatmap_pivot.columns,y=heatmap_pivot.index,colorscale='Viridis'))
fig7.update_layout(title='Heatmap of Candidates by District and Party')
st.plotly_chart(fig7, use_container_width=True)





# 9. Scatter Plot – Age vs Total Assets by Party
st.subheader("9. Scatter Plot – Age vs Total Assets")
fig8 = px.scatter(filtered_df, x='Age', y='Total Assets', color='Party',title='Age vs Total Assets Colored by Party')
st.plotly_chart(fig8, use_container_width=True)





# 10. Sunburst – Party, Education, Gender
st.subheader("10. Sunburst - Party > Education > Gender")
fig9 = px.sunburst(filtered_df, path=['Party', 'Education', 'Gender'], title='Party-Education-Gender Sunburst',template='plotly_dark')
st.plotly_chart(fig9, use_container_width=True)





# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Adarsh | Powered by Plotly & Streamlit")
