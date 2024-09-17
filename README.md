# H2OExpress

**H2OExpress** is a Django web application that allows users to conveniently purchase household water online. The platform simplifies water delivery by providing an easy-to-use interface for purchases, profile management, and transaction tracking.

## Features

- **User Registration**: Sign up by providing a username, email, meter number, name, address, phone number, and password.
- **Water Purchase**: Select your desired water quantity and complete the purchase through secure payment options.
- **Transaction History**: Access a detailed history of past purchases, including units bought, transaction details, and payment methods.
- **Profile Management**: Update personal information, including meter number, address, and phone number.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AugustHottie/H2OExpress.git
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv <env-name>
   source <env-name>/bin/activate
   ```

3. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the database migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Technologies Used

- **Python** & **Django**
- **HTML**, **CSS** (Tailwind), **JavaScript**
- **AWS RDS**: Managed PostgreSQL database
- **AWS S3**: Storage for static files
- **AWS EC2**: Deployment of the Dockerized application
- **Docker**: Containerization of the application
- **Braintree**: Secure payment processing

## Deployment

H2OExpress is deployed using the following services:

- **AWS S3**: Serves static assets like CSS, JavaScript, and images, ensuring scalability and fast delivery.
- **AWS RDS**: A managed PostgreSQL database for reliable and scalable data management.
- **AWS EC2**: For deployment of the Dockerized application.
- **Docker**: Used for containerization of the application.
- **Braintree**: Handles secure payment processing for water purchases via credit card transactions.

### Deployment Steps

To deploy the application in your environment, follow these steps:

1. **AWS S3 Setup**:
   - Create an S3 bucket for static files.
   - Update `settings.py` with your AWS S3 bucket name, access key, and secret key.

2. **AWS RDS Setup**:
   - Create an RDS PostgreSQL instance.
   - Update `settings.py` with your RDS endpoint, database name, username, and password.

3. **Braintree Setup**:
   - Sign up for a Braintree account.
   - Update `settings.py` with your Braintree merchant ID, public key, and private key.

4. **Migrate the Database**:
   - Run Django migration commands to apply the database schema.

5. **Collect Static Files**:
   - Use `collectstatic` to gather all static files and upload them to AWS S3.

6. **Run the Server**:
   - Use `manage.py runserver` to start the Django development server.

### Live Demo

Check out the live application [here](https://h20express.pythonanywhere.com).

### Payment Testing

To test the payment functionality using Braintree, use the following test credit card numbers:

- **Visa**: 4111 1111 1111 1111
- **Mastercard**: 5555 5555 5555 4444

### Docker Deployment

To deploy with Docker:

1. Build the Docker image:

   ```bash
   docker build -t <image-name> .
   ```

2. Run Docker Compose:

   ```bash
   docker-compose build && docker-compose up
   ```

### EC2 Deployment

To deploy the Dockerized application on AWS EC2 using an AWS Linux image:

1. **Update the instance and install necessary dependencies**:
   ```bash
   sudo yum update -y
   sudo yum install -y python3 python3-pip nginx git docker
   ```

2. **Start Docker and enable it**:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ec2-user
   ```

3. **Install Docker Compose**:
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

4. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. **Run Docker Compose to start the application**:
   ```bash
   docker compose up -d --build
   ```

**Note**: Ensure you open the necessary ports in the security group (e.g., `8000`, `80`, `443`) for the application to work.

For detailed instructions on setting up AWS services, refer to the [AWS documentation](https://docs.aws.amazon.com/). Similarly, consult the [Braintree documentation](https://support.checkfront.com/hc/en-us/articles/115004847353-Setting-up-Braintree-Direct-as-your-Checkfront-payment-provider) for payment integration details.

## Contributing

Contributions are welcome! If you encounter a bug or have suggestions for improvement, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
