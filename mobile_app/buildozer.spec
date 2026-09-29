[app]

# (str) Title of your application
title = Face Recognition System

# (str) Package name
package.name = facerecognition

# (str) Package domain (needed for android/ios packaging)
package.domain = org.spdi

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.2.1,kivymd==1.1.1,opencv-python,numpy,pillow,face_recognition,dlib,cmake

# (str) Supported orientation (portrait / landscape / all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 23b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to whitelist for the whole project
android.whitelist = lib-dynload/_csv.so

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules (Android API >=31)
# android.backup_rules =

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1

# (str) The format used to package the app for release mode (aab or apk).
# android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aab).
# android.debug_artifact = apk

# -----------------------------------------------------------------------------
# iOS specific
# -----------------------------------------------------------------------------

# (str) Name of the certificate to use for signing the debug version
# ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
# ios.codesign.release = %(ios.codesign.debug)s


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns.
#    Instead of doing:
#
# [app]
# source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    This can be translated into:
#
# [app:source.exclude_patterns]
# license
# data/audio/*.wav
# data/images/original/*
#

# -----------------------------------------------------------------------------
# Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in the name
#    and extend the excluded directories to remove the HD content.
#
# [app@demo]
# title = My Application (demo)
#
# [app:source.exclude_patterns@demo]
# images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
# buildozer --profile demo android debug
