''' sentiment_analysis.py
Simon Kinsey
'''

# Import Required Libraries
import random
import pandas as pd
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# to supress warning about using spacy sm model:
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Configuration
CSV_FILE_PATH = 'amazon_product_reviews.csv'

# Initialize Spacy - requires user to enter choice
def get_spacy_model_choice():
    """
    Prompt the user to choose between 'en_core_web_sm' and 'en_core_web_md'
    models.
    Returns:
        str: The chosen Spacy model name.
    """
    choice = ""
    while choice not in ['1', '2']:
        print('\nChoose a Spacy model to use for analysis:')
        print('1: en_core_web_sm (smaller, faster but no vectors) or')
        print('2: en_core_web_md (medium, more accurate)')
        choice = input("Enter 1 or 2: ").strip()

        if choice not in ['1', '2']:
            print("Invalid choice. Please enter 1 or 2.")

    if choice == '1':
        return 'en_core_web_sm'
    else:
        return 'en_core_web_md'

# Get Preprocessing choices
def get_preprocessing_choices():
    """
    Prompt the user for preprocessing choices and return these choices.
    Returns:
        A dictionary with boolean values for lemmatization, remove
        punctuation and removes_stop_words.
    """
    choices = {
        "lemmatize": False,
        "remove_punctuation": False,
        "remove_stop_words": False
    }
    # function to prompt the user and validate input
    def ask_user_choice(prompt):
        while True:
            choice = input(prompt).lower().strip()
            if choice in ['yes', 'y']:
                return True
            elif choice in ['no', 'n']:
                return False
            else:
                print("Invalid response. Please answer with 'yes' or 'no'.")

    # Ask for each preprocessing choice
    for choice in choices:
        prompt = f"Would you like to {choice.replace('_', ' ')}? (yes/no): "
        choices[choice] = ask_user_choice(prompt)

    return choices

# Data Preprocessing
def load_and_preprocess_data(file_path,
                             lemmatize=False,
                             remove_punctuation=False,
                             remove_stop_words=False, nlp=None):
    """
    Load and preprocess data from CSV file.
    
    Parameters:
        file_path (str): Path to the CSV file.
        lemmatize (bool): If True, lemmatize words.
        remove_punctuation (bool): If True, remove punctuation.
        remove_stop_words (bool): If True, remove stop words.
        nlp (spacy.lang): Loaded spaCy language model.
    """
    # Load data
    data = pd.read_csv(file_path)

    # Check if 'reviews.text' column exists
    if 'reviews.text' not in data.columns:
        raise ValueError("Data does not contain 'reviews.text' column.")

    # Initial preprocessing (lowercasing and stripping spaces)
    data['cleaned_reviews'] = data['reviews.text'].str.lower().str.strip()

    # Further preprocessing based on user choices
    if lemmatize or remove_punctuation or remove_stop_words:
        if not nlp:
            raise ValueError(
                "spaCy model not provided for advanced preprocessing.")
        def preprocess_text(doc):
            tokens = []
            for token in doc:
                if remove_stop_words and token.is_stop:
                    continue
                elif remove_punctuation and token.is_punct:
                    continue
                else:
                    tokens.append(token.lemma_ if lemmatize else token.text)
            return " ".join(tokens)
        # Apply preprocessing
        data['cleaned_reviews'] = data['cleaned_reviews'].apply(
            lambda x: preprocess_text(nlp(x)))
    # Optionally, drop rows where the cleaned text is now empty
    data = data[data['cleaned_reviews'] != '']
    return data[['reviews.text', 'cleaned_reviews']]

# Sentiment Analysis
def analyze_sentiment(text, nlp):
    """
    Analyze sentiment of the given text using the specified spaCy model.
    Returns the polarity score, subjectivity score, and a textual polarity
    rating.
    """
    doc = nlp(text)
    polarity = doc._.polarity
    subjectivity = doc._.subjectivity
    # Determine polarity rating based on polarity score
    if polarity > 0.15:
        polarity_rating = 'positive'
    elif polarity < -0.15:
        polarity_rating = 'negative'
    else:
        polarity_rating = 'neutral'
    return polarity, subjectivity, polarity_rating

# Sentiment summary for printing
def sentiment_analysis(reviews):
    '''
    Calculate the counts of ratings and percentage of total reviews
    by polarity rating
    Returns - formatted string for simple print
    '''
    value_counts = reviews['polarity_rating'].value_counts()
    positive_count = value_counts.get('positive', 0)
    negative_count = value_counts.get('negative', 0)
    neutral_count = value_counts.get('neutral', 0)

    total = reviews['polarity_rating'].count()

    positive_perc = (positive_count / total) * 100 if total else 0
    negative_perc = (negative_count / total) * 100 if total else 0
    neutral_perc = (neutral_count / total) * 100 if total else 0

    result_string = (
        'Overall counts of reviews by polarity rating:\n'
        f'Positive ratings: {positive_count: }\n'
        f'Negative ratings: {negative_count: }\n'
        f'Neutral ratings: {neutral_count: }\n\n'

        'Sentiment analysis percentages of total:\n'
        f'Positive ratings: {positive_perc:.2f}%\n'
        f'Negative ratings: {negative_perc:.2f}%\n'
        f'Neutral ratings: {neutral_perc:.2f}%\n'
        )
    return result_string

