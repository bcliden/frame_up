from typing import Any, Optional

import zmq
from PIL.Image import Image

from frame_up.models import ImageEmailPayload
from frame_up.serialization import base64_decode_image, base64_encode_image

# source from .env or something configurable?
service_index = {
    "email": {"host": "localhost", "port": "7777"},
    "antique": {"host": "localhost", "port": "8673"},
    "vibrant": {"host": "localhost", "port": "8674"},
    "monochrome": {"host": "localhost", "port": "8675"},
}


def antique_filter(image: Image, intensity: Optional[float] = None) -> Image:
    return get_filtered_image("antique", image, intensity)


def vibrant_filter(image: Image, intensity: Optional[float] = None) -> Image:
    return get_filtered_image("vibrant", image, intensity)


def monochrome_filter(image: Image, intensity: Optional[float] = None) -> Image:
    return get_filtered_image("monochrome", image, intensity)


def send_recv_zmq(host: str, port: str, payload: str) -> Any:
    connection = f"tcp://{host}:{port}"

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(connection)

    socket.send_string(payload)
    return socket.recv_json()


def get_filtered_image(filter: str, image: Image, intensity: float = 1) -> Image:
    host, port = service_index[filter]

    if host is None or port is None:
        raise ValueError("couldn't find configuration for filter: ", filter)

    payload = {"image": base64_encode_image(image), "intensity": intensity}
    response = send_recv_zmq(host, port, payload)

    if response["status"] == "error":
        raise SystemError("antique_filter failed")
    return base64_decode_image(response["image"])


def email_image(payload: ImageEmailPayload) -> bool:
    """contact email service w/ contract info"""
    host, port = service_index["email"]

    response = send_recv_zmq(host, port, payload.to_microservice_json())

    if not response.success:
        raise SystemError("send_email failed")
    return response.success
