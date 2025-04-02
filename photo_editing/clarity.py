import cv2
import numpy as np

def apply_unsharp_mask(image, strength=1.0, kernel_size=(9, 9), sigma=10):
    """
    Apply unsharp masking to enhance edges and details.
    
    Parameters:
        image: Input BGR image.
        strength: Weight factor for the sharpening effect.
        kernel_size: Gaussian blur kernel size.
        sigma: Standard deviation for Gaussian blur.
        
    Returns:
        Sharpened image.
    """
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
    return sharpened

def apply_clahe(image, strength=1.0, clip_limit=2.0, tile_grid_size=(8, 8)):
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to the L channel.
    
    Parameters:
        image: Input BGR image.
        strength: Used to adjust the clip limit.
        clip_limit: Base clip limit for CLAHE.
        tile_grid_size: Grid size for dividing the image into tiles.
        
    Returns:
        Image after applying CLAHE.
    """
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    adjusted_clip = clip_limit + strength
    clahe = cv2.createCLAHE(clipLimit=adjusted_clip, tileGridSize=tile_grid_size)
    cl = clahe.apply(l)
    merged = cv2.merge((cl, a, b))
    result = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    return result

def clarity_effect(image, strength=1.0):
    """
    Enhance image clarity by combining unsharp masking and local contrast enhancement.
    
    Parameters:
        image: Input BGR image.
        strength: Clarity strength; higher values yield a stronger effect.
    
    Returns:
        Enhanced image.
    """
    sharpened = apply_unsharp_mask(image, strength=strength)
    enhanced = apply_clahe(sharpened, strength=strength)
    return enhanced

def adjust_exposure(image, exposure=1.0):
    """
    Adjust image exposure by scaling pixel values.
    
    Parameters:
        image: Input BGR image.
        exposure: Exposure factor where 1.0 means no change.
        
    Returns:
        Image with adjusted exposure.
    """
    adjusted = cv2.convertScaleAbs(image, alpha=exposure, beta=0)
    return adjusted

def scale_image_for_display(img, min_width=800, min_height=600):
    """
    Scale the image up if it's smaller than the minimum dimensions.
    
    Parameters:
        img: Input image.
        min_width: Minimum width to display.
        min_height: Minimum height to display.
        
    Returns:
        Resized image if scaling was necessary, otherwise the original image.
    """
    h, w = img.shape[:2]
    scale_factor = max(min_width / w, min_height / h, 1.0)  
    if scale_factor > 1.0:
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)
        return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    return img

def main():
    
    input_path = 'test_gym.jpg'
    image = cv2.imread(input_path)
    if image is None:
        print("Error: Could not load image from", input_path)
        return

    window_name = "Clarity & Exposure Adjuster"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    initial_strength = 100 
    cv2.createTrackbar("Strength", window_name, initial_strength, 300, lambda x: None)
    
   
    initial_exposure = 100  
    cv2.createTrackbar("Exposure", window_name, initial_exposure, 200, lambda x: None)
    
    while True:
        slider_val = cv2.getTrackbarPos("Strength", window_name)
        strength = slider_val / 100.0
        
        exposure_val = cv2.getTrackbarPos("Exposure", window_name)
        exposure = exposure_val / 100.0
        
       
        output_image = clarity_effect(image, strength=strength)
        
       
        output_image = adjust_exposure(output_image, exposure=exposure)
        
       
        display_image = scale_image_for_display(output_image, min_width=800, min_height=600)
        
        cv2.imshow(window_name, display_image)
        
    
        key = cv2.waitKey(50) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
