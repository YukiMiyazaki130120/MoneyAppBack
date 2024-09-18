from flask import Flask, jsonify
import mysql.connector

# MySQLに接続
conn = mysql.connector.connect(
    host='127.0.0.1',
    user="root",
    password="22426Free",
    database="appBank"  # appBankデータベースを使用
)

# Flaskのコンストラクタ
app = Flask(__name__, static_folder="static")

# ルーティング定義
@app.route('/top', methods=['GET'])
def get_account():
    try:
        # カーソルを取得
        cursor = conn.cursor(dictionary=True)
        
        # 口座番号123456の情報を取得
        cursor.execute("SELECT * FROM account_info WHERE account_num = '123456'")
        account = cursor.fetchone()
        
        if account:
            return jsonify(account)
        else:
            return jsonify({"error": "Account not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()

# ルーティング定義
@app.route('/send_money', methods=['GET'])
def send_money():
    try:
        # カーソルを取得
        cursor = conn.cursor(dictionary=True)
        
        # 口座番号123456の情報を取得
        cursor.execute("SELECT account_num, image_path, user_name FROM account_info ")
        account = cursor.fetchall()
        
        if account:
            return jsonify(account)
        else:
            return jsonify({"error": "Account not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()


# プログラム起動
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)