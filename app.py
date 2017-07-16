from __future__ import division
import sys, json;

# Receive the data passed from runApp.js
data = json.load(sys.stdin)

# Parse the data for 'user'
fitbitData = data[0]['fitbit']
profileData = fitbitData[0]['profile']
userData = profileData[0]['user']

# Perform calculations on Fitbit data
bodyInfo = {
    'weight': round(userData['weight'] * 2.2, 2),
    'height': round(userData['height'] / 2.54, 2),
    'bmi': round(userData['weight'] / ((userData['height']/100)**2), 2)
}


# Format into html (with bootstrap)
html = '<div class="container">Weight: ' + str(bodyInfo['weight']) + '<br>Height: ' + str(bodyInfo['height']) + '<br>BMI: ' + str(bodyInfo['bmi']) + '</div>'

# Output
print(json.dumps({'html': html}))
