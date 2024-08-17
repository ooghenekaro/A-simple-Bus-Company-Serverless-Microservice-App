# Define Lambda Functions
data "archive_file" "lambda_zips" {
  for_each = {
    "register_function"              = "${path.module}/register"
    "login_function"                 = "${path.module}/login"
    "booking_function"                  = "${path.module}/booking"
    "order_function"                 = "${path.module}/order"
    "view_cart_function"             = "${path.module}/view"
    "contact_function"               = "${path.module}/contact"
  }

  type        = "zip"
  source_dir = each.value
  output_path = "${path.module}/${each.value}/${each.key}.zip"
}

resource "aws_lambda_function" "lambda_functions" {
  for_each = data.archive_file.lambda_zips

  function_name    = each.key
  runtime           = "python3.12"
  role              = aws_iam_role.lambda_exec.arn
  handler           = "${each.key}.lambda_handler"
  source_code_hash  = base64sha256(filebase64(each.value.output_path))
  filename          = each.value.output_path

  environment {
    variables = {
      USERS_TABLE    = aws_dynamodb_table.users.name
      BOOKINGS_TABLE = aws_dynamodb_table.bookings.name
      ORDERS_TABLE   = aws_dynamodb_table.orders.name
      CARTS_TABLE    = aws_dynamodb_table.carts.name
    }
  }
}

resource "aws_lambda_permission" "api_gw_lambda_permission" {
  for_each = aws_lambda_function.lambda_functions

  statement_id  = "${each.key}-allow-execution"
  action        = "lambda:InvokeFunction"
  function_name = each.value.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.bus_api.execution_arn}/*/*"
}

# IAM Role for Lambda Functions
resource "aws_iam_role" "lambda_exec" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_policy.arn
  role     = aws_iam_role.lambda_exec.name
}

data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    actions   = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "lambda_policy" {
  name   = "lambda_policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:Scan", "dynamodb:Query"]
        Resource = [
          aws_dynamodb_table.users.arn,
          aws_dynamodb_table.bookings.arn,
          aws_dynamodb_table.orders.arn,
          aws_dynamodb_table.carts.arn
        ]
      }
    ]
  })
}

# Define DynamoDB Tables
resource "aws_dynamodb_table" "users" {
  name           = "Users"
  hash_key       = "user_id"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "user_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "bookings" {
  name           = "Bookings"
  hash_key       = "booking_id"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "booking_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "orders" {
  name           = "Orders"
  hash_key       = "order_id"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "order_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "carts" {
  name           = "Carts"
  hash_key       = "user_id"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "user_id"
    type = "S"
  }
}
