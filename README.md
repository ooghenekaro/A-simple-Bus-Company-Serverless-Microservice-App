# Bus Company Services API

This project provides a serverless microservice architecture for a bus company using AWS services. It includes a frontend static website, an API Gateway, Lambda functions, and DynamoDB tables. The setup is designed to handle various services for the bus company, such as user registration, login, booking, and ordering.

![mermaid-diagram-2024-08-17-165727](https://github.com/user-attachments/assets/61d66dce-b6e3-4567-a8c2-6982c007600a)


## Architecture Overview

1. **Frontend**:
   - **Hosted on S3**: The static website (HTML/CSS/JS) is deployed to an S3 bucket.

2. **API Gateway**:
   - Acts as the entry point for API requests and routes them to the appropriate Lambda functions.

3. **Lambda Functions**:
   - Implemented as microservices handling different functionalities:
     - **Register Lambda**: Handles user registration.
     - **Login Lambda**: Manages user login.
     - **Book Lambda**: Processes trip bookings.
     - **Order Lambda**: Manages product orders.

4. **DynamoDB**:
   - Each Lambda function interacts with its corresponding DynamoDB table to store and retrieve data:
     - **Users Table**: Used by Register and Login Lambdas.
     - **Bookings Table**: Used by the Book Lambda.
     - **Orders Table**: Used by the Order Lambda.

5. **CORS Configuration**:
   - Configured to allow cross-origin requests from the frontend hosted on S3.

## How It Works

1. **Frontend Interaction**:
   - Users interact with the frontend deployed on S3.
   - The frontend sends API requests to API Gateway.

2. **API Gateway Routing**:
   - API Gateway routes the requests to the appropriate Lambda functions based on the service requested (e.g., register, login, book, order).

3. **Lambda Functions Execution**:
   - Each Lambda function processes the request and interacts with DynamoDB as needed.
   - Lambda functions return responses which are sent back through API Gateway to the frontend.

4. **Error Handling**:
   - Detailed error handling is implemented in Lambda functions to ensure proper feedback is provided to the frontend.

## Deployment

- **Frontend**: Deployed to an S3 bucket.
- **API Gateway & Lambda Functions**: Managed and deployed via AWS.
- **DynamoDB Tables**: Configured to store data for each service.

## Getting Started

1. Deploy the static website to S3.
2. Configure API Gateway and deploy Lambda functions.
3. Ensure DynamoDB tables are created and linked with Lambda functions.

![image](https://github.com/user-attachments/assets/1637f490-bcaa-441d-9d07-82117290d21d)



## Author

**Oghenekaro Oboido**
