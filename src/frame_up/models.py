import json
from dataclasses import dataclass

from PIL.Image import Image

from frame_up.serialization import base64_encode_image


@dataclass
class ImageEmailPayload:
    to: str
    subject_line: str
    data: Image

    def to_microservice_json(self) -> str:
        """Specifically for Ryan's Microservice A"""
        encoded_image = base64_encode_image(self.data)
        body = {
            "data": encoded_image,
            "data_type": "image",
            "subject": self.subject_line,
            "receiver_email": self.to,
        }
        return json.dumps(body)
