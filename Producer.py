from confluent_kafka import Producer
import base64
import os
import shutil

dirt = '/home/sid/Documents/EP-01-07728_0016/'
#dirtfolder='/home/sid/Documents/'
p=Producer({'bootstrap.servers':'130.127.55.239:9092', 'queue.buffering.max.messages':1000000, 'batch.num.messages':50})

listoffiles=os.listdir(dirt)
number_files=len(listoffiles)
print(number_files)
num=1
number_files_str=str(number_files)


#Writing number of files, the folder name and name of the files into a Text file
f=open("/home/sid/Documents/kafka_files/file_meta.txt","w")
f.close()
f=open("/home/sid/Documents/kafka_files/file_meta.txt","a")
f.write(number_files_str)
f.write("\n")

folder=os.path.basename(os.path.normpath(dirt))
f.write(folder)
f.write("\n")

for files in sorted(listoffiles):
	f.write(files)
	f.write("\n")
f.close()
f1=open("/home/sid/Documents/kafka_files/file_meta.txt", "r")
for data in f1.read():
	p.produce('meta', data.encode('utf-8'))
p.flush()
f=open("/home/sid/Documents/kafka_files/file_meta.txt","r")
f.readline()
f.readline()
while 1:
	i=0
	j=0
	line=f.readline()
	line=line.rstrip()
	topic=line
	if not line:
		break
	fileloc=dirt+line
	image=open(fileloc,'rb')
	size=os.path.getsize(fileloc)
	size10kb=size/10240
	while j<size10kb:
		image.seek(i,0)
		image_read=image.read(10240)
		image_64_encode=base64.encodestring(image_read)
		p.produce(topic, image_64_encode)
		i+=10240
		j+=1
	p.flush()
f.close()


