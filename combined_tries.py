# STANDARD TRIE (PREFIX TREE)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class StandardTrie:
    def __init__(self):
        self.root = TrieNode()
        self.freq = {}

    def insert(self, word):
        """add a word to the trie"""
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        """find all words that start with prefix"""
        node = self.root
        prefix = prefix.lower()
        
        # navigate to where the prefix ends
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # collect all words from this node onwards
        words = []
        
        def collect(cur_node, cur_word):
            if cur_node.is_end_of_word:
                words.append(cur_word)
            for char, child in cur_node.children.items():
                collect(child, cur_word + char)
        
        collect(node, prefix)
        
        # track frequency
        for w in words:
            self.freq[w] = self.freq.get(w, 0) + 1
        return words

    def autocomplete(self, prefix):
        """show suggestions for prefix"""
        suggestions = self.search(prefix)
        # sort by how many times searched, then alphabetically
        suggestions.sort(key=lambda w: (-self.freq.get(w, 0), w))
        
        print(f"suggestions for '{prefix}':")
        if suggestions:
            for i, word in enumerate(suggestions, 1):
                print(f"  {i}. {word.capitalize()} (searches: {self.freq.get(word, 0)})")
        else:
            print("  no suggestions")
        return suggestions

# TERNARY SEARCH TRIE

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

#DEMONSTRATIONS

def demo_standard_trie():
    print("=" * 50)
    print("STANDARD TRIE")
    print("=" * 50)
    
    trie = StandardTrie()
    words = ["Sample", "Samplers", "Same", "Sampling", "Summer", "Sad"]
    
    print("\nadding words:", ", ".join(words))
    # insert all the test words
    for word in words:
        trie.insert(word)
    
    print("\n" + "-" * 50)
    print("autocomplete test:")
    print("-" * 50)
    # test autocomplete with "Sam" prefix
    trie.autocomplete("Sam")
    
    # simulate some searches to build up frequency
    print("\nsimulating searches...")
    trie.search("sample")
    trie.search("sample")
    trie.search("same")
    
    # show how results changed based on search frequency
    print("\nresults after searches:")
    trie.autocomplete("Sam")
    print("=" * 50)


def demo_ternary_trie():
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


def interactive_mode():
    """Allow user to test insertion and search interactively"""
    print("\n" + "=" * 50)
    print("INTERACTIVE MODE")
    print("=" * 50)
    
    choice = input("\nChoose trie type:\n1. Standard Trie\n2. Ternary Trie\n3. Both\nEnter choice (1-3): ").strip()
    
    if choice in ["1", "3"]:
        print("\n--- STANDARD TRIE ---")
        trie = StandardTrie()
        
        # Insert initial words
        words = ["Sample", "Samplers", "Same", "Sampling", "Summer", "Sad"]
        for word in words:
            trie.insert(word)
        print(f"Inserted: {', '.join(words)}")
        
        # Interactive search
        while True:
            prefix = input("\nEnter prefix to search (or 'quit' to exit): ").strip()
            if prefix.lower() == 'quit':
                break
            trie.autocomplete(prefix)
    
    if choice in ["2", "3"]:
        print("\n--- TERNARY TRIE ---")
        trie = TernaryTrie()
        
        # Insert initial words
        words = ["Sample", "Samplers", "Same", "Sampling", "Summer", "Sad"]
        for word in words:
            trie.insert(word)
        print(f"Inserted: {', '.join(words)}")
        
        # Interactive search
        while True:
            prefix = input("\nEnter prefix to search (or 'quit' to exit): ").strip()
            if prefix.lower() == 'quit':
                break
            trie.autocomplete(prefix)


def main():
    demo_standard_trie()
    print("\n\n")
    demo_ternary_trie()
    
    # Ask if user wants interactive mode
    if input("\n\nWant to test interactively? (y/n): ").strip().lower() == 'y':
        interactive_mode()


if __name__ == "__main__":
    main()
