import rclpy
import cv2
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import pytesseract

class ImageConvertor(Node):
    def __init__(self):
        super().__init__('img_convert')

        self.create_subscription(
            CompressedImage, 'camera/image/compressed',
            self.get_compressed, 10)
        self.bridge = CvBridge()
        self.pytesseract_config = '--psm 7 --oem 0'  # Tesseract OCR 설정

    def get_compressed(self, msg):
        cv_img = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        if cv_img is None:
            self.get_logger().info("Image not found")
            return
            
            
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)
        img_blur_thresh = cv2.adaptiveThreshold(
        img_blurred,
        maxValue=255.0,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=19,
        C=9) 
        contours, _ = cv2.findContours(
        img_blur_thresh,
        mode=cv2.RETR_LIST,
        method=cv2.CHAIN_APPROX_SIMPLE)
        temp_result = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255,255,255))
        temp_result = np.zeros((480, 640, 3), dtype=np.uint8)
                
        contours_dict = []
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(temp_result, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255), thickness=2)
            contours_dict.append({
            'contour': contour,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'cx': x + (w / 2),
            'cy': y + (h / 2)
        })
        
        MIN_AREA = 80
        MIN_WIDTH, MIN_HEIGHT = 2, 8
        MIN_RATIO, MAX_RATIO = 0.25, 1.0

        possible_contours = []

        cnt = 0
        
        for d in contours_dict:
            area = d['w'] * d['h']
            ratio = d['w'] / d['h']
            if area > MIN_AREA \
                and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
                and MIN_RATIO < ratio < MAX_RATIO:
                d['idx'] = cnt
                cnt += 1
                possible_contours.append(d)
            
            temp_result = np.zeros((480, 640, 3), dtype=np.uint8)
            
            for d in possible_contours:
                cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(255, 255, 255),thickness=2)
            MAX_DIAG_MULTIPLYER = 5
            MAX_ANGLE_DIFF = 12.0
            MAX_AREA_DIFF = 0.5
            MAX_WIDTH_DIFF = 0.8
            MAX_HEIGHT_DIFF = 0.2
            MIN_N_MATCHED = 3
            
            def find_chars(contour_list):
                matched_result_idx = []
                
                for d1 in contour_list:
                    matched_contours_idx = []
                    for d2 in contour_list:
                        if d1['idx'] == d2['idx']:
                            continue
                            
                        dx = abs(d1['cx'] - d2['cx'])
                        dy = abs(d1['cy'] - d2['cy'])
                        
                        diagonal_length1 = np.sqrt(d1['w'] ** 2 + d1['h'] ** 2)
                        
                        distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))
                        
                        if dx == 0:
                            angle_diff = 90
                        else:
                            angle_diff = np.degrees(np.arctan(dy / dx))
                        area_diff = abs(d1['w'] * d1['h'] - d2['w'] * d2['h']) / (d1['w'] * d1['h'])
                        width_diff = abs(d1['w'] - d2['w']) / d1['w']
                        height_diff = abs(d1['h'] - d2['h']) / d1['h']
                        
                        if distance < diagonal_length1 * MAX_DIAG_MULTIPLYER \
                                and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
                                and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                            matched_contours_idx.append(d2['idx'])
                    matched_contours_idx.append(d1['idx'])
                    
                    if len(matched_contours_idx) < MIN_N_MATCHED:
                        continue
                        
                    matched_result_idx.append(matched_contours_idx)
                    unmatched_contour_idx = []
                    for d4 in contour_list:
                        if d4['idx'] not in matched_contours_idx:
                            unmatched_contour_idx.append(d4['idx'])
                    unmatched_contour = np.take(possible_contours, unmatched_contour_idx)
                    recursive_contour_list = find_chars(unmatched_contour)
                    for idx in recursive_contour_list:
                        matched_result_idx.append(idx)
                    break           ##############################
                return matched_result_idx
                
                result_idx = find_chars(possible_contours)
                matched_result = []
                for idx_list in result_idx:
                    matched_result.append(np.take(possible_contours, idx_list))
                temp_result = np.zeros((480, 640, 3), dtype=np.uint8)
                for r in matched_result:
                    for d in r:
                        cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(255, 255, 255), thickness=2)
                PLATE_WIDTH_PADDING = 1.3  # 1.3
                PLATE_HEIGHT_PADDING = 1.5  # 1.5
                MIN_PLATE_RATIO = 3
                MAX_PLATE_RATIO = 10
          
                plate_imgs = []
                plate_infos = []
          
                for i, matched_chars in enumerate(matched_result):
                    sorted_chars = sorted(matched_chars, key=lambda x: x['cx'])
                    plate_cx = (sorted_chars[0]['cx'] + sorted_chars[-1]['cx']) / 2
                    plate_cy = (sorted_chars[0]['cy'] + sorted_chars[-1]['cy']) / 2
                    plate_width = (sorted_chars[-1]['x'] + sorted_chars[-1]['w'] - sorted_chars[0]['x']) * PLATE_WIDTH_PADDING
                    sum_height = 0
                    for d in sorted_chars:
                        sum_height += d['h']
                    plate_height = int(sum_height / len(sorted_chars) * PLATE_HEIGHT_PADDING)
                    triangle_height = sorted_chars[-1]['cy'] - sorted_chars[0]['cy']
                    triangle_hypotenus = np.linalg.norm(
                    np.array([sorted_chars[0]['cx'], sorted_chars[0]['cy']]) -
                    np.array([sorted_chars[-1]['cx'], sorted_chars[-1]['cy']])
                    )
                    angle = np.degrees(np.arcsin(triangle_height / triangle_hypotenus))
                    rotation_matrix = cv2.getRotationMatrix2D(center=(plate_cx, plate_cy), angle=angle, scale=1.0)
                    img_rotated = cv2.warpAffine(img_thresh, M=rotation_matrix, dsize=(width, height))
                    img_cropped = cv2.getRectSubPix(
                img_rotated,
                patchSize=(int(plate_width), int(plate_height)),
                center=(int(plate_cx), int(plate_cy))
            )
                    if img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO or img_cropped.shape[1] / img_cropped.shape[
                        0] < MIN_PLATE_RATIO > MAX_PLATE_RATIO:
                        continue
                        
                    plate_imgs.append(img_cropped)
                    plate_infos.append({
                        'x': int(plate_cx - plate_width / 2),
                        'y': int(plate_cy - plate_height / 2),
                        'w': int(plate_width),
                        'h': int(plate_height)
                        })
                longest_idx, longest_text = -1, 0
                plate_chars = []
        
                for i, plate_img in enumerate(plate_imgs):
                    plate_img = cv2.resize(plate_img, dsize=(0, 0), fx=1.6, fy=1.6)
                    _, plate_img = cv2.threshold(plate_img, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                    contours, _ = cv2.findContours(plate_img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
                    plate_min_x, plate_min_y = plate_img.shape[1], plate_img.shape[0]
                    plate_max_x, plate_max_y = 0, 0

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        ratio = w / h
    if area > MIN_AREA and w > MIN_WIDTH and h > MIN_HEIGHT and MIN_RATIO < ratio < MAX_RATIO:
        # 여기에 추출된 번호판 이미지 처리 및 Tesseract를 사용한 텍스트 추출 코드 추가
        plate_img = cv_img[y:y + h, x:x + w]
        plate_img_gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        _, plate_img_thresh = cv2.threshold(plate_img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        chars = pytesseract.image_to_string(
            plate_img_thresh, lang='kor', config=self.pytesseract_config)
        if chars:
            self.get_logger().info(f"Extracted Text: {chars}")
def main(args=None):
    rclpy.init(args=args)
    node = ImageConvertor()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main':
    main()
