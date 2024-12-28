from bs4      import BeautifulSoup
from requests import get as requests_get
from bisect   import insort
from sys      import argv, exit as sys_exit
from copy     import deepcopy


#  display the help message on the terminal and exit the program
if((len(argv) == 2) and (argv[1].lower() == "help")):
    readme_file = open("README.txt", "r")
    print(readme_file.read(), end="")
    readme_file.close()
    sys_exit()


class TrieNode:
    def __init__(self, value: str | int = "[ROOT]") -> None:
        self.value: str | int = value
        self.children: list[TrieNode] = []
        self.size: int = 1         #  total number of nodes in the trie
        self.wordCount: int = 0    #  total number of words (non-root leaves) in the trie, i.e. the number of nodes with integer values

    #  This method inserts the given word into the trie (nothing is inserted if the word is already in the trie),
    #  and returns the value of the leaf node of that word in the trie (this value is equal to the number of words
    #  that were in the trie before that word was inserted into the trie).
    def insert(self, word: str) -> int:
        def insertHelper(node: TrieNode = self, w: str = word) -> int:
            if(w == ""):
                for child in node.children:
                    if(type(child.value) == int):
                        return child.value   #  the trie already contains the word
                insort(node.children, TrieNode(self.wordCount), key = lambda n: str(n.value))
                self.size += 1
                self.wordCount += 1
                return self.wordCount - 1
                
            for child in node.children:
                if(child.value == w[0]):
                    return insertHelper(child, w[1:])
            insort(node.children, currentNode := TrieNode(w[0]), key = lambda n: str(n.value))
            for letter in w[1:]:
                currentNode.children = [TrieNode(letter)]
                currentNode = currentNode.children[0]
            currentNode.children = [TrieNode(self.wordCount)]
            self.size += len(w) + 1
            self.wordCount += 1
            return self.wordCount - 1
        
        return insertHelper()
    
    #  If the given word is in the trie, this method returns the value of the leaf node of that word in the trie (which
    #  is its corresponding index in the inverted index). But if the word is not in the trie, this method returns -1.
    def search(self, word: str) -> int:
        if((word == "")):
            for child in self.children:
                if(type(child.value) == int):
                    return child.value
            return -1
        for child in self.children:
            if(child.value == word[0]):
                return TrieNode.search(child, word[1:])
        return -1
    
    #  returns all the words in the trie in alphabetical order
    def getAllWords(self) -> list[str]:
        result = []
        def getAllWordsHelper(node: TrieNode = self, wordSoFar: str = "") -> None:
            nonlocal result
            for child in node.children:
                if(type(child.value) == int):
                    result += [wordSoFar]
                else:
                    getAllWordsHelper(child, wordSoFar + child.value)
        
        getAllWordsHelper()
        return result

    def __str__(self) -> str:
        result = ""
        def strHelper(node: TrieNode = self, flags: list[bool] = self.size*[True], depth: int = 0, isLast: bool = False) -> None:
            nonlocal result
            for i in range(1, depth):
                if(flags[i] == True):
                    result += "|"
                result += 4*" "

            if(depth == 0):
                result += str(node.value) + "\n"
            else:
                result += "+---" + str(node.value) + "\n"
                if(isLast):
                    flags[depth] = False
        
            it = 0
            for child in node.children:
                it += 1
                strHelper(child, flags, depth + 1, it == (len(node.children) - 1))
            flags[depth] = True
        
        strHelper()
        return result


