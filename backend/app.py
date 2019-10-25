from flask import Flask, request, Response, json
from flask_cors import CORS
from functools import wraps
from obj.grupo import Grupo
from obj.time import Time
import func.campeonato as fc
import func.banco as fb
import pymongo as pm


# mongodb://<dbuser>:<dbpassword>@ds023303.mlab.com:23303/test-db
# db-user
# db-pass123

app = Flask(__name__)
CORS(app)

# Conexão com o DB
CONN = pm.MongoClient('ds023303.mlab.com', 23303)
DB = CONN['test-db']
DB.authenticate('db-user', 'db-pass123')

# Autenticação
def checa_autenticacao(u, p):
    return u == 'user' and p == 'user-pass'

def nao_autorizado():
    return Response(
        'Não foi possível autorizar o acesso ao recurso requisitado.\n'
        'É necessário passar o "username" com o valor "user" e a "password" com o valor "user-pass".\n',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def autenticacao_necessaria(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        # Se não estiver autorizado, chama a função nao_autorizado
        if not auth or not checa_autenticacao(auth.username, auth.password):
            return nao_autorizado()
        return f(*args, **kwargs)
    return decorated

# Rota que retorna os jogos de um determinado time na fase de grupos
@app.route('/time/fase-de-grupos/<time>')
@autenticacao_necessaria
def fase_de_grupos(time):
    # Verifica se o time é formato apenas por numeros
    if time.isdigit():
        t = int(time)

        # O nome do time precisa estar entre 1 e 80
        if not 1 <= t <= 80:
            return Response('Os times vão de 1 a 80, você procurou pelo time {:d}.\n'.format(t), 404)

        # Busca pelo time
        query = { "$or": [ { "vencedor.nome": t }, { "perdedor.nome": t}]}
        l = fb.recupera_documentos(DB, 'partidas-fase-de-grupos', query)

        if not l:
            return Response('O banco está vazio, certifique-se de que um campeonato já foi simulado.\n', 404)

        return Response(json.dumps(l), 200, mimetype='application/json')

    return Response('O nome dos times são números, que vão de 1 a 80, você procurou pelo time {:s}.\n'.format(time), 404)

# Rota que retorna os jogos de um determinado time nos playoffs
@app.route('/time/partidas-playoffs/<time>')
@autenticacao_necessaria
def partidas_playoffs(time):
    # Verifica se o time é formato apenas por numeros
    if time.isdigit():
        t = int(time)

        # O nome do time precisa estar entre 1 e 80
        if not 1 <= t <= 80:
            return Response('Os times vão de 1 a 80, você procurou pelo time {:d}.\n'.format(t), 404)

        # Busca pelo time
        query = { "$or": [ { "vencedor.nome": t }, { "perdedor.nome": t}]}
        l = fb.recupera_documentos(DB, 'partidas-playoffs', query)
        
        # Se a lista for vazia, o time não foi classificado para os playoffs ou o banco está vazio
        if not l:
            return Response('O time {:d} não foi classificado para os playoffs.\nOu o banco está vazio, certifique-se de que um campeonato já foi simulado.\n'.format(t), 404)
        
        return Response(json.dumps(l), 200, mimetype='application/json')
    return Response('O nome dos times são números, que vão de 1 a 80, você procurou pelo time {:s}.\n'.format(time), 404)

# Rota que retorna a situação final de todos os times após a fase de grupos
@app.route('/pontuacao-final-grupos')
@autenticacao_necessaria
def pontuacao_final_grupos():
    query = {}
    l = fb.recupera_documentos(DB, 'classificados-fase-de-grupos', query)

    if not l:
        return Response('O banco está vazio, certifique-se de que um campeonato já foi simulado.\n', 404)
    
    return Response(json.dumps(l), 200, mimetype='application/json')

# Rota que retorna o resultado da final
@app.route('/final')
@autenticacao_necessaria
def grande_final():
    query = {}
    l = fb.recupera_documentos(DB, 'final', query)

    if not l:
        return Response('O banco está vazio, certifique-se de que um campeonato já foi simulado.\n', 404)
    
    return Response(json.dumps(l), 200, mimetype='application/json')

# Rota que simula um novo campeonato
@app.route('/simular', methods=['GET', 'DELETE'])
@autenticacao_necessaria
def simular_camp():
    if request.method == 'DELETE' or request.method == 'GET':
        # Limpa o DB para a nova simulação
        for i in ['partidas-fase-de-grupos', 'partidas-playoffs', 'classificados-fase-de-grupos', 'final']:
            fb.limpa_banco(DB, i)

        if request.method == 'DELETE':
            return Response('Dados do campeonado removido do banco.\n', 200)

    if request.method == 'GET':
        partidas_fase_grupos, pontuacao, partidas_playoffs = fc.simula()
        
        # Iterando a lista e formando a lista que sera inserida no DB
        l = []
        for i in partidas_fase_grupos:
            l.append({ 'vencedor': i[0].__dict__, 'perdedor': i[1].__dict__ })
        fb.salva_dados(DB, 'partidas-fase-de-grupos', l)

        l = []
        for i in partidas_playoffs:
            obj1, obj2 = {'nome': i[0].nome, 'rounds': i[0].rounds}, {'nome': i[1].nome, 'rounds': i[1].rounds}
            l.append({'vencedor': obj1, 'perdedor': obj2})

        # Remove o ultimo, que é o campeao e o vice
        l.pop()

        fb.salva_dados(DB, 'partidas-playoffs', l)
        
        obj1 = { 'nome': partidas_playoffs[-1][0].nome, 'rounds': partidas_playoffs[-1][0].rounds }
        obj2 = { 'nome': partidas_playoffs[-1][1].nome, 'rounds': partidas_playoffs[-1][1].rounds }
        fb.salva_um(DB, 'final', {'campeao': obj1, 'vice': obj2})

        l = []
        for i in pontuacao:
            l.append(i.__dict__)
        fb.salva_dados(DB, 'classificados-fase-de-grupos', l)

        return Response('Campeonato simulado!\n', 201)

@app.errorhandler(404)
def page_not_found(e):
    return Response('Endpoint não encontrado.\n',  404)

if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0')
    app.run()