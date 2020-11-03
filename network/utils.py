def isHashTag(word):
    if len(word) < 2:
        return False
    if word[0] == '#':
        # only digit cannot be hashtag
        if word[1:].isdigit():
            return False
        if word[1:].isalnum():
            return True
    return False

def isMention(word):
    if len(word) < 2:
        return False
    if word[0] == '@' and word[1:].isalnum():
        return True
    return False