# X(Twitter) Space 通知Bot

これは、指定したTwitterユーザーリストが開始したTwitter Spaceを監視し、新しいSpaceが開始された際に自動でツイートして通知するBotです。AWS Chaliceフレームワークを使用して構築されており、AWS Lambda上で定期的に実行されます。

## 主な機能

- **定期的な監視**: AWS LambdaとAmazon EventBridgeを利用して、6分ごとに指定されたTwitterアカウントのSpaceを自動的にチェックします。
- **自動ツイート通知**: 新しいTwitter Spaceが検出された場合、そのSpaceのタイトルとURLを含むツイートを自動的に投稿します。
- **重複通知の防止**: 通知済みのSpace IDをAmazon S3に保存することで、同じSpaceについて重複して通知することを防ぎます。
- **スレッド形式での投稿**: 以前の通知ツイートに返信する形で新しいツイートを投稿し、通知をスレッド形式でまとめます。

## 必要なもの

このBotを実行するためには、以下のものが必要です。

-   Python 3.8以上
-   AWSアカウントと設定済みの認証情報
-   Twitter開発者アカウントと以下のAPIキー:
    -   Consumer Key
    -   Consumer Secret
    -   Access Token
    -   Access Token Secret
    -   Bearer Token
-   通知済みのSpace IDや最後のツイートIDを保存するためのAmazon S3バケット

## 環境設定

1.  **リポジトリをクローンします。**
    ```bash
    git clone https://github.com/your-username/Twitter-Space-NoticeBot.git
    cd Twitter-Space-NoticeBot
    ```

2.  **必要なPythonライブラリをインストールします。**
    ```bash
    pip install -r requirements.txt
    ```

3.  **環境変数を設定します。**
    このプロジェクトでは、AWS Chaliceの機能を利用して環境変数を管理します。プロジェクトルートの`.chalice/config.json`ファイルに、以下のように環境変数を設定してください。

    ```json
    {
      "version": "2.0",
      "app_name": "Twitter-Space-NoticeBot",
      "stages": {
        "dev": {
          "environment_variables": {
            "CONSUMER_KEY": "YOUR_CONSUMER_KEY",
            "CONSUMER_SECRET": "YOUR_CONSUMER_SECRET",
            "ACCESS_TOKEN": "YOUR_ACCESS_TOKEN",
            "ACCESS_TOKEN_SECRET": "YOUR_ACCESS_TOKEN_SECRET",
            "BEARER_TOKEN": "YOUR_BEARER_TOKEN",
            "BUCKET_NAME": "your-s3-bucket-name"
          }
        }
      }
    }
    ```

## デプロイ方法

AWS Chaliceを使用して、簡単にアプリケーションをデプロイできます。

```bash
chalice deploy
```

このコマンドを実行すると、ChaliceがLambda関数、IAMロール、およびEventBridgeルールを自動的にプロビジョニングし、デプロイします。

## 監視対象の更新方法

監視したいTwitterアカウントのリストは、`chalicelib/hololive.py`ファイル内の`get_twitter_num`静的メソッドで管理されています。

新しいアカウントを追加または削除するには、このメソッド内の辞書を編集してください。キーにはアカウント名（任意）、値にはTwitterのユーザーID（数値）を指定します。

```python
# chalicelib/hololive.py

class Hololive:
    # ...（他のメソッド）...

    @staticmethod
    def get_twitter_num():
        return {
            '友人A(えーちゃん)' : 1064352899705143297,
            '春先のどか' : 1499026372089778181,
            # ... 他のアカウント ...
            # ここに新しいアカウントを追加
            '新しいアカウント名': 1234567890
        }
```
