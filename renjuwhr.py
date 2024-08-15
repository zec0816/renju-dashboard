import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

st.set_page_config(page_title='RenjuRating', page_icon = 'icon.png', layout = 'wide', initial_sidebar_state = 'auto')

data = pd.read_excel('players_with_coordinates.xlsx', sheet_name='players')

LANGUAGES = {
    'en': {
        'title': 'Player Rating Dashboard',
        'description': 'This dashboard allows you to explore the distribution of player ratings and filter players by country, city, and rating range.',
        'filters': 'Filters',
        'country': 'Select Country',
        'city': 'Select City',
        'rating_range': 'Select Rating Range',
        'search_name': 'Search Player by Name',
        'filtered_data': 'Filtered Data',
        'download_csv': 'Download data as CSV',
        'distribution': 'Distribution of Player Ratings',
        'top_n_players': 'Top {} Players',
        'country_stats': 'Country-wise Statistics',
        'player_details': 'Player Details',
        'compare_players': 'Compare Players',
        'rating_trends': 'Rating Trends Over Time',
        'player_map': 'Player Distribution Map',
        'player_name': 'Name',
        'player_country': 'Country',
        'player_city': 'City',
        'player_rating': 'Rating',
        'average_rating': 'Average Rating',
        'player_count': 'Player Count',
        'rank': 'Rank'
    },
    'zh': {
        'title': '棋手评分仪表板',
        'description': '此仪表板让您可以探索棋手等级分的分布，并按国家、城市和评分范围筛选棋手。',
        'filters': '筛选器',
        'country': '选择国家',
        'city': '选择城市',
        'rating_range': '选择等级分范围',
        'search_name': '按姓名搜索棋手',
        'filtered_data': '筛选后的数据',
        'download_csv': '下载数据为CSV',
        'distribution': '棋手等级分分布',
        'top_n_players': '前{}名棋手',
        'country_stats': '按国家统计',
        'player_details': '棋手详情',
        'compare_players': '比较棋手',
        'rating_trends': '评分趋势',
        'player_map': '棋手分布图',
        'player_name': '姓名',
        'player_country': '国家',
        'player_city': '城市',
        'player_rating': '等级分',
        'average_rating': '平均等级分',
        'player_count': '棋手数量',
        'rank': '名次'
    }
}

language = st.sidebar.radio('Select Language', options=['English', 'Chinese'])
lang_code = 'zh' if language == 'Chinese' else 'en'

st.title(LANGUAGES[lang_code]['title'])
st.write(LANGUAGES[lang_code]['description'])

st.sidebar.header(LANGUAGES[lang_code]['filters'])

country_filter = st.sidebar.multiselect(
    LANGUAGES[lang_code]['country'],
    options=data['Country'].unique(),
    default=[]
)

if country_filter:
    city_options = data[data['Country'].isin(country_filter)]['City'].unique()
else:
    city_options = data['City'].unique()

city_filter = st.sidebar.multiselect(
    LANGUAGES[lang_code]['city'],
    options=city_options,
    default=[]
)

rating_filter = st.sidebar.slider(
    LANGUAGES[lang_code]['rating_range'],
    min_value=int(data['Rating'].min()),
    max_value=int(data['Rating'].max()),
    value=(int(data['Rating'].min()), int(data['Rating'].max()))
)

search_name = st.sidebar.text_input(LANGUAGES[lang_code]['search_name'])

filtered_data = data[
    (data['Country'].isin(country_filter) | (country_filter == [])) &
    (data['City'].isin(city_filter) | (city_filter == [])) &
    (data['Rating'] >= rating_filter[0]) &
    (data['Rating'] <= rating_filter[1])
]

if search_name:
    filtered_data = filtered_data[
        filtered_data['Name'].str.contains(search_name, case=False)
    ]

filtered_data_display = filtered_data.drop(columns=['latitude', 'longitude'])
filtered_data_display = filtered_data_display.rename(columns={
    'Rank': LANGUAGES[lang_code]['rank'],  # No need to change 'Rank' if the name stays the same
    'Name': LANGUAGES[lang_code]['player_name'],
    'Country': LANGUAGES[lang_code]['player_country'],
    'City': LANGUAGES[lang_code]['player_city'],
    'Rating': LANGUAGES[lang_code]['player_rating']
})

st.dataframe(filtered_data_display, hide_index=True)


csv = filtered_data_display.to_csv(index=False)
st.download_button(
    label=LANGUAGES[lang_code]['download_csv'],
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv',
)

