def parse(response : str):
    i = 0
    blocks = []

    while i < len(response) - 1:

        if response[i:i+2] == "$$":
            i += 2
            name = ""
            while i < len(response) and response[i] != ":" :
                name += response[i]
                i+=1
            i += 1
            body = ""
            while i < len(response) and response[i :i + len(name)+3+2] != f"$${name}END":
                body += response[i]
                i+=1
            i += len(name)+3+2
            blocks.append({"name":name,"body": body})
        else:
            i+=1
    result = {
        "descriptions":[],
        "commands":[],
        "questions" : []
    }
    for block in blocks:
        if block["name"] == "説明":
            result["descriptions"].append(block["body"])
        elif block["name"] == "コマンド" :
            result["commands"]= parseCommandBlock(block["body"])
        elif  block["name"] == "質問":
            result["questions"].append(block["body"])
    if len(blocks) == 0:
        return None
    return result

def parseCommandBlock(response):
    i = 0
    commands = []
    names = ["python", "terminal", "getResult", "editFile"]
    while i < len(response) - 1:

        if response[i] == "$":
            name = inspect_command_names(response, names,i)
            if name == None:
                i+=1
                continue
            if name == "NONE":
                return None
            i += len(name) + 2
            body = ""
            while i < len(response) and response[i :i + len("$ANSWEREND")] != "$ANSWEREND" :
                body += response[i]
                i+=1
            i += len("$ANSWEREND")
            commands.append({"name":name,"body": body})
        else:
            i+=1
    return commands

def inspect_command_names(response:str,names:[str],i:int):
    for name in names:
        if response[i+1:i+len(name)+1] == name :
            return name
        if response[i+1:i+len("NONE")+1] == "NONE" :
            return "NONE"
    return None

