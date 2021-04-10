webpackJsonp([1], {
    "42hw": function (t, e) { },
    hYS1: function (t, e, o) {
        "use strict";
        Object.defineProperty(e, "__esModule", { value: !0 });
        var setting = {
            view: {
                dblClickExpand: dblClickExpand,
                selectedMulti: false,
                showIcon: true,
                addHoverDom: addHoverDom,
                removeHoverDom: removeHoverDom,
            },
            data: {
                simpleData: {
                    enable: true
                }
            },
            edit: {
                enable: true,
                showRemoveBtn: showRemoveBtn,
                showRenameBtn: showRenameBtn
            },
            callback: {
                beforeExpand: beforeExpand,
                onExpand: onExpand,
                onClick: onClick,
                beforeEditName: beforeEditName,
                beforeRemove: beforeRemove,
                beforeRename: beforeRename,
                onRemove: onRemove,
                onRename: onRename
            }
        };
        var log, className = "dark";
        function dblClickExpand(treeId, treeNode) {
            return treeNode.level > 0;
        }
        function beforeEditName(treeId, treeNode) {
            className = (className === "dark" ? "" : "dark");
            showLog("[ " + getTime() + " beforeEditName ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name);
            var zTree = $.fn.zTree.getZTreeObj("tree");
            zTree.selectNode(treeNode);
            setTimeout(function () {
                if (confirm("进入节点 -- " + treeNode.name + " 的编辑状态吗？")) {
                    setTimeout(function () {
                        zTree.editName(treeNode);
                    }, 0);
                }
            }, 0);
            return false;
        }
        function beforeRemove(treeId, treeNode) {
            className = (className === "dark" ? "" : "dark");
            showLog("[ " + getTime() + " beforeRemove ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name);
            var zTree = $.fn.zTree.getZTreeObj("tree");
            zTree.selectNode(treeNode);
            return confirm("确认删除 节点 -- " + treeNode.name + " 吗？");
        }
        function onRemove(e, treeId, treeNode) {
            showLog("[ " + getTime() + " onRemove ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name);
        }
        function beforeRename(treeId, treeNode, newName, isCancel) {
            className = (className === "dark" ? "" : "dark");
            showLog((isCancel ? "<span style='color:red'>" : "") + "[ " + getTime() + " beforeRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name + (isCancel ? "</span>" : ""));
            if (newName.length == 0) {
                setTimeout(function () {
                    var zTree = $.fn.zTree.getZTreeObj("tree");
                    zTree.cancelEditName();
                    alert("节点名称不能为空.");
                }, 0);
                return false;
            }
            return true;
        }
        function onRename(e, treeId, treeNode, isCancel) {
            showLog((isCancel ? "<span style='color:red'>" : "") + "[ " + getTime() + " onRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name + (isCancel ? "</span>" : ""));
        }
        function showRemoveBtn(treeId, treeNode) {
            return !treeNode.isFirstNode;
        }
        function showRenameBtn(treeId, treeNode) {
            return !treeNode.isLastNode;
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

        function addHoverDom(treeId, treeNode) {
            var sObj = $("#" + treeNode.tId + "_span");
            if (treeNode.editNameFlag || $("#addBtn_" + treeNode.tId).length > 0) return;
            var addStr = "<span class='button add' id='addBtn_" + treeNode.tId
                + "' title='add node' onfocus='this.blur();'></span>";
            sObj.after(addStr);
            var btn = $("#addBtn_" + treeNode.tId);
            if (btn) btn.bind("click", function () {
                var zTree = $.fn.zTree.getZTreeObj("tree");
                treeNode = zTree.addNodes(treeNode, { id: (100 + newCount), pId: treeNode.id, name: "new_node" + (newCount++) });
                if (treeNode) {
                    zTree.editName(treeNode[0]);
                }
                return false;
            });
        };
        function removeHoverDom(treeId, treeNode) {
            $("#addBtn_" + treeNode.tId).unbind().remove();
        };

        var curExpandNode = null;
        function beforeExpand(treeId, treeNode) {
            var pNode = curExpandNode ? curExpandNode.getParentNode() : null;
            var treeNodeP = treeNode.parentTId ? treeNode.getParentNode() : null;
            var zTree = $.fn.zTree.getZTreeObj("tree");
            for (var i = 0, l = !treeNodeP ? 0 : treeNodeP.children.length; i < l; i++) {
                if (treeNode !== treeNodeP.children[i]) {
                    zTree.expandNode(treeNodeP.children[i], false);
                }
            }
            while (pNode) {
                if (pNode === treeNode) {
                    break;
                }
                pNode = pNode.getParentNode();
            }
            if (!pNode) {
                singlePath(treeNode);
            }

        }
        function singlePath(newNode) {
            if (newNode === curExpandNode) return;

            var zTree = $.fn.zTree.getZTreeObj("tree"),
                rootNodes, tmpRoot, tmpTId, i, j, n;

            if (!curExpandNode) {
                tmpRoot = newNode;
                while (tmpRoot) {
                    tmpTId = tmpRoot.tId;
                    tmpRoot = tmpRoot.getParentNode();
                }
                rootNodes = zTree.getNodes();
                for (i = 0, j = rootNodes.length; i < j; i++) {
                    n = rootNodes[i];
                    if (n.tId != tmpTId) {
                        zTree.expandNode(n, false);
                    }
                }
            } else if (curExpandNode && curExpandNode.open) {
                if (newNode.parentTId === curExpandNode.parentTId) {
                    zTree.expandNode(curExpandNode, false);
                } else {
                    var newParents = [];
                    while (newNode) {
                        newNode = newNode.getParentNode();
                        if (newNode === curExpandNode) {
                            newParents = null;
                            break;
                        } else if (newNode) {
                            newParents.push(newNode);
                        }
                    }
                    if (newParents != null) {
                        var oldNode = curExpandNode;
                        var oldParents = [];
                        while (oldNode) {
                            oldNode = oldNode.getParentNode();
                            if (oldNode) {
                                oldParents.push(oldNode);
                            }
                        }
                        if (newParents.length > 0) {
                            zTree.expandNode(oldParents[Math.abs(oldParents.length - newParents.length) - 1], false);
                        } else {
                            zTree.expandNode(oldParents[oldParents.length - 1], false);
                        }
                    }
                }
            }
            curExpandNode = newNode;
        }

        function onExpand(event, treeId, treeNode) {
            curExpandNode = treeNode;
        }

        function onClick(e, treeId, treeNode) {
            var zTree = $.fn.zTree.getZTreeObj("tree");
            zTree.expandNode(treeNode, null, null, null, true);
            zTree.selectNode()
        }

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
                        var t = $("#tree");
                        t = $.fn.zTree.init(t, setting, res.data);
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
                        console.log("[+] path length: ", sub.length, sub)
                        // return this.__cutPath(sub, i - 1);
                        return sub
                    } else {
                        return path
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
                                                        style: { width: "260px", overflow: "auto" },
                                                        attrs: { id: "tree" }
                                                    })]
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
                                        action: this.upurl,
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
