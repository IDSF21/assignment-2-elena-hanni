import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import plotly.express as px

st.set_page_config(layout="wide", page_title="Exploration of Chocolate Bar Ratings",
                   )

df = pd.read_csv("output.csv")

st.title("Exploration of Chocolate Bar Ratings")


st.header("1. What factors are related to Rating for chocolate bars?")

st.markdown("Chocolate bars are very popular snacks and treats. When we choose from so many brands available in the "
            "market, a score that rates chocolate bars will help us make the choice. One thing that we would be "
            "curious about is, what external factors influences the rating? In the following boxplot, you can choose"
            "the categorical variables that you are interested in and get the box plot for distribution "
            "of rating over this variable.")

option = st.selectbox('Type of external factor', ('bean_type', 'general_location', 'review_date'), 0)
plot_df = df.replace(r'^\s*$', np.NaN, regex=True)

# The following code referred to the documentation:
# https://plotly.com/python/box-plots/

fig = px.box(plot_df, x=option, y="rating")
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig, use_container_width=True)

st.markdown("From the box plots above, we observe that the rating fluctuates with all of the categorical variables. "
            "Among three categorical variables, it seems that ratings are most stable along the review dates(years), "
            "and fluctuate most with the general location, the origin of the beans.")


st.header("2. What’s the relationship between cocoa solids percentage and rating?")

st.markdown("Cocoa percentage of chocolate bars is an important scale that we would like to check when we buy "
            "chocolates. However, the higher cocoa percentage means a stronger, and usually not public welcomed "
            "bitter taste. Chocolates with appropriate cocoa percentage blend in other ingredients like sugar "
            "and milk to create a sweet and silky taste. Does this also applies to the rating of cocoa? "
            "In this part, we will try to explore the relationship between cocoa solids percentage and rating.")

st.markdown("Here, we can specifically inspect the date from some years in order to consider fluctuations due to "
            "weather and other external aspects in different years.")

st.markdown("A linear regression is also provided on the plot to help understanding the potential relationship.")


year_list = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]

start_year, end_year = st.select_slider('Select a range of year for review date of chocolate bars',
                                          options=year_list,
                                          value=(2006, 2017))
st.write('You selected year between', start_year, 'and', end_year)

df['percentage'] = df['cocoa_percentage'].map(lambda x: x.rstrip('%')).astype(float)
plot_df3 = df[(df.review_date >= start_year) & (df.review_date <= end_year)]

# The following code referred to the documentation:
# https://plotly.com/python/line-and-scatter/

fig = px.scatter(plot_df3, x="percentage", y="rating", trendline="ols",
                 title="Scatterplot of cocoa Percentage vs Rating for Chocolate Bars",
                 labels={
                     "percentage": "cocoa Percentage(%)",
                     "rating": "Rating(Scale from 1 to 5, Worst to Best)"
                 },
                 opacity=0.5
                 )
st.plotly_chart(fig, use_container_width=True)


st.write("By observing the scatterplots, we can find that there might exists some negative relationship between cocoa "
         "percentage and the rating. However, since the dataset only includes chocolate bars that have cocoa percentage"
         "higher than 60 percent, this relationship only applies to chocolates that are in this range; this might also"
         "indicates the rating standards: are chocolates with low cocoa percentage actually considered as "
         "**'chocolates'**? ")


st.header("3. Which countries produce the highest-rated bars?")

st.markdown("When we think of chocolate bars, we usually select the companies that we are familiar with -- the ones "
            "that we always see on TV commercials or the brands that we have been always buying. However, are there "
            "countries of company locations that are specifically trustworthy? We will try to find some insights by"
            "looking into the average rating over chocolate company locations.")

np.random.seed(2021)
default_list = np.random.choice(df.company_location.unique(), 10, replace=False)
company_location = st.multiselect("Choose the Company Location of Chocolate Bars (Default values are 10 random countries)", df.company_location.unique(),
                                  default_list)

st.markdown("By hovering on the bars in the chart, you will also be able to get a list of companies names that are "
            "located at that country to help you decide which brand to buy next time!")

avg_df1 = df.groupby('company_location')[["rating"]].mean()
avg_df1['company_location'] = avg_df1.index
avg_df1["avg_rating"] = avg_df1["rating"].astype(float)
test_df = df.groupby('company_location')['company'].agg(['unique'])
avg_df1["company_name"] = test_df
plot_df1 = avg_df1[avg_df1.company_location.isin(company_location)]

# The following code referred to altair documentation:
# https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/streamlit_app.py
# https://altair-viz.github.io/user_guide/customization.html
# https://altair-viz.github.io/user_guide/encoding.html
# https://altair-viz.github.io/user_guide/generated/core/altair.Color.html
# https://altair-viz.github.io/gallery/scatter_tooltips.html


st.altair_chart((
    alt.Chart(plot_df1, title="Average Rating by Company Location",)
    .mark_bar()
    .encode(
        x=alt.X("avg_rating", title="Average Rating(Scale from 1 to 5, Worst to Best)"),
        y=alt.Y("company_location", sort=alt.EncodingSortField(field="avg_rating"),
                title="Company Location(By Country)",),
        color=alt.Color('rating', scale=alt.Scale(scheme='plasma')),
        tooltip=["avg_rating", "company_name"])), use_container_width=True)


