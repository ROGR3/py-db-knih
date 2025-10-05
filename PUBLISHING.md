# Publishing db-knih-api to PyPI

## Quick Start

Your package is ready to publish! Here's how to do it:

### 1. Update Package Information

Before publishing, update these files with your information:

**setup.py** - Replace these placeholders:
- `"Your Name"` → Your actual name
- `"your.email@example.com"` → Your actual email
- `"https://github.com/yourusername/db-knih-api"` → Your GitHub repository URL

**LICENSE** - Update the copyright line:
- `Copyright (c) 2024 Your Name` → Your actual name

### 2. Create PyPI Account

1. Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Create an account
3. Verify your email

### 3. Build the Package

```bash
# Make sure you're in the project directory
cd /home/rogr/Projects/db-knih/python-db-knih-api

# Activate your virtual environment
source .venv/bin/activate

# Build the package (already done, but you can rebuild if needed)
python3 setup.py sdist bdist_wheel
```

### 4. Upload to PyPI

```bash
# Upload to PyPI (you'll be prompted for username/password)
python3 -m twine upload dist/*
```

### 5. Test Installation

After uploading, test that others can install your package:

```bash
# Create a new virtual environment to test
python3 -m venv test_env
source test_env/bin/activate

# Install your package from PyPI
pip install db-knih-api

# Test it works
python -c "from db_knih_api import db_knih; print('Success!')"
```

## Alternative: Test PyPI First

If you want to test first, upload to Test PyPI:

```bash
# Upload to Test PyPI
python3 -m twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ db-knih-api
```

## Package Structure

Your package includes:
- ✅ **Main package**: `db_knih_api/` with all the scraping logic
- ✅ **Tests**: `tests/` directory with comprehensive test suite
- ✅ **Examples**: `examples/` directory with usage examples
- ✅ **Documentation**: `README.md` with full documentation
- ✅ **License**: MIT License
- ✅ **Dependencies**: All required packages specified

## What Users Get

After installing with `pip install db-knih-api`, users can:

```python
from db_knih_api import db_knih

# Search for books
results = db_knih.search("harry potter")
print(f"Found {len(results)} books")

# Get detailed book information
book_info = db_knih.get_book_info("harry-potter-12345")
print(f"Rating: {book_info.rating}%")
```

## Files Created

The build process creates:
- `dist/db_knih_api-1.0.0-py3-none-any.whl` - Wheel distribution
- `dist/db_knih_api-1.0.0.tar.gz` - Source distribution

Both are ready for upload to PyPI!

## Next Steps

1. Update your personal information in `setup.py` and `LICENSE`
2. Create a GitHub repository (optional but recommended)
3. Upload to PyPI: `python3 -m twine upload dist/*`
4. Share your package with the world! 🚀
