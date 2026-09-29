"""
រៀបចំ Dataset សម្រាប់ទិន្នន័យសិស្ស
Prepare Dataset for Student Data

Script នេះជួយរៀបចំឈ្មោះឯកសារសម្រាប់រូបភាពសិស្ស
This script helps prepare filenames for student photos
"""

import csv
import os
import shutil
from pathlib import Path


def read_students_csv(csv_file='students_list.csv'):
    """អានទិន្នន័យសិស្សពីឯកសារ CSV"""
    students = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append({
                    'លរ': row['ល.រ'],
                    'អត្តលេខ': row['អត្តលេខ'],
                    'ឈ្មោះ': row['ឈ្មោះ'].strip(),
                    'ភេទ': row['ភេទ']
                })
    except Exception as e:
        print(f"❌ មានបញ្ហាក្នុងការអានឯកសារ CSV: {e}")
        return []
    
    return students


def create_filename_mapping(students):
    """បង្កើតឈ្មោះឯកសារតាមទម្រង់ [លរ]_[អត្តលេខ]_[ឈ្មោះ].jpg"""
    mapping = []
    
    for student in students:
        # ទម្រង់លេខរៀងជា 3 ខ្ទង់ (001, 002, 003, ...)
        formatted_num = f"{int(student['លរ']):03d}"
        
        # ស្អាតឈ្មោះ (ដកចេញចន្លោះ និងតួអក្សរពិសេស)
        clean_id = student['អត្តលេខ'].replace('-', '')
        clean_name = student['ឈ្មោះ'].replace(' ', '_')
        
        # ទម្រង់: 001_DUC20240002_កាំង_ប៊ុនឆៃ.jpg
        filename = f"{formatted_num}_{clean_id}_{clean_name}.jpg"
        
        mapping.append({
            'លរ': student['លរ'],
            'អត្តលេខ': student['អត្តលេខ'],
            'ឈ្មោះ': student['ឈ្មោះ'],
            'ភេទ': student['ភេទ'],
            'filename': filename
        })
    
    return mapping


def generate_filename_list(mapping, output_file='dataset_filenames.txt'):
    """បង្កើតបញ្ជីឈ្មោះឯកសារ"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("បញ្ជីឈ្មោះឯកសាររូបភាពសិស្ស (Student Photo Filenames)\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("ទម្រង់ (Format): [លរ]_[អត្តលេខ]_[ឈ្មោះ].jpg\n\n")
        
        f.write("-" * 80 + "\n")
        f.write(f"{'ល.រ':<6} {'អត្តលេខ':<18} {'ឈ្មោះ':<25} {'ឈ្មោះឯកសារ'}\n")
        f.write("-" * 80 + "\n")
        
        for item in mapping:
            f.write(f"{item['លរ']:<6} {item['អត្តលេខ']:<18} {item['ឈ្មោះ']:<25} {item['filename']}\n")
        
        f.write("-" * 80 + "\n")
        f.write(f"\nសរុប: {len(mapping)} នាក់\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("ការណែនាំ (Instructions):\n")
        f.write("-" * 80 + "\n")
        f.write("1. ថតរូបសិស្សម្នាក់ៗ (Take photos of each student)\n")
        f.write("2. ប្តូរឈ្មោះឯកសារតាមបញ្ជីខាងលើ (Rename files according to list above)\n")
        f.write("3. ដាក់ឯកសារក្នុងថត dataset/ (Put files in dataset/ folder)\n")
        f.write("4. រត់ពាក្យបញ្ជា (Run command):\n")
        f.write("   .\\venv\\Scripts\\python.exe register_from_dataset.py\n")
        f.write("-" * 80 + "\n")
    
    print(f"✓ បានបង្កើតឯកសារ: {output_file}")


def generate_rename_script(mapping, output_file='rename_photos.py'):
    """បង្កើត script សម្រាប់ប្តូរឈ្មោះរូបភាពដោយស្វ័យប្រវត្តិ"""
    
    script_content = '''"""
Script ប្តូរឈ្មោះរូបភាពដោយស្វ័យប្រវត្តិ
Auto-rename Photos Script

