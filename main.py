# -*- coding: utf-8 -*-

import os
import json
import time
import shutil

import magic
import yaml
from flask import (Flask, Response, jsonify, make_response, render_template,
                   request, send_from_directory)
from PIL import Image

from utils import *

with open("configuration.yaml", "r", encoding="utf-8") as f:
    dataMapsd = yaml.safe_load(f)

app = Flask(__name__)


if dataMapsd["configuration"]["Storage"] == "mysql":
    import pymysql
    ismysql = True
    connsx = pymysql.connect(host=dataMapsd["configuration"]["mysql"]["host"], user=dataMapsd["configuration"]["mysql"]["user"], passwd=dataMapsd["configuration"]["mysql"]["passwd"], db='jncloud',
                             port=dataMapsd["configuration"]["mysql"]["port"], charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
else:
    # import json
    ismysql = False
    # fileList = os.path.join(dataPath, "filelist.json")

app.config['MAX_CONTENT_LENGTH'] = dataMapsd["configuration"]["maxsize"] * 1024 * 1024

app.config['JSON_AS_ASCII'] = False

ALLOWED_EXTENSIONS = set(dataMapsd["configuration"]["type"])


@app.route('/')
def index():
    return render_template('index.html', cloudname=dataMapsd["configuration"]["name"])


@app.route('/tc/<filename>')
def uploaded_file(filename):
    if ismysql:
        cur = connsx.cursor()
        cur.connection.ping()
        sql = "SELECT * FROM `tuchuan` WHERE name = %s"
        cur.execute(sql, filename)
        data = cur.fetchall()
        cur.close()
        store_path = os.path.join(rawFiles, data[0]["md5"])
        makediv = data[0]["md5"]
    else:
        with open(fileList, 'r') as f:
            cur = json.load(f)
        for i in cur:
            if i["name"] == filename:
                store_path = os.path.join(rawFiles, i["name"])
                break
        makediv = i["name"]
    minetpye = magic.from_file(store_path, mime=True)
    if "video" in minetpye and (not request.args.get("download")):
        response = make_response(send_from_directory(rawFiles,
                                                     makediv))
    else:
        def send_chunk():
            with open(store_path, 'rb') as target_file:
                while True:
                    chunk = target_file.read(1024 * 1024)  # 每次读取20M
                    if not chunk:
                        break
                    yield chunk
        response = Response(send_chunk())
        response.headers['content-length'] = os.stat(str(store_path)).st_size
    if request.args.get("download"):
        response.headers["Content-Type"] = "application/octet-stream"
        response.headers["Content-Disposition"] = \
            "attachment;" \
            "filename*=UTF-8''{utf_filename}".format(
                utf_filename=filename.encode('utf-8')
        )
    else:
        if str.lower(filename.rsplit('.', 1)[1]) == "mp3":
            response.headers["Content-Type"] = "audio/mpeg"
        else:
            response.headers["Content-Type"] = minetpye
    return response


@app.route('/icon/<fid>')
def icon(fid):
    # ftype = getFileType(filename)
    thumbnail = getThumbnail(fid)
    response = make_response(send_from_directory(
        "/".join(thumbnail.split('/')[:-1]), thumbnail.split('/')[-1]))
    response.headers["Content-Type"] = "image/png"
    return response


@app.route('/tclist', methods=['GET'])
def tclist():
    if (not request.args.get("limit")) or (not request.args.get("offset")) or (not request.args.get("path")):
        return jsonify({"err": "参数欠缺", "author": "Kun"})
    else:
        if ismysql:
            curxsd = connsx.cursor()
            curxsd.connection.ping()
            sql = "SELECT name,date FROM `tuchuan` order by id desc limit %s offset %s"
            curxsd.execute(sql, (int(request.args.get("limit")),
                                 int(request.args.get("offset"))))
            datasds = curxsd.fetchall()
            curxsd.close()
        else:
            path = request.args.get("path")
            with open(fileList, 'r') as f:
                xsdawe = json.load(f)
                files = []
                for i in xsdawe:
                    if i['path'] == path:
                        files.append(i)
                # files = xsdawe
                files.reverse()
                datasds = files[int(request.args.get("offset")):int(
                    request.args.get("offset"))+int(request.args.get("limit"))]
                print(datasds)
        sdwewqrt = []
        for ix in datasds:
            if len(ix["name"]) >= 24:
                xsdwok = ix["name"][0:24]+"..."
            else:
                xsdwok = ix["name"]
            sdwewqrt.append(
                {
                    "id": ix["id"],
                    "pId": ix["pId"],
                    "name": xsdwok,
                    "date": ix["date"],
                    "type": ix["type"],
                    "down": ix["name"],
                    "path": ix["path"],
                }
            )
        return jsonify(sdwewqrt)


@app.route('/uploads/', methods=['POST', "PUT"])
def upload_files():
    file = request.files['file']
    path = request.args.get("path")
    if file and allowed_file(file.filename):
        if not fileExists(file.filename, path):
            upload_file(file, path)
            result = {
                "success": True,
                "result": file.filename,
                "author": "kun",
                "update": time.strftime("%Y/%m/%d %H:%M:%S")
            }
            return jsonify(result)
        else:
            return jsonify({"success": True, "result": '已存在同名文件！'})
    else:
        return jsonify({"success": False, "result": '文件类型不支持！'})


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, rawFiles)
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)


@app.route('/delete/<fid>')
def delete(fid):
    delete_file(fid)
    return jsonify("Delete file: %s" % fid)


@app.route('/newfolder/<path>')
def newfolder(path):
    newFolder(path)
    return jsonify("New folder: %s" % path)


@app.route('/browse/', methods=['POST', "PUT", "GET"])
def browse():
    ###
    # 返回值：
    # [{ id: '', pid: '', name: ''}, { id: '', pid: '', name: ''},]
    ###
    path = request.args.get("path")
    print(" [+] path: ", path)
    res = []
    with open(fileList, 'r') as f:
        datasds = json.load(f)
        for i in datasds:
            if i['type'] == 'folder':
                res.append(i)
    res = [{'id': '1', 'pId': '0', 'name': 'root', 'open': True, "type": "folder"},
           {'id': '101', 'pId': '1', 'name': 'fd111', "type": "folder"},
           {'id': '201', 'pId': '101', 'name': 'fd2', "type": "folder"},
           {'id': '202', 'pId': '201', 'name': 'fd3', "type": "folder"},
           {'id': '301', 'pId': '101', 'name': 'fd4', "type": "folder"},
           {'id': '401', 'pId': '1', 'name': 'fd5', "type": "folder"},
           {'id': '501', 'pId': '1', 'name': 'fd6', "type": "folder"},
           {'id': '111', 'pId': '101', 'name': 'fd7', "type": "folder"},
           {'id': '112', 'pId': '111', 'name': 'fd8', "type": "folder"}]
    return jsonify(res)

# TODO: implement clean schedule for tarsh fold
# TODO: upload to folders, display folders
# TODO: rename a file
# TODO: 列表模式、树结构模式，
# TODO: 误删恢复：维护另一个tarsh.json，删除与恢复就成为了两个文件互换元素


if '__main__' == __name__:
    init()
    app.run("0.0.0.0", debug=True)
