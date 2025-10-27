# 🎨 Koenig Logo Setup Guide (Mac)

## Quick Setup - Add Your Logo

### Step 1: Locate Your Logo File
Your logo is at:
```
~/Downloads/followup_reminder_app/assets/koenig_logo.png
```

### Step 2: Copy Logo to App Folder

**Option A: Using Finder (Easy)**
1. Open Finder
2. Navigate to `Downloads/followup_reminder_app/assets/`
3. Copy `koenig_logo.png`
4. Navigate to your app folder `followup_reminder_app/`
5. Create folder named `assets` if it doesn't exist
6. Paste `koenig_logo.png` inside the `assets` folder

**Option B: Using Terminal (Quick)**
```bash
# Navigate to your app folder
cd /path/to/followup_reminder_app

# Create assets directory
mkdir -p assets

# Copy logo from Downloads
cp ~/Downloads/followup_reminder_app/assets/koenig_logo.png ./assets/

# Verify it's there
ls -la assets/koenig_logo.png
```

### Step 3: Verify File Structure
Your folder should look like this:
```
followup_reminder_app/
├── app.py
├── requirements.txt
├── assets/
│   └── koenig_logo.png       ← Logo should be here
├── README.md
├── QUICK_START.md
└── ... (other files)
```

### Step 4: Run the App
```bash
cd followup_reminder_app
streamlit run app.py
```

The Koenig logo will now appear:
- ✅ On the login page (top center)
- ✅ In the sidebar (when logged in)

---

## Logo Display Details

### Where Logo Appears:
1. **Login/Register Page**: Top center, above title
2. **Main App Sidebar**: Top of sidebar, above username
3. **Max Width**: 200px (automatically scaled)
4. **Centered**: Logo is center-aligned

### Customizing Logo Display:

If you want to change logo size or position, edit `app.py`:

```python
# Find this function in app.py
def display_logo():
    """Display Koenig logo in the app"""
    logo_base64 = load_logo()
    if logo_base64:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 10px;">
                <img src="data:image/png;base64,{logo_base64}" 
                     alt="Koenig Logo" 
                     style="max-width: 200px; height: auto;">
            </div>
            """,
            unsafe_allow_html=True
        )
```

**Customize:**
- `max-width: 200px` → Change to `300px` for larger logo
- `text-align: center` → Change to `left` or `right` for different alignment
- `padding: 10px` → Adjust spacing around logo

---

## Troubleshooting

### Logo Not Showing?

**Check 1: File exists in correct location**
```bash
cd followup_reminder_app
ls -la assets/koenig_logo.png
```
Should show the file. If not, copy it again.

**Check 2: File name is correct**
- Must be exactly: `koenig_logo.png`
- Case-sensitive on Mac
- Check for spaces or extra characters

**Check 3: File is a valid PNG**
```bash
file assets/koenig_logo.png
```
Should say: `PNG image data`

**Check 4: File permissions**
```bash
chmod 644 assets/koenig_logo.png
```

**Check 5: Restart Streamlit**
- Stop the app (Ctrl+C in terminal)
- Run again: `streamlit run app.py`
- Clear browser cache if needed

### Logo Too Big/Small?

Edit `app.py` and change `max-width: 200px` to your preferred size:
- Small: `150px`
- Medium: `200px` (default)
- Large: `300px`

---

## For Deployment (Streamlit Cloud)

### Important: Include Logo in GitHub

When deploying to Streamlit Cloud:

1. **Upload logo to GitHub**
   ```bash
   cd followup_reminder_app
   git add assets/koenig_logo.png
   git commit -m "Add Koenig logo"
   git push
   ```

2. **Verify folder structure in GitHub**
   - Check that `assets/koenig_logo.png` is visible in your repo
   - Path should be: `assets/koenig_logo.png`

3. **Deploy to Streamlit Cloud**
   - Logo will automatically be included
   - No additional configuration needed

### Using GitHub Web Interface:

1. Go to your repository on GitHub
2. Click "Add file" → "Upload files"
3. Create folder named `assets`
4. Upload `koenig_logo.png` to `assets` folder
5. Commit changes
6. Redeploy on Streamlit Cloud (or it will auto-update)

---

## Alternative: Use Different Logo

If you want to use a different logo:

### Option 1: Replace the file
1. Rename your new logo to: `koenig_logo.png`
2. Copy it to `assets/` folder
3. Restart app

### Option 2: Update code for different filename
Edit `app.py`:
```python
# Change this line:
LOGO_PATH = Path("assets/koenig_logo.png")

# To your logo name:
LOGO_PATH = Path("assets/my_logo.png")
```

---

## Supported Image Formats

The app currently expects PNG format, but you can modify to support other formats:

### To support JPG/JPEG:
```python
# In display_logo() function, change:
<img src="data:image/png;base64,{logo_base64}"

# To:
<img src="data:image/jpeg;base64,{logo_base64}"
```

### To auto-detect format:
```python
import mimetypes

def display_logo():
    if LOGO_PATH.exists():
        mime_type = mimetypes.guess_type(str(LOGO_PATH))[0]
        with open(LOGO_PATH, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <div style="text-align: center; padding: 10px;">
                <img src="data:{mime_type};base64,{logo_base64}" 
                     alt="Logo" style="max-width: 200px;">
            </div>
            """,
            unsafe_allow_html=True
        )
```

---

## Quick Commands Summary (Mac)

```bash
# Navigate to app folder
cd ~/path/to/followup_reminder_app

# Create assets folder
mkdir -p assets

# Copy logo from Downloads
cp ~/Downloads/followup_reminder_app/assets/koenig_logo.png ./assets/

# Verify
ls -la assets/

# Run app
streamlit run app.py
```

---

## Testing Logo Display

After adding the logo:

1. ✅ **Login Page**: Should see logo at top center
2. ✅ **After Login**: Should see logo in sidebar
3. ✅ **Responsive**: Logo should scale on mobile
4. ✅ **All Pages**: Logo stays visible in sidebar

---

## Need Help?

**Logo file issues:**
- Make sure it's a valid PNG file
- Check file size (should be < 5MB for best performance)
- Verify file path is correct

**Display issues:**
- Clear browser cache (Cmd+Shift+R)
- Restart Streamlit app
- Check browser console for errors (Cmd+Option+I)

---

**Your Koenig logo will add professional branding to your app! 🎨**
