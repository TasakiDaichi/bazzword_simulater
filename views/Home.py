from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, Blueprint
from flask_cors import CORS, cross_origin
import os
from views.simu_threads import start_simulation_thread
from views.share_config import simulation_config

# run.pyにこのviewファイルを認識させるために必要
home_blueprint = Blueprint("Home", __name__, url_prefix="/")

@home_blueprint.route("/", methods=["GET", "POST"])
@cross_origin(origin="*")
def form():
    if request.method == "POST":
        # フォーム入力値をセッションに保存
        session["general_agents"] = int(request.form["general_agents"])
        session["persistent_agents"] = int(request.form["persistent_agents"])
        session["forgetful_agents"] = int(request.form["forgetful_agents"])
        session["contrarian_agents"] = int(request.form["contrarian_agents"])
        session["mass_follower_agents"] = int(request.form["mass_follower_agents"])
        
        # 初期単語ごとの人数を辞書でまとめる
        initial_agents = {}
        global simulation_config
        for i in range(1, 5):
            word = request.form.get(f"word{i}")
            count = request.form.get(f"count{i}")
            if word and count:
                initial_agents[word] = int(count)
        simulation_config["initial_agents"] = initial_agents
        return redirect(url_for("Home.simu"))
    return render_template("form.html")

@home_blueprint.route("/simu")
def simu():
    if not hasattr(simu, "started"):
        start_simulation_thread()
        simu.started = True
    return render_template("simu.html")

# 静的ファイルの配信（Flaskのstaticフォルダを利用）
@home_blueprint.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(home_blueprint.root_path, 'static'), filename)
