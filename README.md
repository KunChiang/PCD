# PCD

存储数据结构 json:

```json
{
    "root": {
        "name": "",//当前文件或文件夹的名称
        "path": "",//当前文件或文件夹的实际存储路径
        "type": "folder",
        "date": "2021/03/26 18:20:55",
        "thumbnail": "icon/folder.png",
        "children":[
            {
                "name": "Kareo API Guide.pdf",
                "path": "",
                "thumbnail": "icon/pdf.png",
                "type": "pdf",
                "date": "2021/03/26 18:20:55"
            },
            {
                "name": "123",
                "path": "",
                "type": "folder",
                "date": "2021/03/26 18:20:55",
                "thumbnail": "icon/folder.png",
                "children":
                [
                    "file_id2": {},
                    "fold_id2": {},
                    ...
                ]
            }
        ]
    }
}
```

```json
[
    {
        "id": 0,
        "pId": 0,
        "name": "root",
        "type": "folder",
        "path": "/path/",
        "thumbnail": "icon/folder.png",
        "date": "2021/03/26 18:20:55",
    },
    {
        "id": ,
        "pId": 0,
        "name": "Kareo API Guide.pdf",
        "type": "pdf",
        "path": "",
        "thumbnail": "icon/pdf.png",
        "date": "2021/03/26 18:20:55"
    },
    {
        "id": 0,
        "pId": 0,
        "name": "123",
        "type": "folder",
        "path": "",
        "thumbnail": "icon/folder.png",
        "date": "2021/03/26 18:20:55",
    },
]
```
