# ការណែនាំប្រើប្រាស់ជាភាសាខ្មែរ
# Face Recognition Camera System with Dataset

## 📂 ថត Dataset

ប្រព័ន្ធនេះមានថត `dataset` សម្រាប់រក្សាទុករូបភាពមុខរបស់មនុស្សម្នាក់ៗ។

### ទម្រង់ឈ្មោះឯកសារ (Filename Format)

```
[ID]_[ឈ្មោះ].jpg
```

**ឧទាហរណ៍:**
- `001_Narith.jpg` → ID: 1, ឈ្មោះ: Narith
- `002_Dara.jpg` → ID: 2, ឈ្មោះ: Dara
- `003_Sokha.jpg` → ID: 3, ឈ្មោះ: Sokha

---

## 🚀 របៀបប្រើប្រាស់ (How to Use)

### វិធី 1: ចុះឈ្មោះតាមរយៈកាមេរ៉ា (Register via Camera)

**ពាក្យបញ្ជា (Command):**
```powershell
.\venv\Scripts\python.exe register_face.py
```

**ជំហានៗ (Steps):**
1. វាយបញ្ចូលឈ្មោះ (ឧទាហរណ៍: Narith)
2. ចុច SPACEBAR ៥ដង ដើម្បីថតរូប
3. ប្រព័ន្ធនឹងផ្តល់ ID ដល់អ្នកដោយស្វ័យប្រវត្តិ (ឧទាហរណ៍: ID: 1)
4. រូបភាពនឹងត្រូវរក្សាទុកក្នុង `dataset/001_Narith.jpg`

---

### វិធី 2: ចុះឈ្មោះពីរូបភាពដែលមានស្រាប់ (Register from Existing Images)

**ជំហានទី 1: រៀបចំរូបភាព**

ដាក់រូបភាពក្នុងថត `dataset` ជាមួយទម្រង់ឈ្មោះ:
```
dataset/
├── 001_Narith.jpg
├── 002_Dara.jpg
├── 003_Sokha.jpg
├── 004_Chanthy.jpg
└── 005_Bopha.jpg
```

**ជំហានទី 2: រត់ស្គ្រីប (Run Script)**

**ពាក្យបញ្ជា:**
```powershell
.\venv\Scripts\python.exe register_from_dataset.py
```

**ឬចុចលើឯកសារ (Or double-click):**
```
run_register_from_dataset.bat
```

**លទ្ធផល (Output):**
```
📂 REGISTER FROM DATASET
Found 5 image(s)

📷 Processing: 001_Narith.jpg -> Narith...
   ✓ Registered: Narith (ID: 1)

📷 Processing: 002_Dara.jpg -> Dara...
   ✓ Registered: Dara (ID: 2)

...

📊 REGISTRATION SUMMARY
✓ Successfully registered: 5
```

---

## 🎯 ដំណើរការពេញលេញ (Complete Workflow)

### 1. រៀបចំរូបភាព (Prepare Images)

ចម្លងរូបភាពទៅក្នុងថត `dataset` ហើយដាក់ឈ្មោះតាមទម្រង់:
```
001_ឈ្មោះ.jpg
002_ឈ្មោះ.jpg
003_ឈ្មោះ.jpg
```

**គន្លឹះសំខាន់ៗ (Important Tips):**
- ប្រើរូបភាពមុខច្បាស់ (Use clear face images)
- មានពន្លឺល្អ (Good lighting)
- មុខត្រង់ទៅកាន់កាមេរ៉ា (Face forward to camera)
- ទំហំរូបភាព: អប្បបរមា 200x200 pixels (Minimum image size: 200x200 pixels)

---

### 2. ចុះឈ្មោះ (Register)

**ពីរូបភាព (From images):**
```powershell
.\venv\Scripts\python.exe register_from_dataset.py
```

**ឬពីកាមេរ៉ា (Or from camera):**
```powershell
.\venv\Scripts\python.exe register_face.py
```

