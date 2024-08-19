from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from openpyxl.utils.exceptions import InvalidFileException

def home(request):
    return render(request, 'home.html')




def upload_member_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        if not uploaded_file.name.endswith('.xlsx'):
            return JsonResponse({'status': 'error', 'message': 'Please upload a valid .xlsx file.'})

        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(file_path)

        try:
            # Read the entire sheet
            df = pd.read_excel(file_path, engine='openpyxl', header=None)

            # Print the first few rows to understand the structure
            print(df.head(15))

            # Skip rows up to the header (e.g., 9 rows if header is on row 10)
            df = pd.read_excel(file_path, engine='openpyxl', skiprows=9)

            # Print the columns to see if they are correctly read
            print("Columns after skipping rows:", df.columns.tolist())

            # Rename columns based on their position
            df.columns = ['A', 'B', 'First Name', 'D', 'Last Name', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

            # Extract the relevant columns
            df = df[['First Name', 'Last Name']]

        except InvalidFileException:
            return JsonResponse({'status': 'error', 'message': 'The file is not a valid .xlsx file or it is corrupted.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to read the Excel file: {str(e)}'})

        try:
            # Ensure the column names are correct
            if 'First Name' not in df.columns or 'Last Name' not in df.columns:
                return JsonResponse({'status': 'error', 'message': 'Missing expected columns: "First Name" and/or "Last Name".'})

            first_names = df['First Name']
            last_names = df['Last Name']
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing expected columns: {str(e)}'})

        name_counts = df.groupby(['First Name', 'Last Name']).size().reset_index(name='Count')

        return JsonResponse({'status': 'success', 'name_counts': name_counts.to_dict('records')})

    return render(request, 'upload_member_file.html')

def upload_palms_report(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        if not uploaded_file.name.endswith('.xlsx'):
            return JsonResponse({'status': 'error', 'message': 'Please upload a valid .xlsx file.'})

        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(file_path)

        try:
            # Read the file without headers
            df = pd.read_excel(file_path, engine='openpyxl', header=None)

            # Print the initial structure of the DataFrame
            print("Initial DataFrame shape:", df.shape)
            print("Initial DataFrame columns:", df.columns.tolist())
            print("Initial DataFrame head:\n", df.head(15))

            # Use row 8 (index 7) as header
            df = pd.read_excel(file_path, engine='openpyxl', header=7)

            # Print the DataFrame structure after setting header
            print("DataFrame shape after setting header:", df.shape)
            print("DataFrame columns after setting header:", df.columns.tolist())
            print("DataFrame head after setting header:\n", df.head(15))

            # Define the expected columns and filter out unnecessary columns
            expected_columns = [
                'First Name', 'Last Name', 'P', 'A', 'L', 'M', 'S', 'RGI', 'RGO', 'RRI', 'RRO', 'V', '1-2-1', 'TYFCB', 'CEU', 'T'
            ]

            # Ensure that we are working with the exact number of columns
            df = df[expected_columns]

        except InvalidFileException:
            return JsonResponse({'status': 'error', 'message': 'The file is not a valid .xlsx file or it is corrupted.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Column not found: {str(e)}'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to read the Excel file: {str(e)}'})

        # Convert the DataFrame to a dictionary for the JSON response
        data = df.to_dict('records')

        return JsonResponse({'status': 'success', 'data': data})

    return render(request, 'upload_palms_report.html')

