import pytest
from app import app, db, Enquete, Opcao

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_criar_enquete(client):
    response = client.post('/api/enquetes', json={'titulo': 'Enquete Teste', 'descricao': 'Descrição Teste'})
    assert response.status_code == 201
    assert b'Enquete criada com sucesso' in response.data

def test_listar_enquetes(client):
    client.post('/api/enquetes', json={'titulo': 'Enquete Teste', 'descricao': 'Descrição Teste'})
    response = client.get('/api/enquetes')
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_obter_detalhes_enquete(client):
    client.post('/api/enquetes', json={'titulo': 'Enquete Teste', 'descricao': 'Descrição Teste'})
    response = client.get('/api/enquetes/1')
    assert response.status_code == 200
    assert b'Enquete Teste' in response.data

def test_votar_enquete(client):
    client.post('/api/enquetes', json={'titulo': 'Enquete Teste', 'descricao': 'Descrição Teste'})
    client.post('/api/enquetes/1/opcoes', json={'descricao': 'Opção 1'})
    response = client.post('/api/enquetes/1/votar', json={'opcao_id': 1})
    assert response.status_code == 200
    assert b'Voto computado com sucesso' in response.data

def test_resultados_enquete(client):
    client.post('/api/enquetes', json={'titulo': 'Enquete Teste', 'descricao': 'Descrição Teste'})
    client.post('/api/enquetes/1/opcoes', json={'descricao': 'Opção 1'})
    client.post('/api/enquetes/1/votar', json={'opcao_id': 1})
    response = client.get('/api/enquetes/1/resultados')
    assert response.status_code == 200
    assert response.get_json()[0]['votos'] == 1

def test_visualizar_opcoes(client):
    client.post('/api/enquetes', json={'titulo': 'Enquete Teste', 'descricao': 'Descrição Teste'})
    client.post('/api/enquetes/1/opcoes', json={'descricao': 'Opção 1'})
    response = client.get('/api/enquetes/1/opcoes')
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_adicionar_opcao(client):
    client.post('/api/enquetes', json={'titulo': 'Enquete Teste', 'descricao': 'Descrição Teste'})
    response = client.post('/api/enquetes/1/opcoes', json={'descricao': 'Opção 1'})
    assert response.status_code == 201
    assert b'Opcao adicionada com sucesso' in response.data

def test_deletar_enquete(client):
    client.post('/api/enquetes', json={'titulo': 'Enquete Teste', 'descricao': 'Descrição Teste'})
    response = client.delete('/api/enquetes/1')
    assert response.status_code == 200
    assert b'Enquete deletada com sucesso' in response.data

def test_deletar_opcao(client):
    client.post('/api/enquetes', json={'titulo': 'Enquete Teste', 'descricao': 'Descrição Teste'})
    client.post('/api/enquetes/1/opcoes', json={'descricao': 'Opção 1'})
    response = client.delete('/api/enquetes/1/opcoes/1')
    assert response.status_code == 200
    assert b'Opcao deletada com sucesso' in response.data