---

### 3. មើលមនុស្សដែលបានចុះឈ្មោះ (View Registered People)

```powershell
.\venv\Scripts\python.exe main.py --show-database
```

**លទ្ធផល (Output):**
```
📋 REGISTERED PERSONS DATABASE
ID     Name         Registered            Last Seen
1      Narith       2026-09-27 21:00:00   Never
2      Dara         2026-09-27 21:00:00   Never
3      Sokha        2026-09-27 21:00:00   Never
Total: 3 person(s)
```

---

### 4. ដំណើរការស្គាល់មុខ (Run Face Recognition)

```powershell
.\venv\Scripts\python.exe main.py
```

**លទ្ធផល (What happens):**
- កាមេរ៉ាបើក (Camera opens)
- មុខដែលស្គាល់ត្រូវបានបង្ហាញជាមួយឈ្មោះនិង ID (Known faces show with name and ID)
  - **ID:1 Narith** (ប្រអប់ពណ៌បៃតង / Green box)
  - **ID:2 Dara** (ប្រអប់ពណ៌បៃតង / Green box)
- មុខមិនស្គាល់បង្ហាញជា "Unknown" (Unknown faces show as "Unknown")
  - **Unknown** (ប្រអប់ពណ៌ក្រហម / Red box)

**ការគ្រប់គ្រងដោយក្តារចុច (Keyboard Controls):**
- **Q** = បិទកម្មវិធី (Quit)
- **R** = ផ្ទុកមូលដ្ឋានទិន្នន័យឡើងវិញ (Reload database)
- **S** = រក្សាទុករូបភាព (Save screenshot)
- **D** = បើក/បិទរបៀប Debug (Toggle debug mode)

---

## 📋 ពាក្យបញ្ជាទាំងអស់ (All Commands)

### ការចុះឈ្មោះ (Registration)

```powershell
# ចុះឈ្មោះតាមរយៈកាមេរ៉ា (Register via camera)
.\venv\Scripts\python.exe register_face.py

# ចុះឈ្មោះពី dataset (Register from dataset)
.\venv\Scripts\python.exe register_from_dataset.py

# ចុះឈ្មោះពីរូបភាពជាក់លាក់ (Register from specific image)
.\venv\Scripts\python.exe register_face.py --name "Narith" --image photo.jpg
```

### ការស្គាល់មុខ (Face Recognition)

```powershell
# ដំណើរការស្គាល់មុខ (Run recognition)
.\venv\Scripts\python.exe main.py

# ស្ទង់កាមេរ៉ា (Test camera)
.\venv\Scripts\python.exe main.py --test-camera

# ស្គាល់មុខសាមញ្ញ (Simple detection)
.\venv\Scripts\python.exe simple_face_detection.py
```

### មូលដ្ឋានទិន្នន័យ (Database)

```powershell
# មើលមនុស្សទាំងអស់ (View all people)
.\venv\Scripts\python.exe main.py --show-database

# មើលស្ថិតិ (View statistics)
.\venv\Scripts\python.exe main.py --stats

# មើលព័ត៌មានលម្អិត (View detailed info)
.\venv\Scripts\python.exe manage_database.py --view 1

# ស្វែងរកតាមឈ្មោះ (Search by name)
.\venv\Scripts\python.exe manage_database.py --search "Narith"

# លុបមនុស្ស (Delete person)
.\venv\Scripts\python.exe manage_database.py --delete 1

# បម្រុងទុកមូលដ្ឋានទិន្នន័យ (Backup database)
.\venv\Scripts\python.exe manage_database.py --backup
```

---

## 📁 ឯកសារ Batch សម្រាប់ចុចលើ (Batch Files to Double-Click)

