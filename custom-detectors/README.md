# Custom Detector

Examples of custom detector for Local Motion. Custom detector must be Web API which takes image as input and returns normalized positions of bouding boxes.

### Requirements of Custom Detector
Please refer to the sample source code of examples for details on how to implement it to meet the following requirement.

- Custom Detector Web API has POST method
- Local Motion sends an image of part of screenshot as base64 encoded string. Payload is supposed to have `image_data` field.
```
{
    "image_data": "base64_encoded_image_here"
}
```
- Custom Detector Web API must return `boxes` which is list of bouding box position [xmin, ymin, xmax, ymax]. The each value must be normalized to 0~1. For example, if image width is 400px and xmin of a bouding box is 100px, xmin should be 0.25.
```
{
    "boxes": [[0, 0, 0.2, 0.3], [0.3, 0.4, 0.5, 0.45]]
}
```

### List of Examples
- Word Detector: Google Cloud Vision API is used to detect words for custom detector of Local Motion.
- Whole Image Detector: Fixed single box position is returned.
