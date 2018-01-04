#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class Capital:
    def __init__(self, capital, country, image):
        self.capital = capital
        self.country = country
        self.image = image


def setup_data():
    lj = Capital(capital="Ljubljana", country="Slovenia", image="../assets/img/Ljubljana.jpg")
    wi = Capital(capital="Vienna", country="Austria", image="../assets/img/Wien.jpeg")
    pa = Capital(capital="Paris", country="France", image="../assets/img/Paris.jpg")
    am = Capital(capital="Amsterdam", country="Netherlands", image="../assets/img/Amsterdam.jpg")
    za = Capital(capital="Zagreb", country="Croatia", image="../assets/img/Zagreb.jpg")
    mo = Capital(capital="Moscow", country="Russia", image="../assets/img/Moscow.jpg")
    at = Capital(capital="Athens", country="Greece", image="../assets/img/Athens.jpg")
    ro = Capital(capital="Rome", country="Italy", image="../assets/img/Rome.jpg")
    be = Capital(capital="Berlin", country="Germany", image="../assets/img/Berlin.jpg")
    ma = Capital(capital="Madrid", country="Spain", image="../assets/img/Madrid.jpg")

    return [lj, wi, pa, am, za, mo, at, ro, be, ma]


class MainHandler(BaseHandler):
    def get(self):
        capital = setup_data()[random.randint(0, 9)]

        params = {"capital": capital}

        return self.render_template("main.html", params=params)


class ResultHandler(BaseHandler):
    def post(self):
        answer = self.request.get("answer")
        country = self.request.get("country")

        capitals = setup_data()
        for item in capitals:
            if item.country == country:
                if item.capital.lower() == answer.lower():
                    result = True
                else:
                    result = False

                params = {"result": result, "item": item}

                return self.render_template("result.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler),
], debug=True)
