#!/usr/bin/env python3

import scrapy
import re
import json
import os


class LotofacilSpider(scrapy.Spider):
    name = "lotofacil"

    def __init__ (self, first_game, last_game):
        self.first_game = first_game
        self.last_game = last_game


    def start_requests(self):
        urls = [
            'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def get_numbers_sequences(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        games_sequences_filename = os.path.join(dir_path, "games_sequences.json")
        mock_sequences_filename = os.path.join(dir_path, "mock_games_sequences.json")

        if os.path.exists(games_sequences_filename):
            return games_sequences_filename

        return mock_sequences_filename

    def parse(self, response):
        princ_url = response.css("base::attr(href)").extract()[0]
        search_url = response.css("div#resultados input[type=hidden][id=urlBuscarResultado]::attr(value)").extract()[0]
        search_key = response.css("div#resultados input[type=text]::attr(name)").extract()[0]

        for game_number in range(int(self.first_game), int(self.last_game) + 1):
            url = princ_url + search_url + "?" + search_key + "=" + str(game_number)
            yield scrapy.Request(url=url, callback=self.parse_game)


    def parse_game(self, response):
        concurso_dict = json.loads(response.body_as_unicode())
        numeros_sorteados = [int(s) for s in concurso_dict["resultadoOrdenado"].split("-")]

        games_sequences_filename = self.get_numbers_sequences()
        with open(games_sequences_filename) as json_data:
            jogos_dict = json.load(json_data)

        jogos = jogos_dict.values()

        ganhos_lst = []
        for i, jogo in enumerate(jogos):
            acertos = len(set(jogo).intersection(numeros_sorteados))
            if acertos >= 11:
                ganho_dict = self.get_ganhos_info(concurso_dict, acertos, i + 1)
                ganhos_lst.append(ganho_dict)

        return ganhos_lst


    def get_ganhos_info(self, concurso_dict, acertos, i):
        dict_infos_interesse = {}
        dict_infos_interesse["jogo"] = i
        dict_infos_interesse["concurso"] = concurso_dict["nu_concurso"]
        dict_infos_interesse["data"] = concurso_dict["dt_apuracaoStr"]

        if acertos == 11:
            dict_infos_interesse["ganho"] = 4
        elif acertos == 12:
            dict_infos_interesse["ganho"] = 8
        elif acertos == 13:
            dict_infos_interesse["ganho"] = 20
        elif acertos == 14:
            dict_infos_interesse["ganho"] = concurso_dict["vr_rateio_faixa2"]
        else:
            dict_infos_interesse["ganho"] = concurso_dict["vr_rateio_faixa1"]

        return dict_infos_interesse
