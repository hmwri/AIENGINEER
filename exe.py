import re
import subprocess
import rich


def exe(commands: [{str}]):
    results = []
    for command in commands:
        if command is None:
            continue
        if command["name"] == "terminal" or command["name"] == "getResult":
            args = command["body"].strip()
            if ">" in args:
                return 1, {"at": command, "error": "このコマンドはpythonを通して呼ばれるため、リダイレクトは使えません、editFileコマンド等を使用してください"}
            try:
                result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                        encoding='utf-8')
            except OSError as e:
                return 1, {"at": command, "error": f"{e}"}
            rich.print(f"[italic] 実行します:{args} [/italic]")
            if result.returncode != 0:
                return 1, {"at": command, "error": result.stderr}
            rich.print(f"[green italic] 成功しました [/green italic]")
            if "Requirement already satisfied" in f"{result.stdout}".strip() or not f"{result.stdout}".strip():
                continue
            results.append(f"{result.stdout}".strip())
            if command["name"] == "getResult":
                results.append({"at": command, "result": f"{result.stdout}"})
                rich.print(f"[green italic] {result.stdout} [/green italic]")

        elif command["name"] == "editFile":
            body = command["body"]
            name, body = extractFileNameAndBody(body)
            rich.print(f"[italic]　ファイルを編集します:{name}:{body} [/italic]")
            try:
                with open(name, mode="w", encoding="utf8") as f:
                    f.write(body)
            except OSError as e:
                return 1, {"at": command, "error": f"{e}"}

        elif command["name"] == "python":
            with open("python.py", mode="w", encoding="utf8") as f:
                f.write(command["body"].strip())
            rich.print(f"[italic] pythonプログラム{command['body']}を実行します [/italic]")
            result = subprocess.run(["python3", "python.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                    encoding='utf-8')

            if result.returncode != 0:
                return 1, {"at": command, "error": result.stderr}
            rich.print(f"[italic bold green] 成功 [/italic bold green]")
            if result.stdout:
                results.append(f"{result.stdout}".strip())
                rich.print(f"[blue italic] --実行結果--\n{result.stdout} [/blue italic]")
    return 0, results


def extractFileNameAndBody(body):
    i = 0
    name = ""
    body = body.strip()
    while body[i] != ' ' and body[i] != '\n':
        name += body[i]
        i += 1
    bodybody = body[i + 1:]
    return name, bodybody.strip()
