import pytest
import os
import cv2 as cv
import numpy as np

decorator_image_names = ["test_normal_logout_button.png", "test_dark_logout_button.png", "test_bright_logout_button.png"]


def initialize_test_images(image_to_test):
    test_image_path = os.path.join(os.path.dirname(__file__), "test_assets", image_to_test)
    test_image = cv.imread(test_image_path)

    if test_image is None:
        raise FileNotFoundError(f"test image not found at {test_image_path}")
    
    test_image = np.array(test_image)
    test_image = cv.cvtColor(test_image, cv.COLOR_RGB2BGR)
    test_imageHSV = cv.cvtColor(test_image, cv.COLOR_BGR2HSV)
    return test_image, test_imageHSV

def button_assets():
    assets_path = os.path.join(os.path.dirname(__file__), "..", "undercut_checker", "assets", "logout.png")
    assets_path = os.path.abspath(assets_path)

    button = cv.imread(assets_path)

    if button is None:
        raise FileNotFoundError(f"button asset not found at {assets_path}")

    return button


def find_button(test_image, button_asset, threshold=0.75):
    found_button = cv.matchTemplate(test_image, button_asset, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(found_button)
    if max_val >= threshold:
        return max_loc, max_val
    else:
        return None, max_val

@pytest.mark.parametrize("image_name", decorator_image_names)
def test_find_button_with_custom_threshold(image_name):
    """
    using the same image but with altered settings for brightness (to attempt to emulate different monitor settings),
    this test allows to finetune the exact treshold settings
    """
    button_asset = button_assets()
    test_image, _ = initialize_test_images(image_name)
    
    # Run the find_button function with the current threshold
    result, max_loc = find_button(test_image, button_asset)

    print(f"{image_name} passed with a threshold of {max_loc}")

    # asserts different combinations and then 
    assert result is not None, f"Button not found for image & threshold: {image_name}. the threshhold was: {max_loc}"