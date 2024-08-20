from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from openpyxl.utils.exceptions import InvalidFileException
from django.urls import reverse
from pandas.errors import EmptyDataError, ParserError
from io import BytesIO


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
            df = pd.read_excel(file_path, engine='openpyxl', skiprows=9)
            df.columns = ['A', 'B', 'First_Name', 'D', 'Last_Name', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
            df = df[['First_Name', 'Last_Name']]

            # Calculate the count of each combination of first and last names
            name_counts = df.groupby(['First_Name', 'Last_Name']).size().reset_index(name='Count')

            # Save the data including counts in the session
            request.session['member_data'] = name_counts.to_dict('records')

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to read the Excel file: {str(e)}'})

        return JsonResponse({
            'status': 'success',
            'message': 'Data captured',
            'redirect_url': reverse('upload_palms_report')
        })

    return render(request, 'upload_member_file.html')


def upload_palms_report(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        if not uploaded_file.name.endswith('.xlsx'):
            return JsonResponse({'status': 'error', 'message': 'Please upload a valid .xlsx file.'})

        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(file_path)

        try:
            # Read the file with headers
            df = pd.read_excel(file_path, engine='openpyxl', header=7)

            # Define the expected columns
            expected_columns = [
                'First Name', 'Last Name', 'P', 'A', 'L', 'M', 'S', 'RGI', 'RGO', 'RRI', 'RRO', 'V', '1-2-1', 'TYFCB', 'CEU', 'T'
            ]

            # Ensure that we are working with the expected columns
            df = df[expected_columns]

            # Rename columns to match the desired template variable names
            df.rename(columns={'First Name': 'First_Name', 'Last Name': 'Last_Name'}, inplace=True)

            # Fetch the member data from session
            member_data = request.session.get('member_data', [])
            member_df = pd.DataFrame(member_data)

            # Merge the PALMS data with member data to include the training value (Count)
            df = df.merge(member_df, how='left', on=['First_Name', 'Last_Name'])

            # Calculate additional fields
            df['Absent_Score'] = df['A'].map({0: 15, 1: 10, 2: 5, 3: 0})
            df['Late_Score'] = df['L'].apply(lambda x: 5 if x == 0 else 0)
            df['Referral_Score'] = df.apply(lambda row: 
                20 if (row['RGO'] + row['RGI']) >= 32 else
                15 if (row['RGO'] + row['RGI']) >= 26 else
                10 if (row['RGO'] + row['RGI']) >= 20 else
                5 if (row['RGO'] + row['RGI']) >= 13 else 0,
                axis=1
            )
            df['Visitor_Score'] = df['V'].apply(lambda x: 
                20 if x >= 20 else
                15 if x >= 13 else
                10 if x >= 7 else
                5 if x >= 3 else 0
            )
            df['TYFCB_Score'] = df['TYFCB'].apply(lambda x: 
                15 if x >= 20 else
                10 if x >= 10 else
                5 if x >= 5 else 0
            )
            df['Testimonial_Score'] = df['T'].apply(lambda x: 
                10 if x >= 2 else
                5 if x == 1 else 0
            )

            # Calculate the training score based on the Count column
            df['training_Score'] = df['Count'].apply(lambda x: 
                15 if x >= 3 else
                10 if x == 2 else
                5 if x == 1 else 0
            )

            # Calculate the total score
            df['Total_Score'] = df[['Absent_Score', 'Late_Score', 'Referral_Score', 'Visitor_Score', 'TYFCB_Score', 'Testimonial_Score', 'training_Score']].sum(axis=1)
            df['Projected_Score'] = df['Total_Score'].apply(lambda x:
                'Green' if x >= 70 else
                'Amber' if x >= 50 else
                'Red' if x >= 30 else 'Grey'
            )

            # Store the data in session
            request.session['palms_data'] = df.to_dict('records')

        except (EmptyDataError, ParserError):
            return JsonResponse({'status': 'error', 'message': 'The file is not a valid .xlsx file or it is corrupted.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Column not found: {str(e)}'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to read the Excel file: {str(e)}'})

        return JsonResponse({
            'status': 'success', 
            'message': 'Data captured', 
            'redirect_url': reverse('final_data')  # Redirect to final data page
        })

    return render(request, 'upload_palms_report.html')



    

def final_data_view(request):
    # Retrieve data from session
    member_data = request.session.get('member_data', [])
    palms_data = request.session.get('palms_data', [])

    # Pass the data to the template
    context = {
        'member_data': member_data,
        'palms_data': palms_data
    }

    return render(request, 'final_data.html', context)


def export_go_green_excel(request):
    # Retrieve data from session
    palms_data = request.session.get('palms_data', [])

    # Create a DataFrame from the session data
    df = pd.DataFrame(palms_data)

    # Calculate the Referral_Value as the sum of RGO and RGI
    df['Referral_Value'] = df['RGO'] + df['RGI']

    # Create the 'Name' field by combining 'First_Name' and 'Last_Name'
    df['Name'] = df['First_Name'] + ' ' + df['Last_Name']

    # Rename columns as specified
    df.rename(columns={
        'A': 'Absent Value',
        'L': 'Late Value',
        'V': 'Visitor Value',
        'TYFCB': 'TYFCB Vale',
        'T': 'Testimonial Value',
        'Count': 'Training Value',
        'Absent_Score': 'Absents = Score',
        'Late_Score': 'Late = Score',
        'Referral_Score': 'Total Ref = Score',
        'Visitor_Score': 'Total Vis = Score',
        'TYFCB_Score': 'Total Amt = Score',
        'training_Score': 'Total Trngs = Score',
        'Testimonial_Score': 'Tot Testimonails = Score',
        'Total_Score': 'Total Score'
    }, inplace=True)

    # Define the fields to include in the export
    fields = [
        'Name', 'Absent Value', 'Late Value', 'Visitor Value', 'Referral_Value',
        'TYFCB Vale', 'Testimonial Value', 'Training Value', 'Absents = Score',
        'Late = Score', 'Total Ref = Score', 'Total Vis = Score',
        'Total Amt = Score', 'Total Trngs = Score', 'Tot Testimonails = Score', 'Total Score'
    ]

    # Filter the DataFrame to include only the specified fields
    df = df[fields]

    # Create a BytesIO buffer for the Excel file
    buffer = BytesIO()

    # Write the DataFrame to the buffer as an Excel file
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Go Green Data', index=False)

    # Rewind the buffer's position to the beginning
    buffer.seek(0)

    # Create the HttpResponse to send the file
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=go_green_data.xlsx'

    return response