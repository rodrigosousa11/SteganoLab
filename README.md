# SteganoLab

This web application allows users to encode secret messages into images with or without passwords using the LSB-Steganography technique in which we replace the least significant bits of the image with the bits of a message to be hidden and decode them back to retrieve the original message. Users can optionally sign up for an account and this provides them the opportunity to keep track of their past activities, including the images they've encoded and decoded.

This type of technique only works with lossless image formats like PNG and BMP, as lossy formats like JPEG can lose the hidden data during compression. So before the encoding process, the application checks if the image is in a lossless format and if not, it converts it to PNG, so that **every image file the user uploads works**. 

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
