import requests
import json

url = "http://52.6.211.36:8181/backend-api/conversation"
payload = {
    "action": "next",
    "arkose_token": "null",
    "conversation_id": "73f458de-4dea-4d37-a019-0c519540d847",
    "conversation_mode": {"kind": "primary_assistant"},
    "force_paragen": False,
    "force_rate_limit": False,
    "history_and_training_disabled": False,
    "messages": [
        {
            "author": {"role": "user"},
            "content": {"content_type": "text", "parts": ["介绍一下你自己"]},
            "metadata": {},
        }
    ],
    "model": "gpt-3.5",
    "parent_message_id": "2e946b79-d453-4ead-b778-031cac0dcabb",
    "suggestions": [],
    "timezone_offset_min": -480,
}
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiIxMzk2MzYxNTA1QHFxLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9hdXRoIjp7InBvaWQiOiJvcmctbFVFTXZtd253UnJCd2doOHlGNFRkNlRWIiwidXNlcl9pZCI6InVzZXItRnlIY2ZnQmw5MThkV1lNNTBTbFF4U3FoIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2JiY2UzY2M1MDgzN2MwYTI4YjExMTciLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzAwMzk2NTYzLCJleHAiOjE3MDEyNjA1NjMsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIG9mZmxpbmVfYWNjZXNzIn0.WZrJuX4M73jSKIColp6gvyU0sX_CvesQs5gfsVTCJYKKNbpkCPihE_jy3m0sUkz_Sq2b0l3W9b6h_Sa3mUxbt98sfcoRY76RJFqqd1fzeP-b4M7tJOS8l-74taqWCxUZHE1ESyNoSkxeo822eRjjwlmQOchPxnq41RVj6GbaCkLEWtytTJPc_eqnE_Iju1nkrFD_W1tvtWwdzqbYNkWprcDVwFEVlnHHHWByOcNhqT7C5R6Q6Db1qnW76R_y9RXavF2cjpc3Y8JGDI14XSdrS3xnSCV6BPn7N2EdEQxGSFYyNWnScTzY6o1UtpPHCmHDCcXFTJ6eDcLLQwLE-CzyPQ",
}
response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
print(response.text)
