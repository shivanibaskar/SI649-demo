import pandas as pd
import altair as alt
import streamlit as st
st.set_page_config(layout="wide")
st.markdown("# Analysis Of Popularity Of Visualizations In [r/DataisBeautiful](https://www.reddit.com/r/dataisbeautiful/)  ")
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("#### As an anonymous social network, Reddit has a ton of interesting data to offer. Subreddits like r/dataisbeautiful and r/visualization are some \
of the best places to look for creative visualization ideas. But rarely does a visualization posted in these subreddits \
become popular or trending. Oftentimes, complex visualizations that display a lot of information receive very few upvotes. For instance, aesthetics are not the only factor for a \
visualization to gain upvotes as beautiful in the r/dataisbeautiful subreddit.What factors cause an image to trend in the subreddit? ")

#Container 1
with st.container():
    st.subheader("Relationship between the metrics")
    col_spacer1,col1, col2,col2_spacer = st.columns((.1, 5,5, .1))
    with col1:
        st.subheader("How do the metrics correlate with one another?")
         # You can call any Streamlit command, including custom components:
        data = pd.read_csv("reddit_data_v1.csv")
        data["author_karma"] = data["author_comment_karma"] + data["author_link_karma"]
        cor_data = (data.drop(columns=['Unnamed: 0', 'time_created', 'author_name', 'titles', 'text',
                'is_interactive', 'is_dynamic','total_votes',
            'is image downloaded', 'urls', 'awards', 'flairs',
            'isoriginal', 'isdistinguished', 'isselfpost', 'is_author_verified',
            'is_author_reddit_employee', 'author_has_reddit_premium',
            'author_link_karma', 'author_comment_karma', 'is_trending', 'extension',
            'type'])
                    .corr().stack()
                    .reset_index()     # The stacking results in an index on the correlation values, we need the index as normal columns for Altair
                    .rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'}))
        cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal

        base = alt.Chart(cor_data).encode(
            x=alt.X('variable2:O',axis=alt.Axis(title=' ')),
            y=alt.Y('variable:O',axis=alt.Axis(title=' '))    
        ).properties(width=550,height=550)

        # Text layer with correlation labels
        # Colors are for easier readability
        text = base.mark_text(size=20).encode(
            text='correlation_label',
            color=alt.condition(
                alt.datum.correlation > 0.5, 
                alt.value('white'),
                alt.value('black')
            )
        ).properties(width=550,height=550)

        # The correlation heatmap itself
        cor_plot = base.mark_rect().encode(
            color='correlation:Q'
        )
        plot1 = (cor_plot + text).configure_axis(labelFontSize=15) 
        st.write(plot1)

    with col2:
        st.subheader("Does an author with a better Karma score more likely to get more awards?")
        plot2=alt.Chart(data).mark_circle(size=60).encode(
        x=alt.X('author_karma:Q',axis=alt.Axis(grid=False,title="Author Karma"),scale=alt.Scale(domain=[0,400000])),
        y=alt.Y('total_awards:Q',axis=alt.Axis(grid=False,title="Total awards")),
        color=alt.Color('author_has_reddit_premium',legend=alt.Legend(title="Premium User")),
        tooltip = [
            alt.Tooltip(field = 'author_karma', type = "quantitative",title = "Author Karma"),
            alt.Tooltip(field = 'total_awards', type = "quantitative",title = "Total Awards"),
            alt.Tooltip(field = 'author_has_reddit_premium', type = "quantitative",title = "Premium User")]).interactive()
        st.write(plot2.properties(width=550,height=550))



filter_data = data[["urls",'author_karma',"total_awards","total_votes",'author_has_reddit_premium']]
data1 =filter_data.melt(['urls','author_karma','author_has_reddit_premium'], var_name='attribute', value_name='count')
attribute_selected = st.radio("Select Attribute",('total_awards', 'total_votes'))
plot3=alt.Chart(data1).mark_circle(size=60).encode(
    x=alt.X('author_karma:Q',axis=alt.Axis(grid=False,title="Author Karma"),scale=alt.Scale(domain=[0,400000])),
    y=alt.Y('count:Q',axis=alt.Axis(grid=False,title="Attribute")),
    color=alt.Color('author_has_reddit_premium',legend=alt.Legend(title="Premium User")),
    tooltip = [
        alt.Tooltip(field = 'author_karma', type = "quantitative",title = "Author Karma"),
        alt.Tooltip(field = 'total_awards', type = "quantitative",title = "Total Awards"),
        alt.Tooltip(field = 'author_has_reddit_premium', type = "quantitative",title = "Premium User")]
).transform_filter(attribute_selected == alt.datum.attribute).interactive()
st.write(plot3)    

import datetime
data.time_created = data.time_created.apply(lambda x: datetime.datetime.fromtimestamp(x).hour)
data['image'] = data['Unnamed: 0'].apply(lambda x:'https://raw.githubusercontent.com/shivanibaskar/SI649-demo/main/scrapedimages/'+str(x+2)+'.png')


# Scatterplot 1 - By Hour of Creation
scatterplot1 = alt.Chart(data).mark_circle().\
encode(
    alt.X('time_created:Q',title='Hour of Creation',axis=alt.Axis(labelAngle=0),scale = alt.Scale(domain = [min(data.time_created),max(data.time_created)])),
    alt.Y('upvotes:Q',title='Number of upvotes'),
    alt.Color('is_trending:N',title='Trending or Not Trending'),
    tooltip=['image','flairs','is_dynamic','is_interactive']
    ). \
properties(width=600,height=300).configure_axis(
    labelFontSize=12,
    titleFontSize=14).configure_legend(titleColor='black', titleFontSize=14,labelFontSize=12).interactive()

selection=alt.selection_single(on='mouseover',empty="none");
sizeCondition=alt.condition(selection,alt.value(400),alt.value(80))
scatterplot1 = scatterplot1.add_selection(
    selection                       # step 3, chart 1
).encode(
    size=sizeCondition,             # step 4, chart 1 (only size)
)
scatterplot1

import altair as alt
import pandas as pd

source = pd.DataFrame.from_records(
    [{'a': 1, 'b': 1, 'image': 'https://raw.githubusercontent.com/shivanibaskar/SI649-demo/main/scrapedimages/11.png'},
     {'a': 2, 'b': 2, 'image': 'https://raw.githubusercontent.com/shivanibaskar/SI649-demo/main/piecharts/10.png'}]
)
alt.Chart(source).mark_circle(size=200).encode(
    x='a',
    y='b',
    tooltip=['image']  # Must be a list for the image to render
)
