from flask import Flask, request, Response
from flask_cors import CORS

# 使うviewファイルをインポート
from views.Home import home_blueprint

app = Flask(__name__)

app.secret_key = "sim"

# CORSエラーを回避するために必要
CORS(app, origins="*", support_credentials=True)

# 日本語に対応
app.config["JSON_AS_ASCII"] = False

# viewを登録し、使えるようにする
app.register_blueprint(home_blueprint)

# preflight requestに対してOKのレスポンスを返す
@app.before_request
def before_request():
    if request.method.lower() == "options":
        return Response()

# responseのヘッダーに必要なものを渡す、CORSエラーが発生する際はこの辺りが課題の場合あり
@app.after_request
def after_request(response):
    origin = request.headers.get("Origin")
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers.add("Access-Control-Allow-Credentials", "true")
    # preflight requestが飛ぶ時に必要らしい、ほぼ入れた方が良い
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Headers", "X-Requested-With")
    response.headers.add("Access-Control-Allow-Headers", "Origin")
    response.headers.add("Access-Control-Allow-Headers", "Accept")
    # 使うヘッダーに合わせて追加する
    # response.headers.add('Access-Control-Allow-Headers', 'access')
    # response.headers.add('Access-Control-Allow-Headers', 'jwt')

    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
