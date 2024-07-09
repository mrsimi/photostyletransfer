# import cv2
# import numpy as np


# def combine_rgb(red, green, blue):
#     assert red.shape == green.shape == blue.shape, "All input arrays must have the same shape"
#     image = np.stack((red, green, blue), axis=-1)
#     image = np.clip(image, 0, 255)
#     image = image.astype(np.uint8)
    
#     return image

# def take_image_split(image):
#     image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#     image_to_copy_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     return image_to_copy_rgb

# def transformAToB(A, B):
#      # Calculate means
#     mean1 = np.mean(A)
#     mean2 = np.mean(B)
    
#     # Calculate standard deviations
#     std1 = np.std(A)
#     std2 = np.std(B)
    
#     # Standardize array1
#     standardized_array1 = (A - mean1) / std1
    
#     # Scale and shift to match mean and std of array2
#     matched_array1 = standardized_array1 * std2 + mean2
    
#     # Clip the values to be within the range [0, 255]
#     clipped_array1 = np.clip(matched_array1, 0, 255)
#     return clipped_array1

# def transfromAToBImage(from_image, to_image):
#     nr = transformAToB(to_image[:,:,0], from_image[:,:,0])
#     ng = transformAToB(to_image[:,:,1], from_image[:,:,1])
#     nb = transformAToB(to_image[:,:,2], from_image[:,:,2])
#     return nr, ng, nb

# def transferStyleInAToB(imageA, imageB, output_dir):
#     from_image = take_image_split(imageA)
#     to_image = take_image_split(imageB)
#     nr, ng, nb = transfromAToBImage(from_image, to_image)

#     rgb_image = combine_rgb(nb, ng, nr)

#     output_path = f'{output_dir}/image.jpg'
#     cv2.imwrite(output_path, rgb_image)
#     return output_path

from PIL import Image
import numpy as np

def combine_rgb(red, green, blue):
    assert red.shape == green.shape == blue.shape, "All input arrays must have the same shape"
    image = np.stack((red, green, blue), axis=-1)
    image = np.clip(image, 0, 255)
    image = image.astype(np.uint8)
    
    return image

def take_image_split(image_path):
    image = Image.open(image_path).convert('RGB')
    image_array = np.array(image)
    return image_array

def transformAToB(A, B):
    # Calculate means
    mean1 = np.mean(A)
    mean2 = np.mean(B)
    
    # Calculate standard deviations
    std1 = np.std(A)
    std2 = np.std(B)
    
    # Standardize array1
    standardized_array1 = (A - mean1) / std1
    
    # Scale and shift to match mean and std of array2
    matched_array1 = standardized_array1 * std2 + mean2
    
    # Clip the values to be within the range [0, 255]
    clipped_array1 = np.clip(matched_array1, 0, 255)
    return clipped_array1

def transfromAToBImage(from_image, to_image):
    nr = transformAToB(to_image[:,:,0], from_image[:,:,0])
    ng = transformAToB(to_image[:,:,1], from_image[:,:,1])
    nb = transformAToB(to_image[:,:,2], from_image[:,:,2])
    return nr, ng, nb

def transferStyleInAToB(imageA_path, imageB_path, output_dir):
    from_image = take_image_split(imageA_path)
    to_image = take_image_split(imageB_path)
    nr, ng, nb = transfromAToBImage(from_image, to_image)

    rgb_image = combine_rgb(nr, ng, nb)
    
    output_image = Image.fromarray(rgb_image)
    output_path = f'{output_dir}/image.jpg'
    output_image.save(output_path)
    return output_path