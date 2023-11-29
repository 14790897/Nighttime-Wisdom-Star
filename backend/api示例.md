curl  -X POST -H "Content-Type: application/json"  --location 'http://52.6.211.36:8181/backend-api/conversation' -H "Authorization: Bearer $token" -d '
{
    "action": "next",
    "messages": [
        {
            "id": "aaa243c4-799e-4340-b17a-fb378626cbed",
            "author": {
                "role": "user"
            },
            "content": {
                "content_type": "text",
                "parts": [
                    "骑自行车要戴头盔吗"
                ]
            },
            "metadata": {}
        }
    ],
    "conversation_id": "ed5b639b-8f0d-4493-bfbb-c1aca6166a1e",
    "parent_message_id": "072dddc7-b319-42be-b24d-f49c5ee99c9a",
    "model": "text-davinci-002-render-sha",
    "timezone_offset_min": -480,
    "suggestions": [],
    "history_and_training_disabled": false,
    "arkose_token": null,
    "conversation_mode": {
        "kind": "primary_assistant"
    },
    "force_paragen": false,
    "force_rate_limit": false
}'