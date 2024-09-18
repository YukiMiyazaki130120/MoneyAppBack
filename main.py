from flask import Flask, jsonify, session, request
import mysql.connector
from flask_cors import CORS

# MySQLに接続
conn = mysql.connector.connect(
    host='127.0.0.1',
    user="root",
    password="Kouki052315",
    database="appBank"  # appBankデータベースを使用
)

# Flaskのコンストラクタ
app = Flask(__name__, static_folder="static")
CORS(
    app,
    supports_credentials=True
)

# Sessionの暗号化キー
app.secret_key = b'abcdefghijklmn'


# ルーティング定義
@app.route('/top', methods=['GET'])
def get_account():

    session["account"] = "123456"  # セッションに口座番号をセット
    
    try:

        # カーソルを取得
        cursor = conn.cursor(dictionary=True)
        
        # セッションから口座番号を取得
        account_num = session.get("account")
        
        if account_num is None:
            return jsonify({"error": "No account number in session"}), 400
        
        # 口座番号に基づいて情報を取得
        cursor.execute("SELECT * FROM account_info WHERE account_num = %s", (account_num,))
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
@app.route('/RemittanceDest', methods=['GET'])
def send_money():
    try:

        # カーソルを取得
        cursor = conn.cursor(dictionary=True)
        
        # 全ての口座情報を取得
        cursor.execute("SELECT account_num, image_path, user_name FROM account_info WHERE account_num NOT IN (%s)", (session.get("account"),))
        accounts = cursor.fetchall()
        
        if accounts:
            return jsonify(accounts)
        else:
            return jsonify({"error": "No accounts found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()


# ルーティング定義
@app.route('/Step4', methods=['GET'])
def send_account_info():
    try:
        # カーソルを取得
        cursor = conn.cursor(dictionary=True)
        
        # 送り先の口座情報を取得
        cursor.execute("SELECT account_num, image_path, user_name, balance FROM account_info WHERE account_num IN (%s)", ("送信先の口座番号",))
        accounts = cursor.fetchone()
        
        if accounts:
            return jsonify(accounts)
        else:
            return jsonify({"error": "No accounts found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()


# ルーティング定義
@app.route('/Step5_complete', methods=['GET'])
def step5_complete():
    try:
        # カーソルを取得
        cursor = conn.cursor(dictionary=True)
        
        # 全ての口座情報を取得
        cursor.execute("UPDATE account_info SET balance = balance + 金額 WHERE account_num = %s", ('送り先の口座番号',))
        cursor.execute("UPDATE account_info SET balance = balance + 金額 WHERE account_num = %s", ('送り元の口座番号',))

        cursor.execute("""INSERT INTO remittance_log (sender,destination,amount,msg,dateinfo,flag)
                        VALUES (送金元,送金先,金額,メッセージ,日付,TRUE)""")

        conn.commit()

        return '完了'
    finally:
        cursor.close()


# プログラム起動
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)