# r = parse("""
# $$説明:
# index.htmlに以下のコードを入力します。
# <!DOCTYPE html>
# <html>
#   <head>
#     <title>ChatGPT無限の可能性</title>
#     <link rel="stylesheet" href="styles.css">
#   </head>
#   <body>
#     <header>
#       <h1>ChatGPT無限の可能性</h1>
#     </header>
#     <main>
#       <section>
#         <img src="https://i.imgur.com/CaM1G10.png" alt="ChatGPTのロゴ">
#         <h2>ChatGPTとは？</h2>
#         <p>ChatGPTはGPTと呼ばれるニューラルネットワークを使った自然言語処理の技術に基づいたチャットボットです。その学習モデルをもとに、より自然なやりとりができるようになっています。</p>
#       </section>
#       <section>
#         <h2>ChatGPTの良さ</h2>
#         <ul>
#           <li>学習によってより高度な対話が可能</li>
#           <li>大量の会話ログから自然な返答を生成できる</li>
#           <li>精度が高く、文法的な正確さが保証される</li>
#         </ul>
#       </section>
#     </main>
#     <footer>
#       <p>&copy; ChatGPT無限の可能性. All rights reserved.</p>
#     </footer>
#   </body>
# </html>
# 次に、styles.cssに以下のコードを入力します
# :root {
#   --orange: #FFA500;
# }
#
# header {
#   background-color: var(--orange);
#   text-align: center;
#   padding-top: 1em;
#   padding-bottom: 2em;
# }
#
# h1 {
#   color: white;
#   font-size: 3em;
# }
#
# section {
#   max-width: 800px;
#   margin: auto;
#   margin-top: 2em;
# }
#
# section h2 {
#   color: var(--orange);
# }
#
# section ul {
#   list-style: none;
#   padding-left: 0;
# }
#
# section li::before {
#   content: "✔  ";
#   color: var(--orange);
# }
#
# footer {
#   text-align: center;
#   margin-top: 2em;
#   margin-bottom: 1em;
# }
# ### コマンドについて説明
# 1. まず空のindex.htmlファイルを作成します。
# 2. HTMLのCSSのコードが別々になっているため、styles.cssを作成します。
# 3. サイトのタイトルをChatGPT無限の可能性としたため、titleタグにそのように記述します。
# 4. HTMLの<body>タグの中に、サイトのレイアウトや情報を入力します。
# 5. オレンジ色を貴重にしたいため、変数を定義してそれに沿ったCSSの適用をしています。
# 6. GoogleChromeでオレンジ色を基調にしたページが表示されれば成功です。
# $$説明END
# $$コマンド:
# $python:
# with open("index.html", mode="w") as f:
#     f.write('<!DOCTYPE html>\n')
#     f.write('<html>\n')
#     f.write('  <head>\n')
#     f.write('    <title>ChatGPT無限の可能性</title>\n')
#     f.write('    <link rel="stylesheet" href="styles.css">\n')
#     f.write('  </head>\n')
#     f.write('  <body>\n')
#     f.write('    <header>\n')
#     f.write('      <h1>ChatGPT無限の可能性</h1>\n')
#     f.write('    </header>\n')
#     f.write('    <main>\n')
#     f.write('      <section>\n')
#     f.write('        <img src="https://i.imgur.com/CaM1G10.png" alt="ChatGPTのロゴ">\n')
#     f.write('        <h2>ChatGPTとは？</h2>\n')
#     f.write('        <p>ChatGPTはGPTと呼ばれるニューラルネットワークを使った自然言語処理の技術に基づいたチャットボットです。その学習モデルをもとに、より自然なやりとりができるようになっています。</p>\n')
#     f.write('      </section>\n')
#     f.write('      <section>\n')
#     f.write('        <h2>ChatGPTの良さ</h2>\n')
#     f.write('        <ul>\n')
#     f.write('          <li>学習によってより高度な対話が可能</li>\n')
#     f.write('          <li>大量の会話ログから自然な返答を生成できる</li>\n')
#     f.write('          <li>精度が高く、文法的な正確さが保証される</li>\n')
#     f.write('        </ul>\n')
#     f.write('      </section>\n')
#     f.write('    </main>\n')
#     f.write('    <footer>\n')
#     f.write('      <p>&copy; ChatGPT無限の可能性. All rights reserved.</p>\n')
#     f.write('    </footer>\n')
#     f.write('  </body>\n')
#     f.write('</html>\n')
# with open("styles.css", mode="w") as f:
#     f.write(':root {\n')
#     f.write('  --orange: #FFA500;\n')
#     f.write('}\n')
#     f.write('\n')
#     f.write('header {\n')
#     f.write('  background-color: var(--orange);\n')
#     f.write('  text-align: center;\n')
#     f.write('  padding-top: 1em;\n')
#     f.write('  padding-bottom: 2em;\n')
#     f.write('}\n')
#     f.write('\n')
#     f.write('h1 {\n')
#     f.write('  color: white;\n')
#     f.write('  font-size: 3em;\n')
#     f.write('}\n')
#     f.write('\n')
#     f.write('section {\n')
#     f.write('  max-width: 800px;\n')
#     f.write('  margin: auto;\n')
#     f.write('  margin-top: 2em;\n')
#     f.write('}\n')
#     f.write('\n')
#     f.write('section h2 {\n')
#     f.write('  color: var(--orange);\n')
#     f.write('}\n')
#     f.write('\n')
#     f.write('section ul {\n')
#     f.write('  list-style: none;\n')
#     f.write('  padding-left: 0;\n')
#     f.write('}\n')
#     f.write('\n')
#     f.write('section li::before {\n')
#     f.write('  content: "✔  ";\n')
#     f.write('  color: var(--orange);\n')
#     f.write('}\n')
#     f.write('\n')
#     f.write('footer {\n')
#     f.write('  text-align: center;\n')
#     f.write('  margin-top: 2em;\n')
#     f.write('  margin-bottom: 1em;\n')
#     f.write('}')
# $terminal: "open", "-a", "Google Chrome", "index.html" $ANSWEREND
# $$コマンドEND
# """)
#
# print(r)
#
