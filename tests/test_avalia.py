"""
def test_create_avaliacao_without_content(client, user, user2):
    avaliacao = {
        'id_autor': user.id,
        'id_destinatario': user2.id,
        'tipo_de_avaliado': 'CARONISTA',
        'nota': 'BOM',
        'conteudo': None,
    }

    response = client.post('/avaliacoes', data=avaliacao)

    print(response.json())  # Adicione este print para inspecionar a resposta

    # assert response.status_code == HTTPStatus.OK
    assert response.json()['id_autor'] == user.id

    # assert response.status_code == HTTPStatus.OK
    assert response.json()['id_autor'] == user.id
    assert response.json()['id_destinatario'] == user2.id
    assert response.json()['nota'] == 'BOM'
    assert response.json()['conteudo'] is None


def test_create_avaliacao_with_content(client, user, user2):
    avaliacao = {
        'id_autor': user.id,
        'id_destinatario': user2.id,
        'tipo_de_avaliado': 'CARONISTA',
        'nota': 'OTIMO',
        'conteudo': 'Excelente experiencia!',
    }

    response = client.post('/avaliacoes', data=avaliacao)

    # assert response.status_code == HTTPStatus.OK
    assert response.json()['id_autor'] == user.id
    assert response.json()['id_destinatario'] == user2.id
    assert response.json()['nota'] == 'OTIMO'
    assert response.json()['conteudo'] == 'Excelente experiencia!'


def test_create_same_avaliacao(client, user, user2, avaliacao):
    avaliacao_data = {
        'id_autor': avaliacao.id_autor,
        'id_destinatario': avaliacao.id_destinatario,
        'tipo_de_avaliado': avaliacao.tipo_de_avaliado.value,
        'nota': avaliacao.nota.value,
        'conteudo': avaliacao.conteudo,
    }

    response = client.post('/avaliacoes', data=avaliacao_data)

    # assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Avaliacao ja existe'


def test_create_invalid_avaliacao(client, user):
    avaliacao = {
        'id_autor': user.id + 1,  # Usuario invalido
        'id_destinatario': user.id,
        'tipo_de_avaliado': 'CARONEIRO',
        'nota': 'RUIM',
        'conteudo': 'Experiencia ruim',
    }

    response = client.post('/avaliacoes', data=avaliacao)

    # assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Input invalid'


def test_get_avaliacao(client, avaliacao):
    response = client.get(f'/avaliacoes/{avaliacao.id}')

    # assert response.status_code == HTTPStatus.OK
    assert response.json()['avaliacao_id'] == avaliacao.id
    assert response.json()['nome_autor'] == avaliacao.nome_autor
    assert response.json()['email_autor'] == avaliacao.email_autor
    assert response.json()['nome_destinatario'] == avaliacao.nome_destinatario
    assert response.json()['nota_avaliacao'] == avaliacao.nota_avaliacao.value


def test_get_nonexistent_avaliacao(client):
    response = client.get('/avaliacoes/99999')  # ID que nao existe

    # assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Avaliacao nao encontrada'
"""
