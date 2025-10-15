# Default VPC + Subnets
data "aws_vpc" "default" { default = true }
data "aws_subnets" "default_public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# CloudWatch Logs
resource "aws_cloudwatch_log_group" "indexer" {
  name              = "/ecs/x-monitor-indexer"
  retention_in_days = 14
}

# ECR Repository
resource "aws_ecr_repository" "indexer" {
  name = "x-monitor-indexer"
  image_scanning_configuration { scan_on_push = true }
  force_delete = true
}

# ECS Cluster
    resource "aws_ecs_cluster" "xmonitor" {
  name = "x-monitor-cluster"
}

# Security Group für Fargate
resource "aws_security_group" "fargate" {
  name        = "x-monitor-fargate-sg"
  description = "Fargate task egress"
  vpc_id      = data.aws_vpc.default.id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# IAM: Task Execution Role (zieht Image, schreibt Logs)
resource "aws_iam_role" "task_execution" {
  name = "x-monitor-task-exec-role"
  assume_role_policy = jsonencode({
    Version="2012-10-17",
    Statement=[{Effect="Allow", Principal={Service="ecs-tasks.amazonaws.com"}, Action="sts:AssumeRole"}]
  })
}

resource "aws_iam_role_policy_attachment" "task_exec_basic" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# IAM: Task Role (S3 & DynamoDB Zugriff)
resource "aws_iam_role" "task" {
  name = "x-monitor-task-role"
  assume_role_policy = jsonencode({
    Version="2012-10-17",
    Statement=[{Effect="Allow", Principal={Service="ecs-tasks.amazonaws.com"}, Action="sts:AssumeRole"}]
  })
}

resource "aws_iam_policy" "task_access" {
  name = "x-monitor-task-access"
  policy = jsonencode({
    Version="2012-10-17",
    Statement=[
      { Effect="Allow", Action=["s3:PutObject","s3:PutObjectAcl","s3:ListBucket","s3:GetObject"], Resource=[
          aws_s3_bucket.indexes.arn,
          "${aws_s3_bucket.indexes.arn}/*"
      ]},
      { Effect="Allow", Action=["dynamodb:Scan","dynamodb:DescribeTable"], Resource="arn:aws:dynamodb:*:*:table/x-monitor-mock-data" },
      { Effect="Allow", Action=["logs:CreateLogStream","logs:PutLogEvents"], Resource="*" }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "task_attach" {
  role       = aws_iam_role.task.name
  policy_arn = aws_iam_policy.task_access.arn
}

# Task Definition (Fargate, CPU/Mem klein)
resource "aws_ecs_task_definition" "indexer" {
  family                   = "x-monitor-indexer"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"     # 0.5 vCPU
  memory                   = "1024"    # 1 GB

  execution_role_arn = aws_iam_role.task_execution.arn
  task_role_arn      = aws_iam_role.task.arn

  container_definitions = jsonencode([{
    name      = "indexer"
    image     = "${aws_ecr_repository.indexer.repository_url}:latest"
    essential = true
    environment = [
      { name="INDEX_S3_BUCKET", value=aws_s3_bucket.indexes.bucket },
      { name="INDEX_S3_PREFIX", value="faiss" },
      { name="DDB_TABLE", value="x-monitor-mock-data" },
      { name="MODEL_DIR", value="/app/model" },
      { name="INDEX_DIM", value="384" }
    ]
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        awslogs-group         = aws_cloudwatch_log_group.indexer.name,
        awslogs-region        = "eu-central-1",
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}