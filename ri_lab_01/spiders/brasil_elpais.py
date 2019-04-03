# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('seeds/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        #
        # inclua seu código aqui
        #
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        for container in response.css('div.articulo__envoltorio'):
            yield {
                # título
                titulo: container.css('h1.articulo-titulo::text').get(),
                # subtítulo
                subtitulo: container.css('h2.articulo-subtitulo::text').get(),
                # autor
                autor: container.css('span.autor-nombre::text').get(),
                # data (dd/mm/yyyy hh:mi:ss)
                data: container.css('time.articulo-actualizado::datetime').get(),
                # seção (esportes, economia, etc.)
                secao: container.css('span.enlace::text').get(),
                # texto
                texto: container.css('div.articulo__contenedor::text').get(),
                # url 
                url: container.css('meta.url::content').get(),
            }

        #
        #
        #
