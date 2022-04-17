import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd
import altair as alt
import streamlit as st
st.set_page_config(layout="wide")
st.markdown("## Analysis of Popularity of Visualizations in [r/DataisBeautiful](https://www.reddit.com/r/dataisbeautiful/)  ")
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("##### As an anonymous social network, Reddit has a ton of interesting data to offer. Subreddits like r/dataisbeautiful and r/visualization are some \
of the best places to look for creative visualization ideas. But rarely does a visualization posted in these subreddits \
become popular or trending.")
    st.markdown("##### Oftentimes, complex visualizations that display a lot of information receive very few upvotes. For instance, aesthetics are not the only factor for a \
visualization to gain upvotes as beautiful in the r/dataisbeautiful subreddit")
    st.markdown("##### What factors cause a visualization to trend in this subreddit? This would be the same answering what makes the Reddit feed algorithm tag a post as 'rising'?")
    st.markdown("##### To answer this, we collected data in regular intervals over one week to obtain 102 trending posts and 71 non trending posts.")
    st.markdown("##### Let us consider the following metrics")
    st.markdown("##### - Number of Upvotes")
    st.markdown("##### - Number of Downvotes")
    st.markdown("##### - Number of Awards")

with st.container():
    st.subheader("Difference in metrics for trending and non trending posts")
    col_spacer1,col1, col2,col3,col3_spacer = st.columns((.1, 5,5,5, .1))
    with col1:
        df = pd.read_csv('reddit_data.csv')
        df = df.reset_index()
        df['flairs'] = df.flairs.apply(lambda x: 'Original' if x=='OC' else 'Not Original')
        import datetime
        df.time_created = df.time_created.apply(lambda x: datetime.datetime.fromtimestamp(x).hour)
        #df['image'] = df['index'].apply(lambda x: 'http://localhost:8888/files/Desktop/MDS/SI%20649/Group%20Project/Notebooks/images/'+str(x+2)+'.png?_xsrf=2%7Cc9d848e0%7Cdbff42938cb51350c2ae90bc3422db02%7C1646800167')
        df['image'] = df['index'].apply(lambda x:'https://raw.githubusercontent.com/shivanibaskar/SI649-demo/main/scrapedimages/'+str(x+2)+'.png')




        # alter this variable according to the dropdown list
        attribute = 'upvotes'

        df['is_dynamic'] = df.is_dynamic.apply(lambda x: 'Dynamic' if x==1 else 'Static')
        df['is_interactive'] = df.is_interactive.apply(lambda x: 'Interactive' if x==1 else 'Not Interactive')
        df['is_trending'] = df.is_trending.apply(lambda x: 'Trending' if x==1 else 'Not Trending')
        df['downvotes'] = df['total_votes']-df['upvotes']


        # Average of Attribute value for Trending vs Non Trending Chart

        trending_or_not_chart = alt.Chart(df).mark_bar(width=30).encode(
            alt.X('is_trending:N',title='Type of Post',axis=alt.Axis(labelAngle=0)),
            alt.Y('mean(upvotes):Q',title='Avg Number of '+attribute.title()),
        ).properties(
             width = 350,height=300
        ).configure_axis(
            labelFontSize=20,
            titleFontSize=20)
        trending_or_not_chart

    with col2:
        trending_or_not_chart = alt.Chart(df).mark_bar(width=30).encode(
            alt.X('is_trending:N',title='Type of Post',axis=alt.Axis(labelAngle=0)),
            alt.Y('mean(downvotes):Q',title='Avg Number of Downvotes'),
        ).properties(
             width = 350,height=300
        ).configure_axis(
            labelFontSize=20,
            titleFontSize=20)
        trending_or_not_chart

    with col3:
        trending_or_not_chart = alt.Chart(df).mark_bar(width=30).encode(
            alt.X('is_trending:N',title='Type of Post',axis=alt.Axis(labelAngle=0)),
            alt.Y('mean(total_awards):Q',title='Avg Number of Awards'),
        ).properties(
             width = 350,height=300
        ).configure_axis(
            labelFontSize=20,
            titleFontSize=20)
        trending_or_not_chart
    st.markdown("#####   Trending posts gain a lot of attention and on an average, have more upvotes, downvotes and awards than non-trending posts")

  
