import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from matplotlib.path import Path
import numpy as np
import yaml
import os
inside_positions = np.array([])
def visualize_and_extract_area(map_path, threshold):
    global inside_positions
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
        # print(inside_positions)

        # Display the image
        #plt.imshow(map_img, cmap='gray')
        #plt.title('Map Visualization')
        #plt.axis('on')  # Turn off axis labels

        # Plot the original selected pixel positions on the map
        #plt.plot(inside_positions[:, 0], inside_positions[:, 1], 'go', label='Original Positions')

        # Interactive mode for selecting points
        #plt.ion()

        # Prompt the user to select points and end the process by pressing a button
        #print("Select points on the map. Press 'Enter' to finish.")
        #area_corners = plt.ginput(n=-1, timeout=0)

        # Turn off interactive mode
        #plt.ioff()

        #inverrt height
        inside_positions[:, 1] = h - inside_positions[:, 1]
        #invert pixcel to meter
        inside_positions=inside_positions*resolution
        # print(inside_positions)
        #relocate to origin
        for i in range(len(inside_positions)):
            inside_positions[i][0] += origin[0]
            inside_positions[i][1] += origin[1]

        #round numbers
        inside_positions=np.round(inside_positions, 1)
        #git rid of repetitive pairs
        inside_positions=np.unique(inside_positions, axis=0)
        inside_positions=np.unique(inside_positions, axis=1)

        # You can use the filtered 'inside_positions' variable to perform further operations
        # print("Filtered pixel positions inside the selected area:", inside_positions)
    else:
        print("No points selected.")
def save_positions_to_file(positions, output_file):
    with open(output_file, 'w') as file:
        # file.write("# Filtered Pixel Positions\n")
        # file.write("filtered_positions = [\n")
        for pos in positions:
            file.write(f"    {pos}\n")
        # file.write("]\n")
if __name__ == "__main__":
    # map_file_path = r'C:\Users\MEHRDAD\Desktop\map.pgm'
    # yaml_file_path = r'C:\Users\MEHRDAD\Desktop\map.yaml'
    map_file_path = os.path.expanduser('~/robot_ws/src/p0/map.pgm')
    yaml_file_path = os.path.expanduser('~/robot_ws/src/p0/map.yaml')
    output_file_path = os.path.expanduser('~/robot_ws/src/p0/scripts/poses.txt')

    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    # Extract 'origin' and 'resolution' values
    origin = yaml_data.get('origin', [])
    resolution = yaml_data.get('resolution', None)

    # Set the threshold value (default is 128)
    threshold_value = 250

    visualize_and_extract_area(map_file_path, threshold=threshold_value)
    if inside_positions is not None and inside_positions.size > 0:
        # Save filtered positions to a Python file
        save_positions_to_file(inside_positions, output_file_path)
    else:
        print("No points selected.")