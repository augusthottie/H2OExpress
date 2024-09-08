# H2OExpress

**H2OExpress** is a Django web application that allows users to conveniently purchase household water online. The platform is designed to simplify water delivery by providing an easy-to-use interface for making purchases, managing profiles, and tracking transactions.

## Features

- **User Registration**: Sign up by providing your username, email, meter number, name, address, phone number, and password.
- **Water Purchase**: Choose your desired quantity of water and complete the purchase through secure payment options.
- **Transaction History**: View a detailed history of past water purchases, including units bought, transaction details, and payment methods.
- **Profile Management**: Update personal information such as meter number, address, and phone number.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AugustHottie/H2OExpress.git
   ```

2. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the database migrations:

   ```bash
   python manage.py migrate
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Technologies Used

- **Python** & **Django**
- **HTML**, **CSS** (Tailwind), **JavaScript**
- **AWS RDS**: Managed PostgreSQL database
- **AWS S3**: Static file storage
- **Braintree**: Secure payment processing

## Deployment

H2OExpress is deployed using the following services:

- **AWS S3**: For serving static assets (CSS, JavaScript, images), ensuring scalability and fast delivery.
- **AWS RDS**: A managed PostgreSQL database for reliable and scalable data management.
- **Braintree**: Handles secure payment processing for water purchases via credit card transactions.

### Deployment Steps

To deploy the application in your environment, follow these steps:

1. **AWS S3 Setup**:
   - Create an S3 bucket for static files.
   - Update `settings.py` with your AWS S3 bucket name, access key, and secret access key.

2. **AWS RDS Setup**:
   - Create an RDS PostgreSQL instance.
   - Update the database configuration in `settings.py` with the RDS endpoint, database name, username, and password.

3. **Braintree Setup**:
   - Sign up for a Braintree account.
   - Update `settings.py` with your Braintree merchant ID, public key, and private key.

4. **Migrate the Database**:
   - Run Django migration commands to apply the database schema.

5. **Collect Static Files**:
   - Use `collectstatic` to gather all static files and upload them to AWS S3.

6. **Run the Server**:
   - Use `manage.py runserver` to start the Django server.

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

Ensure you have the necessary AWS credentials to access S3 and RDS. Refer to the [AWS documentation](https://docs.aws.amazon.com/) for guidance on setting up these services and [Braintree documentation](https://support.checkfront.com/hc/en-us/articles/115004847353-Setting-up-Braintree-Direct-as-your-Checkfront-payment-provider) for API credentials setup.

## Contributing

Contributions are welcome! If you encounter a bug or have suggestions for improvement, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
