import cv2
import numpy as np

def match_means_and_stds(array1, array2):
    mean1 = np.mean(array1)
    mean2 = np.mean(array2)
    
    std1 = np.std(array1)
    std2 = np.std(array2)
    
    standardized_array1 = (array1 - mean1) / std1
    
    matched_array1 = standardized_array1 * std2 + mean2
    clipped_array1 = np.clip(matched_array1, 0, 255)
    
    return clipped_array1

def combine_rgb(red, green, blue):
    assert red.shape == green.shape == blue.shape, "All input arrays must have the same shape"
    image = np.stack((red, green, blue), axis=-1)
    image = np.clip(image, 0, 255)
    image = image.astype(np.uint8)
    
    return image

def transfer_style(from_image, to_image, output_dir):
    # from_image = cv2.imread(from_image)
    # to_image = cv2.imread(to_image)

    from_image = cv2.imdecode(from_image, cv2.IMREAD_COLOR)
    to_image = cv2.imdecode(to_image, cv2.IMREAD_COLOR)

    from_image_rgb = cv2.cvtColor(from_image, cv2.COLOR_BGR2RGB)
    to_image_rgb = cv2.cvtColor(to_image, cv2.COLOR_BGR2RGB)

    r_fr, g_fr, b_fr = cv2.split(from_image_rgb)
    r_to, g_to, b_to = cv2.split(to_image_rgb)

    adj_r = match_means_and_stds(r_fr, r_to)
    adj_g = match_means_and_stds(g_fr, g_to)
    adj_b = match_means_and_stds(b_fr, b_to)

    rgb_image = combine_rgb(adj_b, adj_g, adj_r)

    output_path = f'{output_dir}/image.jpg'
    cv2.imwrite(output_path, rgb_image)
    return output_path