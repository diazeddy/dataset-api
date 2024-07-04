# Dataset Management API Service
Create a backend service that ingests machine learning data and stores it in a database for further processing. The service should expose Restful API endpoints to handle various operations related to data ingestion.

![img.png](images/img.png)

## Tasks
1. **API Endpoints:**
   - **Upload Data:** An endpoint to upload a CSV file containing training data.
     - **Endpoint:** `POST /upload`
     - **Request:** Multipart/form-data with a file parameter named `file`.
     - **Response:** 200 OK on success with a JSON response containing a message and status.
   - **List Datasets:** An endpoint to list all uploaded datasets.
     - **Endpoint:** `GET /datasets`
     - **Response:** 200 OK with a JSON array of dataset metadata (e.g., ID, filename, upload date).
   - **Get Dataset:** An endpoint to retrieve a specific dataset by ID.
     - **Endpoint:** `GET /datasets/{id}`
     - **Response:** 200 OK with the dataset content in JSON format.
   - **Delete Dataset:** An endpoint to delete a specific dataset by ID.
     - **Endpoint:** `DELETE /datasets/{id}`
     - **Response:** 200 OK on success with a JSON response containing a message and status.
2. **Database:**
   - Use a NoSQL database ( e.g., MongoDB, CouchDB) to store dataset metadata and content.
   - Define appropriate schemas and data models to validate and store dataset details and content.
3. **Error Handling:**
   - Handle file upload errors, missing dataset errors, and other potential issues gracefully with appropriate HTTP status codes and messages.
4. **Documentation:**
   - Provide API documentation (e.g., using Swagger/OpenAPI) to describe the available endpoints, request parameters, and responses.
5. **Testing:**
   - Write unit and integration tests to ensure the correctness of the API.
6. **Code Quality:**
   - Follow best practices for code quality, including proper structure, naming conventions, and comments.
   - Use version control (e.g., Git) to manage the codebase.
7. Implement authentication and authorization for the API.
8. Use Docker to containerize the application.
9. Deploy the service on a cloud platform (e.g., AWS, GCP, Azure).
10. Implement logging and monitoring for the service.

## Environment
- OS: Ubuntu 22.04
- Python: 3.10.2
- Pip: 22.0.2
- Docker: 27.0.2

## Tech Stacks
- FastAPI
- JWT
- Pydantic
- Mongo DB
- pytest
- docker
- AWS
- CI/CD

## Steps to setup development environment
- Create virtual environment.
  ```shell
  python3 -m venv venv
  ```
- Activate virtual environment.
  ```shell
    source "venv/bin/activate"
  ```
- Install python packages.
  ```shell
  pip install -r requirements.txt
  ```
- Create .env file
  ```
  DATABASE_URL="MONGO DB URL"
  DATABASE_NAME="DATABASE NAME"
  SECRET_KEY="SECRET KEY FOR JWT TOKEN"
  ```
- Run the project
  ```shell
  uvicorn app.main:app --reload
  ```
  This will host the project on http://localhost:8000, and you can see the swagger UI on http://localhost:8000/docs


- Test the project
  ```shell
  pytest
  ```

## Steps to run project with Docker
- Build a docker image
  ```shell
  docker build --build-arg DATABASE_URL='MONGO DB URL' --build-arg DATABASE_NAME="DATABASE NAME" --build-arg SECRET_KEY="SECRET KEY FOR JWT TOKEN" -t dataset-api .
  ```
- Run docker image
  ```shell
  docker run -p 80:80 dataset-api:latest
  ```
  This will host the project on http://127.0.0.1, and you can see the swagger UI on http://127.0.0.1/docs.

## Steps to deploy project to AWS ECS and implement the logging and monitoring the app with AWS CloudWatch

### Steps to Create a Repository on Amazon Elastic Container Registry (ECR)
- Navigate to the Amazon ECR service and click on “Create repository”.
  
- Choose "private" for "Visibility settings".
  ![img.png](images/img_1.png)
- Input your repository name.
  ![img.png](images/img_2.png)
- Click "Create repository" button.

### Steps to Push a docker image to Amazon ECR Repository
- Click "View push commands" to push docker image to repository
  ![img.png](images/img_3.png)
  ![img.png](images/img_4.png)

### Steps to create ECS cluster
- Navigate to the Amazon ECS service and click on "Create cluster".
- Input cluster name.
- Choose "Aws Fargate" for infrastructure.
  ![img.png](images/img_5.png)
- Set Container Insights for monitoring the deployed ecs service.
  ![img.png](images/img_6.png)
- Click "Create".

### Steps to create task definition
- Click "Create new task definition".
  ![img.png](images/img_7.png)
- Input task definition family name. 
  ![img.png](images/img_8.png)
- Choose AWS Fargate for launch type
- Choose Linux/X86_64 for Operating system/Architecture
  ![img.png](images/img_9.png)
- Input container name and image uri
- Input port name
  ![img.png](images/img_10.png)
- Add Environment values
  ```
  DATABASE_URL="MONGO DB URL"
  DATABASE_NAME="DATABASE NAME"
  SECRET_KEY="SECRET KEY FOR JWT TOKEN"
  ```
- Click "Create".

### Steps to create ECS service
- Navigate to the ECS cluster and select the cluster created earlier and click on create in the services section.
  ![img.png](images/img_11.png)
- Choose Launch type for Compute options
- Choose Fargate as launch type
  ![img.png](images/img_12.png)
- Choose Service as Application type
- Choose Task Definition we created before
- Input service name
  ![img.png](images/img_13.png)
- Choose Create a new security group option
- Add rule to allow HTTP port 80 from anywhere.
- Turn on assign public ip address
  ![img.png](images/img_14.png)
- Choose Application Load Balancer as a load balancer type
- Input load balancer name
- Input health check path as "/docs"
  ![img_1.png](images/img_15.png)
- Click "Create".

### Steps to create target group
- Navigate to the target group section and click create Target Group
- Choose Application Load Balancer as for target type
- Choose IPv4 for  IP address type
- Input target group name
  ![img.png](images/img_22.png)
- Input "/docs" for health check path
  ![img.png](images/img_23.png)
- Click "Next" button.
- Select application load balancer created in previous step
  ![img.png](images/img_24.png)
- Click create target group

### Steps to add network load balancing to prevent from changing public ip address
- Navigate to the load balancing and click create Network Load Balancer
- Input network load balancer name
- Choose Internet-facing for Scheme
- Choose IPv4 for Load Balancer IP address type
  ![img.png](images/img_19.png)
- Mapped availability zone with subnets
  ![img.png](images/img_20.png)
- Choose security group that allow http 80 port from anywhere.
  ![img_1.png](images/img_21.png)
- Choose target group that created in previous step.
  ![img.png](images/img_25.png)
- Click Create Load Balancer

Now the ECS service is deployed, and we can be able to access the project.
Currently, the service is deployed on http://datasetapiapp-load-balancer-04340e1eebd0a70e.elb.us-east-2.amazonaws.com and can check the swagger page on http://datasetapiapp-load-balancer-04340e1eebd0a70e.elb.us-east-2.amazonaws.com/docs,
Also I built the CI/CD pipeline with GitHub actions that will deploy the project to AWS ECS automatically when the new code is pushed to the main branch.

### Logging for ECS
![img.png](images/img_16.png)

### Monitoring Metrics for ECS
![img.png](images/img_17.png)
![img.png](images/img_18.png)