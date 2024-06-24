1. *Set Up the Project Structure*
2. *Develop the Backend Logic*
3. *Implement the Frontend Interface*
4. *Integrate Frontend and Backend*
5. *Testing and Deployment*

### Step 1: Set Up the Project Structure

#We'll use a Python Flask backend with a React.js frontend. Create a folder structure as follows:


'''hospitality-app/
|-- backend/
|   |-- app.py
|   |-- allocation.py
|   |-- requirements.txt
|-- frontend/
|   |-- public/
|   |-- src/
|   |-- package.json
|-- README.md'''


### Step 2: Develop the Backend Logic

#### backend/app.py
'''python'''
from flask import Flask, request, jsonify
import pandas as pd
from allocation import allocate_rooms

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_files():
    group_file = request.files['groupFile']
    hostel_file = request.files['hostelFile']

    group_df = pd.read_csv(group_file)
    hostel_df = pd.read_csv(hostel_file)

    allocation_result = allocate_rooms(group_df, hostel_df)

    return jsonify(allocation_result)

if __name__ == '__main__':
    app.run(debug=True)


#### backend/allocation.py
'''python''''
import pandas as pd

def allocate_rooms(groups, hostels):
    allocations = []
    group_by_gender = {'Boys': [], 'Girls': []}
    
    # Separate groups by gender
    for _, row in groups.iterrows():
        if row['Gender'] in group_by_gender:
            group_by_gender[row['Gender']].append(row)
        else:
            boys = row['Members'] // 2
            girls = row['Members'] - boys
            group_by_gender['Boys'].append({'Group ID': row['Group ID'], 'Members': boys, 'Gender': 'Boys'})
            group_by_gender['Girls'].append({'Group ID': row['Group ID'], 'Members': girls, 'Gender': 'Girls'})
    
    for gender, group_list in group_by_gender.items():
        hostels_for_gender = hostels[hostels['Gender'] == gender]
        room_idx = 0
        
        for group in group_list:
            members_left = group['Members']
            while members_left > 0 and room_idx < len(hostels_for_gender):
                hostel = hostels_for_gender.iloc[room_idx]
                capacity = hostel['Capacity']
                if capacity >= members_left:
                    allocations.append({
                        'Group ID': group['Group ID'],
                        'Hostel Name': hostel['Hostel Name'],
                        'Room Number': hostel['Room Number'],
                        'Members Allocated': members_left
                    })
                    hostels_for_gender.at[room_idx, 'Capacity'] -= members_left
                    members_left = 0
                else:
                    allocations.append({
                        'Group ID': group['Group ID'],
                        'Hostel Name': hostel['Hostel Name'],
                        'Room Number': hostel['Room Number'],
                        'Members Allocated': capacity
                    })
                    members_left -= capacity
                    room_idx += 1
                    
    return allocations


### Step 3: Implement the Frontend Interface

#### frontend/src/App.js
jsx
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [groupFile, setGroupFile] = useState(null);
  const [hostelFile, setHostelFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileUpload = (e, setFile) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('groupFile', groupFile);
    formData.append('hostelFile', hostelFile);

    try {
      const response = await axios.post('/upload', formData);
      setResult(response.data);
    } catch (error) {
      console.error("There was an error uploading the files!", error);
    }
  };

  return (
    <div>
      <h1>Group Accommodation Allocation</h1>
      <input type="file" onChange={(e) => handleFileUpload(e, setGroupFile)} />
      <input type="file" onChange={(e) => handleFileUpload(e, setHostelFile)} />
      <button onClick={handleSubmit}>Upload and Allocate</button>
      
      {result && (
        <div>
          <h2>Allocation Result</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;


### Step 4: Integrate Frontend and Backend

In the frontend/package.json, add the proxy to the backend server:
json
"proxy": "http://localhost:5000"


### Step 5: Testing and Deployment

1. *Run the Backend:*
   bash
   cd backend
   pip install -r requirements.txt
   flask run
   

2. *Run the Frontend:*
   bash
   cd frontend
   npm install
   npm start
   

### Documentation

- *Backend:* A Flask app that handles file uploads, processes the data, and performs room allocation.
- *Frontend:* A React app that allows users to upload CSV files and displays the allocation results.
- *How to Run:*
  - Start the backend server.
  - Start the frontend server.
  - Use the web interface to upload the CSV files and view the allocation results.

This setup ensures that group accommodations are efficiently allocated according to the specified requirements.