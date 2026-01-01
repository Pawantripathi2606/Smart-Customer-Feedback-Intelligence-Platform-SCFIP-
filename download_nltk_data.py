"""
Download all required NLTK data for the project
Run this script once before starting the application
"""
import nltk
import sys

print("=" * 60)
print("Downloading NLTK Data")
print("=" * 60)
print()

# List of required NLTK data packages
required_packages = [
    'punkt',
    'punkt_tab',
    'stopwords',
    'wordnet',
    'omw-1',
    'averaged_perceptron_tagger'
]

success_count = 0
failed_packages = []

for package in required_packages:
    try:
        print(f"Downloading {package}...", end=" ")
        nltk.download(package, quiet=False)
        print("✓ Done")
        success_count += 1
    except Exception as e:
        print(f"✗ Failed: {e}")
        failed_packages.append(package)

print()
print("=" * 60)
print(f"Downloaded {success_count}/{len(required_packages)} packages successfully")
print("=" * 60)

if failed_packages:
    print(f"\n⚠ Failed packages: {', '.join(failed_packages)}")
    print("You may need to download these manually.")
    sys.exit(1)
else:
    print("\n✓ All NLTK data downloaded successfully!")
    print("You can now run the application.")
    sys.exit(0)
