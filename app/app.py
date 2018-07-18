from flask import Flask, render_template, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

#Instancia aplicação e banco sqlite#
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bd.sqlite')
db = SQLAlchemy(app)

#Classes#
class Score(db.Model):
    """
    Classe de pontuação com referencia direta ao banco de dados
    """
    # Cria a referencia de cada coluna no banco de dados com seus respectivos atributos 
    id = db.Column(db.Integer, primary_key=True)
    _user_id = db.Column(db.Integer)
    _score = db.Column(db.Integer)
    user_name = db.Column(db.String(100))
    date_score = db.Column(db.DateTime)
    
    #Construtor da classe
    def __init__(self, user_id, name, date_score, score=0):
        self._user_id = user_id
        self._max_score = 999999
        self._score = score if score < self._max_score else self._max_score
        self.user_name = name
        self.date_score = datetime.strptime(date_score, '%Y-%m-%d')
    
    #Get and SeT
    @property
    def user_id(self):
        return self._user_id
    @property
    def max_score(self):
        return self._max_score

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, score):
        if(score <= self._max_score):
            self._score = score
        else:
            self._score = self._max_score
            print("Usuário atigiu o limite maximo de pontos")

    @property
    def data_score(self):
        return self.date_score.strftime("%d/%m/%Y")
    
    @property
    def total_score(self):
        scores = Score.query.with_entities(Score._score).filter_by(_user_id=self._user_id).all()
        total_score = sum([x[0] for x in scores])
        return int(total_score)
    
    @staticmethod
    def add_score(scores):
        """ 
        Adiciona score ou lista de score ao banco 
        sempre verificando o total de pontos.

        @param scores: Objeto ou lista de scores
        @except: Em caso de erro uma mensagem é enviada
        """
        try:
            if(type(scores) == list):
                for s in scores:
                    new_score = s.score + s.total_score
                    if (new_score > s.max_score):
                        s.score = s.max_score - s.total_score
                    db.session.add(s)
                db.session.commit()
            else:
                new_score = scores.score + scores.total_score
                if (new_score > scores.max_score):
                    scores.score = scores.max_score - scores.total_score
                db.session.add(scores)
                db.session.commit()


        except Exception as e:
            print("Erro para adicionar o usuário")
            print(e)

    def to_dic(self):
        """ 
        Converte o objeto em um dicionario com os principais atributos 

        """
        return {
            'id': self._user_id, 
            'name': self.user_name, 
            'score': self._score, 
            'date':self.date_score 
        }

#Navegação da aplicação

#URL index
@app.route('/')
def index():
    return render_template('index.html', Score=Score)

#URI GET que retornar todos os scores do banco 
@app.route('/scores')
def scores():
    return jsonify([ score.to_dic() for score in Score.query.all()])

#URI POST que recebe o arquivo csv no formato: {content_csv: [[data,nome,id,potuação]]}
@app.route('/create_score', methods=["POST"])
def create_score():
    try:
        data = request.json
        content_csv =  data['content_csv']
        list_score = []
        for row in content_csv:
           list_score.append(Score(row[2].strip(),row[1].strip(),row[0].strip(),int(row[3].strip())))
        Score.query.delete()#Apaga os dados do arquivo antigo
        Score.add_score(list_score)#Insere novos dados
        return jsonify({'status': 200, 'mensagem': 'Dados salvos com sucesso!'})
    except Exception as e:
        print("Erro ao tentar salvar o csv")
        return jsonify({'status': 400, 'mensagem': e})
        

#inicia aplicação
if __name__ == '__main__':
    try:
        db.create_all()
        app.run(debug=False)
    except Exception as e:   
        print(e)
        db.drop_all()

    

