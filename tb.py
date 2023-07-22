from textblob import TextBlob
import nltk
import pandas as pd


df=pd.read_csv("mouthshut_reviews.csv")

df['sentiment_analysis']=None

df.columns=["Comment","Profile_Link","Stars","Sentiment_Analysis"]
num_rows, num_columns = df.shape

nltk.download('punkt') 


for i in range(0,num_rows):
    text=df.loc[i,'Comment']
    obj = TextBlob(text)
    sentiment = obj.sentiment.polarity


    if sentiment == 0:
        df.at[i, 'Sentiment_Analysis']="Neutral"
    elif sentiment > 0:
        df.at[i, 'Sentiment_Analysis']="Positive"
    else:
        df.at[i, 'Sentiment_Analysis']="Negative"

print(df)
