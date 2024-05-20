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

# words = ["listen", "silent", "eat", "abc", "cab", "enlist", "tea", "ate", "mode", "demo"]
# grouped_anagrams = group_anagrams(words)
# print(grouped_anagrams)

def main():
    print("Enter words separated by spaces:")
    user_input = input()  
    words = user_input.split()  
    grouped_anagrams = group_anagrams(words)
    print("Grouped anagrams:", grouped_anagrams)
    wordList = list()
    num = int(input("Enter number of words you'll like to add: "))
    for i in range(0, num):
        str = input(f"Enter word {i+1}: ")
        wordList.append(str)
    anagramList = group_anagrams(wordList)
    print("Grouped anagrams:", anagramList)

main()