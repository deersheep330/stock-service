[
  {
    "essential": true,
    "name": "stock-container",
    "memory": 512,
    "cpu": 512,
    "image": "${image}",
    "portMappings": [
      { "containerPort": 8000, "hostPort": 8000 }
    ],
    "environment": [
      { "name": "DB_CONNECTION_URL", "value": "${db_connection_url}" },
      { "name": "REDIS_HOST", "value": "${redis_host}" },
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