1. **`run_simple_detection.bat`** - ស្គាល់មុខសាមញ្ញ (Simple detection)
2. **`run_register.bat`** - ចុះឈ្មោះតាមកាមេរ៉ា (Register via camera)
3. **`run_register_from_dataset.bat`** - ចុះឈ្មោះពី dataset (Register from dataset)
4. **`run_recognition.bat`** - ដំណើរការស្គាល់មុខ (Run recognition)

---

## 🎨 ឧទាហរណ៍ប្រើប្រាស់ (Usage Examples)

### ឧទាហរណ៍ទី 1: ប្រព័ន្ធចូលរួម (Attendance System)

```powershell
# 1. រៀបចំរូបភាពសិស្ស (Prepare student images)
#    dataset/001_Narith.jpg
#    dataset/002_Dara.jpg
#    dataset/003_Sokha.jpg

# 2. ចុះឈ្មោះសិស្ស (Register students)
.\venv\Scripts\python.exe register_from_dataset.py

# 3. ដំណើរការស្គាល់មុខ (Run recognition)
.\venv\Scripts\python.exe main.py

# សិស្សដែលមកដល់នឹងត្រូវបានកត់ត្រាដោយស្វ័យប្រវត្តិ
# Students who arrive will be logged automatically
```

### ឧទាហរណ៍ទី 2: ប្រព័ន្ធសន្តិសុខ (Security System)

```powershell
# 1. ចុះឈ្មោះបុគ្គលិក (Register staff)
.\venv\Scripts\python.exe register_from_dataset.py

# 2. ដំណើរការស្គាល់មុខ (Run recognition)
.\venv\Scripts\python.exe main.py

# មុខដែលមិនស្គាល់នឹងបង្ហាញជា "Unknown" ជាពណ៌ក្រហម
# Unknown faces will show as "Unknown" in red
```

---

## ⚙️ ការកំណត់រចនាសម្ព័ន្ធ (Configuration)

កែឯកសារ `config/config.json`:

### ប្តូរកាមេរ៉ា (Change Camera)
```json
{
  "camera": {
    "source": 0    // សាកល្បង 0, 1, ឬ 2 (Try 0, 1, or 2)
  }
}
```

### កែសម្រួលភាពច្បាស់លាស់នៃការស្គាល់ (Adjust Recognition Accuracy)
```json
{
  "recognition": {
    "tolerance": 0.6   // តិចជាង = តឹងរឹង (Lower = stricter)
                       // 0.4-0.5: តឹងរឹង (Strict)
                       // 0.6-0.7: រលុង (Lenient)
  }
}
```

---

## 💡 គន្លឹះសំខាន់ៗ (Important Tips)

### ពេលថតរូប/ចុះឈ្មោះ (During Registration):
1. ✅ ពន្លឺល្អ (Good lighting)
2. ✅ មុខត្រង់ (Face forward)
3. ✅ រក្សាមុខនៅកណ្តាល (Keep face centered)
4. ✅ គម្លាត 2-3 ហ្វីត (Distance: 2-3 feet)
5. ✅ កុំពាក់វ៉ែនតា/ម៉ាស (No glasses/mask)

### ទម្រង់រូបភាពល្អ (Good Image Quality):
- ទំហំអប្បបរមា: 200x200 pixels (Minimum size: 200x200 pixels)
- ទម្រង់: JPG, JPEG, PNG (Format: JPG, JPEG, PNG)
- មុខច្បាស់ (Clear face)
- ពន្លឺល្អ (Good lighting)
- មិនមានវត្ថុបិទបាំងមុខ (No objects blocking face)

---

## 🔧 ការដោះស្រាយបញ្ហា (Troubleshooting)

### បញ្ហា: "No face detected"
**ដំណោះស្រាយ:**
- ពន្លឺកាន់តែល្អ (Better lighting)
- មុខត្រង់ទៅកាមេរ៉ា (Face camera directly)
- ចេញចូលថ្វាយ (Move closer)
- ប្រើរូបភាពច្បាស់ជាង (Use clearer image)

