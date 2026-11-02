
'''Python で Slack に投稿します。

0. https://slack.com/apps/A0F7XDUAZ--web-
1. Menu > Configure Apps > Custom Integrations > Incoming WebHooks > Add Configuration
2. Post対象のChannelを選択

'''

import argparse
import os

import requests


class SlackPostman:
    '''PythonからSlackへメッセージを送信します。'''

    def __init__(self, webhook_url, *, sender='Alien', sender_emoji=':alien:'):
        self.webhook_url  = webhook_url
        self.sender       = sender
        self.sender_emoji = sender_emoji

    def post(self, text):
        return requests.post(
            self.webhook_url,
            json = {
                'text'      : text,
                'username'  : self.sender,
                'icon_emoji': self.sender_emoji,
            },
            timeout = 10,
        )


def main(args=None):
    parser = argparse.ArgumentParser(
        description='環境変数 SLACK_WEBHOOK_URL の Webhook にメッセージを送ります。')
    parser.add_argument('text', help='送信するメッセージ')
    text = parser.parse_args(args).text

    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    if not webhook_url:
        parser.error('環境変数 SLACK_WEBHOOK_URL を設定してください。')

    # 例外メッセージには Webhook URL が入るため、型名だけ表示します。
    try:
        response = SlackPostman(webhook_url).post(text)
    except requests.RequestException as e:
        parser.exit(1, f'送信に失敗しました: {type(e).__name__}\n')
    if not response.ok:
        parser.exit(1, f'送信に失敗しました: {response.status_code} {response.text}\n')


if __name__ == "__main__":
    main()
