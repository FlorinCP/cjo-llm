import csv
from zeep import Client

# Connect to the SOAP web service
wsdl_url = 'http://portalquery.just.ro/Query.asmx?WSDL'
client = Client(wsdl_url)

def search_cases_by_institution(institution_name, start_date, end_date):
    # Call the SOAP method
    response = client.service.CautareDosare(
        institutie=institution_name,
        dataStart=start_date,
        dataStop=end_date
    )
    return response

# Example usage of the search function
institution_name = 'TribunalulSIBIU'  # Example institution
start_date = '2023-01-01'  # Start date in YYYY-MM-DD format
end_date = '2023-12-31'  # End date in YYYY-MM-DD format
cases = search_cases_by_institution(institution_name, start_date, end_date)

# Now let's write this data to a CSV file
with open('cases.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Numar', 'Numar Vechi', 'Data', 'Institutie', 'Departament', 'Categorie Caz', 'Stadiu Procesual', 'Obiect'])

    # Write the data rows
    for case in cases:
        writer.writerow([
            case.numar,
            case.numarVechi,
            case.data.strftime('%Y-%m-%d') if case.data else '',  # Ensure date is formatted
            case.institutie,
            case.departament,
            case.categorieCaz,
            case.stadiuProcesual,
            case.obiect
        ])

print("CSV file has been created.")
