# 📚 Git Quick Guide for Your Project

## ✅ Your Repository Status

**✓ Repository:** https://github.com/narithby225-ai/Face-Recognition-Camera-System  
**✓ Status:** Up to date with GitHub  
**✓ Branch:** main  
**✓ Latest commit:** Merge remote README, keeping comprehensive local version

---

## 🚀 Common Git Commands

### 📋 Check Status
```powershell
# See what files changed
git status

# See commit history
git log --oneline -n 5
```

### 💾 Save Changes to GitHub

```powershell
# Step 1: Stage all changes
git add .

# Step 2: Commit with message
git commit -m "Add new feature" 

# Step 3: Push to GitHub
git push origin main
```

**Example workflow:**
```powershell
# After editing files...
git status                                  # See what changed
git add .                                   # Stage all changes
git commit -m "Updated mobile app UI"      # Commit with message
git push origin main                        # Push to GitHub
```

### 🔄 Get Latest Changes from GitHub

```powershell
# Pull latest code
git pull origin main
```

### 📝 Specific File Operations

```powershell
# Stage specific files only
git add file1.py file2.py

# Unstage a file
git restore --staged filename.py

# Discard changes to a file
git restore filename.py
```

---

## 📊 Useful Commands

### View Changes
```powershell
# See what changed in files
git diff

# See changes for specific file
git diff filename.py

# See staged changes
git diff --staged
```

### Branch Management
```powershell
# See all branches
git branch -a

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

### History
```powershell
# Detailed history
git log

# Compact history
git log --oneline

# Show last 10 commits
git log --oneline -n 10

# See who changed what
git blame filename.py
```

---

## 🎯 Common Workflows

### Scenario 1: Fixed a Bug
```powershell
# Edit files to fix bug
# ...

git add .
git commit -m "Fix camera initialization bug"
git push origin main
```

### Scenario 2: Added New Feature
```powershell
# Create new files, edit existing ones
# ...

git add .
git commit -m "Add attendance export feature"
git push origin main
```

### Scenario 3: Updated Documentation
```powershell
# Edit README.md or guides
# ...

git add README.md
git commit -m "Update installation instructions"
git push origin main
```

### Scenario 4: Added New Students
```powershell
# Add photos to dataset/
# Update students_list.csv
# ...

git add dataset/ students_list.csv
git commit -m "Add 5 new students"
git push origin main
```

---

## ⚠️ Important Notes

### DO NOT Commit These:
- ✗ Virtual environment (`venv/`)
- ✗ Database files (`*.db`, `*.sqlite`)
- ✗ Cache files (`__pycache__/`, `*.pyc`)
- ✗ Environment variables (`.env`)
- ✗ Large compiled files (`*.pkl` encodings)

**These are already in `.gitignore`** ✓

### Good Commit Messages:
✅ "Add mobile app welcome screen"  
✅ "Fix camera not starting on Windows"  
✅ "Update README with installation guide"  
✅ "Add support for 43 students"  

### Bad Commit Messages:
❌ "Update"  
❌ "Fix"  
❌ "Changes"  
❌ "asdf"  

---

## 🔧 Fix Common Issues

### "Your branch is behind origin/main"
```powershell
git pull origin main
```

### "Merge conflict"
```powershell
# Edit conflicted files manually
# Look for <<<<<<< markers
# Choose which code to keep
# Then:
git add .
git commit -m "Resolve merge conflict"
git push origin main
```

### "Already up to date" when pushing
```powershell
# Nothing to worry about! 
# This means GitHub already has your latest code
```

### Accidentally committed wrong files
```powershell
# Undo last commit but keep changes
git reset --soft HEAD~1

# Remove files from staging
git restore --staged unwanted-file.txt

# Commit again correctly
git add correct-files.py
git commit -m "Correct commit"
```

---

## 📱 For Your Face Recognition Project

### Adding New Students:
```powershell
# 1. Add photos to dataset/
# 2. Update students_list.csv
# 3. Commit changes

git add dataset/ students_list.csv
git commit -m "Add 3 new students: Names here"
git push origin main
```

### Updating Mobile App:
```powershell
# After editing mobile_app files

git add mobile_app/
git commit -m "Improve mobile UI and add settings"
git push origin main
```

### Backend API Changes:
```powershell
# After updating backend/

git add backend/
git commit -m "Add new endpoint for attendance export"
git push origin main
```

### Documentation Updates:
```powershell
git add *.md
git commit -m "Update documentation with new features"
git push origin main
```

---

## 🎓 Quick Reference Card

```
Status Check:        git status
Save Changes:        git add . && git commit -m "message" && git push
Get Updates:         git pull origin main
View History:        git log --oneline
See Changes:         git diff
Undo Changes:        git restore filename
```

---

## 🌐 Your Repository Info

**GitHub URL:**  
https://github.com/narithby225-ai/Face-Recognition-Camera-System

**Clone Command (for others):**
```bash
git clone https://github.com/narithby225-ai/Face-Recognition-Camera-System.git
```

**Your Local Path:**
```
D:\Lessons_and_Codes\SPDI-II\Face Recognition Camera System
```

---

## 💡 Pro Tips

1. **Commit Often:** Small, frequent commits are better than large ones
2. **Meaningful Messages:** Write clear commit messages
3. **Pull Before Push:** Always `git pull` before `git push` if working with others
4. **Check Status:** Run `git status` frequently to see what's changed
5. **Test First:** Test your code before committing

---

## 🆘 Need Help?

```powershell
# Git help
git --help

# Help for specific command
git commit --help

# Check Git version
git --version
```

---

## ✅ Daily Workflow

**Morning (if working with team):**
```powershell
git pull origin main
```

**After making changes:**
```powershell
git status                          # Check what changed
git add .                           # Stage all changes
git commit -m "Descriptive message" # Commit
git push origin main                # Push to GitHub
```

**Before leaving:**
```powershell
git status  # Make sure everything is committed
```

---

**Your repository is ready! Happy coding! 🚀**
