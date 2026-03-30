"""standard trie (prefix tree) implementation"""

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


def main():
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


if __name__ == "__main__":
    main()
