# OpenEphys_SyncVideo

by Laura Berkowitz and [Ryan Harvey](https://github.com/ryanharvey1)

This repository includes a script to sync video/ephys recordings using PyZMQ and OpenCV in Python 3.8. 

![alt text](https://github.com/lolaBerkowitz/OpenEphys_SyncVideo/blob/main/recording_setup.PNG)

*Note. Ideally one would use a TTL pulse to control camera shutter to insure accurate sync. At the moment, this method syncs video and Open Ephys using PyZMQ and thus is suseptible to error. Use of a high quality video camera is necessary to insure frames are not dropped. This is a work in progress.* 
