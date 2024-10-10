from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_db():
    conn = sqlite3.connect('db.sqlite')
    return conn

# Rota para a página de cadastro
@app.route('/', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        turma = request.form['turma']
        
        # Salvar no banco de dados
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pessoas (nome, cpf, turma) VALUES (?, ?, ?)", (nome, cpf, turma))
        conn.commit()
        conn.close()
        
        return redirect(url_for('cadastrar'))
    
    return render_template('cadastro.html')

# Rota para listar as pessoas cadastradas
@app.route('/pessoas')
def listar_pessoas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas")
    pessoas = cursor.fetchall()
    conn.close()
    
    return render_template('pessoas.html', pessoas=pessoas)

# Rota para limpar o banco de dados
@app.route('/limpar', methods=['POST'])
def limpar():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pessoas")  # Apaga todas as entradas
        conn.commit()
        conn.close()
        print("Tabela limpa com sucesso!")
        return jsonify({'status': 'success', 'message': 'Tabela limpa com sucesso!'})
    except Exception as e:
        print(f"Erro ao limpar a tabela: {e}")
        return jsonify({'status': 'error', 'message': 'Erro ao limpar a tabela.'})

if __name__ == '__main__':
    # Criar tabela se não existir
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pessoas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cpf TEXT NOT NULL,
                        turma TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()
    
    app.run(debug=True)
