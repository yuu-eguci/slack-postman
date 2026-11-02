import json
import unittest
from unittest import mock

from SlackPostman import SlackPostman

WEBHOOK_URL = 'https://hooks.example.invalid/services/TEST'


class SlackPostmanPostTest(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('SlackPostman.requests.post')
        self.post = patcher.start()
        self.addCleanup(patcher.stop)

    def sent_payload(self):
        _, kwargs = self.post.call_args
        return json.loads(kwargs['data'])

    def test_posts_text_with_sender_and_emoji(self):
        postman = SlackPostman(
            WEBHOOK_URL, sender='Invader', sender_emoji=':trollface:')

        postman.post('どうもどうも')

        self.post.assert_called_once()
        args, _ = self.post.call_args
        self.assertEqual(args, (WEBHOOK_URL,))
        self.assertEqual(self.sent_payload(), {
            'text': 'どうもどうも',
            'username': 'Invader',
            'icon_emoji': ':trollface:',
        })

    def test_uses_default_sender_and_emoji(self):
        SlackPostman(WEBHOOK_URL).post('hi')

        payload = self.sent_payload()
        self.assertEqual(payload['username'], 'Alien')
        self.assertEqual(payload['icon_emoji'], ':alien:')

    def test_returns_response(self):
        response = SlackPostman(WEBHOOK_URL).post('hi')

        self.assertIs(response, self.post.return_value)

    def test_sender_options_are_keyword_only(self):
        with self.assertRaises(TypeError):
            SlackPostman(WEBHOOK_URL, 'Invader')


if __name__ == '__main__':
    unittest.main()
