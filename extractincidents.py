import pypdf
from pypdf import PdfReader
from io import BytesIO
import re


#Extracts fields "Date / Time", "Incident Number", "Location", "Nature", "Incident ORI" from the incident data
def extractincidents(incident_data):

    incident_file = BytesIO(incident_data) #Converts the data returned from the url to bytes
    incident_file_pdf = PdfReader(incident_file) #Converts the data in bytes to a pdf and reads it
    records = []
    exclude_line = ["Date / Time", "Incident Number", "Location", "Nature", "Incident ORI"]
    
    
    # Regex to match the Date/Time pattern
    date_time_pattern = re.compile(r'^\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}')
   
    #Extract data from each page of the pdf
    for page in incident_file_pdf.pages:
        text = page.extract_text(extraction_mode="layout") #Using the mode layout extraction becomes way easier
        for line in text.split('\n'):
            line=line.strip()

            for str in exclude_line:
                if line.startswith(str): #Ignore the first line as it contains the names of the columns and not data
                    continue
           
            # Check if the current line starts with a date to take of the data present on multiple lines edge case
            if re.match(r'^\d{1,2}/\d{1,2}/\d{4}', line):
                chunks = re.split(r'\s{2,}', line)
                if len(chunks) >= 5:        #Extracts each field from the incident data
                    incident = {
                        'Date Time': chunks[0],
                        'Incident Number': chunks[1],
                        'Location': chunks[2],
                        'Nature': chunks[3],
                        'ORI': chunks[4]
                    }
                    records.append(incident)    #Saves each of the fields corresponding to a record as a list of dictionaries
                

    return records