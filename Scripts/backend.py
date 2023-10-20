import pandas as pd
import plotly.express as px
df=pd.read_csv('Results.csv')
#Pie chart
fig=px.histogram(x=df['Gender'],color=df['Sentiment'])
fig.show()





