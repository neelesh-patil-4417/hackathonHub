# hackathonHub
Imagine you are working for an Edtech company and you are asked to create a simple Hackathon hosting application. The hackathon can be posted by anyone and they will be authorized before they are allowed to post hackathons. Users should be able to come and submit some code or files as hackathon submissions. 

# **Find the link for the schema**
https://excalidraw.com/#json=PKJx176jHCXdmaY6foUzE,YleI9XOwOrDGFPyvE9_7QQ


# Django Project Setup

This guide will help you set up the Django project locally on your machine.

## Prerequisites

Make sure you have the following installed:

- Python 3.9 or higher
- pip (Python package installer)
- (Optional) Virtual Environment (recommended)


Clone the project repository using Git:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name


## Step 2: Create a Virtual Environment

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate


## Step 3: Install Dependencies

pip install -r requirements.txt


## Step 4: Run Migrations

python manage.py migrate


## Step 5: Create a Superuser (Optional)

python manage.py createsuperuser


## Step 6: Run the Development Server

python manage.py runserver


## Step 7: Access the Admin Interface (Optional

If you created a superuser, you can access the Django admin interface at http://127.0.0.1:8000/admin/
