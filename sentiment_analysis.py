from textblob import TextBlob
import nltk
import pandas as pd

df = pd.read_csv("mouthshut_reviews.csv")

# Initialize a new column with None values
df['Sentiment_Analysis'] = None

num_rows, num_columns = df.shape

nltk.download('punkt')

for i in range(0, num_rows):
    text = df.loc[i, 'Comment']
    stars = df.loc[i, 'Stars']

    # Perform sentiment analysis using TextBlob polarity
    obj = TextBlob(text)
    sentiment_polarity = obj.sentiment.polarity

    # Determine Sentiment_Analysis based on both Comment and Stars
    if stars in [1, 2]:
        df.at[i, 'Sentiment_Analysis'] = "Negative"
    elif stars == 3:
        df.at[i, 'Sentiment_Analysis'] = "Neutral"
    elif stars in [4, 5]:
        if sentiment_polarity > 0:
            df.at[i, 'Sentiment_Analysis'] = "Positive"
        elif sentiment_polarity < 0:
            df.at[i, 'Sentiment_Analysis'] = "Negative"
        else:
            df.at[i, 'Sentiment_Analysis'] = "Neutral"


df1=df.copy()

condition = df['Sentiment_Analysis'] == 'Positive'

df2 = df.drop(df[condition].index, inplace=True)


#df1-->before filtering
#df-->after filtering

#print("before filtering:", df1)
#print("after filtering:", df)

df1.to_csv("before_filter.csv", index=False)
df.to_csv("after_filter.csv", index=False)