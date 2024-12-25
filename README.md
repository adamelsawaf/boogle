# Boogle

This program is an implementation of a small-scale search engine, called Boogle. To run it, simply run the Bash command
python3 boogle.py

To display a simple small example to help visualize a trie, run
python3 boogle.py small_example

To display this help message on the terminal, run
python3 boogle.py help

Boogle utilizes an inverted index together with a trie data structure to store the lexicographic data of each webpage.
The human-readable data of each of these webpages is preprocessed and parsed, then tokenized at the word-level in order
to be stored in the trie and inverted index. This computational model allows efficient storage and fast retrieval of
the data held by the webpages provided in the database that is kept in input.txt. The external node of every word stored
in the trie is its corresponing index in the inverted index. The inverted index is cached as a list of tuples, where the
first element of each of these tuples is a string, and the second element of each of these tuples is a dictionary of
integers. Each element of the inverted index will store the set of webpages that contain a given word, and how many times
each of those webpages contain that word. Each webpage is stored as the corresponing index of its URL in input.txt, where
each of its lines is a URL. See inverted_index.txt for an example of what the inverted index looks like.
