from flask import Flask, render_template,request, redirect,url_for, jsonify, json
from urllib.request import urlopen

app=Flask(__name__)
app.template_folder = 'templates'


@app.route("/",methods=["POST", "GET"])
def home():
    if request.method=="POST":
        a=request.form["word"]
        return redirect(url_for("finder", word=a))
    else:
        return render_template("word.html")

@app.route("/<word>")
def finder(word):
    z = word
    b = "https://api.dictionaryapi.dev/api/v2/entries/en/" + z
    response = urlopen(b)
    c = json.loads(response.read())
    
    word_to_send = ""
    partofspeech = []
    meanings_by_pos = {}
    audio = []
    no_of_def_in_each_cat = []  # Add this line
    
    for entry in c:
        if "word" in entry:
            word_to_send = entry["word"]
        audio=entry["phonetics"][0]["audio"]

        for meaning_data in entry["meanings"]:
            part_of_speech = meaning_data["partOfSpeech"]
            if part_of_speech not in partofspeech:
                partofspeech.append(part_of_speech)
                meanings_by_pos[part_of_speech] = []
                print(meanings_by_pos)
            
            for definition_data in meaning_data["definitions"]:
                defo = definition_data["definition"]
                meanings_by_pos[part_of_speech].append(defo)
                no_of_def_in_each_cat.append(len(meanings_by_pos[part_of_speech]))

    max_defs = max(no_of_def_in_each_cat)
    return render_template(
        "finder.html",
        word_to_send=word_to_send,
        partofspeech=partofspeech,
        meanings_by_pos=meanings_by_pos,
        audio=audio,
        max_defs=max_defs
    )


if __name__=="__main__":
    app.run(debug=True)


# @app.route("/<word>")
# def finder(word):
#     z=word
#     b="https://api.dictionaryapi.dev/api/v2/entries/en/" + z
#     response=urlopen(b)
#     c=json.loads(response.read())
#     l=[]
#     m=[]
#     audio=[]
#     no_of_def_in_each_cat=[]
#     alensum=0
#     for i in c:
#         length=len(i["meanings"]) #3
#         print("length of mean: ",length)
#         audio=i["phonetics"][0]["audio"]
#         if i["word"]:
#             word=i["word"]
#         for j in range(length): # noun verb adjective 3
#             print("j",j)
#             alen=len(i["meanings"][j]["definitions"])
#             print("hi",alen) # 5 2 3
#             no_of_def_in_each_cat.append(alen) # o=[5,2,3]
#             print("alen list value: ",no_of_def_in_each_cat) #...........
#         for j in range(len(no_of_def_in_each_cat)):
#             for k in range(len(no_of_def_in_each_cat)): # k=0,1,2
#                 print("value of k: ",k)
#                 print("element",no_of_def_in_each_cat[k] )
#                 for la in range(no_of_def_in_each_cat[k] ): # la= 0 to 4, 0 to 1, o to 2
#                     defo=i["meanings"][j]["definitions"][k]["definition"]
#                     pos=i["meanings"][j]["partOfSpeech"]
#                     l.append(defo)
#                     m.append(pos)
#     return render_template("finder.html", word_to_send=word, meaning=l, partofspeech=m,length=length,audio=audio)

        
        #if i["meanings"]:
    #     for j in range(len(i["meanings"])):
    #         #print(len(i["meanings"]))
    #         alen=len(i["meanings"][j]["definitions"])
    #         print(alen) # 5 2 3
    #         o.append(alen) #o=[5,3,2]
    #         alensum+=alen #alensum=10
    #         pos=i["meanings"][j]["partOfSpeech"]
    #         m.append(pos)
    #         for k in range(alen):
    #             defo=i["meanings"][j]["definitions"][k]["definition"]
    #             l.append(defo)
    # return render_template("finder.html", word_to_send=word, meaning=l, partofspeech=m,length=len(m),audio=audio)