#  display small test trie example to the terminal and exit the program
if((len(argv) == 2) and (argv[1].lower() == "small_example")):
    print("Constructing trie...")
    testTrie = TrieNode()
    testTrie.insert("hello")
    testTrie.insert("world")
    testTrie.insert("good")
    testTrie.insert("golf")
    testTrie.insert("glowing")
    testTrie.insert("big")
    testTrie.insert("bigger")
    print("Printing trie:\n")
    print(testTrie)
    print("Number of nodes in trie:", testTrie.size)
    print("Number of words in trie:", testTrie.wordCount)
    print("All words in trie:", testTrie.getAllWords())
    print("\nTesting words for the values of their external nodes in the trie:")
    print("hello:   ", testTrie.search("hello"))
    print("world:   ", testTrie.search("world"))
    print("good:    ", testTrie.search("good"))
    print("golf:    ", testTrie.search("golf"))
    print("glowing: ", testTrie.search("glowing"))
    print("big:     ", testTrie.search("big"))
    print("bigger:  ", testTrie.search("bigger"))
    print("bruh:   " , testTrie.search("bruh"))
    print("goodbye:" , testTrie.search("goodbye"))
    print("hell:   " , testTrie.search("hell"))
    print("worlds: " , testTrie.search("worlds"))
    print("worldly:" , testTrie.search("worldly"))
    print("a:      " , testTrie.search("a"))
    print("g:      " , testTrie.search("g"))
    print("good:    ", testTrie.search("good"))
    print("hell:   " , testTrie.search("hell"))
    sys_exit()


