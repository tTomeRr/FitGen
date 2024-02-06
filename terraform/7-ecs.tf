resource "aws_ecs_cluster" "flex_app_cluster" {
  name = "flexApp"


}

resource "aws_ecs_task_definition" "db_flask_task" {
  family = "db_flask_task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 3072
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn
  container_definitions    = jsonencode([
    {
      name          = "flex_app"
      image         = var.flex_app_image
      essential     = true
      environment = [
  {
    name  = "POSTGRES_USER"
    value = var.POSTGRES_USER
  },
  {
    name  = "POSTGRES_PASSWORD"
    value = var.POSTGRES_PASSWORD
  },
  {
    name  = "POSTGRES_DB"
    value = var.POSTGRES_DB
  },
  {
    name  = "POSTGRES_HOST"
    value = var.POSTGRES_HOST
  }
]

      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-create-group" = "true"
          "awslogs-group"        = "/ecs/db_flask_task"
          "awslogs-region"       = "eu-central-1"
          "awslogs-stream-prefix" = "ecs"
        }
        secretOptions = []
      }
    },
    {
      name          = "flex_db"
      image         = var.flex_db_image
      essential     = true
     environment = [
  {
    name  = "POSTGRES_USER"
    value = var.POSTGRES_USER
  },
  {
    name  = "POSTGRES_PASSWORD"
    value = var.POSTGRES_PASSWORD
  },
  {
    name  = "POSTGRES_DB"
    value = var.POSTGRES_DB
  },
  {
    name  = "POSTGRES_HOST"
    value = var.POSTGRES_HOST
  }
]

      portMappings = [
        {
          containerPort = 5432
          hostPort      = 5432
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-create-group" = "true"
          "awslogs-group"        = "/ecs/db_flask_task"
          "awslogs-region"       = "eu-central-1"
          "awslogs-stream-prefix" = "ecs"
        }
        secretOptions = []
      }
    }
  ])
}

resource "aws_ecs_service" "flex_app_service" {
 name                               = "flex-service"
 cluster                            = aws_ecs_cluster.flex_app_cluster.id
 task_definition                    = aws_ecs_task_definition.db_flask_task.arn
 desired_count                      = 1
 deployment_minimum_healthy_percent = 100
 deployment_maximum_percent         = 200
 launch_type                        = "FARGATE"
 scheduling_strategy                = "REPLICA"
 
network_configuration {
  security_groups  = [aws_security_group.allow_all.id]
  subnets          = aws_subnet.private_subnets[*].id
  assign_public_ip = false
}

 load_balancer {
   target_group_arn = aws_alb_target_group.flex_alb_tg.arn
   container_name   = "flex_app"
   container_port   = 5000
 }
 
 lifecycle {
   ignore_changes = [task_definition, desired_count]
 }
}

resource "aws_cloudwatch_log_group" "ecs_log_group" {
  name = "/ecs/db_flask_task"
  retention_in_days = 7
}