របៀបប្រើ (How to use):
1. ដាក់រូបភាពទាំងអស់ក្នុងថត 'photos_to_rename/'
2. ដាក់ឈ្មោះឯកសារជាលេខរៀង: 1.jpg, 2.jpg, 3.jpg, ... 43.jpg
3. រត់ script នេះ: python rename_photos.py
4. រូបភាពនឹងត្រូវចម្លងទៅ dataset/ ជាមួយឈ្មោះត្រឹមត្រូវ
"""

import os
import shutil

# ឈ្មោះឯកសារគោលដៅ (Target filenames)
FILENAME_MAPPING = {
'''
    
    for item in mapping:
        num = int(item['លរ'])
        filename = item['filename']
        script_content += f"    {num}: '{filename}',\n"
    
    script_content += '''}

def rename_photos(source_dir='photos_to_rename', target_dir='dataset'):
    """ប្តូរឈ្មោះរូបភាព"""
    
    # បង្កើតថតគោលដៅ
    os.makedirs(target_dir, exist_ok=True)
    
    if not os.path.exists(source_dir):
        print(f"❌ រកមិនឃើញថត: {source_dir}")
        print(f"   សូមបង្កើតថត '{source_dir}' ហើយដាក់រូបភាពចូលទៅ")
        return
    
    print("\\n" + "="*70)
    print("ប្តូរឈ្មោះរូបភាព (Renaming Photos)")
    print("="*70 + "\\n")
    
    success_count = 0
    error_count = 0
    
    for num, target_filename in FILENAME_MAPPING.items():
        # ឈ្មោះឯកសារដើម (Original filename)
        extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
        source_file = None
        
        for ext in extensions:
            test_file = os.path.join(source_dir, f"{num}{ext}")
            if os.path.exists(test_file):
                source_file = test_file
                break
        
        if not source_file:
            print(f"⚠️  រកមិនឃើញ: {num}.jpg (សូមពិនិត្យឯកសារ)")
            error_count += 1
            continue
        
        # ច្រឹបឈ្មោះឯកសារគោលដៅ
        target_file = os.path.join(target_dir, target_filename)
        
        try:
            # ចម្លងឯកសារ
            shutil.copy2(source_file, target_file)
            print(f"✓ {num}.jpg → {target_filename}")
            success_count += 1
        except Exception as e:
            print(f"❌ មានបញ្ហា {num}.jpg: {e}")
            error_count += 1
    
    # សង្ខេប (Summary)
    print("\\n" + "="*70)
    print("សង្ខេប (Summary)")
    print("="*70)
    print(f"✓ ជោគជ័យ: {success_count}")
    print(f"❌ មានបញ្ហា: {error_count}")
    print(f"📁 រូបភាពត្រូវបានរក្សាទុកក្នុង: {target_dir}/")
    print("="*70 + "\\n")
    
    if success_count > 0:
        print("ជំហានបន្ទាប់ (Next step):")
        print("  .\\\\venv\\\\Scripts\\\\python.exe register_from_dataset.py")

if __name__ == "__main__":
    rename_photos()
'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✓ បានបង្កើត script: {output_file}")


def create_directory_structure():
    """បង្កើតរចនាសម្ព័ន្ធថត"""
    directories = [
        'dataset',
        'photos_to_rename',
        'data/database',
        'data/registered_faces'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✓ បានបង្កើតថតទាំងអស់")


def main():
    """ដំណើរការសំខាន់"""
    print("\n" + "="*70)
    print("រៀបចំ Dataset សម្រាប់ទិន្នន័យសិស្ស")
    print("Prepare Dataset for Student Data")
    print("="*70 + "\n")
    
    # អានទិន្នន័យ
    print("1. កំពុងអានទិន្នន័យសិស្ស...")
    students = read_students_csv()
    
    if not students:
        print("❌ មិនអាចអានទិន្នន័យបាន!")
        return
    
    print(f"   ✓ បានអាន {len(students)} នាក់")
    
    # បង្កើតឈ្មោះឯកសារ
    print("\n2. កំពុងបង្កើតឈ្មោះឯកសារ...")
    mapping = create_filename_mapping(students)
    print(f"   ✓ បានបង្កើត {len(mapping)} ឈ្មោះឯកសារ")
    
    # បង្កើតបញ្ជី
    print("\n3. កំពុងបង្កើតបញ្ជីឈ្មោះឯកសារ...")
    generate_filename_list(mapping)
    
    # បង្កើត rename script
    print("\n4. កំពុងបង្កើត rename script...")
    generate_rename_script(mapping)
    
    # បង្កើតថត
    print("\n5. កំពុងបង្កើតថត...")
    create_directory_structure()
    
    # សង្ខេប
    print("\n" + "="*70)
    print("✅ រួចរាល់! (Completed!)")
    print("="*70)
    print("\nឯកសារដែលបានបង្កើត (Created files):")
    print("  📄 students_list.csv - ទិន្នន័យសិស្ស")
    print("  📄 dataset_filenames.txt - បញ្ជីឈ្មោះឯកសារ")
    print("  📄 rename_photos.py - script ប្តូរឈ្មោះ")
    print("\nថតដែលបានបង្កើត (Created folders):")
    print("  📁 dataset/ - សម្រាប់រូបភាពដែលមានឈ្មោះត្រឹមត្រូវ")
    print("  📁 photos_to_rename/ - សម្រាប់រូបភាពដើម")
    
    print("\n" + "="*70)
    print("ជំហានបន្ទាប់ (Next Steps):")
    print("="*70)
    print("\nវិធី 1: ប្តូរឈ្មោះដោយដៃ (Manual Rename)")
    print("  1. មើលឯកសារ dataset_filenames.txt")
    print("  2. ថតរូបសិស្សម្នាក់ៗ")
    print("  3. ប្តូរឈ្មោះតាមបញ្ជី ហើយដាក់ក្នុង dataset/")
    print("  4. រត់: .\\venv\\Scripts\\python.exe register_from_dataset.py")
    
    print("\nវិធី 2: ប្តូរឈ្មោះដោយស្វ័យប្រវត្តិ (Auto Rename)")
    print("  1. ដាក់រូបភាពក្នុង photos_to_rename/ ជាឈ្មោះ 1.jpg, 2.jpg, ...")
    print("  2. រត់: python rename_photos.py")
    print("  3. រត់: .\\venv\\Scripts\\python.exe register_from_dataset.py")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ មានបញ្ហា: {e}")
        import traceback
        traceback.print_exc()
