webpackJsonp(
    [3],
    {
        E4d3: function (t, e, n) {
            var o = {
                "./list": ["pjeT", 0],
                "./list.vue": ["pjeT", 0],
                "./upload": ["hYS1", 1],
                "./upload.vue": ["hYS1", 1],
            };

            function a(t) {
                var e = o[t];
                return e
                    ? n.e(e[1]).then(function () {
                        return n(e[0]);
                    })
                    : Promise.reject(new Error("Cannot find module '" + t + "'."));
            }
            (a.keys = function () {
                return Object.keys(o);
            }),
                (a.id = "E4d3"),
                (t.exports = a);
        },
        FbjC: function (t, e) { },
        NHnr: function (t, e, n) {
            "use strict";
            Object.defineProperty(e, "__esModule", { value: !0 });
            var o = n("7+uW"),
                a = n("zL8q"),
                r = n.n(a),
                i =
                    (n("tvR6"),
                    {
                        name: "App",
                        data: function () {
                            return { upurl: document.title };
                        },
                    }),
                u = {
                    render: function () {
                        var t = this,
                            e = t.$createElement,
                            n = t._self._c || e;
                        return n(
                            "div",
                            {
                                staticStyle: {
                                    "max-width": "900px",
                                    margin: "0 auto",
                                },
                            },
                            [
                                [
                                    n(
                                        "el-container",
                                        [
                                            n("el-header", { attrs: { height: "80px" } }, [
                                                n(
                                                    "h1",
                                                    {
                                                        staticStyle: {
                                                            margin: "0",
                                                            color: "#fff",
                                                            "font-size": "1.875rem",
                                                            "font-weight": "normal",
                                                            float: "left",
                                                        },
                                                        attrs: { to: "/" }
                                                    },
                                                    [t._v(t._s(t.upurl))]
                                                ),
                                                // t._v(" "),
                                                // n(
                                                //     "div",
                                                //     {
                                                //         staticStyle: { float: "right" },
                                                //     },
                                                //     [
                                                //         n(
                                                //             "router-link",
                                                //             {
                                                //                 staticClass: "swewq",
                                                //                 attrs: { to: "/" },
                                                //             },
                                                //             [t._v("列表")]
                                                //         ),
                                                //         t._v(" "),
                                                //         n(
                                                //             "router-link",
                                                //             {
                                                //                 staticClass: "swewq",
                                                //                 attrs: { to: "/upload" },
                                                //             },
                                                //             [t._v("上传")]
                                                //         ),
                                                //     ],
                                                //     1
                                                // ),
                                            ]),
                                            t._v(" "),
                                            n("el-main", [n("router-view")], 1),
                                            t._v(" "),
                                            n("el-footer", { attrs: { height: "60px" } }, [
                                                n("div", { staticClass: "foot-copys", color: "#fff" }, [
                                                    t._v("\n          © 2021\n          "),
                                                    n(
                                                        "a",
                                                        {
                                                            staticClass: "foot-copy",
                                                            attrs: {
                                                                href: "https://github.com/kunchiang",
                                                                target: "_blank",
                                                            },
                                                        },
                                                        [t._v("KunChiang")]
                                                    ),
                                                ]),
                                            ]),
                                        ],
                                        1
                                    ),
                                ],
                            ],
                            2
                        );
                    },
                    staticRenderFns: [],
                };
            var l = n("VU/8")(
                i,
                u,
                !1,
                function (t) {
                    n("FbjC");
                },
                null,
                null
            ).exports,
                s = n("/ocq");

            function c(t) {
                return function () {
                    return n("E4d3")("./" + t);
                };
            }
            o.default.use(s.a);
            var p = new s.a({
                routes: [
                    {
                        path: "/upload",
                        name: "upload",
                        component: c("upload"),
                    },
                    { path: "/", name: "list", component: c("list") },
                ],
            }),
                f = n("mtWM"),
                d = n.n(f);
            o.default.use(r.a),
                (o.default.config.productionTip = !1),
                (o.default.prototype.$axios = d.a),
                (d.a.defaults.baseURL =
                    window.location.protocol + "//" + window.location.host),
                new o.default({
                    el: "#app",
                    router: p,
                    components: { App: l },
                    template: "<App/>",
                });
        },
        tvR6: function (t, e) { },
    },
    ["NHnr"]
);
