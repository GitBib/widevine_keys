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

    # Find all the AdaptationSet elements
    for aset in root.iter('{urn:mpeg:dash:schema:mpd:2011}AdaptationSet'):
        # Find all the cenc:pssh elements that are inside a ContentProtection element
        # without a value attribute equal to "MSPR 2.0"
        for cp in aset.iter('{urn:mpeg:dash:schema:mpd:2011}ContentProtection'):
            if cp.attrib.get('value') != 'MSPR 2.0':
                for pssh in cp.iter('{urn:mpeg:cenc:2013}pssh'):
                    pssh_data = pssh.text
                    # Get the id, contentType, and lang attributes of the AdaptationSet
                    aset_id = aset.attrib.get('id')
                    aset_contentType = aset.attrib.get('contentType')
                    aset_lang = aset.attrib.get('lang')
                    # Append the pssh data and the attributes to the list
                    pssh_data_list.append((pssh_data, aset_id, aset_contentType, aset_lang))

    return pssh_data_list
