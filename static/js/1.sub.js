webpackJsonp([1], {
    "42hw": function (t, e) { },
    hYS1: function (t, e, o) {
        "use strict";
        Object.defineProperty(e, "__esModule", { value: !0 });
        var curMenu = null, zTree_Menu = null;
        var setting = {
            view: {
                showLine: false,
                showIcon: true,
                selectedMulti: false,
                dblClickExpand: false,
                addDiyDom: addDiyDom,
            },
            data: {
                simpleData: {
                    enable: true
                }
            },
            edit: {
                enable: true,
            },
            callback: {
                beforeClick: beforeClick,
                beforeDrag: beforeDrag,
                beforeRemove: beforeRemove,
                beforeRename: beforeRename,
                onRemove: onRemove
            }
        };
        function addDiyDom(treeId, treeNode) {
            var spaceWidth = 10;
            var switchObj = $("#" + treeNode.tId + "_switch"),
                icoObj = $("#" + treeNode.tId + "_ico");
            switchObj.remove();
            icoObj.before(switchObj);

            if (treeNode.level > 0) {
                var spaceStr = "<span style='display: inline-block;width:" + (spaceWidth * treeNode.level) + "px'></span>";
                switchObj.before(spaceStr);
            }
        }

        function beforeClick(treeId, treeNode) {
            if (treeNode.level >= 0) {
                var zTree = $.fn.zTree.getZTreeObj("tree");
                zTree.expandNode(treeNode);
                return true;
            }
            return true;
        }
        var log, className = "dark";
        function beforeDrag(treeId, treeNodes) {
            return false;
        }
        function beforeRemove(treeId, treeNode) {
            className = (className === "dark" ? "" : "dark");
            showLog("[ " + getTime() + " beforeRemove ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name);
            return confirm("确认删除 节点 -- " + treeNode.name + " 吗？");
        }
        function onRemove(e, treeId, treeNode) {
            showLog("[ " + getTime() + " onRemove ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name);
        }
        function beforeRename(treeId, treeNode, newName) {
            if (newName.length == 0) {
                alert("节点名称不能为空.");
                var zTree = $.fn.zTree.getZTreeObj("tree");
                setTimeout(function () { zTree.editName(treeNode) }, 10);
                return false;
            }
            return true;
        }
        function showLog(str) {
            if (!log) log = $("#log");
            log.append("<li class='" + className + "'>" + str + "</li>");
            if (log.children("li").length > 8) {
                log.get(0).removeChild(log.children("li")[0]);
            }
        }
        function getTime() {
            var now = new Date(),
                h = now.getHours(),
                m = now.getMinutes(),
                s = now.getSeconds(),
                ms = now.getMilliseconds();
            return (h + ":" + m + ":" + s + " " + ms);
        }

        var newCount = 1;
        function add(e) {
            console.log(e);
            var zTree = $.fn.zTree.getZTreeObj("tree");
            console.log(zTree);
            var isParent = e.data.isParent,
                nodes = zTree.getSelectedNodes(),
                treeNode = nodes[0];
            if (treeNode) {
                treeNode = zTree.addNodes(treeNode, { id: (100 + newCount), pId: treeNode.id, isParent: isParent, name: "new node" + (newCount++) });
            } else {
                treeNode = zTree.addNodes(null, { id: (100 + newCount), pId: 0, isParent: isParent, name: "new node" + (newCount++) });
            }
            if (treeNode) {
                zTree.editName(treeNode[0]);
            } else {
                alert("叶子节点被锁定，无法增加子节点");
            }
        };
        function edit() {
            var zTree = $.fn.zTree.getZTreeObj("tree"),
                nodes = zTree.getSelectedNodes(),
                treeNode = nodes[0];
            if (nodes.length == 0) {
                alert("请先选择一个节点");
                return;
            }
            zTree.editName(treeNode);
        };
        function remove(e) {
            var zTree = $.fn.zTree.getZTreeObj("tree"),
                nodes = zTree.getSelectedNodes(),
                treeNode = nodes[0];
            if (nodes.length == 0) {
                alert("请先选择一个节点");
                return;
            }
            var callbackFlag = $("#callbackTrigger").attr("checked");
            zTree.removeNode(treeNode, callbackFlag);
        };
        function clearChildren(e) {
            var zTree = $.fn.zTree.getZTreeObj("tree"),
                nodes = zTree.getSelectedNodes(),
                treeNode = nodes[0];
            if (nodes.length == 0 || !nodes[0].isParent) {
                alert("请先选择一个父节点");
                return;
            }
            zTree.removeChildNodes(treeNode);
        };
        var n = {
            name: "upload",
            data: function () {
                return {
                    upurl:
                        window.location.protocol +
                        "//" +
                        window.location.host +
                        "/uploads",
                    currpath: "/root",
                    newCount: 1,
                };
            },
            methods: {
                weqewqq2: function (t, e, o) {
                    console.log(o);
                },
                weqweqeq: function (t) {
                    if (t.status === "success") {
                        window.open(
                            window.location.protocol +
                            "//" +
                            window.location.host +
                            "/tc/" +
                            t.name
                        );
                    } else {
                        this.$notify.error({
                            title: "错误",
                            message: "上传失败，请重试！",
                        });
                    }
                },
                browseFolder: function (c) {
                    console.log("BrowseFolder");
                    var e = this;
                    var res = e.$axios.get("/browse?path=" + c).then(res => {
                        // console.log(res.data);
                        var treeObj = $("#tree");
                        treeObj = $.fn.zTree.init(treeObj, setting, res.data);
                        zTree_Menu = $.fn.zTree.getZTreeObj("tree");
                        curMenu = zTree_Menu.getNodes()[0].children[0].children[0];
                        zTree_Menu.selectNode(curMenu);
                        // treeObj.addClass("showIcon");

                        // treeObj.extend.hover(function () {
                        //     if (!treeObj.hasClass("showIcon")) {
                        //         treeObj.addClass("showIcon");
                        //     }
                        // }, function () {
                        //     treeObj.removeClass("showIcon");
                        // });
                    })
                },
                __getFullPath: function (nodes) {
                    var path = '/';
                    for (var i = 0; i < nodes.length; i++) {
                        path = path + nodes[i].name + '/';
                    }
                    return path;
                },
                __cutPath: function (path, i = 2) {
                    if (path.length > 24) {
                        var sub = path.split('/');
                        sub = '/' + sub.slice(1, 2) + '/.../' + sub.slice(-3, -3 + i).join('/');
                        // console.log("[+] path length: ", sub.length, sub)
                        // return this.__cutPath(sub, i - 1);
                        return sub
                    } else {
                        return path
                    }
                },
                add_node: function () {
                    var zTree = $.fn.zTree.getZTreeObj("tree");
                    console.log(zTree);
                    var isParent = zTree.setting.data.isParent,
                        nodes = zTree.getSelectedNodes(),
                        treeNode = nodes[0];
                    if (treeNode) {
                        treeNode = zTree.addNodes(treeNode, { id: (100 + this.newCount), pId: treeNode.id, isParent: isParent, name: "new node" + (newCount++) });
                    } else {
                        treeNode = zTree.addNodes(null, { id: (100 + this.newCount), pId: 0, isParent: isParent, name: "new node" + (newCount++) });
                    }
                    if (treeNode) {
                        zTree.editName(treeNode[0]);
                    } else {
                        alert("叶子节点被锁定，无法增加子节点");
                    }
                    console.log("新建成功：", treeNode)
                },
                edit_node: function () {
                    var zTree = $.fn.zTree.getZTreeObj("tree"),
                        nodes = zTree.getSelectedNodes(),
                        treeNode = nodes[0];
                    if (nodes.length == 0) {
                        alert("请先选择一个节点");
                        return;
                    }
                    zTree.editName(treeNode);
                },
                remove_node: function () {
                    var zTree = $.fn.zTree.getZTreeObj("tree"),
                        nodes = zTree.getSelectedNodes(),
                        treeNode = nodes[0];
                    if (nodes.length == 0) {
                        alert("请先选择一个节点");
                        return;
                    }
                    var r = confirm("确定要删除文件：" + t + " 吗？？");
                    if (r) {
                        var callbackFlag = $("#callbackTrigger").attr("checked");
                        zTree.removeNode(treeNode, callbackFlag);
                    } else {
                        console.log("取消删除");
                    }
                },
                getSelect: function () {
                    var treeObj = $.fn.zTree.getZTreeObj("tree");
                    var nodes = treeObj.getSelectedNodes();
                    if (nodes.length > 0) {
                        console.log("上传至： ", this.__getFullPath(nodes[0].getPath()));
                        this.currpath = this.__getFullPath(nodes[0].getPath())
                    } else {
                        console.log("没有选择路径！")
                    }
                    $('#selectModel').modal('hide')
                }
            },
        },
            i = {
                render: function () {
                    var x = this,
                        t = this.$createElement,
                        e = this._self._c || t;
                    return e(
                        "div",
                        {
                            attrs: {
                                type: "flex",
                            },
                        },
                        [
                            e(
                                "div",
                                {
                                    staticClass: "select_wrap",
                                    attrs: { id: "selectWrap" },
                                },
                                [
                                    e(
                                        "el-button",
                                        {
                                            on: { click: x.browseFolder(x.currpath) },
                                            attrs: {
                                                "data-toggle": "modal",
                                                "data-target": "#selectModel",
                                            },
                                        },
                                        [x._v(x._s("选择路径"))]
                                    ),
                                    e("div", {
                                        attrs: {
                                            class: "modal fade",
                                            id: "selectModel",
                                            tabindex: "-1",
                                            role: "dialog",
                                            "aria-labelledby": "exampleModalLabel",
                                            "aria-hidden": "true",
                                        },
                                    },
                                        [e("div", {
                                            class: "modal-dialog modal-dialog-centered",
                                            attrs: {
                                                "role": "document"
                                            }
                                        },
                                            [e("div", {
                                                class: "modal-content",
                                            },
                                                [e("div", {
                                                    class: "modal-header",
                                                },
                                                    [e("h5", {
                                                        class: "modal-title",
                                                        attrs: {
                                                            id: "exampleModalLabel"
                                                        }
                                                    }, [x._v(x._s("选择路径"))]),
                                                    ]),
                                                e("div", {
                                                    class: "modal-body"
                                                },
                                                    [e("ul", {
                                                        class: "ztree",
                                                        style: { width: "97%", height: "80%", overflow: "auto" },
                                                        attrs: { id: "tree" }
                                                    }),
                                                    e("button", {
                                                        style: { "margin-top": "10px" },
                                                        attrs: {
                                                            "type": "button",
                                                            class: "btn btn-primary",
                                                        }, on: { click: x.add_node },
                                                    }, [x._v(x._s("新建"))]),
                                                    e("button", {
                                                        style: { "margin-top": "10px" },
                                                        attrs: {
                                                            "type": "button",
                                                            class: "btn btn-primary",
                                                        }, on: { click: x.edit_node },
                                                    }, [x._v(x._s("编辑"))]),
                                                    e("button", {
                                                        style: { "margin-top": "10px" },
                                                        attrs: {
                                                            "type": "button",
                                                            class: "btn btn-primary",
                                                        }, on: { click: x.remove_node },
                                                    }, [x._v(x._s("删除"))]),
                                                    ]
                                                    // [x._v(x._s("选择一个路径"))]
                                                ),
                                                e("div", {
                                                    class: "modal-footer",
                                                },
                                                    [e("button", {
                                                        attrs: {
                                                            "type": "button",
                                                            "data-dismiss": "modal",
                                                            class: "btn btn-secondary",
                                                        }
                                                    }, [x._v(x._s("关闭"))]),
                                                    e("button", {
                                                        attrs: {
                                                            "type": "button",
                                                            class: "btn btn-primary",
                                                        },
                                                        on: { click: x.getSelect },
                                                    }, [x._v(x._s("确定"))])],
                                                )

                                                ]
                                            )]
                                        )]
                                    ),
                                    e("span", { staticStyle: { "font-size": "14px" } }, [this._v(" 上传路径: " + x.__cutPath(x.currpath))]),
                                ]
                            ),
                            // e("span", { staticStyle: { "font-size": "14px" } }, [x._v("上传到: " + x.currpath)]),
                            this._v(" "),
                            e(
                                "el-upload",
                                {
                                    attrs: {
                                        drag: "",
                                        action: this.upurl + "/?path=" + x.currpath,
                                        "on-success": this.weqewqq2,
                                        "on-preview": this.weqweqeq,
                                        multiple: "",
                                    },
                                },
                                [
                                    e("i", {
                                        staticClass: "el-icon-upload",
                                    }),
                                    this._v(" "),
                                    e("div", { staticClass: "el-upload__text" }, [
                                        this._v("\n    将文件拖到此处，或\n    "),
                                        e("em", [this._v("点击上传")]),
                                    ]),
                                ]
                            ),
                        ]
                    );
                },
                staticRenderFns: [],
            };
        var s = o("VU/8")(
            n,
            i,
            !1,
            function (t) {
                o("42hw");
            },
            null,
            null
        );
        e.default = s.exports;
    },
});
