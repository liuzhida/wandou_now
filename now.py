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

from jsonphandler import JSONPHandler

c = redis.Redis(host='127.0.0.1', port=6379, db=0)


class TestHandler(tornado.web.RequestHandler):

    def get(self):
        shoplist = '<h1><a href="dianping://shopinfo?id=4175436">test</></h1>'
        self.set_header('Access-Control-Allow-Origin', '*')
        self.finish(shoplist)
        return


class ShopHandler(JSONPHandler):
#class ShopHandler(tornado.web.RequestHandler):

    def get(self):
        idlist = c.lrange("shoplist", 0, -1)
        shoplist = list()
        for id in idlist[::-1]:
            shop = c.hgetall(id)
            shop['tags'] = eval(shop['tags'])
            shoplist.append(shop)
        shoplist = json.dumps(shoplist)
        self.finish(shoplist)
        return


#class MovieHandler(JSONPHandler):
class MovieHandler(tornado.web.RequestHandler):

    def get(self):
        idlist = c.lrange("movielist", 0, -1)
        #self.finish(json.dumps(idlist))
        shoplist = list()
        for id in idlist[::-1]:
            shop = c.hgetall(id)
            shoplist.append(shop)
        shoplist = json.dumps(shoplist)
        self.finish(shoplist)
        return


def main():
    define("port", default=8089, help="run on the given port", type=int)
    settings = {"debug": True, "template_path": "templates",
                "static_path": "static",
                "cookie_secret": "z1DAVh+WTvyqpWGmOtJCQLETQYUznEuYskSF06To="}
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/shop", ShopHandler),
        (r"/movie", MovieHandler),
        (r"/test", TestHandler),

    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
