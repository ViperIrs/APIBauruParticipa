from flask import Flask, request, jsonify
from models import db, Enquete, Opcao

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bauru_participa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

@app.route('/api/enquetes', methods=['POST'])
def criar_enquete():
    data = request.get_json()
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    if not titulo or not descricao:
        return jsonify({'message': 'Dados incompletos'}), 400
    enquete = Enquete(titulo=titulo, descricao=descricao)
    db.session.add(enquete)
    db.session.commit()
    return jsonify({'id': enquete.id, 'message': 'Enquete criada com sucesso'}), 201

@app.route('/api/enquetes', methods=['GET'])
def listar_enquetes():
    enquetes = Enquete.query.all()
    return jsonify([{'id': e.id, 'titulo': e.titulo, 'descricao': e.descricao} for e in enquetes]), 200

@app.route('/api/enquetes/<int:id>', methods=['GET'])
def obter_detalhes_enquete(id):
    enquete = Enquete.query.get_or_404(id)
    return jsonify({'id': enquete.id, 'titulo': enquete.titulo, 'descricao': enquete.descricao}), 200

@app.route('/api/enquetes/<int:id>/votar', methods=['POST'])
def votar_enquete(id):
    data = request.get_json()
    opcao_id = data.get('opcao_id')
    opcao = Opcao.query.filter_by(id=opcao_id, enquete_id=id).first()
    if not opcao:
        return jsonify({'message': 'Opção não encontrada'}), 404
    opcao.votos += 1
    db.session.commit()
    return jsonify({'message': 'Voto computado com sucesso'}), 200

@app.route('/api/enquetes/<int:id>/resultados', methods=['GET'])
def resultados_enquete(id):
    enquete = Enquete.query.get_or_404(id)
    resultados = [{'id': opcao.id, 'descricao': opcao.descricao, 'votos': opcao.votos} for opcao in enquete.opcoes]
    return jsonify(resultados), 200

@app.route('/api/enquetes/<int:id>/opcoes', methods=['GET'])
def visualizar_opcoes(id):
    enquete = Enquete.query.get_or_404(id)
    opcoes = [{'id': opcao.id, 'descricao': opcao.descricao} for opcao in enquete.opcoes]
    return jsonify(opcoes), 200

@app.route('/api/enquetes/<int:id>/opcoes', methods=['POST'])
def adicionar_opcao(id):
    data = request.get_json()
    descricao = data.get('descricao')
    if not descricao:
        return jsonify({'message': 'Descrição não fornecida'}), 400
    enquete = Enquete.query.get_or_404(id)
    opcao = Opcao(descricao=descricao, enquete_id=id)
    db.session.add(opcao)
    db.session.commit()
    return jsonify({'id': opcao.id, 'message': 'Opção adicionada com sucesso'}), 201

@app.route('/api/enquetes/<int:id>', methods=['DELETE'])
def deletar_enquete(id):
    enquete = Enquete.query.get_or_404(id)
    db.session.delete(enquete)
    db.session.commit()
    return jsonify({'message': 'Enquete deletada com sucesso'}), 200

@app.route('/api/enquetes/<int:enquete_id>/opcoes/<int:opcao_id>', methods=['DELETE'])
def deletar_opcao(enquete_id, opcao_id):
    opcao = Opcao.query.filter_by(id=opcao_id, enquete_id=enquete_id).first_or_404()
    db.session.delete(opcao)
    db.session.commit()
    return jsonify({'message': 'Opção deletada com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)
