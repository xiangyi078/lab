def F(s):
    cleaned = s.lower().replace(' ', '')
    return cleaned == cleaned[::-1]