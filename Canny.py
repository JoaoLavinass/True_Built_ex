import numpy as np
from pdf2image import convert_from_path
from flask import Flask, request, jsonify
from pypdf import PdfReader
import argparse
import cv2 as cv

parser = argparse.ArgumentParser(description='Input data')
parser.add_argument('--path', type=str, default='/input', help='input image is here')
parser.add_argument('--text', type=str, default='/output', help='output image is here')

args = parser.parse_args()

UPLOAD_FOLDER = args.path
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
text = args.text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEXT'] = text

@app.route('/', methods=['GET', 'POST'])
def process_image_text():
  # Get image data from request (assuming multipart form data)

  file = app.config['UPLOAD_FOLDER']
  if file:
      if app.config['TEXT'] == 'walls':
         
        class Canny(object):
          def __init__(self, max_low_thresh_hold=100, ratio=3, kernel_size=5):
            self.max_low_threshold = max_low_thresh_hold
            self.ratio = ratio
            self.kernel_size = kernel_size

          def get_edge_map(self, image, val):
            image = np.reshape(image, (image.shape[0], image.shape[1], 1))
            img_blur = cv.blur(image, (5, 5))
            low_threshold = val
            edges = cv.Canny(img_blur, low_threshold, 150, self.kernel_size)
            mask = edges != 0
            dst = image * (mask[:, :, None].astype(image.dtype))
            return edges, image, dst
          
        Canny = Canny()

        img = convert_from_path(file)

        img1 = img[0].convert('L')

        img_array = np.array(img1)

        _,_, dst = Canny.get_edge_map(image=img_array, val=475)

        # Perform Hough line detection
        # Define parameters for Hough Transform (experiment with these values)
        rho = 1  # Distance resolution in pixels
        theta = np.pi/180  # Angle resolution in radians
        threshold = 100  # Minimum number of votes to consider a line
        min_line_length = 50  # Minimum length of line in pixels
        max_line_gap = 30  # Maximum gap between line segments

        lines = cv.HoughLinesP(dst, rho, theta, threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)
        
        z = lines[0][0]

        for i in range(len(lines)):
          if z[2] < lines[i][0][2]:
            lines[i][0][2] = 0
              
          elif z[0] > lines[i][0][0]:
            lines[i][0][0] = 0

        walls = []
        for i in range(len(lines)):
            x1,y1,x2,y2 = lines[i][0]

            if x1 == 0 or x2 == 0:
              continue
            
            else:
            
              aux = {'wallId': 'wall_' + str(i), 'position':{'start':{'x':int(x1), 'y':int(y1)}, 'end':{'x':int(x2), 'y':int(y2)}}}

              walls.append(aux)
        
        

        #walls = json.dumps(list(walls))

        final = {'type':app.config['TEXT'],'imageId': "image", 'detectionResults': list(walls)}

        return jsonify(final)

      else:
        reader = PdfReader(file) 
  
        # printing number of pages in pdf file 
        print(len(reader.pages)) 
          
        # creating a page object 
        page = reader.pages[0] 
          
        # extracting text from page 
        text = page.extract_text()
        for i in range(len(text)):
            if text[i] + text[i+1] == 'A-' or text[i] + text[i+1] == 'A0':
                sheet = text[i:i+5]
                break
      
        return jsonify({'type': app.config['TEXT'], "imageId": "image", "detectionResults": {"sheet_number": sheet}})


      
if __name__ == '__main__':
  app.run(debug=True)  # For development only, remove in production




