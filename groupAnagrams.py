def group_anagrams(words):
    
    anagrams = {}

    for word in words:
        sorted_word = sort_word(word)
        
        if sorted_word in anagrams:
            anagrams[sorted_word].append(word)
        else:
            anagrams[sorted_word] = [word]

    return list(anagrams.values())

def sort_word(word):
        return ''.join(sorted(word))

words = ["listen", "silent", "eat", "abc", "cab", "enlist", "tea", "ate", "mode", "demo"]
grouped_anagrams = group_anagrams(words)
print(grouped_anagrams)
