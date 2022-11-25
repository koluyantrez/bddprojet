import tokenizer

stopList = ["stop","close","exit"]
specialTokken = ["let","print"]

def readUserQuery():
    while(True):
        query = input()
        if stopList.__contains__(query):
            break
        tokens = tokenizer.tokenize(query)