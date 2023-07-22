import nltk
from tb import TextBlob

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def analyze_sentiment_nltk(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Initialize lists to store positive and negative words
    positive_words = []
    negative_words = []

    # Load a list of positive and negative words (you can create your own lists)
    with open('positive_words.txt', 'r') as f:
        positive_words = f.read().splitlines()
    with open('negative_words.txt', 'r') as f:
        negative_words = f.read().splitlines()

    # Initialize sentiment score
    sentiment_score = 0

    # Analyze sentiment for each sentence using positive and negative words
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        positive_count = sum(1 for word in words if word.lower() in positive_words)
        negative_count = sum(1 for word in words if word.lower() in negative_words)
        sentiment_score += (positive_count - negative_count)

    # Determine overall sentiment
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

def analyze_sentiment_textblob(text):
    # Create a TextBlob object
    blob = TextBlob(text)

    # Get the sentiment polarity (ranging from -1 to 1)
    sentiment_polarity = blob.sentiment.polarity

    # Determine overall sentiment
    if sentiment_polarity > 0:
        return "Positive"
    elif sentiment_polarity < 0:
        return "Negative"
    else:
        return "Neutral"

if __name__ == "__main__":
    text_to_analyze = "I love this product! It's amazing."

    # Using NLTK for sentiment analysis
    nltk_sentiment = analyze_sentiment_nltk(text_to_analyze)
    print("Sentiment using NLTK:", nltk_sentiment)

    # Using TextBlob for sentiment analysis
    textblob_sentiment = analyze_sentiment_textblob(text_to_analyze)
    print("Sentiment using TextBlob:", textblob_sentiment)

