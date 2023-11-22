#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This is the imputation server web UI."""
from flask import Flask, render_template, request
from subprocess import Popen

import datetime
import os
import shlex
import subprocess
import threading


app = Flask(__name__)

# set the secret key.  keep this really secret:
app.secret_key = "k9SZr98j/3yX R~XHH!jmN]0d2,?RT"

# top

home_directory = "USER_HOME_DIRECTORY"

config_directory = "CONFIG_DIRECTORY"

command_path = "COMMAND_PATH"

# コマンドを実行する関数
def run_command(command):
    try:
        # コマンドを実行し、標準出力と標準エラー出力を取得
        result = subprocess.run(command, env=os.environ.copy(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # 標準出力を表示
        print("標準出力:")
        print(result.stdout)
        # 標準エラー出力を表示
        print("標準エラー出力:")
        print(result.stderr)
    except Exception as e:
        print("エラー:", e)
def run_command_in_thread(command):
    run_command(command)

def run_command_popen(command):
    process = Popen(shlex.split(command),  # pylint: disable=consider-using-with
                #cwd=str(run_dir),
                env=os.environ.copy(),
                encoding="utf-8")

@app.route("/", methods=["GET", "POST"])
def index():
    """Show the main page."""
    # GET
    if request.method == "GET":
        return render_template("index.html")
    # POST
    elif request.method == "POST":
        configcontent = ""
        configcontent += "gt:\n  class: File\n"
        configcontent += "  path: " + request.form["target_vcf"] + "\n"
        configcontent += "gp: " + "\"" + request.form["output_genotype_prob"] + "\"" + "\n"
        configcontent += "nthreads: " + request.form["num_threads"] + "\n"

        # read the reference panel config file
        refpanel = request.form["reference_panel"]

        referencepanelconfigfile =""
        if refpanel == "GRCh37.1KGP":
            referencepanelconfigfile = "/home/ddbjshare-pg/imputation-server/reference/GRCh37.1KGP/default.config.yaml"
        elif refpanel == "GRCh37.1KGP-EAS":
            referencepanelconfigfile = "/home/ddbjshare-pg/imputation-server/reference/GRCh37.1KGP-EAS/default.config.yaml"
        elif refpanel == "GRCh38.1KGP":
            referencepanelconfigfile = "/home/ddbjshare-pg/imputation-server/reference/GRCh38.1KGP/default.config.yaml"
        elif refpanel == "GRCh38.1KGP-EAS":
            referencepanelconfigfile = "/home/ddbjshare-pg/imputation-server/reference/GRCh38.1KGP-EAS/default.config.yaml"
        elif refpanel == "others":
            referencepanelconfigfile = request.form["ref_panel_config"]
        with open(referencepanelconfigfile, "r") as f:
            configcontent += f.read()
        return render_template("index.html", configcontent=configcontent)

@app.route("/new_ui", methods=["GET", "POST"])
def new_ui():
    """Show the main page."""
    # GET
    if request.method == "GET":
        return render_template("new_ui.html")
    # POST
    elif request.method == "POST":
        configcontent = ""
        configcontent += "gt:\n  class: File\n"
        configcontent += "  path: " + home_directory + "/" + request.form["target_vcf"] + "\n"
        configcontent += "gp: " + "\"" + request.form["output_genotype_prob"] + "\"" + "\n"
        configcontent += "nthreads: " + request.form["num_threads"] + "\n"

        # read the reference panel config file
        refpanel = request.form["reference_panel"]
        referencepanelconfigfile =""
        if refpanel == "GRCh37.1KGP":
            referencepanelconfigfile = "/home/ddbjshare-pg/imputation-server/reference/GRCh37.1KGP/default.config.yaml"
        elif refpanel == "GRCh37.1KGP-EAS":
            referencepanelconfigfile = "/home/ddbjshare-pg/imputation-server/reference/GRCh37.1KGP-EAS/default.config.yaml"
        elif refpanel == "GRCh38.1KGP":
            referencepanelconfigfile = "/home/ddbjshare-pg/imputation-server/reference/GRCh38.1KGP/default.config.yaml"
        elif refpanel == "GRCh38.1KGP-EAS":
            referencepanelconfigfile = "/home/ddbjshare-pg/imputation-server/reference/GRCh38.1KGP-EAS/default.config.yaml"
        elif refpanel == "others":
            referencepanelconfigfile = request.form["ref_panel_config"]
        with open(referencepanelconfigfile, "r") as f:
            configcontent += f.read()

        ## configcontentをファイルに書き出す

        ### 現在時刻から、ファイル名を生成する。
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")
        file_name = "toilconfig/toilconfig_" + formatted_datetime + ".yaml"
        with open(file_name, 'w') as file:
            # ファイルに文字列を書き込む
            file.write(configcontent)
        ## outputdirの指定
        output_dir = request.form["outputDirectory"]+"/"+request.form["output_prefix"]
        ## config file path の設定
        config_file_path = config_directory+"/"
        config_file_path += file_name

        ### コマンド実行
        command_to_run = "/bin/bash "+command_path+" "
        command_to_run += home_directory+"/"+output_dir+" "
        command_to_run += config_file_path
        print(f"Command {command_to_run}")
        print("Throw job thread start")
        #thread = threading.Thread(target=run_command_in_thread, args=(command_to_run,))
        #thread.start()
        run_command_popen(command_to_run)
        print("Throw job thread end")
        # デモのため：joinするとまつことになるので、joinしない。


        return render_template("new_ui.html", configcontent=configcontent)


@app.route("/plink", methods=["GET", "POST"])
def plink():
    """Show the plink2vcf conversion configuration page."""
    # GET
    if request.method == "GET":
        return render_template("plink.html")
    elif request.method == "POST":
        configcontent = ""
        configcontent += "in_ped:\n    class: File\n    path: " + request.form["in_ped"] + "\n"
        configcontent += "out_name: " + request.form["out_name"] + "\n"
    return render_template("plink.html", configcontent=configcontent)

@app.route("/bplink", methods=["GET", "POST"])
def bplink():
    """Show the bplink2vcf conversion configuration page."""
    # GET
    if request.method == "GET":
        return render_template("bplink.html")
    elif request.method == "POST":
        configcontent = ""
        configcontent += "in_bed:\n    class: File\n    path: " + request.form["in_bed"] + "\n"
        configcontent += "out_name: " + request.form["out_name"] + "\n"
    return render_template("bplink.html", configcontent=configcontent)

if __name__ == "__main__":
    # run host 0.0.0.0
    # Base.metadata.create_all(bind=ENGINE)

    app.run(
        debug=True,
        host="0.0.0.0",
    )
