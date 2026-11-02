
SlackPostman
===

Slackに投稿するよ!

![1](media/POSTMAN.jpg)

## Webhook URL

ここから登録。

[https://slack.com/apps/A0F7XDUAZ--web-](https://slack.com/apps/A0F7XDUAZ--web-)

## Usage

Python のほう。

```python
postman = SlackPostman(
    webhook_url,
    sender = 'Invader',
    sender_emoji = ':trollface:'
)
postman.post('どうもどうも')
```

`post()` は JSON 形式で送信し、`requests.Response` をそのまま返します。10 秒でタイムアウトします。

PHP のほう。

```php
$postlady = new SlackPostlady(
    $webhookUrl,
    'Invader',
    ':trollface:'
);
print($postlady->post('test'));
```

## テスト

Python 版は Slack に送信せず、モックで確認します。

```bash
pip install -r requirements.txt
python -m unittest -v
```

GitHub Actions でも master への push と PR のたびに実行します。
