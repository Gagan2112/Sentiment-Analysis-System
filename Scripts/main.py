import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Sentiment Analysis System",page_icon="https://cdn.iconscout.com/icon/premium/png-256-thumb/expression-3118033-2607314.png")
st.title("SENTIMENT ANALYSIS SYSTEM")
choice=st.sidebar.selectbox("My Menu",("HOME","ANALYSIS","RESULT"))
if(choice=="HOME"):
    st.image("https://i.pinimg.com/originals/52/ad/6a/52ad6a11c1dcb1692ff9e321bd520167.gif")
elif(choice=="ANALYSIS"):
    sid=st.text_input("Enter Sheet ID")
    r=st.text_input("Enter Range of columns from user")
    c=st.text_input("Enter the column to be analyzed")
    btn=st.button("Analyze")
    if btn:
        if "cred" not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file("key.json",['https://www.googleapis.com/auth/spreadsheets'])
            st.session_state['cred']=f.run_local_server()
        service=build('sheets','V4',credentials=st.session_state['cred']).spreadsheets().values()
        d=service.get(spreadsheetId=sid,range=r).execute()
        d=d['values']
        df=pd.DataFrame(columns=d[0],data=d[1:])
        print(df)
        mymodel=SentimentIntensityAnalyzer()
        l=[]
        for i in df[c]:
            pred=mymodel.polarity_scores(i)
            if(pred['compound']>0.5):
                l.append('Positive')
            elif(pred['compound']<-0.5):
                l.append("Negative")
            else:
                l.append("Neutral")
        df['Sentiment']=l
        df.to_csv("Results.csv",index=False)
        st.header("The Analysis results are saved by the file name Results.csv")
if(choice=="RESULT"):
    df=pd.read_csv("Results.csv")
    st.dataframe(df)    
    choice2=st.selectbox("Choose Visualization",("NONE","PIE","HISTOGRAM"))
    if(choice2=="PIE"):
        posper=(len(df[df['Sentiment']=="Positive"])/len(df))*100
        negper=(len(df[df['Sentiment']=="Negative"])/len(df))*100
        neuper=(len(df[df['Sentiment']=="Neutral"])/len(df))*100
        fig=px.pie(values=[posper,negper,neuper],names=['Positive','Negative','Neutral'])
        st.plotly_chart(fig)
    elif(choice2=="HISTOGRAM"):
        k=st.selectbox("Choose a column",df.columns)
        if k:
            fig=px.histogram(x=df[k],color=df['Sentiment'])
            st.plotly_chart(fig)
    
        
   
        
        