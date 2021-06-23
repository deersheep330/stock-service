[
  {
    "essential": true,
    "name": "stock-container",
    "memory": 512,
    "cpu": 512,
    "image": "${image}",
    "environment": [
      { "name": "DB_CONNECTION_URL", "value": "${db_connection_url}" },
      { "name": "FUGLE_API_TOKEN", "value": "${fugle_api_token}" }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${awslogs_group}",
        "awslogs-region": "${awslogs_region}",
        "awslogs-stream-prefix": "${awslogs_prefix}"
      }
    }
  }
]