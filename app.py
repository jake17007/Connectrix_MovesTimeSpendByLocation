from __future__ import division
from datetime import datetime
import matplotlib.pyplot as plt
import mpld3
import sys
import json

# Receive the data passed from runApp.js
data = json.load(sys.stdin)

#with open('./data.json') as data_file:
#    data = json.load(data_file)
movesData = data[0]['moves']

# Do some calculation

places = []
for dayData in movesData[0]['storyLine']:
    segments = dayData['segments']
    for segment in segments:
        if (segment['type'] == 'place'):

            # Get the place id, name, type, and location (lat, lon)
            place = segment['place']

            # Get the duration at that location and add it to place
            endTime = datetime.strptime(segment['endTime'], '%Y%m%dT%H%M%S%z')
            startTime = datetime.strptime(segment['startTime'], '%Y%m%dT%H%M%S%z')
            duration = ((endTime - startTime).total_seconds() / 60 )/ 60
            place['duration'] = duration

            places.append(place)

distinctPlaces = []
for place in places:
    if 'name' in place and ({'name': place['name'], 'location': place['location']} in distinctPlaces) == False:
        distinctPlaces.append({'name': place['name'], 'location': place['location']})
    if ('name' in place) == False and ({'name': 'unknown', 'location': place['location']} in distinctPlaces) == False:
        distinctPlaces.append({'name': 'unknown', 'location': place['location']})

for distinctPlace in distinctPlaces:
    for place in places:
        if distinctPlace['location'] == place['location'] and 'totalTime' in distinctPlace:
            distinctPlace['totalTime'] += place['duration']
        elif distinctPlace['location']  == place['location']:
            distinctPlace['totalTime'] = place['duration']

# Put the data into a dictionary and sort it by total time
histData = []
for distinctPlace in distinctPlaces:
    if distinctPlace['name'] == 'unknown':
        histData.append({'name': str(distinctPlace['location']['lat']) + ', ' +
                                 str(distinctPlace['location']['lon']),
                         'totalTime': distinctPlace['totalTime']})
    else:
        histData.append({'name': distinctPlace['name'],
                         'totalTime': distinctPlace['totalTime']})

histData_sorted = sorted(histData, reverse=True, key=lambda k: k['totalTime'])

# Put the data into arrays for the bar chart
labels = []
values = []
for place in histData_sorted:
    labels.append(place['name'])
    values.append(place['totalTime'])

# Plot the data

fig, ax = plt.subplots(figsize=(12, 6))
y = range(len(values))
ax.barh(y, values, align='center')
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_xlabel('Total Time (hours)')
ax.set_ylabel('Place')
ax.set_title('Time Spent By Location Over the Last Month')
plt.tight_layout()

# Convert to the plot HTML
plot_html = mpld3.fig_to_html(fig)

html = '<div class="container"><div class="text-center">' # Add some bootsrap
html += plot_html
html += 'Zoom in by clicking the magnifying glass icon and selecting an area.</br>Click the home icon to reset.</div>' # Add some instructions

# Send back data
print(json.dumps({'html': html}))
