from flask import Flask, render_template, request
import requests
import csv
from io import StringIO

app = Flask(__name__)

# Google Sheets "Publish to Web" CSV URL
CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR6Lbbs-AltzrKRL2I_iiWm2hD8ZfKyvFxIGWJyY-Cag4wQ0aALItgGDNl-eQ7aYc2e4c0PQ0Ui43VP/pub?output=csv'


# Function to read CSV data
def read_csv(csv_content):
    data = []
    csvfile = StringIO(csv_content)  # Use StringIO to simulate a file object
    reader = csv.reader(csvfile)
    
    # Skip the first line and read the second line for headers
    next(reader)  # Skip the first line
    headers = next(reader)  # Read the second line for headers
    
    for row in reader:
        if row:  # Check if the row is not empty
            # Strip whitespace from headers and values
            entry = {header.strip(): value.strip() for header, value in zip(headers, row)}
            data.append(entry)
    return data


# Function to fetch and parse the CSV data from the Google Sheets URL
def fetch_csv_data():
    response = requests.get(CSV_URL)
    response.raise_for_status()  # Check if the request was successful
    decoded_content = response.content.decode('utf-8')
    
    # Read and parse the CSV data
    data = read_csv(decoded_content)

    # Debugging output
    print("Fetched data:", data)
    return data

# Fetch data from the CSV (publish to web)
data = fetch_csv_data()

# List of categories
categories = [
    "Healthcare Benefits",
    "Employee Assistance Programs (EAPs)",
    "Mental Health Counseling, Wellness, and Substance Cessation Programs",
    "Financial Counseling and Legal Services",
    "Employee Resource Groups (ERGs) and Employee Activity Clubs",
    "Lifestyle Spending Account (e.g., stipend for gym, childcare, pet care, leisure, travel, wellness)",
    "Volunteer Opportunities",
    "Childcare Programs",
    "Transportation and Transit Offerings",
    "On-site Amenities"
]

# Home page to select a category
@app.route('/')
def home():
    return render_template('index.html', categories=categories)

# Category view route
@app.route('/category/<category>')
def category_view(category):
    # Print data for troubleshooting
    print(data)
    
    # Filter entries based on the selected category
    filtered_data = [entry for entry in data if entry.get('Category') == category]
    
    # Render the category page with the filtered data
    return render_template('category.html', category=category, entries=filtered_data)

# View to show all entries
@app.route('/all_entries')
def all_entries():
    return render_template('all_entries.html', entries=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
