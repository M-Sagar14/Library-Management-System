import os
import sys
import django
import pandas as pd
from django.core.files import File

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # E:\lmspro\project\lmsproject\lmsproject
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)               # E:\lmspro\project\lmsproject
PARENT_ROOT = os.path.dirname(PROJECT_ROOT)               # E:\lmspro\project

# Add both project root and parent root to sys.path
sys.path.append(PROJECT_ROOT)
sys.path.append(PARENT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMS.settings')
django.setup()

from AdminApp.models import Books

csv_path = os.path.join(CURRENT_DIR, 'books.csv')
df = pd.read_csv(csv_path)
image_folder = os.path.join(PROJECT_ROOT, 'media', 'images_folder')
for _,row in df.iterrows():
    image_filename = str(row.get('Image').strip() if pd.notna(row.get('Image'))else None )
    image_path=os.path.join(image_folder, image_filename) if image_filename else None
    book,created=Books.objects.update_or_create(
        ISBN = row['isbn'],
        defaults={
            'Book_Id' : row['Book_Id'],
            'Title' : row['Title'],
            'Author' : row['Author'],
            'Published_Year' : row['Published_Year'],
            'Total_Copies' : row['Total_Copies'],
            'Available_Copies' : row['Available_Copies'],
            'Category' : row['Category'],
            'Edition' : row['Edition'],

        }
    )
    if image_filename and os.path.exists(image_path):
        with open(image_path,'rb') as image_file:
            book.Image.save(image_filename , File(image_file),save=True)
    else:
        print(f"Path does not exist or image not found at {image_path}")

    print(f"{'Created' if created else 'Updated'}: {row['Title']}")
