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
        for art in response.css('div.articulo__interior'):            
            yield response.follow(art.css('h2')[0].css('a')[0].attrib['href'], callback = self.info)


    def info(self, response):
        texts = response.css('div.articulo__contenedor p::text').getall()
        text = ''
        for p in texts:
            text += p

        yield {
            # título
            'titulo': response.css('h1.articulo-titulo::text').get(default='Sem título').strip(),
            # subtítulo
            'subtitulo': response.css('h2.articulo-subtitulo::text').get(default='Sem subtítulo').strip(),
            # autor
            'autor': response.css('span.autor-nombre a::text').get(default='Sem autor').strip(),
            # data (dd/mm/yyyy hh:mi:ss)
            'data': response.css('time::attr(datetime)').get(default='Sem data').strip(),
            # seção (esportes, economia, etc.)
            'secao': response.url.split('/')[-2],
            # texto
            'texto': text,
            # url 
            'url': response.url
        }

    def get_text(texts):
        text = ''
        for p in texts:
            text += p
        return text
