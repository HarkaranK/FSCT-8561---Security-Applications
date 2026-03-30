from PIL import Image
import stepic

stegoimage = Image.open("profile.png")
decodedata = stepic.decode(stegoimage)

print("\nExtracted Data:", decodedata)