def formatRGB(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

GREEN    : str = formatRGB(  0, 255,   0)
RED      : str = formatRGB(255,   0,   0)
BLUE     : str = formatRGB(  0,   0, 255)
YELLOW   : str = formatRGB(255, 255,   0)
DEFAULT  : str = "\033[0m"
BOLD     : str = "\033[1m"
ITALICS  : str = "\033[3m"
UNDERLINE: str = "\033[4m"

SEARCH_ENGINE_NAME       : str       = "Boogle"
SEARCH_ENGINE_NAME_COLORS: list[str] = [BLUE, RED, YELLOW, BLUE, GREEN, RED]


#  display the error message if there are any other command-line arguments
if(len(argv) >= 2):
    print(f"{RED}Unrecognized arguments.{DEFAULT}\n")
    readme_file = open("README.txt", "r")
    print(readme_file.read(), end="")
    readme_file.close()
    sys_exit(1)

print("Booting up...", end="", flush=True)

def searchEngineName(searchEngineName: str = SEARCH_ENGINE_NAME, colors: list[str] = SEARCH_ENGINE_NAME_COLORS, incognito: bool = False) -> str:
    result = DEFAULT + BOLD
    for i in range(len(searchEngineName)):
        result += (colors[i] if not incognito else "") + searchEngineName[i]
    return result + DEFAULT


inputFile = open("input.txt", "r")
urls: str = inputFile.read().split("\n")
inputFile.close()

webpage_texts : list[list[str]] = []
webpage_titles: list[str]       = []

#  punctuation here does not include the apostrophe ('), since contractions and possesives (like "can't" and "Dijkstra's") use them and are very common in English
PUNCTUATION_MARKS: str = ".,!?‽;:…\"()[]{}-–—*/\\|&~#^@%‰‱•<>$+=§"
for url in urls:
    #  use each given webpage url to generate the HTML of that webpage
    webpage_html: BeautifulSoup = BeautifulSoup(
                        (
                            requests_get(
                                    url,
                                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
                            )
                        ).text,
                        features="lxml"
                   )
    webpage_titles += [webpage_html.title.string]

    #  text preprocessing for later parsing: remove all punctuation from the human-readable text of each webpage's HTML,
    #  and make all that text lowercase, for standardization
    webpage_text: str = webpage_html.get_text()
    for puncationMark in PUNCTUATION_MARKS:
        webpage_text = webpage_text.replace(puncationMark, " ")
    webpage_texts += [webpage_text.lower().split()]
    print(".", end="", flush=True)


#  the trie will store all the words in the webpages, where the leaves store their position in the inverted index
trie: TrieNode = TrieNode()

"""
The inverted index is a list of tuples, where the first element of each of these tuples is a string, and the
second element of each of these tuples is a dictionary of integers. Each element of the inverted index will store
the set of webpages that contain a given word, and how many times each of those webpages contain that word. Each
webpage is stored as the corresponing index of its URL in input.txt, where each of its lines is a URL.
See inverted_index.txt for an example of what the inverted index looks like.
"""
inverted_index: list[tuple[str, dict[int, int]]] = []

for i in range(len(webpage_texts)):
    for word in webpage_texts[i]:   #  for each word in each webpage human-readable text (the parser isn't perfect, but this is just because )
        trie.insert(word)     #  add that word to the global trie, if it's not there already
        for pair in inverted_index:
            if(pair[0] == word):
                #  increment the webpage's dictionary entry for that word in the inverted index, or create it if it doesn't already exist
                pair[1][i] = pair[1].get(i, 0) + 1
                break
        else:   #  but first add the word to the inverted index if it's not there already
            inverted_index += [(word, {i: 1})]
    print(".", end="", flush=True)

#  copy the inverted index to a file, line by line
inverted_index_file = open("inverted_index.txt", "w")
inverted_index_file.writelines([str(pair) + "\n" for pair in inverted_index[:-1]])
inverted_index_file.write(str(inverted_index[-1]))
inverted_index_file.close()

print(".\n", flush=True)
print(boogleHelpMessage := f"""Hello! Welcome to {SEARCH_ENGINE_NAME}, everyone's favorite search engine! Just type what you want to search for, then press enter. A list of
webpages relating to your query will then be displayed to you, with the best ones at the top. You can make as many searches as you want.
Enter the query "/history" to view your search history.
Enter the query "/clear_history" to clear your search history.
Enter the query "/incognito" to toggle incognito mode, where your search history won't be saved or stored (off by default).
Enter the query "/exit" to exit Boogle.
Enter the query "/help" to display this message again.\n""")
userSearchHistory: list[str] = []
userIncognito    : bool      = False
noResultsMessage : str       = """No results were found for this query. Check your spelling, or try using fewer, more general, or different keywords?
Capitalization, punctuation, and extra spaces shouldn't matter.\n"""

while(True):
    userQuery: str = input(searchEngineName(incognito=userIncognito) + ": ").strip()
    if(userQuery == ""):
        continue
    if(userQuery.lower() == "/incognito"):
        userIncognito = not userIncognito
        print("Incognito mode has been turned " + (f"{GREEN}on{DEFAULT}.\n" if userIncognito else f"{RED}off{DEFAULT}.\n"))
        continue
    elif(userQuery.lower() == "/clear_history"):
        userSearchHistory = []
        print("Your search history has been cleared.\n")
        continue
    elif(not userIncognito): 
        userSearchHistory += [userQuery]
    if((userQuery := userQuery.lower()) == "/history"):
        print("Your search history:")
        if(userSearchHistory == []):
            print("[empty]\n")
        else:
            for i in range(len(userSearchHistory)):
                print((len(str(len(userSearchHistory))) - len(str(i+1))) * " " + f"{i+1}. {userSearchHistory[i]}")
            print()
        continue
    if(userQuery == "/exit"):
        sys_exit("\nThank you for using Boogle, come again soon!")
    if(userQuery == "/help"):
        print(boogleHelpMessage)
        continue
    for puncationMark in PUNCTUATION_MARKS:
        userQuery = userQuery.replace(puncationMark, " ")
    if((userQuery := userQuery.strip()) == ""):
        print(noResultsMessage)
        continue


    userTokens: list[str] = userQuery.split()

    #  the dictionary of output webpages is initally the webpages for just the first user-inputted keyword (which at this point we know must exist)
    if((firstOD_index := trie.search(userTokens[0])) == -1):  #  first occurence dictionary's index
        #  the first user-inputted keyword is not in any of the webpages
        print(noResultsMessage)
        continue
    else:
        outputWebpages: dict[int, int] = deepcopy(inverted_index[firstOD_index][1])

    #  now compute the intersection that incorporates the rest of the user-inputted keywords (after the first one)
    for token in userTokens[1:]:
        currentOD: dict[int, int] = inverted_index[trie.search(token)][1]   #  current occurence dictionary
        for webpage in tuple(outputWebpages):
            if(webpage in currentOD):
                outputWebpages[webpage] += currentOD[webpage]
            else:
                del outputWebpages[webpage]
    if(outputWebpages == {}):
        print(noResultsMessage)
    else:
        outputWebpages = dict(sorted(outputWebpages.items(), key = lambda x: x[1], reverse=True))
        for (i, matches) in outputWebpages.items():
            print(f"{BOLD}{webpage_titles[i]}{DEFAULT} ({matches} {'matches' if matches > 1 else 'match'})\n   {ITALICS}{UNDERLINE}{urls[i]}{DEFAULT}\n")
