# OpenEphys_SyncVideo

This repository includes a script to sync video/ephys recordings using PyZMQ and OpenCV in Python 3.8. 

*Note. Ideally one would use a TTL pulse to control camera shutter to insure accurate sync. At the moment, this method syncs video and Open Ephys using PyZMQ and thus is suseptible to error. Use of a high quality video camera is necessary to insure frames are not dropped. This is a work in progress.* 
