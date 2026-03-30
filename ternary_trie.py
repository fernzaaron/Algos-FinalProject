#ternary search trie implementation for text autocompletion

class TSTNode:
    def __init__(self, char):
        self.char = char  # the actual character stored in this node
        self.left = None  # smaller characters go here
        self.mid = None   # next character in the word goes here
        self.right = None  # larger characters go here
        self.is_end_of_word = False


class TernaryTrie:
    def __init__(self):
        self.root = None  # tree starts empty
        self.freq = {}  # keep track of how often words get searched

    def insert(self, word):
        """add word to the ternary trie"""
        word = word.lower()
        # start inserting from the root
        self.root = self._insert_helper(self.root, word, 0)

    def _insert_helper(self, node, word, idx):
        """recursively insert word into tst"""
        char = word[idx]
        
        # create new node if needed
        if node is None:
            node = TSTNode(char)
        
        # compare with current character to decide which branch to go
        if char < node.char:
            # this char comes before current char alphabetically
            node.left = self._insert_helper(node.left, word, idx)
        elif char > node.char:
            # this char comes after current char alphabetically
            node.right = self._insert_helper(node.right, word, idx)
        else:
            # character matches, now handle next character
            if idx + 1 < len(word):
                # there's another character, go down middle branch
                node.mid = self._insert_helper(node.mid, word, idx + 1)
            else:
                # we're done with the word
                node.is_end_of_word = True
        
        return node

    def search(self, prefix):
        """find all words starting with prefix"""
        prefix = prefix.lower()
        # navigate to where the prefix ends in the tree
        node = self._find_prefix(self.root, prefix, 0)
        
        if node is None:
            # prefix doesn't exist
            return []
        
        # collect all words from this node
        words = []
        def dfs(n, word, explore_siblings):
            if n is None:
                return
            
            # explore alternatives only for children, not the initial prefix node
            if explore_siblings:
                dfs(n.left, word, True)
                dfs(n.right, word, True)
            
            # add current node's character to build the word
            full_word = word + n.char
            
            # check if this marks end of word
            if n.is_end_of_word:
                words.append(full_word)
            
            # traverse mid to next position  
            dfs(n.mid, full_word, True)
        
        # start dfs: don't explore siblings of prefix node,
        # only of its descendants
        dfs(node, prefix[:-1], False)
        
        # update how many times each word has been searched
        for w in words:
            self.freq[w] = self.freq.get(w, 0) + 1
        return words

    def _find_prefix(self, node, prefix, idx):
        """find node at end of prefix"""
        if node is None:
            return None
        
        char = prefix[idx]
        
        # navigate the tree based on character comparison
        if char < node.char:
            return self._find_prefix(node.left, prefix, idx)
        elif char > node.char:
            return self._find_prefix(node.right, prefix, idx)
        else:
            # character matches
            if idx + 1 < len(prefix):
                # more characters in prefix to find
                return self._find_prefix(node.mid, prefix, idx + 1)
            # found where prefix ends
            return node

    def autocomplete(self, prefix):
        """show suggestions for prefix"""
        suggestions = self.search(prefix)
        # sort by popularity first, then alphabetical order
        suggestions.sort(key=lambda w: (-self.freq.get(w, 0), w))
        
        print(f"suggestions for '{prefix}':")
        if suggestions:
            for i, word in enumerate(suggestions, 1):
                print(f"  {i}. {word.capitalize()} (searches: {self.freq.get(word, 0)})")
        else:
            print("  no suggestions")
        return suggestions


def main():
    print("=" * 50)
    print("TERNARY SEARCH TRIE")
    print("=" * 50)
    
    trie = TernaryTrie()
    words = ["Sample", "Samplers", "Same", "Sampling", "Summer", "Sad"]
    
    print("\nadding words:", ", ".join(words))
    # build the trie with test words
    for word in words:
        trie.insert(word)
    
    print("\n" + "-" * 50)
    print("autocomplete test:")
    print("-" * 50)
    # test with "Sam" prefix
    trie.autocomplete("Sam")
    
    # simulate user searches to build frequency data
    print("\nsimulating searches...")
    trie.search("sample")
    trie.search("sample")
    trie.search("same")
    
    # show how ranking changes based on search history
    print("\nresults after searches:")
    trie.autocomplete("Sam")
    print("=" * 50)


if __name__ == "__main__":
    main()
