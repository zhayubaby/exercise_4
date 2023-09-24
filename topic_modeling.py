import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import gensim
from gensim import corpora
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

# Download NLTK data (if not already downloaded)
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Load the text of "Alice's Adventures in Wonderland"
alice_text = gutenberg.raw("carroll-alice.txt")

# Tokenize the text
tokens = word_tokenize(alice_text)

# Remove stopwords and punctuation
stop_words = set(stopwords.words("english"))
filtered_tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]

# Lemmatize the words
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

# Create a dictionary and a corpus
dictionary = corpora.Dictionary([lemmatized_tokens])
corpus = [dictionary.doc2bow(lemmatized_tokens)]

# Build the LDA model
lda_model = gensim.models.LdaModel(corpus, num_topics=5, id2word=dictionary)

# Visualize the topics using pyLDAvis
lda_display = gensimvis.prepare(lda_model, corpus, dictionary, sort_topics=False)
pyLDAvis.display(lda_display)
