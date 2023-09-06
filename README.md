# H2OExpress

H20Express is an innovative Django application that allows users to purchase water for their household online, providing a convenient and easy-to-use platform.

## Features

- User Registration: Users can create an account by providing their username, email, meter number, name, address, phone number, and password.
- Water Purchase: Users can select their desired amount of water and choose a payment method to complete the purchase.
- Transaction History: The application tracks user's purchase history, providing a record of purchased water, units, and payment details.
- Profile Management: Users can update their profile information, including meter number, address, and phone number.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/AugustHottie/H2OExpress.git
2. Install the project dependencies
   ```shell
   pip install requirements.txt

3. Run database migrations:
   ```shell
   python manage.py migrate
   
4. Start the development server:
   ```shell
   python manage.py runserver

## Technologies Used
- Python
- Django
- HTML/CSS/Tailwind
- JavaScript
- AWS RDS: Managed PostgreSQL database service
- AWS S3: Storage service for static files
- Braintree: Payment processing service

## Deployment 
### The application is deployed using the following services:
- AWS S3: Static files (CSS, JavaScript, images, etc.) are stored and served from AWS S3. This ensures efficient delivery and scalability of the static assets.
- AWS RDS: The database for this application is hosted on AWS RDS, which is a managed PostgreSQL database service. It provides reliable and scalable database infrastructure without the need for manual administration.
- Braintree: Payment processing is handled by Braintree, a popular and secure payment gateway. It enables the application to securely process credit card transactions and manage customer payments.

### To deploy the application in your own environment, you will need to perform the following steps:
1. Set up AWS S3: Create an S3 bucket to store your static files. Update the AWS S3 configuration in the Django settings file (settings.py) with your bucket name, access key, and secret access key.
2.  Set up AWS RDS: Create an RDS PostgreSQL database instance. Update the database configuration in the Django settings file (settings.py) with your RDS endpoint, database name, username, and password.
3.  Set up Braintree: Sign up for a Braintree account and obtain your Braintree API credentials (merchant ID, public key, private key). Update the payment configuration in the Django settings file (settings.py) with your Braintree API credentials.
4.  Migrate the database: Run the Django database migration commands to apply the database schema and create the necessary tables.
5.  Collect static files: Use the collectstatic management command to gather all the static files and upload them to your AWS S3 bucket.
6.  Start the Django development server: Run the manage.py runserver command to start the Django development server.

### View live site here;
- https://h20express.pythonanywhere.com
  
Please note that the above steps assume you have the necessary AWS credentials and access rights to create S3 buckets and RDS instances. Refer to the official AWS documentation for more detailed instructions on setting up AWS S3 and AWS RDS. Similarly, refer to the Braintree documentation for guidance on obtaining API credentials and integrating Braintree with your Django application.

## Contributing
Contributions to H2OExpress are welcome! If you find a bug or have a suggestion for improvement, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
