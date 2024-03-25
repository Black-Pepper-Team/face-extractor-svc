# :facepalm: Feature Extractor service

Service for extracting features from the face image. Handles two HTTP requests:
- Getting the closest public key based on the provided image.
- Outputs the `claim_id` from the `issuer` service by providing the image and other metadata.

To run the service, run
```bash
python3 main.py run-api
```