st.write("From the bar chart above, it seems that the best rated companies are not from the major production countries "
         "that we are most familiar with. "
         "These information maybe helpful when you check the companies that produce the chocolate bars.")

st.header("4. Where are the best cocoa beans grown?")

st.markdown("When we buy some products in our daily lives, quality is one of the most important things that we care "
            "about; this also applies to the case of chocolate bars. But how do we find the best chocolate bars from "
            "thousands of brands and companies out there? One thing we can reference is the grown origin of cocoa "
            "beans. Thus, for the last question, we will take at look at the world map, and explore which locations"
            "own the highest rating cocoa.")

st.markdown("For this world map plot, you can zoom in or zoom out to check the details of the origin locations of "
            "different chocolate bars. Each point indicates a location, and the radius is the number of chocolate bars "
            "using cocoa beans there, and the color indicates the average rating score of that location. There are "
            "a total of five colors used on this map, where color closer to red indicates higher rating, and color "
            "closer to blue indicates lower rating. You can also hover on the points to get the specific numeric rating"
            " if the color is not very detailed.")


avg_df2 = df.groupby('general_location')[["rating"]].mean()
location_df2 = df.groupby(['lon', 'lat'], as_index=False)[['rating']].mean()
count_df2 = df.groupby(['lon', 'lat']).size().reset_index(name='counts')
location_df2["count"] = count_df2["counts"]
location_df2["radius"] = location_df2["count"] * 10
color_mapping = location_df2['rating'].quantile([0.2, 0.4, 0.6, 0.8])

# The following scatterplot layer referred to the pydeck documentation:
# https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/streamlit_app.py
# https://deckgl.readthedocs.io/en/latest/gallery/scatterplot_layer.html?highlight=scatterplotlayer
# and https://deckgl.readthedocs.io/en/latest/layer.html

max_row = location_df2.iloc[location_df2['count'].idxmax()]
my_map = pdk.Deck(layers=[pdk.Layer("ScatterplotLayer",
                                    location_df2[location_df2["rating"] <= color_mapping.iloc[0]],
                                    pickable=True,
                                    opacity=0.5,
                                    radius_scale=100,
                                    radius_min_pixels=10,
                                    radius_max_pixels=2000,
                                    get_position=['lon', 'lat'],
                                    get_radius="radius",
                                    get_fill_color=[26, 82, 118],
                                    auto_highlight=True,),
                          pdk.Layer("ScatterplotLayer",
                                    location_df2[(location_df2['rating'] > float(color_mapping.iloc[0])) &
                                                 (location_df2['rating'] <= float(color_mapping.iloc[1]))],
                                    pickable=True,
                                    opacity=0.5,
                                    radius_scale=100,
                                    radius_min_pixels=10,
                                    radius_max_pixels=2000,
                                    get_position=['lon', 'lat'],
                                    get_radius="radius",
                                    get_fill_color=[133, 193, 233],
                                    auto_highlight=True,
                                    ),
                          pdk.Layer("ScatterplotLayer",
                                    location_df2[(location_df2['rating'] > float(color_mapping.iloc[1])) &
                                                 (location_df2['rating'] <= float(color_mapping.iloc[2]))],
                                    pickable=True,
                                    opacity=0.5,
                                    radius_scale=100,
                                    radius_min_pixels=10,
                                    radius_max_pixels=2000,
                                    get_position=['lon', 'lat'],
                                    get_radius="radius",
                                    get_fill_color=[234, 242, 248],
                                    auto_highlight=True,
                                    ),
                          pdk.Layer("ScatterplotLayer",
                                    location_df2[(location_df2['rating'] > float(color_mapping.iloc[2])) &
                                                 (location_df2['rating'] <= float(color_mapping.iloc[3]))],
                                    pickable=True,
                                    opacity=0.5,
                                    radius_scale=100,
                                    radius_min_pixels=10,
                                    radius_max_pixels=2000,
                                    get_position=['lon', 'lat'],
                                    get_radius="radius",
                                    get_fill_color=[245, 183, 177],
                                    auto_highlight=True,
                                    ),
                          pdk.Layer("ScatterplotLayer",
                                    location_df2[location_df2['rating'] > float(color_mapping.iloc[3])],
                                    pickable=True,
                                    opacity=0.5,
                                    radius_scale=100,
                                    radius_min_pixels=10,
                                    radius_max_pixels=2000,
                                    get_position=['lon', 'lat'],
                                    get_radius="radius",
                                    get_fill_color=[231, 76, 60],
                                    auto_highlight=True,
                                    )],
                  initial_view_state={
                      "longitude": max_row['lon'],
                      "latitude": max_row['lat'],
                      "zoom": 1,
                      "min_zoom": 1,
                      "max_zoom": 20,
                  },
                  tooltip={"html": "<b>Rating:</b> {rating}"})
st.pydeck_chart(my_map)

st.markdown("From the world map, we observe that South America has many origins that grow cocoa beans, and Guatemala "
            "grows some high quality cocoa beans. These information provides good quality guidance to customers who"
            "are not very familiar with origins of cocoa beans.")