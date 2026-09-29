"""
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
    1: '001_DUC20240002_កាំង_ប៊ុនឆៃ.jpg',
    2: '002_DUC20240025_ក្វាវ_មេសា.jpg',
    3: '003_DUC20240045_គង់_បារាំង.jpg',
    4: '004_DUC20240083_ងួន​_វណ្ណ.jpg',
    5: '005_DUC20240119_ឆៃ_សោភា.jpg',
    6: '006_DUC20240137_ឈន_សុវណ្ណៈ.jpg',
    7: '007_DUC20240140_ឈឹម_ម៉ាលីន.jpg',
    8: '008_DUC20240147_ឈឿត_ណារិទ្ធ.jpg',
    9: '009_DUC20240150_ញ៉_នេត.jpg',
    10: '010_DUC20240172_ដួង_សុភី.jpg',
    11: '011_DUC20240215_តេង_ស្រីអូន.jpg',
    12: '012_DUC20240271_នាង_ណាន់.jpg',
    13: '013_DUC20240277_នី_ណែត.jpg',
    14: '014_DUC20240281_នឹង​​_កក្កដា.jpg',
    15: '015_DUC20240294_នៀម_ស្រីនិត.jpg',
    16: '016_DUC20240313_បាវ_ចាន់ណា.jpg',
    17: '017_DUC20240375_ពៅ_បញ្ញា.jpg',
    18: '018_DUC20240378_ពៅ​_រដ្ឋា.jpg',
    19: '019_DUC20240380_ព្រំ_សុភ័ក្រ.jpg',
    20: '020_DUC20240395_ភុក_ផាន់ណា.jpg',
    21: '021_DUC20240415_ម៉ឹង_មិ.jpg',
    22: '022_DUC20240575_វ៉ា_ម៉ានី.jpg',
    23: '023_DUC20240469_យ៉េង_ថាវី.jpg',
    24: '024_DUC20240514_រួន_បុលិមុន្នី.jpg',
    25: '025_DUC20240527_រ៉េន_គឹមរ៉ុង.jpg',
    26: '026_DUC20240530_រ៉ែម​_សុនិច្ច.jpg',
    27: '027_DUC20240556_លួន_ណាវី.jpg',
    28: '028_DUC20240576_វ៉ាង_មីនា.jpg',
    29: '029_DUC20240591_វិន_ចាន់សុជាតិ.jpg',
    30: '030_DUC20240609_វ៉េន_ស្រីលាក់.jpg',
    31: '031_DUC20240613_សំ_ប្រោន.jpg',
    32: '032_DUC20240616_ស៊ត_មួយឆេង.jpg',
    33: '033_DUC20240626_សយ_ឡុង.jpg',
    34: '034_DUC20240695_ស៊ុម​_យូអុី.jpg',
    35: '035_DUC20240696_សុស_សូវីណាន់.jpg',
    36: '036_DUC20240703_សួស​_បញ្ញា.jpg',
    37: '037_DUC20240712_សឿន_វិសាល.jpg',
    38: '038_DUC20240734_សេវ_ហៀល.jpg',
    39: '039_DUC20240746_សៅ_បញ្ញា.jpg',
    40: '040_DUC20240747_សៅ_រ៉ាម៉ន.jpg',
    41: '041_DUC20240786_ហូរ_កែវ.jpg',
    42: '042_DUC20240838_អាង_ស៊ីនិន.jpg',
    43: '043_DUC20240855_អ៊ុន_សុខេណារីម.jpg',
}

def rename_photos(source_dir='photos_to_rename', target_dir='dataset'):
    """ប្តូរឈ្មោះរូបភាព"""
    
    # បង្កើតថតគោលដៅ
    os.makedirs(target_dir, exist_ok=True)
    
    if not os.path.exists(source_dir):
        print(f"❌ រកមិនឃើញថត: {source_dir}")
        print(f"   សូមបង្កើតថត '{source_dir}' ហើយដាក់រូបភាពចូលទៅ")
        return
    
    print("\n" + "="*70)
    print("ប្តូរឈ្មោះរូបភាព (Renaming Photos)")
    print("="*70 + "\n")
    
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
    print("\n" + "="*70)
    print("សង្ខេប (Summary)")
    print("="*70)
    print(f"✓ ជោគជ័យ: {success_count}")
    print(f"❌ មានបញ្ហា: {error_count}")
    print(f"📁 រូបភាពត្រូវបានរក្សាទុកក្នុង: {target_dir}/")
    print("="*70 + "\n")
    
    if success_count > 0:
        print("ជំហានបន្ទាប់ (Next step):")
        print("  .\\venv\\Scripts\\python.exe register_from_dataset.py")

if __name__ == "__main__":
    rename_photos()
