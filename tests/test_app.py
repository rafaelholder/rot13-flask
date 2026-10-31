import pytest

from app import MAX_CARACTERES, app, rot13


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_rot13_minusculas_e_maiusculas():
    assert rot13("Hello, World!") == "Uryyb, Jbeyq!"


def test_rot13_aplicado_duas_vezes_volta_ao_original():
    texto = "A cifra de César com chave 13"
    assert rot13(rot13(texto)) == texto


def test_rot13_mantem_numeros_simbolos_e_acentos():
    assert rot13("123 !? çãé") == "123 !? çãé"


def test_pagina_inicial(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "Algoritmo ROT13" in resposta.get_data(as_text=True)


def test_formulario_converte_o_texto(client):
    resposta = client.post("/", data={"texto": "Hello"})
    assert resposta.status_code == 200
    assert "Uryyb" in resposta.get_data(as_text=True)


def test_html_enviado_e_escapado(client):
    resposta = client.post("/", data={"texto": "<script>alert(1)</script>"})
    html = resposta.get_data(as_text=True)
    assert "<script>" not in html
    assert "&lt;fpevcg&gt;" in html


def test_texto_longo_e_cortado(client):
    resposta = client.post("/", data={"texto": "a" * (MAX_CARACTERES + 500)})
    html = resposta.get_data(as_text=True)
    assert "n" * MAX_CARACTERES in html
    assert "n" * (MAX_CARACTERES + 1) not in html


def test_requisicao_grande_demais_e_recusada(client):
    resposta = client.post("/", data={"texto": "a" * 100_000})
    assert resposta.status_code == 413
