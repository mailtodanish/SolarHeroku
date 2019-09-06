import os

# Set environment variables
os.environ['DarkSky'] = '**********************'
os.environ['OpenCage'] = '***********************'

# Retrieve set environment variables
DarkSkyKey = os.environ.get('DarkSky') # USER is now set to 'user@example.com'
OpenCageKey = os.environ.get('OpenCage') # PASSWORD is now set to 'aeb72hasow82ajl'