#Container 1
with st.container():
    st.subheader("How do these metrics correlate with one another?")
    st.markdown("####   \n")
    col_spacer1,col1,spacer, col2,col2_spacer = st.columns((.1, 7,.1,3, .1))
    with col1:
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
            x=alt.X('variable2:O',axis=alt.Axis(title=' ',labelAngle=0)),
            y=alt.Y('variable:O',axis=alt.Axis(title=' '))    
        ).properties(width=750,height=300)

        # Text layer with correlation labels
        # Colors are for easier readability
        text = base.mark_text(size=20).encode(
            text='correlation_label',
            color=alt.condition(
                alt.datum.correlation > 0.5, 
                alt.value('white'),
                alt.value('black')
            )
        )

        # The correlation heatmap itself
        cor_plot = base.mark_rect().encode(
             alt.Color('correlation:Q',title='Correlation',legend=alt.Legend(orient='right')),
        )
        plot1 = (cor_plot + text).configure_axis(labelFontSize=15) 
        st.write(plot1)

    with col2:
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("##### Author Karma doesn't affect the metrics.")
        st.markdown("##### Upvotes, downvotes and total awards have significant positive correlation with each other, supporting the findings in the above graphs.")


        



with st.container():
    st.subheader("Let's explore for different metrics")
    ##create a list of options
    atrribute_options=["Upvotes","Downvotes","Total Number of Awards"]
    ##create a select box
    
    col_spacer1,col1, col2,col3,col3_spacer = st.columns((.1, 5,5,5, .1))
    with col1:
        atrribute_selectbox = st.selectbox(label="Select an attribute to display",options=atrribute_options)
        if (atrribute_selectbox == atrribute_options[0]) :
            attribute = 'upvotes'
        elif (atrribute_selectbox == atrribute_options[1]) :
            attribute = 'downvotes'
        elif (atrribute_selectbox == atrribute_options[2]) :
            attribute = 'total_awards'
        st.markdown("#### Across different visualization types")
        st.markdown("###### Click on a data point for preview of visualization and its details")

with st.container():
    col_spacer1,col1, col2,col3,col3_spacer = st.columns((.1, 5,5,5, .1))
    with col1:
        # Mosaic Plot 1 - Image Type
        mosaic1 = alt.Chart(df).mark_bar(width=30).\
        encode(
            alt.X('is_dynamic:N',title='Image type',axis=alt.Axis(labelAngle=0)),
            alt.Y('mean('+attribute+'):Q',title='Avg Number of '+attribute.title()),
            alt.Color('is_trending:N',title=' ',legend=alt.Legend(orient='top')),
            ).\
        properties(width=350,height=350).configure_axis(
            labelFontSize=20,
            titleFontSize=20).configure_legend(titleColor='black', titleFontSize=18,labelFontSize=18) 
        mosaic1

    with col2:
        # Mosaic Plot 2 - Interactivity Type 
        mosaic2 = alt.Chart(df).mark_bar(width=30).\
        encode(
            alt.X('is_interactive:N',title='Interactivity Type',axis=alt.Axis(labelAngle=0)),
            alt.Y('mean('+attribute+'):Q',title='Avg Number of '+attribute.title()),
            alt.Color('is_trending:N',title=' ',legend=alt.Legend(orient='top')),
            ). \
        properties(width=350,height=350).configure_axis(
            labelFontSize=20,
            titleFontSize=20).configure_legend(titleColor='black', titleFontSize=18,labelFontSize=18)
        mosaic2


    with col3:
        # Mosaic Plot 3 - Original Content
        mosaic3 = alt.Chart(df).mark_bar(width=30).\
        encode(
            alt.X('flairs:N',title='Content Type',axis=alt.Axis(labelAngle=0)),
            alt.Y('mean('+attribute+'):Q',title='Avg Number of '+attribute.title()),
            alt.Color('is_trending:N',title=' ',legend=alt.Legend(orient='top')),
            ).\
        properties(width=350,height=350).configure_axis(
            labelFontSize=20,
            titleFontSize=20).configure_legend(titleColor='black', titleFontSize=18,labelFontSize=18) 
        mosaic3


