import exe
import ai
import parser
import rich


ascii = """
░█▀█░▀█▀░░░█▀▀░█▀█░█▀▀░▀█▀░█▀█░█▀▀░█▀▀░█▀▄
░█▀█░░█░░░░█▀▀░█░█░█░█░░█░░█░█░█▀▀░█▀▀░█▀▄
░▀░▀░▀▀▀░░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀
"""



def ask(askword):
    answer = ai.ask(askword)
    parsed = parser.parse(answer)
    if parsed is None:
        ask("解析エラー。定めてた答えの形式に合っていません。$$説明ENDや$ANSWERENDを忘れている可能性があります。もう一度生成しなさい。")
    else :
        for description in parsed["descriptions"]:
            rich.print(f" [bold blue]AI Engineer:{description}[/bold blue]")

        status, results = exe.exe(parsed["commands"])
        if status != 0:
            rich.print(f" [bold red]エラー発生。解決策を模索します。エラー内容:{results['error']}[/bold red]")
            atinfo = "$"+ results["at"]["name"]+ ":" + results["at"]["body"] + ";"
            ask("エラー:"+atinfo + results["error"])
        else:
            if len(results) > 0:
                words = "実行結果:"
                for result in results:
                    words += result + "\n"
                ask(words)

            for description in parsed["questions"]:
                rich.print(f" [bold blue]AI Engineerからの質問:{description}[/bold blue]")
                user_answer = input()
                ask("質問の答え:"+user_answer)



print(ascii)
print("version 0.0.1")
while True:
    rich.print("[yellow] AI Engineer: なにをお手伝いしましょうか?[/yellow]")
    askword = input()
    ask("タスク:"+askword)
    #ai.rest_history()



