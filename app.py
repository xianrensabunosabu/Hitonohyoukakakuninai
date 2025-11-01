from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        person = request.form["person"]
        message = request.form["message"]

        prompt = f"""
あなたは「人の印象分析AI」です。
以下の情報をもとに、その人の印象・感情トーン・関係性・モテ度を総合的に評価してください。

---
誰から: {person}
どんな感じのメッセージ: {message}
---

出力フォーマット:
感情トーン: （ポジティブ/ネガティブ/ニュートラル + 数値％）
印象: （その人がどんな人か）
モテ度スコア: （0〜100）
詳細評価:
- 優しさ: （数値）
- 興味関心: （数値）
- 信頼度: （数値）
- 警戒心: （数値）
AIコメント: （関係性の見立てや今後のアドバイス）
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        result = response.choices[0].message.content
        return render_template("result.html", result=result, person=person, message=message)

    return render_template("index.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
