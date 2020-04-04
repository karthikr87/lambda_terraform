provider "aws" {
  region = var.region
}
resource "aws_lambda_function" "SG_lambda_function" {
  role             = aws_iam_role.SG_iam_for_lambda_role.arn
  handler          = var.handler
  runtime          = var.runtime
  filename         = "attach_sec.zip"
  function_name    = var.function_name
  source_code_hash = filebase64sha256("attach_sec.zip")
  depends_on = [aws_iam_role_policy_attachment.SG_lambda_policy, aws_cloudwatch_log_group.SG_lambda_group]
}
resource "aws_iam_role" "SG_iam_for_lambda_role" {
  name = "SG_iam_for_lambda_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_cloudwatch_log_group" "SG_lambda_group" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 14
}

# See also the following AWS managed policy: AWSLambdaBasicExecutionRole
resource "aws_iam_policy" "SG_lambda_logging_policy" {
  name        = "SG_lambda_logging_policy"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}
resource "aws_iam_role_policy_attachment" "SG_lambda_policy" {
  role       = aws_iam_role.SG_iam_for_lambda_role.name
  policy_arn = aws_iam_policy.SG_lambda_logging_policy.arn
}

# allow cloud watch event to trigger lambda function
resource "aws_cloudwatch_event_rule" "ec2_state_change_rule" {
    name = "ec2_state_change_rule"
    description = "sends ec2 event to lambda function"
    event_pattern = <<PATTERN
    {
      "source": [
        "aws.ec2"
      ],
      "detail-type": [
        "EC2 Instance State-change Notification"
      ],
      "detail": {
        "state": [
          "running"
        ]
      }
    }
PATTERN
}

resource "aws_cloudwatch_event_target" "trigger_lambda_ec2_change_target" {
    rule = aws_cloudwatch_event_rule.ec2_state_change_rule.name
    target_id = "SG_lambda_function"
    arn = aws_lambda_function.SG_lambda_function.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_SG_lambda_function" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.SG_lambda_function.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.ec2_state_change_rule.arn
}
