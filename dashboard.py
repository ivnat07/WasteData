import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Load data
file_path = 'D:/DV/Assign2_TanviKulkarni/WasteData/assign2_wastedata.csv'  # Adjust the path if running locally
waste_data = pd.read_csv(file_path)

# Title of the dashboard
st.title("Waste Data Visualization Dashboard")

# Background color and custom CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #e6ffe6;
    }
    .story-text {
        font-family: 'Garamond', serif;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Story section
st.markdown("""

## Story: Enhancing Waste Management through Data-Driven Insights

### Introduction
Waste management is a critical component of environmental sustainability. Understanding the patterns and trends in waste generation can help us develop more effective waste reduction and recycling strategies. This dashboard provides a comprehensive analysis of waste data across various buildings and streams, revealing key insights that can drive improvements in our waste management practices.

### Visualization Description
- **Bar Chart**: Displays the weight of waste by date and stream for the selected filters.
- **Pie Chart**: Shows the distribution of waste streams within the selected data.
- **Summary Statistics**: Provides descriptive statistics for the filtered data.

### Analysis and Insights
1. **Dominant Waste Streams**:
    - The pie chart indicates that "Recycling" and "Landfill" are the most significant waste streams. This suggests that while there is a strong effort to recycle, a substantial amount of waste still goes to landfill.

2. **Building-Specific Waste Generation**:
    - Analysis of the filtered data shows that buildings like "Facilities" generate more waste. This may be due to the higher volume of activities or the type of operations conducted in these buildings. Targeted waste reduction programs could be particularly beneficial here.

3. **Seasonal and Temporal Trends**:
    - The bar chart reveals seasonal trends in waste generation. For example, there are noticeable spikes during certain months, which could be linked to specific events like annual cleanups or increased activities during certain times of the year.

4. **Effectiveness of Recycling Programs**:
    - By comparing the volumes of different waste streams over time, we can assess the effectiveness of recycling initiatives. An increase in the proportion of recycling waste over time indicates that the recycling programs are having a positive impact.

### Interpretation and Conclusion
The data and visualizations provide a detailed view of waste management across different buildings. Key insights include the identification of dominant waste streams, building-specific waste generation patterns, and seasonal trends in waste generation. These insights highlight the areas where targeted waste reduction and recycling initiatives can be implemented to improve overall waste management. By leveraging these data-driven insights, we can develop more effective strategies to reduce waste, increase recycling, and move towards a more sustainable future.
</div>
""", unsafe_allow_html=True)

# Filter options
buildings = st.multiselect("Select Buildings", waste_data['Building'].unique(), default=waste_data['Building'].unique())
streams = st.multiselect("Select Streams", waste_data['Stream'].unique(), default=waste_data['Stream'].unique())
start_date = st.date_input("Start Date", value=pd.to_datetime(waste_data['Date']).min())
end_date = st.date_input("End Date", value=pd.to_datetime(waste_data['Date']).max())

# Filter data based on selections
filtered_data = waste_data[
    (waste_data['Building'].isin(buildings)) &
    (waste_data['Stream'].isin(streams)) &
    (pd.to_datetime(waste_data['Date']) >= pd.to_datetime(start_date)) &
    (pd.to_datetime(waste_data['Date']) <= pd.to_datetime(end_date))
]

# Display filtered data
st.write("Filtered Data", filtered_data)

# Bar Chart - Waste Weight by Date
if not filtered_data.empty:
    bar_chart = alt.Chart(filtered_data).mark_bar().encode(
        x='Date:T',
        y='Weight:Q',
        color='Stream:N',
        tooltip=['Date', 'Stream', 'Weight', 'Volume']
    ).interactive()
    st.altair_chart(bar_chart, use_container_width=True)
else:
    st.write("No data available for the selected filters")

# Dynamic Pie Chart - Distribution of Waste Streams
if not filtered_data.empty:
    stream_distribution = filtered_data['Stream'].value_counts().reset_index()
    stream_distribution.columns = ['Stream', 'Count']

    colorblind_friendly_colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7', '#999999']

    fig = px.pie(stream_distribution, values='Count', names='Stream', title='Distribution of Waste Streams',
                 color_discrete_sequence=colorblind_friendly_colors)
    fig.update_traces(textinfo='label+value', textfont_size=12)  # Add count labels to the pie chart

    st.plotly_chart(fig, use_container_width=True)

# Show summary statistics
st.write("Summary Statistics")
st.write(filtered_data.describe())

# Run the Streamlit app with: streamlit run dashboard.py
