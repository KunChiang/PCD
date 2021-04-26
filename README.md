# PCD

## TODOs

Recent work:

- [x] upload to folders, display folders
- [ ] 修改界面展示形式，删除独立的上传页面，只保留列表页面
  - [ ] 添加按钮：
    - [ ] 新建文件夹
    - [x] 上传文件至当前目录
    - [ ] 批量删除
  - [ ] 上传页面功能迁移至上传按钮，不弹出独立页面，考虑浮窗形式弹出进度条
- [x] 新增filesize，同步更新folder size
- [ ] 排序：类型、文件名、上传时间

Future work:

- [ ] 误删恢复：维护另一个tarsh.json，删除与恢复就成为了两个文件互换元素，检查文件在trash中存在的时长，定时清理
- [ ] 列表页面的展示模式：列表模式、卡片模式可切换
- [ ] 搜索功能：按文件名搜索

## 存储数据结构

filelist.json/MySQL:

```json
[
    {
        "id": 0,
        "pId": 0,
        "name": "root",
        "type": "folder",
        "path": "/path/",
        "size": 1111, //(sum of all children)
        "thumbnail": "icon/folder.png",
        "date": "2021/03/26 18:20:55",
    },
    {
        "id": 0,
        "pId": 0,
        "name": "Kareo API Guide.pdf",
        "type": "pdf",
        "path": "",
        "size": 123,
        "thumbnail": "icon/pdf.png",
        "date": "2021/03/26 18:20:55"
    },
    {
        "id": 0,
        "pId": 0,
        "name": "123",
        "type": "folder",
        "path": "",
        "size": 1111, //(sum of all children)
        "thumbnail": "icon/folder.png",
        "date": "2021/03/26 18:20:55",
    },
]
```

