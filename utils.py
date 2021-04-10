import os
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
        json.dump({
            'root': {
                'name': '/root',
                'path': rawFiles,
                'type': 'folder',
                'date': time.strftime("%Y/%m/%d %H:%M:%S"),
                'thumbnail': 'icon/folder.png',
                'children': [],
            }
        }, open(fileList, 'w'))


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


def getThumbnail(filename):
    with open(fileList, 'r') as f:
        datasds = json.load(f)
        for d in datasds['root']['children']:
            if d['name'] == filename:
                return d['thumbnail']
    return None


def generateThumbnail(file):
    ftype = getFileType(file.filename)
    if isImg(ftype):
        thumbnail = os.path.join(thumbnailPath, "%s.png" % (file.filename))
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
        if filename in datasds['root']['children']:
            return True
        else:
            return False


def delete_file(filename, datasource=fileList):
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        for d in datasds['root']['children']:
            if d['name'] == filename:
                shutil.move(os.path.join(d['path'], filename),
                            os.path.join(trash, filename))
                break
        datasds['root']['children'].remove(d)
        with open(datasource, 'w') as f:
            json.dump(datasds, f)


def upload_file(file, path, thumbnail, datasource=fileList):
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        datasds['root']['children'].append({
            "name": file.filename,
            "path": path,
            "thumbnail": thumbnail,
            "type": getFileType(file.filename),
            "date": time.strftime("%Y/%m/%d %H:%M:%S")})
        with open(datasource, 'w') as f:
            json.dump(datasds, f)
