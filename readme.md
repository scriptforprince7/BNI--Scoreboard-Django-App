***Note for developer(s)***

#### there are two apps beside the main app :
1. Scores : deals with csv files, processes data , generates report : working
2. Reports : new app, to support xls fiiles exported from bni-connect : not working 

+ The developer who proceeds to works on this project, should create new django app, take template files from 'scores' app, implement new logics.

+ the files are xml based pre-2003 versions of excel, thus needs to be processed accordingly.  


*do not worry about package.json, you can remove it, it was created to format the code automatically using prettier and doesnt interact with django app*

# Employee Score Management System

Welcome to the Employee Score Management System, a web application designed to manage and visualize employee performance scores. This system allows users to upload performance data from Excel or CSV files, preview and confirm the data, and view the scores with color-coded indicators to easily identify performance levels. The application categorizes scores into different classes such as low, medium, high, and very high, providing a clear visual representation of each employee's performance.

## Features
- **Upload Scores**: Easily upload employee performance data from Excel or CSV files.
- **Preview Data**: Preview the uploaded data before confirming the upload to the database.
- **Score Visualization**: View the employee scores with color-coded indicators to quickly assess performance levels.
- **Score Classes**: Automatically categorize scores into low, medium, high, and very high classes.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```sh
    python manage.py migrate
    ```

5. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

1. Navigate to the web application in your browser:
    ```
    http://127.0.0.1:8000
    ```

2. Use the navigation bar to upload scores, view scorecards, and read about the project.

## Project Code Overview

The project is structured as follows:

1. **Models**: Define the [`EmployeeScore`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fpushpraj%2Frenew%2Fmyproject%2Fscores%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22EmployeeScore%22%5D "/home/pushpraj/renew/myproject/scores/models.py") model to store employee performance data.
2. **Views**: Handle the file upload, data processing, score calculation, and rendering of templates in [`views.py`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fpushpraj%2Frenew%2Fmyproject%2Fscores%2Fviews.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22views.py%22%5D "/home/pushpraj/renew/myproject/scores/views.py").
3. **Forms**: Manage the file upload form in [`forms.py`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fpushpraj%2Frenew%2Fmyproject%2Fscores%2Fforms.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22forms.py%22%5D "/home/pushpraj/renew/myproject/scores/forms.py").
4. **Templates**: Provide HTML templates for uploading files and viewing scores in the `templates` directory.
5. **Static Files**: Include CSS for styling the score classes in the [`static`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fpushpraj%2Frenew%2Fmyproject%2Fstatic%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/pushpraj/renew/myproject/static") directory.
6. **URLs**: Define the URL patterns for uploading and viewing scores in [`urls.py`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fpushpraj%2Frenew%2Fmyproject%2Fscores%2Furls.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22urls.py%22%5D "/home/pushpraj/renew/myproject/scores/urls.py").

## To-do

- Add support for XLS files.
- Improve error handling and validation.
- Enhance the user interface for better user experience.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
