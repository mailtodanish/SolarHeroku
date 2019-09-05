import os

# Set environment variables
os.environ['DarkSky'] = '5636a578a035055f2c69312109749387'
os.environ['OpenCage'] = '7c7eb21a5d4449689e412939a0f9769b'

# Retrieve set environment variables
DarkSkyKey = os.environ.get('DarkSky') # USER is now set to 'user@example.com'
OpenCageKey = os.environ.get('OpenCage') # PASSWORD is now set to 'aeb72hasow82ajl'