# Word Cloud Visualization
def create_word_cloud(text):
    """
    Create and display a word cloud from text.
    """
    wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = set(spacy.lang.en.stop_words.STOP_WORDS),
                min_font_size = 10).generate(text)
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()

# random review sentiment test
def test_random_review_sentiment(reviews, analyze_sentiment_fn, nlp):
    '''tests a random review statement for sentiment and prints results'''
    # Ensure there's at least one review
    if reviews.empty:
        print('No reviews to analyze.')
        return

    # Select a random review
    random_index = random.randint(0, len(reviews) - 1)
    selected_review = reviews.iloc[random_index]
    original_text = selected_review['reviews.text']
    cleaned_text = selected_review['cleaned_reviews']

    # Use the existing analyze_sentiment function
    polarity, subjectivity, polarity_rating = analyze_sentiment_fn(
        cleaned_text, nlp)

    # Print the results
    print(f'Original review (index {random_index}):\n"{original_text}"\n')
    print(f'Sentiment analysis results: Polarity = {polarity:.2f}, '
          f'Subjectivity = {subjectivity:.2f}, Rating = {polarity_rating}\n')


# Similarity Check
def test_random_review_similarity(reviews, nlp):
    '''tests 2 random review statements for similarity and prints results'''
    if len(reviews) < 2:
        print('Not enough reviews to compare.')
        return

    indices = random.sample(range(len(reviews)), 2)
    review_texts = [reviews.iloc[idx]['reviews.text'] for idx in indices]
    docs = [nlp(text) for text in review_texts]

    similarity = docs[0].similarity(docs[1])

    print(f'Comparing review {indices[0]} and review {indices[1]}:')
    print(f'Review {indices[0]}: "{review_texts[0]}"')
    print(f'Review {indices[1]}: "{review_texts[1]}"')
    print(f'Similarity score: {similarity:.2f}'
          f' (0 = "completely different" to 1 = "identical")\n')


# Main Function
def main():
    '''main'''
    # Show intro and user instructions
    print('\nThis program analyses a file called amazon_products_review.csv.\n'
          'The csv file is provided and needs to be in the same directory\n'
          'as this python file. \n\n'
          'After analysing the amazon_products_review.csv file it also\n'
          'tests a random review for sentiment (polarity) and then checks\n'
          'the similarity of 2 random reviews.\n'
          'The program also requires that you already have "corpora"\n'
          'loaded for Spacytextblob and that the Spacy en_core_web_sm and/or\n'
          'or en_core_web_md libraries are available'
          '(your choice)...'
          )

    # Get Spacy model choice and load and also spacytextblob
    spacy_model_choice = get_spacy_model_choice()
    print(f'You have chosen {spacy_model_choice}. Loading model...\n')
    nlp = spacy.load(spacy_model_choice)
    nlp.add_pipe('spacytextblob')

    # Load and preprocess data
    user_choices = get_preprocessing_choices()

    print('Loading data and preprocessing...\n')
    reviews = load_and_preprocess_data(
        CSV_FILE_PATH,
        lemmatize = user_choices["lemmatize"],
        remove_punctuation = user_choices['remove_punctuation'],
        remove_stop_words = user_choices['remove_stop_words'],
        nlp=nlp
    )

    # Analyze sentiment of reviews
    print('Analysing sentiment of processed data...please be patient...\n')
    # Analyze sentiment and directly add results to the DataFrame
    reviews[['polarity', 'subjectivity', 'polarity_rating']] = (
            reviews['cleaned_reviews'].apply(lambda x: analyze_sentiment(x, nlp))
            .apply(pd.Series)
    )

    # Print sentiment analysis results
    print(sentiment_analysis(reviews))

    # Display word cloud for positive sentiment reviews (example)
    print('Word cloud to assist with visualising the review words...\n'
          '...Close the word cloud window when you have finished with it.\n')
    # Using the 'polarity_rating' column
    positive_reviews = ' '.join(reviews[reviews['polarity_rating']
                                == 'positive']['cleaned_reviews'])
    create_word_cloud(positive_reviews)

    # Test sentiment analysis on a random review
    print('Now we will test a random review using the '
          'model for polarity/sentiment analysis:')
    test_random_review_sentiment(reviews, analyze_sentiment, nlp)

    # Test similarity between two random reviews
    print('Now we will test 2 random reviews for similarity:')
    test_random_review_similarity(reviews, nlp)

    print ('Program finished :)...')
if __name__ == "__main__":
    main()
