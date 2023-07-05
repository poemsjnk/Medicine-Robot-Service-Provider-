import json

def load_json_intents(filename):
    if filename.endswith(".json"):
        result = []
        data = json.loads(open(filename).read())
        intents = data["intents"]
        # convert to ascii strings
        for intent in intents:
            intt = {}
            for k in intent:
                # print(type(k), type(intent[k]))
                if type(intent[k]) is list:
                    intt[k.encode('ascii')] = [s.encode('ascii') for s in intent[k]]
                    pass
                else:
                    intt[k.encode('ascii')] = intent[k].encode('ascii')
            result.append(intt)
        return result

if __name__ == "__main__":
    filename = "intents.json"
    intents = load_json_intents(filename)
    print(intents)
