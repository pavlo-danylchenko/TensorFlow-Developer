import io
import wget
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# url = 'https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz'
print(f' TF Version = {tf.__version__ }')

# Load the IMDB Reviews dataset
imdb, info = tfds.load('imdb_reviews', with_info=True, as_supervised=True)

# Print information about the dataset
print(f'INFO = {info}')

# Print the contents of the dataset you downloaded
print(imdb)

# Take 2 training examples and print its contents
for example in imdb['train'].take(2):
    print(example)

# Get the train and test sets
train_data, test_data = imdb['train'], imdb['test']

# Initialize sentences and labels lists
training_sentences = []
training_labels = []

testing_sentences = []
testing_labels = []

# Loop over all training examples and save the sentences and labels
for s,l in train_data:
    training_sentences.append(s.numpy().decode('utf8'))
    training_labels.append(l.numpy())

# Loop over all test examples and save the sentences and labels
for s,l in test_data:
    testing_sentences.append(s.numpy().decode('utf8'))
    testing_labels.append(l.numpy())

# Convert labels lists to numpy array
training_labels_final = np.array(training_labels)
testing_labels_final = np.array(testing_labels)

# Parameters
vocab_size = 10000
max_length = 120
embedding_dim = 16
trunc_type='post'
oov_tok = "<OOV>"

# Initialize the Tokenizer class
tokenizer = Tokenizer(oov_token=oov_tok, num_words=vocab_size)

# Generate the word index dictionary for the training sentences
tokenizer.fit_on_texts(training_sentences)
# word_index = tokenizer.word_index

# Generate and pad the training sequences
sequences = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequences, truncating=trunc_type, maxlen=max_length)

# Generate and pad the test sequences
testing_sequences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(testing_sequences, maxlen=max_length, truncating=trunc_type)

# Build the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(10, activation='relu'),
    #tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Setup the training parameters
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Print the model summary
model.summary()

num_epochs = 10

history = model.fit(padded,
                    training_labels_final,
                    epochs=num_epochs,
                    validation_data=(testing_padded, testing_labels_final)
                    )

# # Get the embedding layer from the model (i.e. first layer)
# embedding_layer = model.layers[0]
#
# # Get the weights of the embedding layer
# embedding_weights = embedding_layer.get_weights()[0]
#
# # Print the shape. Expected is (vocab_size, embedding_dim)
# print(f'Embedding Shape = {embedding_weights.shape}')
#
# # Get the index-word dictionary
# reverse_word_index = tokenizer.index_word
#
# # Open writeable files
# out_v = io.open('../../sources/vecs.tsv', 'w', encoding='utf8')
# out_m = io.open('../../sources/meta.tsv', 'w', encoding='utf8')
#
# # Initialize the loop. Start counting at `1` because `0` is just for the padding
# for word_num in range(1, vocab_size):
#   # Get the word associated at the current index
#   word_name = reverse_word_index[word_num]
#
#   # Get the embedding weights associated with the current index
#   word_embedding = embedding_weights[word_num]
#
#   # Write the word name
#   out_m.write(word_name + "\n")
#
#   # Write the word embedding
#   out_v.write("\t".join([str(x) for x in word_embedding]) + "\n")
#
# out_v.close()
# out_m.close()
