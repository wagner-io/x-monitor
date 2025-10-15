output "ecr_repository_url" {
  value = aws_ecr_repository.indexer.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.xmonitor.name
}

output "task_definition_family" {
  value = aws_ecs_task_definition.indexer.family
}

output "event_rule_name" {
  value = aws_cloudwatch_event_rule.every_15m.name
}