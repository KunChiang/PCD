# -*- coding: utf-8 -*-

import os
import json
import time
import shutil

import magic
import yaml
from art import *
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
init(loadLocal=True)
tprint("ZJUN PCD")

@app.route('/')
def index():
    return render_template('index.html', cloudname=dataMapsd["configuration"]["name"])


@app.route('/view/<filename>')
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
                store_path = os.path.join(i['_realPath'], i["name"])
                break
        _realPath = i['_realPath']
        makediv = i["name"]
    minetpye = magic.from_file(store_path, mime=True)
    if "video" in minetpye and (not request.args.get("download")):
        response = make_response(send_from_directory(_realPath, makediv))
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


@app.route('/filelist', methods=['GET'])
def filelist():
    settings = getSettings('default')
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
            # sortList(by=settings['sort']['by'],
            #          reverse=settings['sort']['reverse'])
            with open(fileList, 'r') as f:
                raw_files = json.load(f)
                raw_files.sort(key=lambda k: (
                    k.get(settings['sort']['by'], 0)), reverse=settings['sort']['reverse'])
                files = []
                for i in raw_files:
                    if i['path'] == path:
                        files.append(i)
                # files = raw_files
                # files.reverse()
                datasds = files[int(request.args.get("offset")):int(
                    request.args.get("offset"))+int(request.args.get("limit"))]
                # print(datasds)
        sdwewqrt = []
        for ix in datasds:
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
                    "size": ix["size"],
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


@app.route('/api/newid/', methods=['GET'])
def newid():
    string = request.args.get("string")
    # print("Get id for: ", string)
    return jsonify({"id": newId(string)})


@app.route('/newfolder/', methods=['POST'])
def newfolder():
    path = request.args.get("path")
    # print("Create folder:", path)
    try:
        info = newFolder(path)
        # print(info)
        return jsonify(info)
    except Exception as e:
        return jsonify({"created": False, "error": str(e)})


@app.route('/rename/', methods=['POST'])
def rename():
    fid = request.args.get("fileid")
    newname = request.args.get("newname")
    try:
        rename_file(fid, newname)
        return jsonify({"rename": "rename {} to {}".format(fid, newname)})
    except Exception as e:
        return jsonify({"rename": False, "error": str(e)})


@app.route('/getSetting', methods=['GET'])
def getSetting():
    id = request.args.get("id")
    return jsonify(getSettings(id if id else 'default'))


@app.route('/updateSort', methods=['GET'])
def setting():
    sort = sortQueue()
    return jsonify({"by": sort['by'], "reverse": sort['reverse'], "desc": sort['desc']})


@app.route('/refresh/', methods=['POST'])
def refresh():
    try:
        refreshLocal()
        return jsonify({"success": True, "error": None})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/search/', methods=['GET'])
def search():
    keyword = request.args.get("keyword")
    res = searchKeyword(keyword)
    sdwewqrt = []
    for ix in res:
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
                "size": ix["size"],
            }
        )
    return jsonify(sdwewqrt)


if '__main__' == __name__:
    tprint("ZJUN PCD")
    app.run("0.0.0.0", 8888)
