# LocalFeathers
A simple RTSP 24/7 local recording implementation, designed with Green Feathers Bird Box Cameras in mind.

By default, the Green Feathers application and Cloud service will only record event data to your device. This is useful for capturing motion events, but isn't suitable for long timelapses of the nesting process.

This simple python script connects directly to the RTSP stream to save a 30 day rolling reel of footage in 15 minute segments (all adjustable). If the camera loses connection at any point, the script logs this and gracefully handles the downtime, trying again every 10 minutes until the connection is restored.

Typical file storage requirements are approx 450GB for a month of footage. Naturally, changing the video retention period will alter the storage consumption.

Run as a cron job or scheduled task to ensure full-time recording. For Windows, adding a scheduled task configured to 'run whether the user is logged in or not' will prevent a terminal window being spawned by the process.

### Requirements
pip3 install opencv-python

Before running, update the script with your camera IP address. Ensure that the camera is bound to a specific IP on your LAN. For help finding your camera IP address, open the camera settings in the Green Feathers app and click 'Onvif'.
