# Dependências
# pip install flask mysql-connector-python
# python api.py

from flask import Flask, request, jsonify, make_response, abort
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuração da conexão com o banco de dados
def get_db_connection():
    try:
        print("Tentando conectar ao MySQL...")
        connection = mysql.connector.connect(
            host='localhost',
            database='mercadinho_db',
            user='root',
            password=''
        )
        print("Conexão com MySQL estabelecida com sucesso!")
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def close_db(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("Conexão com o banco de dados fechada.")

# ENDPOINTS

# 1. Categoria
@app.route('/categorias', methods=['GET'])
@app.route('/categorias/', methods=['GET'])
def get_categorias():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Categoria")
    categorias = cursor.fetchall()
    close_db(conn, cursor)
    return jsonify(categorias)

@app.route('/categorias/<int:id>', methods=['GET'])
def get_categoria(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Categoria WHERE id = %s", (id,))
    categoria = cursor.fetchone()
    close_db(conn, cursor)
    if categoria:
        return jsonify(categoria)
    else:
        abort(404)

@app.route('/categorias', methods=['POST'])
def create_categoria():
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "INSERT INTO Categoria (nome) VALUES (%s)"
    cursor.execute(sql, (data['nome'],))
    conn.commit()
    id = cursor.lastrowid
    close_db(conn, cursor)
    return jsonify({'id': id, 'mensagem': 'Categoria cadastrada com sucesso'}), 201

@app.route('/categorias/<int:id>', methods=['PUT'])
def update_categoria(id):
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "UPDATE Categoria SET nome = %s WHERE id = %s"
    cursor.execute(sql, (data['nome'], id))
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Categoria atualizada com sucesso'})

@app.route('/categorias/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Categoria WHERE id = %s", (id,))
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Categoria removida com sucesso'})

# 2. Cliente
@app.route('/clientes', methods=['GET'])
@app.route('/clientes/', methods=['GET'])
def get_clientes():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cliente")
    clientes = cursor.fetchall()
    close_db(conn, cursor)
    return jsonify(clientes)

@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cliente WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    close_db(conn, cursor)
    if cliente:
        return jsonify(cliente)
    else:
        abort(404)

@app.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    if not data or 'nome' not in data or 'email' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "INSERT INTO Cliente (nome, email, telefone, endereco) VALUES (%s, %s, %s, %s)"
    values = (data['nome'], data['email'], data.get('telefone'), data.get('endereco'))
    cursor.execute(sql, values)
    conn.commit()
    id = cursor.lastrowid
    close_db(conn, cursor)
    return jsonify({'id': id, 'mensagem': 'Cliente cadastrado com sucesso'}), 201

@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    if not data or 'nome' not in data or 'email' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "UPDATE Cliente SET nome = %s, email = %s, telefone = %s, endereco = %s WHERE id = %s"
    values = (data['nome'], data['email'], data.get('telefone'), data.get('endereco'), id)
    cursor.execute(sql, values)
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Cliente atualizado com sucesso'})

@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Cliente WHERE id = %s", (id,))
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Cliente removido com sucesso'})

# 3. Fornecedor
@app.route('/fornecedores', methods=['GET'])
@app.route('/fornecedores/', methods=['GET'])
def get_fornecedores():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Fornecedor")
    fornecedores = cursor.fetchall()
    close_db(conn, cursor)
    return jsonify(fornecedores)

@app.route('/fornecedores/<int:id>', methods=['GET'])
def get_fornecedor(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Fornecedor WHERE id = %s", (id,))
    fornecedor = cursor.fetchone()
    close_db(conn, cursor)
    if fornecedor:
        return jsonify(fornecedor)
    else:
        abort(404)

@app.route('/fornecedores', methods=['POST'])
def create_fornecedor():
    data = request.get_json()
    if not data or 'nome' not in data or 'email' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "INSERT INTO Fornecedor (nome, email, telefone, endereco) VALUES (%s, %s, %s, %s)"
    values = (data['nome'], data['email'], data.get('telefone'), data.get('endereco'))
    cursor.execute(sql, values)
    conn.commit()
    id = cursor.lastrowid
    close_db(conn, cursor)
    return jsonify({'id': id, 'mensagem': 'Fornecedor cadastrado com sucesso'}), 201

@app.route('/fornecedores/<int:id>', methods=['PUT'])
def update_fornecedor(id):
    data = request.get_json()
    if not data or 'nome' not in data or 'email' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "UPDATE Fornecedor SET nome = %s, email = %s, telefone = %s, endereco = %s WHERE id = %s"
    values = (data['nome'], data['email'], data.get('telefone'), data.get('endereco'), id)
    cursor.execute(sql, values)
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Fornecedor atualizado com sucesso'})

@app.route('/fornecedores/<int:id>', methods=['DELETE'])
def delete_fornecedor(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Fornecedor WHERE id = %s", (id,))
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Fornecedor removido com sucesso'})

# 4. Produto
@app.route('/produtos', methods=['GET'])
@app.route('/produtos/', methods=['GET'])
def get_produtos():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Produto")
    produtos = cursor.fetchall()
    close_db(conn, cursor)
    return jsonify(produtos)

@app.route('/produtos/<int:id>', methods=['GET'])
def get_produto(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Produto WHERE id = %s", (id,))
    produto = cursor.fetchone()
    close_db(conn, cursor)
    if produto:
        return jsonify(produto)
    else:
        abort(404)

@app.route('/produtos', methods=['POST'])
def create_produto():
    data = request.get_json()
    if not data or 'nome' not in data or 'preco' not in data or 'quantidade' not in data or 'categoria_id' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "INSERT INTO Produto (nome, preco, quantidade, categoria_id) VALUES (%s, %s, %s, %s)"
    values = (data['nome'], data['preco'], data['quantidade'], data['categoria_id'])
    cursor.execute(sql, values)
    conn.commit()
    id = cursor.lastrowid
    close_db(conn, cursor)
    return jsonify({'id': id, 'mensagem': 'Produto cadastrado com sucesso'}), 201

@app.route('/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    data = request.get_json()
    if not data or 'nome' not in data or 'preco' not in data or 'quantidade' not in data or 'categoria_id' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "UPDATE Produto SET nome = %s, preco = %s, quantidade = %s, categoria_id = %s WHERE id = %s"
    values = (data['nome'], data['preco'], data['quantidade'], data['categoria_id'], id)
    cursor.execute(sql, values)
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Produto atualizado com sucesso'})

@app.route('/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Produto WHERE id = %s", (id,))
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Produto removido com sucesso'})

# 5. Venda
@app.route('/vendas', methods=['GET'])
@app.route('/vendas/', methods=['GET'])
def get_vendas():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Venda")
    vendas = cursor.fetchall()
    close_db(conn, cursor)
    return jsonify(vendas)

@app.route('/vendas/<int:id>', methods=['GET'])
def get_venda(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Venda WHERE id = %s", (id,))
    venda = cursor.fetchone()
    close_db(conn, cursor)
    if venda:
        return jsonify(venda)
    else:
        abort(404)

@app.route('/vendas', methods=['POST'])
def create_venda():
    data = request.get_json()
    if not data or 'cliente_id' not in data or 'total' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "INSERT INTO Venda (cliente_id, total) VALUES (%s, %s)"
    values = (data['cliente_id'], data['total'])
    cursor.execute(sql, values)
    conn.commit()
    id = cursor.lastrowid
    close_db(conn, cursor)
    return jsonify({'id': id, 'mensagem': 'Venda registrada com sucesso'}), 201

@app.route('/vendas/<int:id>', methods=['PUT'])
def update_venda(id):
    data = request.get_json()
    if not data or 'cliente_id' not in data or 'total' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "UPDATE Venda SET cliente_id = %s, total = %s WHERE id = %s"
    values = (data['cliente_id'], data['total'], id)
    cursor.execute(sql, values)
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Venda atualizada com sucesso'})

@app.route('/vendas/<int:id>', methods=['DELETE'])
def delete_venda(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Venda WHERE id = %s", (id,))
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Venda removida com sucesso'})

# 6. ItemVenda
@app.route('/itens-venda', methods=['GET'])
@app.route('/itens-venda/', methods=['GET'])
def get_itens_venda():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ItemVenda")
    itens = cursor.fetchall()
    close_db(conn, cursor)
    return jsonify(itens)

@app.route('/itens-venda/<int:id>', methods=['GET'])
def get_item_venda(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ItemVenda WHERE id = %s", (id,))
    item = cursor.fetchone()
    close_db(conn, cursor)
    if item:
        return jsonify(item)
    else:
        abort(404)

@app.route('/itens-venda', methods=['POST'])
def create_item_venda():
    data = request.get_json()
    if not data or 'venda_id' not in data or 'produto_id' not in data or 'quantidade' not in data or 'preco_unitario' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "INSERT INTO ItemVenda (venda_id, produto_id, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)"
    values = (data['venda_id'], data['produto_id'], data['quantidade'], data['preco_unitario'])
    cursor.execute(sql, values)
    conn.commit()
    id = cursor.lastrowid
    close_db(conn, cursor)
    return jsonify({'id': id, 'mensagem': 'Item de venda cadastrado com sucesso'}), 201

@app.route('/itens-venda/<int:id>', methods=['PUT'])
def update_item_venda(id):
    data = request.get_json()
    if not data or 'venda_id' not in data or 'produto_id' not in data or 'quantidade' not in data or 'preco_unitario' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "UPDATE ItemVenda SET venda_id = %s, produto_id = %s, quantidade = %s, preco_unitario = %s WHERE id = %s"
    values = (data['venda_id'], data['produto_id'], data['quantidade'], data['preco_unitario'], id)
    cursor.execute(sql, values)
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Item de venda atualizado com sucesso'})

@app.route('/itens-venda/<int:id>', methods=['DELETE'])
def delete_item_venda(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ItemVenda WHERE id = %s", (id,))
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Item de venda removido com sucesso'})

# 7. Fornecedores-Produtos
@app.route('/fornecedores-produtos', methods=['GET'])
@app.route('/fornecedores-produtos/', methods=['GET'])
def get_fornecedores_produtos():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Fornecedor_Produto")
    associacoes = cursor.fetchall()
    close_db(conn, cursor)
    return jsonify(associacoes)

@app.route('/fornecedores-produtos', methods=['POST'])
def create_fornecedor_produto():
    data = request.get_json()
    if not data or 'fornecedor_id' not in data or 'produto_id' not in data:
        return jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "INSERT INTO Fornecedor_Produto (fornecedor_id, produto_id) VALUES (%s, %s)"
    values = (data['fornecedor_id'], data['produto_id'])
    cursor.execute(sql, values)
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Associação cadastrada com sucesso'}), 201

@app.route('/fornecedores-produtos/<int:fornecedor_id>/<int:produto_id>', methods=['DELETE'])
def delete_fornecedor_produto(fornecedor_id, produto_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500
    cursor = conn.cursor()
    sql = "DELETE FROM Fornecedor_Produto WHERE fornecedor_id = %s AND produto_id = %s"
    cursor.execute(sql, (fornecedor_id, produto_id))
    conn.commit()
    close_db(conn, cursor)
    return jsonify({'mensagem': 'Associação removida com sucesso'})

# Manipuladores de erro globais com make_response
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'erro': 'A API não entendeu a solicitação por causa de sintaxe inválida'}), 400)

@app.errorhandler(404)
def not_found(error):
    path = request.path
    parts = path.split('/')
    if len(parts) > 2 and (parts[2].isdigit() or (len(parts) > 3 and parts[2].isdigit() and parts[3].isdigit())):
        # Mapeamento manual para evitar erros de ortografia
        resource_map = {
            'categorias': 'Categoria',
            'clientes': 'Cliente',
            'fornecedores': 'Fornecedor',
            'produtos': 'Produto',
            'vendas': 'Venda',
            'itens-venda': 'Item de venda',
            'fornecedores-produtos': 'Associação fornecedor-produto'
        }
        resource_key = parts[1]
        resource = resource_map.get(resource_key, 'Recurso')
        return make_response(jsonify({'erro': f'{resource} não encontrada(o)'}), 404)
    return make_response(jsonify({'erro': 'Recurso não encontrado'}), 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'erro': 'Erro interno do servidor: falha na conexão com o banco de dados'}), 500)

@app.errorhandler(503)
def service_unavailable(error):
    return make_response(jsonify({'erro': 'A API está indisponível'}), 503)

if __name__ == '__main__':
    try:
        print("Iniciando o servidor Flask na porta 5000...")
        app.run(host='localhost', port=5000)
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
