import shutil
import random
import os
import glob

#重複執行會有多的檔案!!!!!!!!執行一次就好
#此程式使用png，若為jpg要再修改
#train:valid:test = 7:2:1

#只要設當按位置的資料夾在這，會自動創子資料夾
# dir_path = "C:/Users/milers/Desktop/YOLOs_RGBD_training_data/"
# dir_path = "C:/Users/milers/Desktop/bunch_tomato20220119_134621/bunch_RGBD/"
dir_path = "C:/Users/milers/Desktop/ALLpicture/"
# path_for_txt = "/home/ubuntu/darknet_RGBD/milers/bunch_tomato_RGBD/"  #.txt內前面的路徑
# path_for_txt = "/home/ubuntu/darknet/20221021_NTU_greenhouse_flower/image_data/"  #.txt內前面的路徑
path_for_txt = "/home/ubuntu/darknet/20221129_NTU_greenhouse_melon/ALLpicture/"  #.txt內前面的路徑

#############################################################
if not os.path.isdir(dir_path + "/train"):
    os.mkdir(dir_path + "/train")
if not os.path.isdir(dir_path + "/valid"):
    os.mkdir(dir_path + "/valid")
if not os.path.isdir(dir_path + "/test"):
    os.mkdir(dir_path + "/test")
if not os.path.isdir(dir_path + "/txt_file"):
    os.mkdir(dir_path + "/txt_file")

all_file_list = []
train_list = []
test_list = []

write_all_file = open(dir_path + "/txt_file/all.txt", "w")
write_train_file = open(dir_path + "/txt_file/train.txt", "w")
write_valid_file = open(dir_path + "/txt_file/valid.txt", "w")
write_test_file = open(dir_path + "/txt_file/test.txt", "w")


for f in glob.glob(os.path.join(dir_path + "*.png")): #取得dir_path路徑中，結尾是.png的檔案
	filename = f.split('\\')[-1] #移除"\"之前的東西，只留下檔名
	all_file_list.append(path_for_txt+filename)



#train:valid:test = 7:2:1
print("All_data: ", len(all_file_list))
print("Train_data: ", len(all_file_list)*0.7)
print("Valid_data: ", len(all_file_list)*0.2)
print("Test_data: ", len(all_file_list)*0.1)

#隨機
random.shuffle(all_file_list)

#依照比例分群
train_list = all_file_list[:int(len(all_file_list)*0.7)]
valid_list = all_file_list[int(len(all_file_list)*0.7):int(len(all_file_list)*0.9)]
test_list = all_file_list[int(len(all_file_list)*0.9):]

#看是不是正確分出來
print(len(train_list),len(valid_list),len(test_list))

#list寫進檔案
for line in all_file_list:
	write_all_file.write(line + "\n")
for line in train_list:
	write_train_file.write(line + "\n")
for line in valid_list:
	write_valid_file.write(line + "\n")
for line in test_list:
	write_test_file.write(line + "\n")

write_all_file.close
write_train_file.close
write_valid_file.close
write_test_file.close


#寫複製檔案到train, valid, test
for line in train_list:
	filename = line.split('/')[-1] #移除字串中前面的路徑
	filename = os.path.splitext(filename)[0] #移除字串中的.png
	shutil.copyfile(dir_path + filename + ".png", dir_path + "train/" + filename + ".png")
	shutil.copyfile(dir_path + filename + ".txt", dir_path + "train/" + filename + ".txt")
for line in valid_list:
	filename = line.split('/')[-1] #移除字串中前面的路徑
	filename = os.path.splitext(filename)[0] #移除字串中的.png
	shutil.copyfile(dir_path + filename + ".png", dir_path + "valid/" + filename + ".png")
	shutil.copyfile(dir_path + filename + ".txt", dir_path + "valid/" + filename + ".txt")
for line in test_list:
	filename = line.split('/')[-1] #移除字串中前面的路徑
	filename = os.path.splitext(filename)[0] #移除字串中的.png
	shutil.copyfile(dir_path + filename + ".png", dir_path + "test/" + filename + ".png")
	shutil.copyfile(dir_path + filename + ".txt", dir_path + "test/" + filename + ".txt")
