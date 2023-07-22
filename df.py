import pandas as pd

df=pd.read_csv("mouthshut_reviews.csv")

df['sentiment_analysis']=None

df.columns=["Comment","Profile_Link","Stars","Sentiment_Analysis"]
num_rows, num_columns = df.shape
print(df)

for i in range(0,num_rows):
    df.iloc[i]['Sentiment_Analysis']=