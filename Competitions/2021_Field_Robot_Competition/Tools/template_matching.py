import numpy as np
from matplotlib import pyplot as plt
import cv2


#讀取模板影象
template1=cv2.imread("C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\red_arrow.jpg")
template2=cv2.imread("C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\red_arrow.jpg")


#建立模板列表
template=[template1,template2]

# 模板匹配：歸一化相關係數匹配方法
res1=cv2.matchTemplate(canny, template1, cv2.TM_SQDIFF)
res2=cv2.matchTemplate(canny, template2, cv2.TM_SQDIFF)


#提取相關係數
min_val1, max_val1, min_loc1, max_loc1 =cv2.minMaxLoc(res1)
min_val2, max_val2, min_loc1, max_loc1 =cv2.minMaxLoc(res2)


#相關係數對比（max_val),越接近1，匹配程度越高
print(min_val1, max_val1,min_val2, max_val2)
if max_val1 < max_val2 :
    j = 0
else:
    j = 1

#根據提取的相關係數得出對應匹配程度最高的模板
h, w = template[j].shape[:2]    # 計算模板影象的高和寬 rows->h, cols->w
pes=cv2.matchTemplate(canny, template[j], cv2.TM_SQDIFF) #模板匹配
in_val, ax_val, in_loc, ax_loc =cv2.minMaxLoc(pes)

#在原圖中框出模板匹配的位置
left_top = ax_loc   # 左上角
right_bottom = (left_top[0] + w, left_top[1] + h)   # 右下角
cv2.rectangle(img, left_top, right_bottom, 255, 2)  # 畫出矩形位置

#繪製模板影象
plt.subplot(121), plt.imshow(template[j], cmap='gray')
plt.title(str(j)),plt.xticks([]), plt.yticks([])

#繪製檢測影象
plt.subplot(122), plt.imshow(img, cmap='gray')
plt.title('img'), plt.xticks([]), plt.yticks([])
plt.show()


# def getPoints(img, template, threshold, method=cv2.TM_SQDIFF):
    # result = cv2.matchTemplate(img, template, method)
 
    # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        # loc = np.where(result <= threshold) #回傳為 y, x
    # else:
        # loc = np.where(result >= threshold) #回傳為 y, x
    
    # pts = zip(*loc[::-1])
    
    # return removeSame(pts, min(template.shape[0], template.shape[1]))
    
 
# # 去掉太過接近的座標
# def removeSame(pts, threshold):
    # elements = []
    # for x,y in pts:
        # for ele in elements:
            # if ((x-ele[0])**2 + (y-ele[1])**2) < threshold**2:
                # break
        # else:
            # elements.append((x,y))
    
    # return elements
    
    
# def drawRectangle(img, pts, w, h, color=(0,0,255), lineW=2):
    # for pt in pts:
        # cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), color, lineW) #因後面會反向顏色順序，所以這邊顯示紅色要反向
    
# def __apply_template_matching(template_rotated, image):

    # # Apply template matching
    # image_templated = cv2.matchTemplate(image, template_rotated, cv2.TM_SQDIFF)

    # # Correct template matching image size difference
    # template_rotated_height = template_rotated.shape[0]
    # template_rotated_width = template_rotated.shape[1]
    # template_half_height = template_rotated_height // 2
    # template_half_width = template_rotated_width // 2

    # image_templated_inrange_size_corrected = cv2.copyMakeBorder(image_templated, template_half_height, template_half_height, template_half_width, template_half_width, cv2.BORDER_CONSTANT, value=0)

    # # Calculate maximum match coefficient
    # max_match = np.max(image_templated_inrange_size_corrected)

    # return (max_match, template_rotated, image_templated_inrange_size_corrected) 
 
# if __name__ == '__main__':
    # img = cv2.imread("C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\red_arrow2.jpg")
    # img_result = img.copy()
    # template = cv2.imread("C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\red_arrow5.2.1.jpg")
    
    # max_match, template_rotated, image_templated_inrange_size_corrected = __apply_template_matching(template, img)
    # print(max_match, template_rotated, image_templated_inrange_size_corrected)
    # cv2.imshow("www",image_templated_inrange_size_corrected)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # w = template.shape[1]
    # h = template.shape[0]
    
    # threshold = 0.4
    
    # elements = getPoints(img, template, threshold)  
    # total_n = len(elements)
    # drawRectangle(img_result, elements, w=template.shape[1], h=template.shape[0])  
 
    # # 逆時針旋轉 90
    # template_r90 = cv2.transpose(template)
    # cv2.flip(template_r90, 0)
    # pts1 = getPoints(img, template_r90, threshold)
    # # 順時針旋轉 90
    # template_r90 = cv2.transpose(template)
    # cv2.flip(template_r90, 1)
    # pts2 = getPoints(img, template_r90, threshold)
    
    # elements = removeSame(pts1+pts2, w)  
    # total_90 = len(elements)
    # drawRectangle(img_result, elements, w=template_r90.shape[1], h=template_r90.shape[0], color=(0,255,0)) 
        
    # plt.subplot(121)
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) #因 openCV 記錄的顏色順序是反過來的
    # plt.title('Original'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122)
    # plt.imshow(cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB)) #因 openCV 記錄的顏色順序是反過來的
    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    # plt.suptitle('Total:{}\nnomral:{}, 90:{}'.format(total_n+total_90, total_n, total_90))
 
    # cv2.imshow("www",img_result)
    # plt.show()
