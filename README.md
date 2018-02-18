#OrderFiles
## Motivation
This project started to order and classify a lot of different types of backups.  
The way you save backup may change a long the time.  
As an example a ten year old kid may select everything on C:/ and drop all files into a zip file stored on an external drive :-). As the kid grow start taking raw images of disks having different internal structures.  

## Purpose
The project aims to solve this problem and classify all these files contained in several types of structures by mime-type and metadata while having an unique index.  

## Supported file types and containers
Partition tables: msdos and gpt. I've just tested msdos parition tables but gpt should work too since the mapping is done by the OS.  
LVMs: Tested  
RAIDs: Not supported by design, It does not look for all the volumes to re-assemble the raid.  
Filesystems: ext[2,3,4], FAT variants, NTFS  
Compressed: tar, gzip, rar, zip, 7z  
Directories ^^  
File types: all suppoted by libmagic. Type ``` file -l ```   

## UseCases
Obviously: to order backups.  
I've used it to index and order all files on some forensic investigations.  
I plan to hook block device discovery with pyudev and to set it up to index and order files upon usb plug in.  

## Howto 
Just edit config.py.  
You can also edit constants.py if you want to add another pattern for detecting sourcecode directories.  
```
pip3 install -r requirements.txt  
python3 main.py <list of files/containers>  
```
Logs to organizer.log  

## Example
Consider that input:  
```
A folder called /test and config pointing to workfolder at /tmp  
1.xlsx -- An ms excel file  
922.pdf -- A pdf   
brcmfmac4366c-pcie.7z -- A 7z compressed archive  
IMG_2014.JPG -- A photo with metadata 
Screenshot from 2018-02-09 12-03-30.png  
Screenshot from 2018-02-10 12-05-07.png  
sp70703.tgz  

python main.py /test  

```

The output is:
```
It will create an index of unique files like that:  
/tmp/index/00/0d/00dfe2232012beba8200e0f015c00f6890d2f525  
...
Files will be classified like:  
   · Names contains the <hash>_<filename>.  
   · All of the following are symlinks to the index.  
   · It will create albums with photos of the same day (extracted from exif data).  
   · Also will group all photos taken with the same camera.   
   · It will try to do the same thing with movies and music files.  
  
/tmp/text/plain/c6144e4ebe5dcc670daedab5049b62c720902a32_README.TXT  
/tmp/text/plain/2b27786cadfb26a9b376c4a3178d2dd2559215d5_DOSFlash.txt  
/tmp/text/html/00dfe2232012beba8200e0f015c00f6890d2f525_History.htm  
/tmp/text/html/2545da21527572eb648f6a7c1f6b6541b928da55_BIOS Flash.htm  
/tmp/application/octet-stream/88797ecdbb9cdcad3c420d0bff9c0e7ea0611ce4_J51_0152.BIN  
/tmp/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet/4945689bbe4a2f379dadcd602a020beb6cbdac09_1.xlsx  
/tmp/application/pdf/9594952f8a59a789aa2edb71b63015698164f17d_922.pdf  
/tmp/application/x-dosexec/f9313264b93a8ba1d4b3ea6ce2c18d0dbb025489_DOSFlash.exe  
/tmp/application/x-dosexec/31585e8e30e90c398f137fcd6124d6da1a308826_flshuefi.cpu  
/tmp/application/x-7z-compressed/49bac65d3f086d205e2b987bbcf159c667075eba_brcmfmac4366c-pcie.7z  
/tmp/image/gif/Icons/sinkDateNotfound/49de6d630a234be2847a3b3233f0060609d988ab_HP_Logo.gif  
/tmp/image/jpeg/camera_Canon EOS 1300D/17_05_21/e9ff0358134d0ffaa44232de4671af2628df12a6_IMG_2014.JPG   
/tmp/image/png/sinkDateNotfound/546284e5bed076afd906d7a583601ee3e232b3be_Screenshot from 2018-02-10 12-05-07.png  
/tmp/image/png/sinkDateNotfound/cee6658a6a77bd190da4377d5d05361cca1ef82a_Screenshot from 2018-02-09 12-03-30.png  
  
```