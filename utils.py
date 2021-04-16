import os
import hashlib
import json
import time
import shutil
from PIL import Image

dataPath = "datas"
thumbnailPath = os.path.join(dataPath, ".thumbs")
rawFiles = os.path.join(dataPath, "root")
trash = os.path.join(dataPath, ".trash")
fileList = os.path.join(dataPath, "filelist.json")


def allowed_file(filename):
    return True
    # return '.' in filename and \
    #        str.lower(filename.rsplit('.', 1)[1]) in ALLOWED_EXTENSIONS


def __initPath(paths):
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)


def init():
    __initPath([dataPath, thumbnailPath, rawFiles, trash])
    if not os.path.exists(fileList):
        json.dump([{
            "id": newId("/root"),
            "pId": '000000',
            "name": "root",
            "type": "folder",
            "path": "/",
            "_realPath": rawFiles,
            "thumbnail": "icon/folder.png",
            "date": time.strftime("%Y/%m/%d %H:%M:%S"),
        }], open(fileList, 'w'))
        # json.dump({
        #     'root': {
        #         'name': '/root',
        #         'path': rawFiles,
        #         'type': 'folder',
        #         'date': time.strftime("%Y/%m/%d %H:%M:%S"),
        #         'thumbnail': 'icon/folder.png',
        #         'children': [],
        #     }
        # }, open(fileList, 'w'))


def isImg(ftype):
    if ftype in ['bmp', 'dib', 'png', 'jpg', 'jpeg', 'pbm', 'pgm', 'ppm', 'tif', 'tiff']:
        return True
    else:
        return False


def isCode(ftype):
    if ftype in ['go', 'sh', 'java', 'perl', 'swift']:
        return True
    else:
        return False


def isTxt(ftype):
    if ftype in ['json', 'jsonnet']:
        return True
    else:
        return False


def getFileType(filename):
    ftype = str.lower(filename.split('.')[-1])
    return ftype


def getThumbnail(fid):
    with open(fileList, 'r') as f:
        datasds = json.load(f)
        for d in datasds:
            if d['id'] == fid:
                return d['thumbnail']
    return None


def generateThumbnail(file, md5Name):
    ftype = getFileType(file.filename)
    if isImg(ftype):
        thumbnail = os.path.join(thumbnailPath, "%s.png" % (md5Name))
        image = Image.open(file.stream)
        image.thumbnail((200, 200))
        image.convert('RGB').save(thumbnail, 'JPEG')
    elif isCode(ftype):
        thumbnail = os.path.join("icon", "code.png")
    elif isTxt(ftype):
        thumbnail = os.path.join("icon", "file.png")
    else:
        thumbnail = os.path.join("icon", ftype + ".png")
        if not os.path.exists(thumbnail):
            thumbnail = os.path.join("icon", "unknown.png")
    return thumbnail


def fileExists(filename, path, datasource=fileList):
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        for d in datasds:
            if d['name'] == filename:
                return True
    return False


def delete_file(fid, datasource=fileList):
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        for d in datasds:
            if d['id'] == fid:
                break
        shutil.move(os.path.join(toRealPath(d['path']), d['name']),
                    os.path.join(trash, d['name']))
        datasds.remove(d)
        with open(datasource, 'w') as f:
            json.dump(datasds, f)


def upload_file(file, path, datasource=fileList):
    print("[+] upload file: ", file.filename)
    md5Name = newId(os.path.join(path, file.filename))
    file.seek(0)
    target_file = os.path.join(toRealPath(path), file.filename)
    print("[+] upload target file: ", target_file)
    file.save(target_file)
    thumbnail = generateThumbnail(file, md5Name)
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        datasds.append({
            "id": md5Name,
            "pId": getId("path", path),
            "name": file.filename,
            "type": getFileType(file.filename),
            "path": path,
            "_realPath": toRealPath(path),
            "thumbnail": thumbnail,
            "date": time.strftime("%Y/%m/%d %H:%M:%S")})
        with open(datasource, 'w') as f:
            json.dump(datasds, f)


def newFolder(path, datasource=fileList):
    os.mkdir(toRealPath(path))
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        datasds.append({
            "id": newId(path),
            "pId": getId("path", "/".join(path.split("/")[:-1])),
            "name": path.split("/")[-1],
            "type": "folder",
            "path": "/".join(path.split("/")[:-1]),
            "_realPath": toRealPath("/".join(path.split("/")[:-1])),
            "thumbnail": "icon/folder.png",
            "date": time.strftime("%Y/%m/%d %H:%M:%S")})
        with open(datasource, 'w') as f:
            json.dump(datasds, f)


def toRealPath(path):
    print(dataPath, "/".join(path.split("/")[1:]))
    return os.path.join(dataPath, "/".join(path.split("/")[1:]))


def getId(key, value, datasource=fileList):
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        for d in datasds:
            if d[key] == value:
                return d['id']
    return newId(value)


def newId(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))  # 转码
    res = md5.hexdigest()
    return res
