import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from matplotlib.path import Path
import numpy as np
import yaml


def visualize_and_extract_area(map_path, threshold=128):
    # Read the PGM file and convert it to a format compatible with matplotlib
    img = Image.open(map_path)
    map_img = mpimg.pil_to_array(img)

    # Display the image
    plt.imshow(map_img, cmap='gray')
    plt.title('Map Visualization')
    plt.axis('on')  # Turn off axis labels

    # Interactive mode for selecting points
    plt.ion()

    # Prompt the user to select points and end the process by pressing a button
    print("Select points on the map. Press 'Enter' to finish.")
    area_corners = plt.ginput(n=-1, timeout=0)

    # Turn off interactive mode
    plt.ioff()

    # Connect the selected points with lines
    if area_corners:
        area_corners.append(area_corners[0])  # Connect the last point to the first point
        plt.plot([p[0] for p in area_corners], [p[1] for p in area_corners], 'ro-')  # 'ro-' represents red color and line connecting points

        # Fill the polygonal area with the selected points
        polygon_path = Path(area_corners)
        plt.gca().add_patch(plt.Polygon(area_corners, fill=None, edgecolor='r'))

        # Display the plot
        plt.show()

        # Extract pixel positions inside the polygonal area
        h, w = map_img.shape[:2]
        y, x = np.mgrid[:h, :w]
        points = np.column_stack((x.ravel(), y.ravel()))

        inside_polygon = polygon_path.contains_points(points)

        # Get pixel positions inside the polygon
        inside_positions = points[inside_polygon]

        # Filter out pixels with values less than the specified threshold
        inside_positions = inside_positions[map_img[inside_positions[:, 1], inside_positions[:, 0]] >= threshold]
        #inverrt height
        inside_positions[:, 1] = h - inside_positions[:, 1]
        #invert pixcel to meter
        inside_positions=inside_positions*resolution
        #relocate to origin
        inside_positions[:, 1]=-origin[1]+inside_positions[:, 1]
        inside_positions[0, :]=-origin[0]+inside_positions[0, :]
        # You can use the filtered 'inside_positions' variable to perform further operations
        print("Filtered pixel positions inside the selected area:", inside_positions)
    else:
        print("No points selected.")

if __name__ == "__main__":
    # Replace 'path/to/your/map.pgm' with the actual path to your PGM file
    map_file_path = r'C:\Users\MEHRDAD\Desktop\map.pgm'
    yaml_file_path = r'C:\Users\MEHRDAD\Desktop\map.yaml'
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    # Extract 'origin' and 'resolution' values
    origin = yaml_data.get('origin', [])
    resolution = yaml_data.get('resolution', None)

    # Set the threshold value (default is 128)
    threshold_value = 250

    visualize_and_extract_area(map_file_path, threshold=threshold_value)
