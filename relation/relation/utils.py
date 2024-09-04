import csv
from relation.models import AIDictionary

def import_ai_dictionary_from_csv():
    csv_file_path = r'C:\Users\roybi\Desktop\group-project\relation\relation\static\AI_dictionary.csv'  # CSV 파일 경로

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            AIDictionary.objects.create(
                term=row['term'],
                term_en=row['term-en'],
                term_kor=row['term-kor'],
                mean=row['mean'],
                detail_mean=row['detail_mean']
            )
