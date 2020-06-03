import json
import urllib.request
import jsbeautifier

vocab = {'vocabulary': []}

f = open("words.txt", "r")
for word in f:
    cleanWord = word.replace(" ", "%20")
    # print("https://api.dictionaryapi.dev/api/v2/entries/en/" + cleanWord)
    try:
        with urllib.request.urlopen("https://api.dictionaryapi.dev/api/v2/entries/en/" + cleanWord) as url:
            jsonStr = url.read()
            data = json.loads(jsonStr)
            for d in data[0]["meanings"]:
                wrd = data[0]["word"].capitalize()
                definition = d["definitions"][0]
                vocab["vocabulary"].append({
                    "word": wrd,
                    "definition": definition["definition"]
                })
            print("Added word: " + wrd)
    except urllib.error.HTTPError as e:
        vocab["vocabulary"].append({
            "word": word.capitalize().replace("\n", ""),
            "definition": "Could not find."
        })
        print("Couldn't find word: " + word.capitalize().replace("\n", ""))

filename = input("Name of file:")
with open("vocab/"+filename + ".js", 'w') as outfile:
    js = "let json = " + str(vocab) + ";"

    opts = jsbeautifier.default_options()
    opts.indent_size = 2
    opts.space_in_empty_paren = True
    res = jsbeautifier.beautify(js, opts)
    outfile.write(res)