st.subheader(LANGUAGES[lang_code]['distribution'])
rating_histogram = px.histogram(filtered_data, x='Rating', nbins=20, title=LANGUAGES[lang_code]['distribution'])
rating_histogram.update_traces(
    hovertemplate='Rating: %{x}<br>Frequency: %{y}',
    marker=dict(
        line=dict(width=2, color='rgba(0,0,0,0.5)'),
        opacity=0.5  
    )
)
rating_histogram.update_layout(
    xaxis_title=LANGUAGES[lang_code]['player_rating'],
    yaxis_title='Frequency',
    hovermode='x unified'
)
st.plotly_chart(rating_histogram)

top_n = st.sidebar.slider(LANGUAGES[lang_code]['top_n_players'].format('N'), min_value=1, max_value=20, value=10)
st.subheader(LANGUAGES[lang_code]['top_n_players'].format(top_n))

top_players = filtered_data.nlargest(top_n, 'Rating')

top_players_display = top_players.drop(columns=['latitude', 'longitude']).rename(columns={
    'Rank': LANGUAGES[lang_code]['rank'],  
    'Name': LANGUAGES[lang_code]['player_name'],
    'Country': LANGUAGES[lang_code]['player_country'],
    'City': LANGUAGES[lang_code]['player_city'],
    'Rating': LANGUAGES[lang_code]['player_rating']
})

st.dataframe(top_players_display, hide_index=True)

st.subheader(LANGUAGES[lang_code]['country_stats'])

if country_filter:
    country_stats = filtered_data.groupby('Country').agg(
        average_rating=pd.NamedAgg(column='Rating', aggfunc='mean'),
        player_count=pd.NamedAgg(column='Rating', aggfunc='count')
    ).reset_index()
    
    country_stats = country_stats.rename(columns={
        'Country': LANGUAGES[lang_code]['player_country'],
        'average_rating': LANGUAGES[lang_code]['average_rating'],
        'player_count': LANGUAGES[lang_code]['player_count']
    })
    
    st.dataframe(country_stats, hide_index=True)

st.subheader(LANGUAGES[lang_code]['player_details'])

selected_player = st.selectbox(LANGUAGES[lang_code]['player_details'], filtered_data['Name'])

if selected_player:
    player_details = filtered_data[filtered_data['Name'] == selected_player].iloc[0]
    
    player_details_display = player_details.drop(labels=['latitude', 'longitude']).rename(pd.Series({
        'Rank': LANGUAGES[lang_code]['rank'],
        'Name': LANGUAGES[lang_code]['player_name'],
        'Country': LANGUAGES[lang_code]['player_country'],
        'City': LANGUAGES[lang_code]['player_city'],
        'Rating': LANGUAGES[lang_code]['player_rating']
    }))
    
    player_details_df = player_details_display.to_frame().T
    
    st.dataframe(player_details_df, hide_index=True)

st.subheader(LANGUAGES[lang_code]['compare_players'])

compare_players = st.multiselect(LANGUAGES[lang_code]['compare_players'], filtered_data['Name'])

if len(compare_players) == 2:
    compare_data = filtered_data[filtered_data['Name'].isin(compare_players)]
    
    compare_data_display = compare_data.drop(columns=['latitude', 'longitude']).rename(columns={
        'Rank': LANGUAGES[lang_code]['rank'],
        'Name': LANGUAGES[lang_code]['player_name'],
        'Country': LANGUAGES[lang_code]['player_country'],
        'City': LANGUAGES[lang_code]['player_city'],
        'Rating': LANGUAGES[lang_code]['player_rating']
    })
    
    st.dataframe(compare_data_display, hide_index=True)

if 'Date' in data.columns:
    st.subheader(LANGUAGES[lang_code]['rating_trends'])
    filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])
    rating_trends = filtered_data.groupby('Date')['Rating'].mean().reset_index()
    line_chart = alt.Chart(rating_trends).mark_line().encode(
        x='Date:T',
        y='Rating:Q'
    )
    st.altair_chart(line_chart, use_container_width=True)

if 'latitude' in data.columns and 'longitude' in data.columns:
    st.subheader(LANGUAGES[lang_code]['player_map'])
    map_fig = px.scatter_mapbox(
        filtered_data,
        lat='latitude',
        lon='longitude',
        hover_name='Name',
        hover_data=['Country', 'City', 'Rating'],
        color='Rating',
        size='Rating',
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15,
        zoom=3,
        center={"lat": filtered_data['latitude'].mean(), "lon": filtered_data['longitude'].mean()}
    )
    map_fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(map_fig)

st.markdown("---")
if lang_code == 'en':
    st.markdown("""
        **Thank you for using the Player Rating Dashboard!**  
        The rating database is sourced from [renju.net](https://renju.net).  
    """)
else:
    st.markdown("""
        **感谢使用棋手评分仪表板！**  
        等级分数据库来源于 [renju.net](https://renju.net)。  
    """)
