from flask import Flask, jsonify, session, request
import mysql.connector
from flask_cors import CORS
from datetime import datetime
import random

# MySQLに接続
conn = mysql.connector.connect(
    host='127.0.0.1',
    user="root",
    password="#",
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
        cursor.execute("SELECT account_num, image_path, user_name FROM account_info WHERE account_num != '123456' ")
        # cursor.execute("SELECT account_num, image_path, user_name FROM account_info WHERE account_num NOT IN (%s)", (session.get("account"),))

        accounts = cursor.fetchall()
        print(session.get("account"))
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



@app.route('/Step5_complete', methods=['POST'])  # GETからPOSTに変更
def step5_complete():
    try:
        data = request.json
    
        # データの取り出し
        amount = data.get('amount')
        destination_account = data.get('account_num')
        destination_name = data.get('user_name')

        message = data.get('message')

        # 送金元の情報（セッションやトークンから取得する必要があります）
        sender_account = "123456" 
        
        # カーソルを取得
        cursor = conn.cursor(dictionary=True)
        
        # 送金先の残高を更新
        cursor.execute("UPDATE account_info SET balance = balance + %s WHERE account_num = %s", (amount, destination_account))
        
        # 送金元の残高を更新（減額）
        cursor.execute("UPDATE account_info SET balance = balance - %s WHERE account_num = %s", (amount, sender_account))

        # 送金ログを記録

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""INSERT INTO remittance_log (sender, destination,destination_name, amount, msg,dateinfo)
                        VALUES (%s, %s, %s, %s, %s, %s)""", 
                        (sender_account, destination_account, destination_name ,amount,message,current_date))

        conn.commit()

        return "OK"

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()

@app.route('/Page3_2', methods=['POST'])  # GETからPOSTに変更

def Page3_2():
    try:
        data = request.json
    
        # データの取り出し
        amount = data.get('amount')
        sender_account = data.get('account_num')
        
        destination_account = "123456"
        destination_name = data.get('user_name')
        message = data.get('message')
        
        # カーソルを取得
        cursor = conn.cursor(dictionary=True)
        
        # 現在の日時を取得
        current_date = datetime.now()
        
        # ランダムな3桁の数値を生成
        random_number = random.randint(100, 999)
        
        # URL_linkを作成
        URL_link = f"http://{current_date.strftime('%Y%m%d%H%M%S')}{amount}{random_number}"
        
        # 送金ログを記録
        cursor.execute("""INSERT INTO claim_log (sender, destination, destination_name, amount, msg, dateinfo, URL_link, flag)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                        (sender_account, destination_account, destination_name, amount, message, current_date, URL_link, True))

        conn.commit()

        return jsonify(URL_link)

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()

@app.route('/Page4', methods=['GET'])
def get_remittance_logs():
    try:

        # カーソルを取得
        cursor = conn.cursor(dictionary=True)

        # 送金ログを取得
        cursor.execute("SELECT * FROM remittance_log ORDER BY dateinfo DESC")
        logs = cursor.fetchall()

        # datetime オブジェクトを文字列に変換
        for log in logs:
            log['dateinfo'] = log['dateinfo'].strftime('%Y-%m-%d %H:%M:%S')

        # JSON形式でレスポンスを返す
        return jsonify({
            "remittance_logs": logs
        }), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()

# プログラム起動
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)