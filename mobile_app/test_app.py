"""
Test Mobile App Locally (Desktop)
Run this to test the app before building APK
"""

import os
import sys

# Ensure dataset exists
if not os.path.exists('dataset'):
    print("Creating symlink to dataset...")
    dataset_path = os.path.join('..', 'dataset')
    if os.path.exists(dataset_path):
        try:
            os.symlink(dataset_path, 'dataset', target_is_directory=True)
        except:
            # Windows: copy instead
            import shutil
            shutil.copytree(dataset_path, 'dataset', dirs_exist_ok=True)
    else:
        print("Warning: No dataset found!")
        os.makedirs('dataset', exist_ok=True)

# Run the app
from main import FaceRecognitionApp

if __name__ == '__main__':
    FaceRecognitionApp().run()
