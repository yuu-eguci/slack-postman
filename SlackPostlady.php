<?php

/**
 * Slackにメッセージ送れるよ。
 * 自分で指定できるのは、「メッセージ送る部屋」「送信者名」「送信者アイコン」「メッセージ」
 * だよ!
 */
class SlackPostlady
{
    function __construct($webhookUrl, $sender='Alien', $senderEmoji=':alien:')
    {
        $this->webhookUrl = $webhookUrl;
        $this->sender = $sender;
        $this->senderEmoji = $senderEmoji;
    }

    public function post($text)
    {
        $context = [
            'http' => [
                'method' => 'POST',
                'header' => implode(PHP_EOL, ['Content-Type: application/json']),
                'content' => json_encode([
                    'text'      => $text,
                    'username'  => $this->sender,
                    'icon_emoji'=> $this->senderEmoji,
                ]),
            ],
        ];

        return file_get_contents(
            $this->webhookUrl,
            false,
            stream_context_create($context)
        );
    }
}

# emoji参照: https://www.webpagefx.com/tools/emoji-cheat-sheet/
$webhookUrl = '***'
$postlady1 = new SlackPostlady(
    $webhookUrl,
    'Invader',
    ':trollface:'
);
# ちゃんと送れればokと出る。
print($postlady1->post('test'));
