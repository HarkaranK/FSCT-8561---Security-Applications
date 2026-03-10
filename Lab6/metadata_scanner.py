import exifread #type: ignore
import os
import base64
import re
from datetime import datetime
from PIL import Image #type: ignore

# https://pypi.org/project/ExifRead/

print("\n")

# part 2
def is_bsae64(s):
    if len(s) < 8 or " " in s:
        return False
    
    try:
        if re.match(r'^[A-Za-z0-9+/]+={0,2}$', s):
            base64.b64decode(s, validate=True)
            return True
        
    except Exception:
        return False


def getting_fields(folder_path):

    # Part 1
    # Tags im looking for are set
    required_tags = {
        'GPS GPSLatitude': 'Latitude',
        'GPS GPSLongitude': 'Longitude',
        'EXIF DateTimeOriginal': 'Date Original',
        'EXIF DateTimeDigitized': 'Create Date',
        'Image DateTime': 'Modify Date',
        'Image Make': 'Camera Make',
        'Image Model': 'Camera Model',
        'Image Software': 'Software',
        'EXIF UserComment': 'User Comment',
        'Image ImageDescription': 'Description'
    }

    # Base for table output
    header = f"{'Filename':<20}"
    for label in required_tags.values():
        header += f" | {label:<20}"
    header += f" | {'Risk Score':<10}" # Added for part 5
    print(header)
    print("-" * len(header))

    
    found_secrets = []  # part 2
    timestamp_anomoly = [] # part 3
    traces = [] # part 4
    
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        file_stats = os.stat(full_path)
        fs_created = datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y:%m:%d %H:%M:%S')

        tags = {}
        row = f"{filename:<20}"
        riskScore = 0

        try:
            with open(full_path, "rb") as file_handle:
                tags = exifread.process_file(file_handle)
        except Exception as e:
            print(f"Skipping EXIF for {filename}: {e}") 

        # Part 5 starts here

        # Hidden secret
        if any(k in str(tags).upper() for k in ["VULN", "LATERAL", "SECRET", "STEP"]):
            riskScore += 10

        # GPS leak
        if 'GPS GPSLatitude' in tags or 'GPS GPSLongitude' in tags:
            riskScore += 5

        # Time stamp anomaly
        exif_time = str(tags.get('EXIF DateTimeOriginal', 'N/A'))
        if exif_time != 'N/A':
            try:
                exif_dt = datetime.strptime(exif_time, '%Y:%m:%d %H:%M:%S')
                if exif_dt > datetime.fromtimestamp(file_stats.st_ctime):
                    timestamp_anomoly.append(f"{filename}: EXIF ({exif_time}) newer than FS")
                    riskScore += 5 
            except: pass

        # Compression
        software = str(tags.get('Image Software', ''))
        if any(ed in software.upper() for ed in ["ADOBE", "PHOTOSHOP", "LIGHTROOM"]):
            riskScore += 5


        # Quantization for 4 & 5
            try:
                with Image.open(full_path) as img:
                    if hasattr(img, "quantization") and len(img.quantization) > 2:
                        traces.append(f"{filename}: Double compression detected")
                        riskScore += 5 
            except: pass

            # Iterating over all the files to search for specified tags
        for tag_key in required_tags.keys():
            val = str(tags.get(tag_key, 'N/A'))

            # Part 3
            exif_time = str(tags.get('EXIF DateTimeOriginal', 'N/A'))
            if exif_time != 'N/A':
                try:
                    # Parse strings into datetime objects to compare
                    exif_dt = datetime.strptime(exif_time, '%Y:%m:%d %H:%M:%S')
                    fs_created_dt = datetime.fromtimestamp(file_stats.st_ctime)
                    
                    if exif_dt > fs_created_dt:
                        timestamp_anomoly.append(f"{filename}: EXIF ({exif_time}) is newer than FS Created ({fs_created})")
                except ValueError:
                    pass


                # Part 2 secret words
                if any(keyword in val.upper() for keyword in ["VULN", "LATERAL", "SECRET", "STEP"]):
                    found_secrets.append(f"{filename} ({required_tags[tag_key]}): {val}")

                if is_bsae64(val):
                    try:
                        decoded = base64.b64decode(val).decode('utf-8')
                        found_secrets.append(f"{filename} (Base64 Decoded): {decoded}")
                    except:
                        pass

            row += f" | {val[:20]:<20}"
        print(f"{row} | {riskScore}")
            # print(row)


    print("\nPart 2 Secrets")
    for secret in found_secrets:
            print(secret)

    print("\nStep 3")
    for a in timestamp_anomoly: 
        print(a)

    print("\nPart 4")
    for trace in traces:
        print(f"{trace}")

if __name__ == "__main__":
    getting_fields("./Images/")

