import os
import hashlib
import json
import time
import datetime
import shutil
from PIL import Image

dataPath = "data"
thumbnailPath = os.path.join(dataPath, ".thumbs")
rawFiles = os.path.join(dataPath, "root")
trash = os.path.join(dataPath, ".trash")
fileList = os.path.join(dataPath, "filelist.json")
settings = os.path.join(dataPath, "settings.json")
ROOTID = "000000"
SORTSET = [
    {"by": "name", "reverse": True, "desc": "按名称正序"},
    {"by": "name", "reverse": False, "desc": "按名称倒序"},
    {"by": "date", "reverse": True, "desc": "按时间正序"},
    {"by": "date", "reverse": False, "desc": "按时间倒序"},
    {"by": "type", "reverse": True, "desc": "按类型排序"},
    {"by": "size", "reverse": True, "desc": "按文件大小正序"},
    {"by": "size", "reverse": False, "desc": "按文件大小倒序"},
]

# path分两种，一种是前端展示的path，一种是实际path，记为_realPath
# path不以'/'结尾，
# path: "/root/path/to/folder"
# _realPath: "datas/root/path/to/folder"
# id: 根据path(string)生成的MD5


class File:
    def __init__(self, id=None, pId=None, name=None, type=None, path=None, size=None, _realPath=None, thumbnail=None, date=None):
        self.json = {
            "id": id,
            "pId": pId,
            "name": name,
            "type": type,
            "path": path,
            "size": size,
            "_realPath": _realPath,
            "thumbnail": thumbnail,
            "date": date
        }

    def check(self):
        for _, v in self.json.items():
            if not v:
                return False
        return True

    def generate(self, path, filename, pId):
        file = os.path.join(path, filename)
        self.json['id'] = newId(file)
        self.json['pId'] = pId
        self.json['name'] = filename
        if os.path.isdir(toRealPath(file)):
            self.json['type'] = 'folder'
        else:
            self.json['type'] = getFileType(filename)
        self.json['path'] = path
        self.json['size'] = os.stat(toRealPath(file)).st_size
        self.json['_realPath'] = toRealPath(path)
        self.json['thumbnail'] = "icon/folder.png" if self.json['type'] == 'folder' \
            else generateThumbnail(toRealPath(file), self.json['id'], True)
        self.json['date'] = time.strftime(
            "%Y/%m/%d %H:%M:%S", time.gmtime(os.stat(toRealPath(file)).st_ctime))


def allowed_file(filename):
    return True
    # return '.' in filename and \
    #        str.lower(filename.rsplit('.', 1)[1]) in ALLOWED_EXTENSIONS


def __initPath(paths):
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)


def __initSettings():
    sets = {"default": {"sort": {"by": "name",
                                 "reverse": True, "desc": "按名称正序", "index": 0}}}
    json.dump(sets, open(settings, 'w'))


def init(loadLocal=False):
    __initPath([dataPath, thumbnailPath, rawFiles, trash])
    if loadLocal:
        readLoacl()
    if not os.path.exists(settings):
        __initSettings()
    if not os.path.exists(fileList):
        f = File(
            id=newId("/root"),
            pId="000000",
            name="root",
            type="folder",
            path="path",
            size=0,
            _realPath=rawFiles,
            thumbnail="icon/folder.png",
            date=time.strftime("%Y/%m/%d %H:%M:%S"),
        )
        json.dump([f.json], open(fileList, 'w'))


def refreshLocal(datasource=fileList):
    os.remove(datasource)
    readLoacl(datasource)


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
    if fid == 'logo':
        return "icon/logo.png"
    with open(fileList, 'r') as f:
        datasds = json.load(f)
        for d in datasds:
            if d['id'] == fid:
                return d['thumbnail']
    return None


def generateThumbnail(file, md5Name, fromLocal=False):
    if fromLocal:
        ftype = getFileType(file)
    else:
        ftype = getFileType(file.filename)
    if isImg(ftype):
        thumbnail = os.path.join(thumbnailPath, "%s.png" % (md5Name))
        if fromLocal:
            image = Image.open(file)
        else:
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
            if d['name'] == filename and d['path'] == path:
                return True
    return False


def __updateSizes(it, data, mode='add'):
    pids = it['pId']
    i = 0
    while i < len(data):
        # for i in range(0, len(data)):
        d = data[i]
        # print("[+] while: ", i, d['id'], d['pId'])
        if d['type'] != 'folder':
            i += 1
            continue
        if d['id'] == pids:
            if mode == 'add':
                d['size'] += it['size']
            elif mode == 'del':
                d['size'] -= it['size']
            if d['pId'] == '0':
                # print("[+] while break")
                break
            else:
                pids = d['pId']
                i = 0
                continue
        i += 1


def delete_file(fid, datasource=fileList):
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        for d in datasds:
            if d['id'] == fid:
                break
        shutil.move(os.path.join(toRealPath(d['path']), d['name']),
                    os.path.join(trash, d['name']))
        datasds.remove(d)
        __updateSizes(d, datasds, 'del')
        with open(datasource, 'w') as f:
            json.dump(datasds, f)


