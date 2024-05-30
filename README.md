# 🎓 CE5 Group 6 Capstone Project

This project consists of a chatbot application and a sentiment analysis API.
Both applications are containerized using Docker and orchestrated using Docker
Compose.

## ⚙️ Installation and Setup

Before you can run the applications, you need to set up Docker and Docker
Compose on your machine. You can download Docker from
the [official website](https://www.docker.com/products/docker-desktop) and
Docker Compose is included as part of most Docker for Mac and Docker for Windows
installations.

1. **Clone the repository**

   First, you need to clone the repository to your local machine. You can do
   this with the following command:

   ```bash
   git clone https://github.com/albertleng-projects/ce5-capstone-project.git
   ```

2. **Set up the environment variables**

   This project requires several environment variables to run. You can set them
   up in a `.env` file in the root directory of the project. Here's an example
   of what the `.env` file should look like:

   ```bash
   OPENAI_API_KEY=<your_openai_api_key>
   AWS_REGION=<your_aws_region>
   DYNAMODB_TABLE=<your_dynamodb_table>
   AWS_ACCESS_KEY_ID=<your_aws_access_key_id>
   AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
   SENTIMENT_API_BASE_URL=<your_sentiment_api_base_url>
   LOGGING_LEVEL=<your_logging_level>
   ```

   Replace `your_openai_api_key`, `your_aws_region`, `your_dynamodb_table`,
   `your_aws_access_key_id`, `your_aws_secret_access_key`, `your_sentiment_api_base_url`,
   and `your_logging_level` with your actual values.


3. **Build and run your services**

   You can use Docker Compose to build the images and run the containers for
   your services with a single command:

   ```bash
   docker-compose up --build
   ```

   This command will start both your services. The chatbot service is set to
   depend on the sentiment analysis API service, so Docker Compose will start
   the sentiment analysis API service first.


4. **Stopping (and removing) your services**

   You can stop your services by running the following command:

   ```bash
   docker-compose down
   ```

   This command stops and removes the containers, networks, and volumes defined
   in your `docker-compose.yml` file.  

   (Optional) To also remove all images used:

   ```bash
   docker-compose down --rmi all
   ```


## TODO:

Add a Makefile or shell script to automate the installation, setup and/or run
process.
