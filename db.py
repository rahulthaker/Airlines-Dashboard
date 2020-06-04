import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px


data_path='D://Tweets.csv'
@st.cache(persist=True)
def load_data():
    data=pd.read_csv(data_path)
    data['tweet_created']=pd.to_datetime(data['tweet_created'])
    return data

data=load_data()
st.title('Sentiment analysis of  tweets about US airlines')
st.sidebar.title('Sentiment analysis of tweets ')
st.sidebar.markdown('This dashboard gives filters and control over the data visuals of tweets 🐦'
                    'Be sure to uncheck the HIDE button to see visuals')
st.sidebar.subheader('show random tweet')
random_tweet=st.sidebar.radio('Sentiment',('positive','negative','neutral'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown('### Number of tweets by Sentiments')
select=st.sidebar.selectbox('Visualization Type',['Histogram','Pychart'])
sentiment_count=data['airline_sentiment'].value_counts()
sentiment_count=pd.DataFrame({'Sentiment':sentiment_count.index,'Tweets':sentiment_count.values})

if not st.sidebar.checkbox('Hide',True):
    st.markdown('### Nummber of tweets by sentiment')
    if select== 'Histogram':
        fig=px.bar(sentiment_count,x='Sentiment',y='Tweets',color='Tweets',height=500)
        st.plotly_chart(fig)
    else:
        fig=px.pie(sentiment_count,values='Tweets',names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader('When and where are the users tweeting from?')
hour=st.sidebar.slider("Hour of day",1,23)
modified_data=data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox('Hide',True,key=1):
    st.markdown('### Tweets location based on the time of the day')
    st.markdown('%i tweets between %i:00 and %i:00' %(len(modified_data),hour,(hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox('Show raw data',False):
        st.write(modified_data)

st.sidebar.subheader('Breakdown airline tweets by sentiments')
choice=st.sidebar.multiselect('Pick airlines',['US Airways','United','American','Southwest','Delta','Virgin America'],key=0)

if len(choice)>0:
    choice_data=data[data.airline.isin(choice)]
    fig_choice=px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment',
                            facet_col='airline_sentiment',labels={'airline_sentiment':'Tweets'},height=600,width=800)
    st.plotly_chart(fig_choice)

