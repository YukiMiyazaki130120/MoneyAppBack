from flask import Flask, jsonify, request, session
import mysql.connector
from flask_cors import CORS

# MySQLに接続
conn = mysql.connector.connect(
    host='127.0.0.1',
    user="root",
    password="aaaaa1234",
    database="appBank"  # appBankデータベースを使用
)

# Flaskのコンストラクタ
app = Flask(__name__, static_folder="static")
CORS(app, supports_credentials=True)

# Sessionの暗号化キー
app.secret_key = b'abcdefghijklmn'

#送金処理
@app.route('/remit', methods=['POST'])
def remit_money():
    data = request.json  # POSTリクエストのデータを取得
    account_num = data.get('account_num')  # 送金先の口座番号
    amount = data.get('amount')  # 送金額

    # 入力データが不足している場合はエラーレスポンスを返す
    if not account_num or not amount:
        return jsonify({"error": "account_num and amount are required"}), 400

    try:
        # カーソルを取得
        cursor = conn.cursor(dictionary=True)

        # 指定された account_num の balance を取得
        cursor.execute("SELECT balance FROM account_info WHERE account_num = %s", (account_num,))
        account = cursor.fetchone()

        # 該当するアカウントが存在しない場合
        if not account:
            return jsonify({"error": "Account not found"}), 404

        # 現在の残高を取得
        current_balance = account['balance']

        # 送金額が残高を超える場合はエラーメッセージを返す
        if float(amount) > current_balance:
            return jsonify({"error": "Insufficient balance"}), 400

        # 新しい残高を計算
        new_balance = current_balance - float(amount)

        # 残高を更新
        cursor.execute("UPDATE account_info SET balance = %s WHERE account_num = %s", (new_balance, account_num))
        conn.commit()  # 変更をコミット

        # 成功レスポンスを返す
        return jsonify({
            "message": "Remittance successful",
            "new_balance": new_balance
        }), 200

    except mysql.connector.Error as err:
        # データベースエラー時の処理
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()  # カーソルを閉じる


# プログラム起動
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
