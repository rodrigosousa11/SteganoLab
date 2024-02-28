# SteganoLab

This web application allows users to encode secret messages into images with or without passwords using the LSB-Steganography technique in which we replace the least significant bit of the image with the bits of a message to be hidden and decode them back to retrieve the original message. Users can optionally sign up for an account and this provides them the opportunity to keep track of their past activities, including the images they've encoded and decoded.

This type of technique only works with lossless image formats like PNG and BMP, as lossy formats like JPEG can lose the hidden data during compression. So before the encoding process, the application checks if the image is in a lossless format and if not, it converts it to PNG, so that **every image file the user uploads works**. 

## Distinctiveness and Complexity

### This project satisfies the distinctiveness and complexity requirements in the following ways:

### Distinctiveness: 
While steganography itself isn't a new concept, this application focuses on encoding and decoding messages in images through a user-friendly web interface. This eliminates the need for technical knowledge or command-line tools, making it accessible to a wider audience.
### Complexity:
The application utilizes Python libraries like Pillow for image processing and dedicated steganography functions to handle encoding and decoding tasks. This demonstrates the ability to integrate different tools and libraries to achieve a specific functionality. The application also includes user authentication, file handling, and error handling to ensure a seamless and secure user experience. This adds complexity to the project by incorporating multiple layers of functionality and security measures.

## Project files

- `capstone/`: Django project directory containing the application settings and configuration.
- `steganography/`: Django app directory containing the main application logic.
    - `media/`: Directory for storing user-uploaded images.
    - `static/steganography/`: Directory for static files including JavaScript and CSS.
        - `script.js`: JavaScript file containing client-side logic for interacting with the server with requests of encoding and decoding in a way that the user can see the results without refreshing the page.
        - `styles.css`: CSS file for styling the web pages.
    - `templates/steganography/`: HTML templates for rendering web pages.
        - `layout.hyml`: Base template for the application.
        - `index.html`: Home page for the application where is the encode and decode tabs.
        - `login.html`: Login page for the application.
        - `register.html`: Register page for the application.
        - `history.html`: Page for displaying user's past encoded and decoded messages.
    - `models.py`: Defines the database models for storing encoded and decoded messages, for the user model I used the django built-in User model.
    - `views.py`: Contains the view functions for handling user requests, login, register, encoding and decoding messages and history.
    - `steganography.py`: Contains the steganography logic for encoding and decoding messages in images. 
        - `generate_binary_data(data)`: This function takes a string data as input and converts each character into its 8-bit binary representation using ASCII values. It returns a list of binary strings.
        - `modify_pixels(image_pixels, data)`: This function modifies the least significant bit (LSB) of the image pixels according to the binary data provided. It iterates through the image pixels and binary data to encode the message. The LSB of each pixel is adjusted to embed the binary data.
        - `encode_data_into_image(image, data)`: This function encodes the provided data into the image. It modifies the pixels of the image to embed the binary data, resulting in a modified image containing the hidden message.
        - `decode(image)`: This function decodes the hidden message from the provided image using LSB-Steganography. It iterates through the image pixels to extract the LSBs and reconstructs the original binary data, which is then converted back to the original message.
        - `encode_data_with_password(image, data, password)`: This function extends the encode_data_into_image function to include a password. It encodes the provided data into the image along with the password. The password and data are combined with a delimiter before encoding.
        - `decode_with_password(image, password)`: This function extends the decode function to handle decoding with a password. It decodes the hidden message from the provided image and verifies the password. If the password is correct, it returns the decoded message; otherwise, it returns None.
        - `has_password(image)`: This function checks if the provided image contains a password-protected message encoded. It examines the last 8 pixels of the image to identify the presence of a password delimiter.
    - `requirements.txt`: List of packages required to run the application.

## How to run the application

1. Install the required Python packages using the following command:
    ```
    pip install -r requirements.txt
    ```

2. Run migrations.
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

3. Navigate to the project directory containing the `manage.py` file and run the development server.
    ```
    python manage.py runserver
    ```


4. Access the application in a web browser using the following URL:
    ```
    http://127.0.0.1:8000/
    ```