### បញ្ហា: "Multiple faces detected"
**ដំណោះស្រាយ:**
- ប្រើរូបភាពមានតែមនុស្សម្នាក់គត់ (Use image with only one person)
- ច្រឹបរូបភាពឱ្យនៅសល់តែមុខ (Crop image to show only face)

### បញ្ហា: កាមេរ៉ាមិនបើក (Camera won't open)
**ដំណោះស្រាយ:**
- បិទកម្មវិធីផ្សេងដែលប្រើកាមេរ៉ា (Close other camera apps)
- សាកល្បងកាមេរ៉ាផ្សេង (Try different camera):
  ```json
  "source": 1  // ក្នុង config.json
  ```

---

## 📊 ទិន្នន័យដែលរក្សាទុក (Stored Data)

### មូលដ្ឋានទិន្នន័យ (Database)
**ទីតាំង:** `data/database/faces.db`
- ID របស់មនុស្ស (Person ID: 1, 2, 3, ...)
- ឈ្មោះ (Name)
- ថ្ងៃចុះឈ្មោះ (Registration date)
- ថ្ងៃឃើញចុងក្រោយ (Last seen)
- ទិន្នន័យស្គាល់មុខ (Face encodings)

### រូបភាព (Images)
- **Dataset:** `dataset/001_Name.jpg, 002_Name.jpg, ...`
- **Registered faces:** `data/registered_faces/[Name]/sample_1.jpg, ...`
- **Screenshots:** `data/screenshots/` (ពេលចុច S / When press S)

---

## 🎓 ឧទាហរណ៍លំអិត (Detailed Example)

```powershell
# ជំហានទី 1: រៀបចំរូបភាព (Step 1: Prepare images)
# ចម្លងរូបភាពទៅ dataset/
# Copy images to dataset/
#   dataset/001_Narith.jpg
#   dataset/002_Dara.jpg
#   dataset/003_Sokha.jpg

# ជំហានទី 2: ចុះឈ្មោះ (Step 2: Register)
.\venv\Scripts\python.exe register_from_dataset.py
# Output:
# ✓ Registered: Narith (ID: 1)
# ✓ Registered: Dara (ID: 2)
# ✓ Registered: Sokha (ID: 3)

# ជំហានទី 3: មើលមូលដ្ឋានទិន្នន័យ (Step 3: View database)
.\venv\Scripts\python.exe main.py --show-database
# Output:
# ID  Name    Registered
# 1   Narith  2026-09-27 21:00:00
# 2   Dara    2026-09-27 21:00:00
# 3   Sokha   2026-09-27 21:00:00

# ជំហានទី 4: ដំណើរការស្គាល់មុខ (Step 4: Run recognition)
.\venv\Scripts\python.exe main.py
# មុខរបស់ Narith នឹងបង្ហាញ: "ID:1 Narith"
# មុខរបស់ Dara នឹងបង្ហាញ: "ID:2 Dara"
# មុខរបស់ Sokha នឹងបង្ហាញ: "ID:3 Sokha"
# ចុច Q ដើម្បីបិទ (Press Q to quit)
```

---

## ✅ បញ្ជីពិនិត្យ (Checklist)

- [ ] បានរៀបចំរូបភាពក្នុង dataset (Images prepared in dataset)
- [ ] ឈ្មោះឯកសារត្រឹមត្រូវ (Correct filename format: 001_Name.jpg)
- [ ] រូបភាពមានគុណភាពល្អ (Good image quality)
- [ ] បានដំឡើងកម្មវិធីរួចរាល់ (Software installed)
- [ ] កាមេរ៉ាដំណើរការ (Camera working)
- [ ] បានចុះឈ្មោះមនុស្ស (People registered)
- [ ] ការស្គាល់មុខដំណើរការ (Recognition working)

---

**ប្រព័ន្ធរបស់អ្នករួចរាល់ហើយ! (Your system is ready!)**

សូមសាកល្បងប្រើ! (Please try it!) 🚀👤📷
