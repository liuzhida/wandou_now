#!/usr/bin/env python
#-*-coding:utf-8-*-
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.auth
from tornado.options import define, options

import json
import redis

c = redis.Redis(host='127.0.0.1', port=6379, db=0)


class TestHandler(tornado.web.RequestHandler):

    def get(self):
        shoplist = '<a href="dianping://shopinfo?id=4175436">test</>'
        return self.finish(shoplist)


class ShopHandler(tornado.web.RequestHandler):

    def get(self):
        idlist = c.lrange("shoplist", 0, -1)
        shoplist = list()
        for id in idlist:
            shop = c.hgetall(id)
            shop['tags'] = eval(shop['tags'])
            shoplist.append(shop)
        shoplist = json.dumps(shoplist)
        return self.finish(shoplist)


def main():
    define("port", default=8089, help="run on the given port", type=int)
    settings = {"debug": True, "template_path": "templates",
                "static_path": "static",
                "cookie_secret": "z1DAVh+WTvyqpWGmOtJCQLETQYUznEuYskSF06To="}
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/shop", ShopHandler),
        (r"/test", TestHandler),

    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
