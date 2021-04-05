import streamlit as st
import pandas as pd
import numpy as np

import utils

st.header('EDA - Hotels in Armenia')

# Cached functions
read_and_cache_data = st.cache(pd.read_csv)

cached_data = read_and_cache_data('armenian_hotels.csv')
data = cached_data.copy()

st.sidebar.markdown('# User Input Variables')
navigation = st.sidebar.radio('Navigation', ('Quantitative Analysis', 'Visualizations'))


##################################
#### Quantitative Analysis #######
##################################

if navigation == 'Quantitative Analysis':
    st.subheader('Overall Info on the Data')
    show_profile = st.checkbox('Show dataset description')
    if show_profile:
        '''
        The data for the analysis is scraped from TripAdvisor, an open online community.
        It contains information on the number of reviews, price, location and category of the hotel, 
        as well as the average score (ranging from 0 to 5) of a hotel given by the reviewers.

        The aim of this app is to conduct an exploratory data analysis for the Armenian hotels
        and show basic summary statistics.
        '''
        profiling_table = pd.DataFrame({
            'Number of variables' : [data.shape[1]],
            'Number of observations' : [data.shape[0]],
            'Missing cells' : [data.isna().sum().sum()],
            'Missing cells (%)' : [data.isna().sum().sum()/data.shape[0]]
        })
        st.table(profiling_table)

    st.markdown('_'*100) # adding a breaking line
    st.subheader('Data Exploration')
    head_count = st.slider('How many rows of data to show?', 5, 50, 5, 5)
    which_columns = st.multiselect('Which columns to show?', data.columns.tolist(), 
    ['Name', 'City', 'Price_AMD', 'Review_Count', 'Average_Score'])
    st.dataframe(data[which_columns].head(head_count))

    st.markdown('_'*100) # adding a breaking line
    st.subheader('Summary Statistics per group')
    col1, col2, col3 = st.beta_columns([1,1,2])
    grouping_var = col1.selectbox('Grouping variable', 
    ['City', 'State', 'Category', 'Free_WiFi', 'Breakfast_Included', 'Free_Parking', 'Swimming_Pool'])
    continuous_var = col2.selectbox('Continuous variable', 
    ['Price_AMD', 'Price_USD', 'Review_Count', 'Average_Score'])
    agg_func = col3.multiselect('Aggregation function', 
    ['mean', 'median', 'std', 'count'], ['mean', 'count'])

    sum_stats = data.groupby(grouping_var)[continuous_var].agg(agg_func)
    st.dataframe(sum_stats)

##################################
####### Visualizations ###########
##################################
if navigation == 'Visualizations':
    col1_bar, col2_bar, col3_bar = st.beta_columns([1, 1, 2])
    x_var_bar = col1_bar.selectbox('X variable (barplot)', 
    ['Price_AMD', 'Price_USD', 'Review_Count'])
    grouping_var_bar = col2_bar.selectbox('Grouping variable (barplot)', 
    [None, 'City', 'Name', 'State', 'Category'])
    n_obs = col3_bar.slider('Number of hotels to show', 5, 25, 10, 5)
    st.plotly_chart(utils.top_barplot(data, x_var_bar, 'Name', grouping_var_bar, n_obs), use_container_width=True) 

    st.markdown('_'*100) # adding a breaking line
    col1_box, col2_box, col3_box = st.beta_columns(3)
    x_var_box = col1_box.selectbox('X variable (boxplot)', 
    ['State', 'City', 'Category'])
    y_var_box = col2_box.selectbox('Y variable (boxplot)', 
    ['Price_AMD', 'Price_USD', 'Review_Count'])
    grouping_var_box = col3_box.selectbox('Color variable (boxplot)', 
    [None, 'City', 'State', 'Category'])
    st.plotly_chart(utils.distribution_box(data, x_var_box, y_var_box, grouping_var_box), use_container_width=True)

    st.markdown('_'*100) # adding a breaking line
    col1_scatter, col2_scatter, col3_scatter = st.beta_columns(3)
    x_var_scatter = col1_scatter.selectbox('X variable (scatter)', 
    ['Price_AMD', 'Price_USD', 'Review_Count', 'Average_Score'])
    y_var_scatter = col2_scatter.selectbox('Y variable (scatter)', 
    ['Price_AMD', 'Price_USD', 'Review_Count', 'Average_Score'], 2)
    grouping_var_scatter = col3_scatter.selectbox('Color variable (scatter)', 
    [None, 'City', 'State', 'Category'])
    st.plotly_chart(utils.scatter_plot(data, x_var_scatter, y_var_scatter, grouping_var_scatter), use_container_width=True)