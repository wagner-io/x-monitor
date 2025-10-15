# EventBridge Rule: alle 15 Minuten
resource "aws_cloudwatch_event_rule" "every_15m" {
  name                = "x-monitor-run-indexer-15min"
  schedule_expression = "rate(15 minutes)"
  description         = "Startet den x-monitor Indexer Fargate Task alle 15 Minuten"
}

# IAM Rolle, damit EventBridge ECS:RunTask ausführen darf
resource "aws_iam_role" "events_invoke_ecs" {
  name = "x-monitor-events-invoke-ecs"
  assume_role_policy = jsonencode({
    Version="2012-10-17",
    Statement=[{Effect="Allow", Principal={Service="events.amazonaws.com"}, Action="sts:AssumeRole"}]
  })
}

resource "aws_iam_role_policy" "events_invoke_ecs_policy" {
  name = "x-monitor-events-invoke-ecs-policy"
  role = aws_iam_role.events_invoke_ecs.id
  policy = jsonencode({
    Version="2012-10-17",
    Statement=[
      { Effect="Allow", Action=["ecs:RunTask"], Resource=aws_ecs_task_definition.indexer.arn },
      { Effect="Allow", Action=["iam:PassRole"], Resource=[aws_iam_role.task_execution.arn, aws_iam_role.task.arn] }
    ]
  })
}

# EventBridge Target → ECS RunTask
resource "aws_cloudwatch_event_target" "run_fargate" {
  rule      = aws_cloudwatch_event_rule.every_15m.name
  arn       = aws_ecs_cluster.xmonitor.arn
  role_arn  = aws_iam_role.events_invoke_ecs.arn

  ecs_target {
     task_definition_arn = aws_ecs_task_definition.indexer.arn
    launch_type         = "FARGATE"
    network_configuration {
        subnets         = data.aws_subnets.default_public.ids
        security_groups = [aws_security_group.fargate.id]
        assign_public_ip = true
    }
  }
}