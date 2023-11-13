from bs4 import BeautifulSoup

html = '''
<label for="name">Name:</label>
<input type="text" id="name" name="name" required><br>

<label for="address">Address:</label>
<input type="text" id="address" name="address" required><br>

<label for="phone-number">Phone Number:</label>
<input type="text" id="phone-number" name="phone-number" required><br>

<label for="dob">Date of Birth:</label>
<input type="date" id="dob" name="dob" required><br>

<label for="gender">Gender:</label>
<select id="gender" name="gender">
    <option value="Male">Male</option>
    <option value="Female">Female</option>
    <option value="Other">Other</option>
</select><br>

<label for="father-name">Father's Name:</label>
<input type="text" id="father-name" name="father-name" required><br>

<label for="mother-name">Mother's Name:</label>
<input type="text" id="mother-name" name="mother-name" required><br>


<input type="submit" value="Submit">
'''

def extract_element_info(element):
    info = {
        "element": element.name,
        "tag": element.name if element.name != "none" else "none",
        "type": element.get('type', 'none'),
        "id": element.get('id', 'none'),
        "name": element.get('name', 'none'),
        "text": element.text.strip(),
        "value": element.get('value', 'none'),
        "for": element.get('for', 'none')
    }
    return info

soup = BeautifulSoup(html, 'html.parser')
all_elements = soup.find_all(['label', 'input', 'select', 'option'])

element_info_list = [extract_element_info(element) for element in all_elements]

for element_info in element_info_list:
    print(element_info)

