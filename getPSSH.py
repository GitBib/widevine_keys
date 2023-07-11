import requests
import xml.etree.ElementTree as ET
import base64

def get_pssh(input):
    # Initialize the list of pssh data
    pssh_data_list = []

    # Check if the input is a URL or a file path
    if input.startswith('http://') or input.startswith('https://'):
        # Make a request to the URL
        r = requests.get(url=input)
        r.raise_for_status()
        # Parse the XML data from the response
        root = ET.fromstring(r.text)
    else:
        # Read the file
        with open(input, 'r') as file:
            file_data = file.read()
        # Parse the XML data from the file
        root = ET.fromstring(file_data)

    # Find all the cenc:pssh elements and extract their content
    for elem in root.iter():
        if 'pssh' in elem.tag:
            pssh_data = elem.text
            # If the pssh data is base64 encoded, let's decode it
            try:
                pssh_data = base64.b64decode(pssh_data).decode('utf-8')
            except:
                pass
            pssh_data_list.append(pssh_data)

    return pssh_data_list
