from textblob import TextBlob
import nltk

# Get user input as the article text
text = input("Enter the text to analyze sentiment: ")

# Perform NLP tasks
nltk.download('punkt')  # Download the NLTK tokenizer (only once)

# Create a TextBlob object for sentiment analysis
obj = TextBlob(text)

# Compute the sentiment polarity of the user input text
sentiment = obj.sentiment.polarity

# Print the sentiment analysis result
if sentiment == 0:
    print('The text is Neutral')
elif sentiment > 0:
    print('The text is Strongly Positive')
else:
    print('The text is Strongly Negative')