# Getting awards for tooltip
list_of_awards = []
for i in range(len(df)):
    awards = df.iloc[i].awards[1:-2].split('), ')
    award_list = []
    for x in awards:
        award_list.append(x[2:-4])
    list_of_awards.append(','.join(award_list))
df['list_of_awards'] = list_of_awards
df.list_of_awards  = df.list_of_awards.apply(lambda x: x if len(x)>0 else 'None')

with st.container():
    col_spacer1,col1,col2, spacer2 = st.columns((.1, 7,3, .1))
    with col1:
        st.markdown("#### Across different times of day")
        st.markdown("###### Click on a data point for preview of visualization and its details")
        # Scatterplot 1 - By Hour of Creation
        scatterplot1 = alt.Chart(df).mark_circle().\
        encode(
            alt.X('time_created:Q',title='Hour of Day (UTC)',axis=alt.Axis(labelAngle=0),scale = alt.Scale(domain = [min(df.time_created),max(df.time_created)])),
            alt.Y(attribute+':Q',title='Number of '+attribute.title()),
            alt.Color('is_trending:N',title=' ',legend=alt.Legend(orient='top')),
            tooltip=['image',attribute,'flairs','is_dynamic','is_interactive','list_of_awards']
            ). \
        properties(width=700,height=500).configure_axis(
            labelFontSize=20,
            titleFontSize=20).configure_legend(titleColor='black', titleFontSize=18,labelFontSize=18).interactive()

        selection=alt.selection_single(on='mouseover',empty="none");
        sizeCondition=alt.condition(selection,alt.value(400),alt.value(80))
        scatterplot1 = scatterplot1.add_selection(
            selection                       # step 3, chart 1
        ).encode(
            size=sizeCondition,             # step 4, chart 1 (only size)
        )
        scatterplot1

    with col2:
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("##### Posts get better traction when posted between 6 AM and 4 PM UTC.")
        st.markdown("##### Interesting find:")
        st.markdown("##### Even some trending posts are found to have very low values of the considered popularity metric, showing that Reddit considers more information in deciding to tag a post as 'rising'.")
        st.markdown("##### An explanation would be the relative time taken to get each vote/award from the time of posting.")

with st.container():
    col_spacer1,col1,col2, spacer2 = st.columns((.1, 7,3, .1))
    with col1:
        st.markdown("#### For different number of colors in images")
        st.markdown("###### Click on a data point for preview of its major colors (leaving out the most dominant/background color)")
        # Manipulations for second scatter plot
        img_df = pd.read_csv('color_data.csv')
        df['colors'] = img_df['number_of_colors']
        df2 = df.copy()
        #df2['image'] = df2['index'].apply(lambda x: 'http://localhost:8888/files/Desktop/MDS/SI%20649/Group%20Project/Notebooks/piecharts/'+str(x+2)+'.png?_xsrf=2%7Cc9d848e0%7Cdbff42938cb51350c2ae90bc3422db02%7C1646800167')
        df2['image'] = df2['index'].apply(lambda x:'https://raw.githubusercontent.com/shivanibaskar/SI649-demo/main/piecharts/'+str(x+2)+'.png')
        # Scatterplot2 - For number of colors
        scatterplot2 = alt.Chart(df2).mark_circle().\
        encode(
            alt.X('colors:Q',title='Number of Colors',axis=alt.Axis(labelAngle=0),scale = alt.Scale(domain = [min(df.time_created),max(df.time_created)])),
            alt.Y(attribute+':Q',title='Number of '+attribute.title()),
            alt.Color('is_trending:N',title=' ',legend=alt.Legend(orient='top')),
            tooltip=['image',attribute,'colors','flairs','is_dynamic','is_interactive','list_of_awards']
            ). \
        properties(width=700,height=500).configure_axis(
            labelFontSize=20,
            titleFontSize=20).configure_legend(titleColor='black', titleFontSize=18,labelFontSize=18).interactive()

        selection=alt.selection_single(on='mouseover',empty="none");
        sizeCondition=alt.condition(selection,alt.value(400),alt.value(80))
        scatterplot2 = scatterplot2.add_selection(
            selection                       # step 3, chart 1
        ).encode(
            size=sizeCondition,             # step 4, chart 1 (only size)
        )
        scatterplot2

    with col2:
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("##### While not every trending post has a lot of colors, it takes at least 4 colors for a trending post to get an award or to cross 1000 upvotes.")
        st.markdown("##### As we explore the data points looking at their tooltip information, it can be noticed that among the posts with more number of colors, the posts that trend tend to utilize bright and contrasting colors compared to the relatively dull ones in the non trending posts.")


