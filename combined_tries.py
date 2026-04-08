# text autocompletion system - standard trie and ternary trie

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class StandardTrie:
    def __init__(self):
        self.root = TrieNode()
        self.freq = {}

    def insert(self, word):
        # insert word character by character
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, prefix):
        # traverse to prefix, collect all words
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]

        words = []
        def collect(n, word):
            if n.is_end:
                words.append(word)
            for c, child in n.children.items():
                collect(child, word + c)
        
        collect(node, prefix.lower())
        for w in words:
            self.freq[w] = self.freq.get(w, 0) + 1
        return words

    def autocomplete(self, prefix):
        suggestions = self.search(prefix)
        suggestions.sort(key=lambda w: (-self.freq.get(w, 0), w))
        print("suggestions for '{}':" .format(prefix))
        for i, w in enumerate(suggestions, 1):
            print("  {}. {}".format(i, w.capitalize()))


class TSTNode:
    def __init__(self, char):
        self.char = char
        self.left = self.mid = self.right = None
        self.is_end = False

class TernaryTrie:
    def __init__(self):
        self.root = None
        self.freq = {}

    def insert(self, word):
        # insert recursively based on char comparison
        self.root = self._ins(self.root, word.lower(), 0)

    def _ins(self, node, word, idx):
        char = word[idx]
        if node is None:
            node = TSTNode(char)
        
        if char < node.char:
            node.left = self._ins(node.left, word, idx)
        elif char > node.char:
            node.right = self._ins(node.right, word, idx)
        else:
            if idx + 1 < len(word):
                node.mid = self._ins(node.mid, word, idx + 1)
            else:
                node.is_end = True
        return node

    def search(self, prefix):
        # find node at prefix end, collect words from there
        node = self._find(self.root, prefix.lower(), 0)
        if not node:
            return []
        
        words = []
        def dfs(n, word, explore):
            if not n:
                return
            if explore:
                dfs(n.left, word, True)
                dfs(n.right, word, True)
            full = word + n.char
            if n.is_end:
                words.append(full)
            dfs(n.mid, full, True)
        
        dfs(node, prefix.lower()[:-1], False)
        for w in words:
            self.freq[w] = self.freq.get(w, 0) + 1
        return words

    def _find(self, node, prefix, idx):
        # navigate to end of prefix
        if not node:
            return None
        char = prefix[idx]
        if char < node.char:
            return self._find(node.left, prefix, idx)
        elif char > node.char:
            return self._find(node.right, prefix, idx)
        else:
            if idx + 1 < len(prefix):
                return self._find(node.mid, prefix, idx + 1)
            return node

    def autocomplete(self, prefix):
        suggestions = self.search(prefix)
        suggestions.sort(key=lambda w: (-self.freq.get(w, 0), w))
        print("suggestions for '{}':" .format(prefix))
        for i, w in enumerate(suggestions, 1):
            print("  {}. {}".format(i, w.capitalize()))


def demo():
    print("\npart a: standard trie\n" + "-" * 40)
    t1 = StandardTrie()
    words = ["sample", "samplers", "same", "sampling", "summer", "sad"]
    for w in words:
        t1.insert(w)
    print("inserted: {}".format(", ".join(words)))
    print("\nwhen user types 'sam':")
    t1.autocomplete("sam")
    
    print("\n\npart b: ternary trie\n" + "-" * 40)
    t2 = TernaryTrie()
    for w in words:
        t2.insert(w)
    print("inserted: {}".format(", ".join(words)))
    print("\nwhen user types 'sam':")
    t2.autocomplete("sam")


def interactive():
    print("\n" + "=" * 40)
    print("test mode")
    print("=" * 40)
    
    choice = input("\ntrie type?\n1. standard\n2. ternary\n3. both\n> ")
    
    # get words once for both tries
    user_words = input("enter words (comma separated): ").strip()
    words = [w.strip() for w in user_words.split(',')] if user_words else ["sample", "samplers", "same", "sampling", "summer", "sad"]
    
    if choice in ["1", "3"]:
        print("\n--- standard trie ---")
        trie = StandardTrie()
        for w in words:
            trie.insert(w)
        print("loaded: {}".format(", ".join(words)))
        
        while True:
            prefix = input("\nsearch prefix (or 'q' to exit): ").strip()
            if prefix.lower() == 'q':
                break
            if prefix:
                trie.autocomplete(prefix)
    
    if choice in ["2", "3"]:
        if choice == "3":
            print("\n" + "=" * 40)
        print("\n--- ternary trie ---")
        trie = TernaryTrie()
        for w in words:
            trie.insert(w)
        print("loaded: {}".format(", ".join(words)))
        
        while True:
            prefix = input("\nsearch prefix (or 'q' to exit): ").strip()
            if prefix.lower() == 'q':
                break
            if prefix:
                trie.autocomplete(prefix)


if __name__ == "__main__":
    demo()
    if input("\ntest interactively? (y/n): ").lower() == 'y':
        interactive()
