# Define Lambda permission for API Gateway
resource "aws_lambda_permission" "allow_api_gateway" {
  for_each = aws_api_gateway_resource.resources

  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_functions[each.key].function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.bus_api.execution_arn}/v1/${aws_api_gateway_method.methods[each.key].http_method}"
}


# Define API Gateway Integration with Lambda for each method
resource "aws_api_gateway_integration" "lambda_integration" {
  for_each = aws_api_gateway_resource.resources

  rest_api_id             = aws_api_gateway_rest_api.bus_api.id
  resource_id             = aws_api_gateway_resource.resources[each.key].id
  http_method             = aws_api_gateway_method.methods[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_functions[each.key].invoke_arn
}


# Define the REST API
resource "aws_api_gateway_rest_api" "bus_api" {
  name        = "BusAPI"
  description = "API for Bus Company Microservice"
}

# Define API resources
resource "aws_api_gateway_resource" "resources" {
  for_each = {
    "register_function"     = "register"
    "login_function"        = "login"
    "booking_function"     = "book"
    "order_function"       = "order"
    "view_cart_function"   = "view_cart"
    "contact_function"     = "contact"
  }

  rest_api_id = aws_api_gateway_rest_api.bus_api.id
  parent_id   = aws_api_gateway_rest_api.bus_api.root_resource_id
  path_part   = each.value
}

# Define POST methods for each resource
resource "aws_api_gateway_method" "methods" {
  for_each = aws_api_gateway_resource.resources

  rest_api_id   = aws_api_gateway_rest_api.bus_api.id
  resource_id   = aws_api_gateway_resource.resources[each.key].id
  http_method   = "ANY"
  authorization = "NONE"
}

# Define OPTIONS method for CORS support
resource "aws_api_gateway_method" "options_method" {
  for_each = aws_api_gateway_resource.resources

  rest_api_id   = aws_api_gateway_rest_api.bus_api.id
  resource_id   = aws_api_gateway_resource.resources[each.key].id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

# CORS integration for OPTIONS method
resource "aws_api_gateway_integration" "cors_integration" {
  for_each = aws_api_gateway_resource.resources

  rest_api_id             = aws_api_gateway_rest_api.bus_api.id
  resource_id             = aws_api_gateway_resource.resources[each.key].id
  http_method             = aws_api_gateway_method.options_method[each.key].http_method
  type                    = "MOCK"
  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

# Method response for OPTIONS to include CORS headers
resource "aws_api_gateway_method_response" "cors_options_200" {
  for_each = aws_api_gateway_resource.resources

  rest_api_id = aws_api_gateway_rest_api.bus_api.id
  resource_id = aws_api_gateway_resource.resources[each.key].id
  http_method = aws_api_gateway_method.options_method[each.key].http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Headers" = true
  }

  response_models = {
    "application/json" = "Empty"
  }
}

# Integration response for OPTIONS method
resource "aws_api_gateway_integration_response" "cors_options_integration_200" {
  for_each = aws_api_gateway_resource.resources

  rest_api_id = aws_api_gateway_rest_api.bus_api.id
  resource_id = aws_api_gateway_resource.resources[each.key].id
  http_method = aws_api_gateway_method.options_method[each.key].http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
    "method.response.header.Access-Control-Allow-Methods" = "'POST,GET,OPTIONS'"
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
  }

  depends_on = [aws_api_gateway_integration.cors_integration]
}

# Define the API Gateway deployment
resource "aws_api_gateway_deployment" "rest_api" {
  depends_on = [
    aws_api_gateway_method.methods,
    aws_api_gateway_method.options_method,
    aws_api_gateway_integration.cors_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.bus_api.id
  stage_name  = "v1"

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.bus_api.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}
