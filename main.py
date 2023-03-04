import pyaudio, time

defaultFrames = 16

paObj = pyaudio.PyAudio()



#Select Device
print ("Available devices:\n")
for i in range(0, paObj.get_device_count()):
    info = paObj.get_device_info_by_index(i)
    if info["hostApi"] == 1:
        print (str(info["index"]) + ": \t %s \n \t %s \n" % (info["name"], paObj.get_host_api_info_by_index(info["hostApi"])["name"]))
        print(info)

#Get input or default
device_id = int(input("Choose device []: ") )
print ("")

#defaultOutputDeviceHandle = paObj.get_default_output_device_info()
defaultOutputDeviceHandle = paObj.get_device_info_by_index(device_id)


while True:
    stream = paObj.open(format = pyaudio.paInt16,
                    channels = defaultOutputDeviceHandle["maxInputChannels"] if (defaultOutputDeviceHandle["maxOutputChannels"] < defaultOutputDeviceHandle["maxInputChannels"]) else defaultOutputDeviceHandle["maxOutputChannels"],
                    rate = int(defaultOutputDeviceHandle["defaultSampleRate"]),
                    input = True,
                    frames_per_buffer = defaultFrames,
                    input_device_index = defaultOutputDeviceHandle["index"],
                    as_loopback = True)

    recordedFrames = list(stream.read(defaultFrames))

    stream.stop_stream()
    stream.close()

    joinedFrames = []
    for i in range(0, len(recordedFrames), 2):
        joinedFrames.append(recordedFrames[i] << 8 | recordedFrames[i+1])
    #print(joinedFrames)
    print((max(joinedFrames) - min(joinedFrames)) * 100 / (1 << 16))
    time.sleep(1)