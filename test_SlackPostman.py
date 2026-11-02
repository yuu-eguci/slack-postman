import unittest
from unittest import mock

import requests

from SlackPostman import SlackPostman, main

WEBHOOK_URL = 'https://hooks.example.invalid/services/TEST'


class SlackPostmanPostTest(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('SlackPostman.requests.post')
        self.post = patcher.start()
        self.addCleanup(patcher.stop)

    def sent_payload(self):
        _, kwargs = self.post.call_args
        return kwargs['json']

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

    def test_sends_json_with_timeout(self):
        SlackPostman(WEBHOOK_URL).post('hi')

        _, kwargs = self.post.call_args
        self.assertNotIn('data', kwargs)
        self.assertEqual(kwargs['timeout'], 10)

    def test_returns_response(self):
        response = SlackPostman(WEBHOOK_URL).post('hi')

        self.assertIs(response, self.post.return_value)

    def test_sender_options_are_keyword_only(self):
        with self.assertRaises(TypeError):
            SlackPostman(WEBHOOK_URL, 'Invader')


class MainTest(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('SlackPostman.requests.post')
        self.post = patcher.start()
        self.addCleanup(patcher.stop)
        self.post.return_value.ok = True

    def run_main(self, args, environ):
        with mock.patch.dict('os.environ', environ, clear=True), \
                mock.patch('sys.stderr') as stderr:
            try:
                main(args)
            except SystemExit as e:
                written = ''.join(c.args[0] for c in stderr.write.call_args_list)
                return e.code, written
        return 0, ''

    def test_posts_message_to_url_from_env(self):
        code, _ = self.run_main(['どうもどうも'], {'SLACK_WEBHOOK_URL': WEBHOOK_URL})

        self.assertEqual(code, 0)
        args, kwargs = self.post.call_args
        self.assertEqual(args, (WEBHOOK_URL,))
        self.assertEqual(kwargs['json']['text'], 'どうもどうも')

    def test_fails_without_webhook_url(self):
        code, err = self.run_main(['hi'], {})

        self.assertEqual(code, 2)
        self.assertIn('SLACK_WEBHOOK_URL', err)
        self.post.assert_not_called()

    def test_fails_without_message(self):
        code, _ = self.run_main([], {'SLACK_WEBHOOK_URL': WEBHOOK_URL})

        self.assertEqual(code, 2)
        self.post.assert_not_called()

    def test_fails_when_slack_rejects(self):
        self.post.return_value.ok = False
        self.post.return_value.status_code = 404
        self.post.return_value.text = 'no_service'

        code, _ = self.run_main(['hi'], {'SLACK_WEBHOOK_URL': WEBHOOK_URL})

        self.assertEqual(code, 1)

    def test_hides_webhook_url_on_connection_error(self):
        self.post.side_effect = requests.ConnectionError(
            f'Max retries exceeded with url: {WEBHOOK_URL}')

        code, err = self.run_main(['hi'], {'SLACK_WEBHOOK_URL': WEBHOOK_URL})

        self.assertEqual(code, 1)
        self.assertNotIn('services/TEST', str(code) + err)


if __name__ == '__main__':
    unittest.main()