def rename_file(fid, newname, datasource=fileList):
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        for d in datasds:
            if d['id'] == fid:
                break
        # print("rename: {} to {}".format(os.path.join(toRealPath(
        #     d['path']), d['name']), os.path.join(toRealPath(d['path']), newname)))
        os.rename(os.path.join(toRealPath(d['path']), d['name']),
                  os.path.join(toRealPath(d['path']), newname))
        d['name'] = newname
        with open(datasource, 'w') as f:
            json.dump(datasds, f)
        if d['type'] == 'folder':
            refreshLocal()


def upload_file(file, path, datasource=fileList):
    # print("[+] upload file: ", file.filename)
    md5Name = newId(os.path.join(path, file.filename))
    file.seek(0)
    target_file = os.path.join(toRealPath(path), file.filename)
    # print("[+] upload target file: ", target_file)
    file.save(target_file)
    thumbnail = generateThumbnail(file, md5Name)
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        add = File(
            id=md5Name,
            pId=getId(path),
            name=file.filename,
            type=getFileType(file.filename),
            path=path,
            size=os.stat(target_file).st_size,
            _realPath=toRealPath(path),
            thumbnail=thumbnail,
            date=time.strftime("%Y/%m/%d %H:%M:%S"),
        )
        datasds.append(add.json)
        __updateSizes(add.json, datasds)
        with open(datasource, 'w') as f:
            json.dump(datasds, f)


def newFolder(path, datasource=fileList):
    os.mkdir(toRealPath(path))
    d = {}
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        d = File(
            id=newId(path),
            pId=getId("/".join(path.split("/")[:-1])),
            name=path.split("/")[-1],
            type="folder",
            path="/".join(path.split("/")[:-1]),
            size=0,
            _realPath=toRealPath("/".join(path.split("/")[:-1])),
            thumbnail="icon/folder.png",
            date=time.strftime("%Y/%m/%d %H:%M:%S"),
        )
        datasds.append(d.json)
        with open(datasource, 'w') as f:
            json.dump(datasds, f)
    return d.json


def toRealPath(path):
    # print(dataPath, "/".join(path.split("/")[1:]))
    return os.path.join(dataPath, "/".join(path.split("/")[1:]))


def getId(path, datasource=fileList):
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        for d in datasds:
            if os.path.join(d['path'], d['name']) == path:
                return d['id']
    return newId(path)


def newId(string):
    md5 = hashlib.md5()
    string = string + time.strftime("%Y/%m/%d %H:%M:%S")
    md5.update(string.encode('utf-8'))  # 转码
    res = md5.hexdigest()
    return res


def updateSetting(id, option, field, value, index, datasource=settings):
    with open(datasource, 'r') as f:
        __settings = json.load(f)
        _setting = __settings[id][option]
        _setting['index'] = index
        for k, v in _setting.items():
            if k == field:
                _setting[k] = value
        with open(datasource, 'w') as f:
            json.dump(__settings, f)


def sortQueue(datasource=settings):
    with open(datasource, 'r') as f:
        __settings = json.load(f)
        index = __settings['default']['sort']['index']
        index = index + 1 if index + 1 < len(SORTSET) else 0
        __settings['default']['sort']['index'] = index
        curr_sort = SORTSET[index]
        __settings['default']['sort']['by'] = curr_sort['by']
        __settings['default']['sort']['reverse'] = curr_sort['reverse']
        with open(datasource, 'w') as f:
            json.dump(__settings, f)
    return curr_sort


def getSettings(id, datasource=settings):
    with open(datasource, 'r') as f:
        settings = json.load(f)[id]
        return settings


def sortList(by, reverse=False, datasource=fileList):
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        datasds.sort(key=lambda k: (k.get(by, 0)), reverse=reverse)
        with open(datasource, 'w') as f:
            json.dump(datasds, f)


def __read(path, curr, pid=ROOTID):
    # return all files in path
    # path: 当前文件夹所在目录（/root/下）
    # curr: 当前文件夹名称
    # id: 当前文件夹的id，作为当前文件夹下所有文件的pId
    # pid: 当前文件夹的pid
    curr_path = os.path.join(toRealPath(path), curr)
    id = newId(os.path.join(path, curr))
    files = os.listdir(curr_path)
    res = []
    total_size = 0
    for f in files:
        fp = os.path.join(curr_path, f)
        f_struct = File()
        f_struct.generate(os.path.join(path, curr), f, id)
        if os.path.isdir(fp):
            tmp_res, tmp_size = __read(os.path.join(path, curr), f, id)
            res.extend(tmp_res)
            total_size += tmp_size
        else:
            total_size += os.stat(fp).st_size
            res.append(f_struct.json)
    # 最后生成当前文件夹的信息
    path_struct = File()
    path_struct.generate(path, curr, pid)
    path_struct.json['size'] = total_size
    res.append(path_struct.json)
    return res, total_size


def readLoacl(datasource=fileList):
    files, _ = __read('/', 'root')
    with open(datasource, 'w') as f:
        json.dump(files, f)


def searchKeyword(keyword, datasource=fileList):
    res = []
    with open(datasource, 'r') as f:
        datasds = json.load(f)
        for d in datasds:
            if keyword in d['name']:
                res.append(d)
    return res