with st.container():
    data['author_has_reddit_premium'] = data.author_has_reddit_premium.apply(lambda x: 'Premium User' if x==1 else 'Not a Premium User')
    col_spacer1,col1,col2, spacer2 = st.columns((.1, 7,3, .1))
    with col1:
        st.markdown("#### What about Reddit Premium users and seasoned users with high 'karma'?")
        plot5=alt.Chart(data).mark_circle(size=60).encode(
        x=alt.X('author_karma:Q',axis=alt.Axis(title="Author Karma"),scale=alt.Scale(domain=[0,400000])),
        y=alt.Y(attribute+':Q',title='Number of '+attribute.title()),
        color=alt.Color('author_has_reddit_premium',legend=alt.Legend(title=" ",orient="top")),
        tooltip = [
             alt.Tooltip(field = attribute, type = "quantitative",title = 'Number of '+attribute.title()),
            alt.Tooltip(field = 'author_karma', type = "quantitative",title = "Author Karma"),
           ]).properties(width=700,height=500)\
            .configure_axis(
            labelFontSize=20,
            titleFontSize=20).configure_legend(titleColor='black', titleFontSize=18,labelFontSize=18).interactive()
        selection=alt.selection_single(on='mouseover',empty="none");
        sizeCondition=alt.condition(selection,alt.value(400),alt.value(80))
        plot5 = plot5.add_selection(
            selection                       # step 3, chart 1
        ).encode(
            size=sizeCondition,             # step 4, chart 1 (only size)
        )
        st.write(plot5)
        
    with col2:
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("####   \n")
        st.markdown("####   \n")
        df['author_has_reddit_premium'] = df.author_has_reddit_premium.apply(lambda x: 'Premium User' if x==1 else 'Not a Premium User')
        mosaic4 = alt.Chart(df).mark_bar(width=30).\
        encode(
            alt.X('author_has_reddit_premium:N',title='Author Acount Type',axis=alt.Axis(labelAngle=0)),
            alt.Y('mean('+attribute+'):Q',title='Avg Number of '+attribute.title()),
            alt.Color('is_trending:N',title=' ',legend=alt.Legend(orient='top')),
            ). \
        properties(width=350,height=350).configure_axis(
            labelFontSize=18,
            titleFontSize=20).configure_legend(titleColor='black', titleFontSize=18,labelFontSize=18)
        mosaic4

with st.container():
    col_spacer1,col1,col2, spacer2 = st.columns((.3, 50,0.1, .1))
    with col1:
        st.markdown("##### While the authors with high karma do not have great posts, it has to be remembered that the correlation map showed no relation between metrics and author karma. The explanation lies in observing that while the users with lower levels of karma have great posts, a majority of the low karma users have mediocre posts lying on the lower end of the votes and awards counts.")


with st.container():
    col_spacer1,col1,col2, spacer2 = st.columns((.1, 7,3, .1))
    with col1:
        st.markdown("#### In summary, what do most trending posts have in common?")
with st.container():
    col_spacer1,col1,col2, spacer2 = st.columns((.3, 50,0.1, .1))
    with col1:
        st.markdown("##### 1. Trending posts are mostly dynamic, interactive and are original content.")
        st.markdown("##### 2. They are posted usually during the times when the rest of the world is active on this subreddit - the first half of the day (before 12 PM EDT).")
        st.markdown("##### 3. Trending posts have bright, constrasting and easily distinguishable colors.")
        st.markdown("##### 4. While the posts of Premium users trend more, there are some non Premium users whose posts perform even better!")


with st.container():
    col_spacer1,col1,col2, spacer2 = st.columns((.1, 7,3, .1))
    with col1:
        st.markdown("###### Thanks for reading this article :)")
        st.markdown("###### Written by Hareeshwar Karthikeyan and Shivani Baskar")
        st.markdown("###### Github repository containing data and analysis [here](https://www.reddit.com/r/dataisbeautiful/)")


