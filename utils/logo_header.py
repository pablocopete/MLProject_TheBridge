 
import base64
from pathlib import Path

def logo_header():
    # Function to get base64 encoded image
    @st.cache_data # Cache the image data to avoid re-reading on every rerun
    def get_base64_image(img_path):
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Get the base64 string for your logo
    logo_base64 = get_base64_image(image_path)

    # Construct the data URL
    # Replace 'png' with 'jpeg' or 'gif' if your image is a different type
    data_url = f"data:image/png;base64,{logo_base64}"

    custom_header_html = f"""
    <style>
        .header-container {{
            display: flex;
            align-items: center;
            background-color: black;
            padding: 10px 20px;
            color: white; /* Default text color for the header */
            margin-bottom: 20px; /* Add some space below the header */
        }}
        .header-logo {{
            height: 60px; /* Adjust as needed */
            margin-right: 20px;
        }}
        .header-title {{
            font-size: 2.5em; /* Adjust font size as needed */
            font-weight: bold;
            display: flex;
            gap: 5px; /* Space between words */
        }}
        .header-title .electro {{
            color: white; /* "ELECTRO" in white */
        }}
        .header-title .verse {{
            color: #00A6D6; /* "VERSE" in the blue/cyan color */
        }}
    </style>
    <div class="header-container">
        <img src="{data_url}" class="header-logo">
        <div class="header-title">
            <span class="electro">ELECTRO</span><span class="verse">VERSE</span>
        </div>
    </div>
    """