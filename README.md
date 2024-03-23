## Abstract

The main propose of this exercise was detect the room walls from architectural blueprints or pre-construction plans. 
Two approaches were considered, but the focus shifted towards creating a room walls detection algorithm. This algorithm leverages image processing techniques specifically chosen for their ability to accentuate the boundaries of walls within an pdf file. To reduce noise, the algorithm starts by applying a Gaussian filter with a 5x5 kernel size. After that, it calculates the edges in the resulting image using a Sobel filter, which is sensitive to horizontal and vertical lines.
The filtering process leaves behind thin lines along the edges, often referred to as tick lines. To address this, the algorithm applies a technique called Non-maximum Suppression (NMS). NMS works by analyzing the image in small neighborhoods (defined by a 3x3 kernel in this case). It considers four specific directions: 0 degrees (horizontal), 90 degrees (vertical), and diagonals at -45 and 45 degrees. Within each neighborhood, NMS only keeps the pixel with the highest intensity value, effectively thinning the detected edges and removing extraneous lines. 
Following the NMS step, the algorithm utilizes a technique called Hough Transform to tackle any remaining spurious lines. The Hough Transform essentially acts like a voting mechanism. Each edge point in the image "votes" for the lines it might belong to, considering different angles and distances from the origin. The lines that receive the most votes are considered the most likely true edges, effectively mitigating the presence of incorrect lines left behind by previous steps.

For the sheet number extraction, it was also developed a algorithm with the function of detect the first sheet number that is present in the pdf file. 

## Run the algoritm
- Clone the repository and then run the following script 
```bash
sh File.sh --path  <path_to_file> --text <type>
```
-Clone the repository and run the scripts to build a docker image and run the container
```bash
docker build -t <docker_name> .
```
```bash
docker run -p 5000:5000 -v "<path_to_file>:/input" -v "<type>:/output"  <docker_name> /usr/local/bin/File.sh
```
