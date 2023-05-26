import openpyxl
from posts.models import Zero

def import_zero_data(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    data = []

    for row in sheet.iter_rows(min_row=2):
        if row[0].value:
            data.append({
                'name': row[0].value,
                'address': row[1].value,
                'region': row[2].value,
                'phone_number': row[3].value if row[3].value else '',
            })

    for item in data:
        store = Zero(
            name=item['name'],
            address=item['address'],
            region=item['region'],
            phone_number=item['phone_number'],
        )
        store.save()
