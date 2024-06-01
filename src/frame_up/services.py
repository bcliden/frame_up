import json
from typing import Any, Optional, Sized

import zmq
from PIL.Image import Image

from frame_up.models import ImageEmailPayload
from frame_up.serialization import base64_decode_image, base64_encode_image

# source from .env or something configurable?
service_index = {
    "email": {"host": "localhost", "port": "5555"},
    "antique": {"host": "localhost", "port": "8673"},
    "vibrant": {"host": "localhost", "port": "8674"},
    "monochrome": {"host": "localhost", "port": "8675"},
}

# Timeouts (in milliseconds)
timeouts: dict[str, int] = {"connect": 1 * 1000, "send": 5 * 1000, "recv": 5 * 1000}


def pretty_print(response: dict[str, str]):
    print("{")
    for key, value in response.items():
        if isinstance(value, Sized) and len(value) > 50:
            value = value[0:50] + " (truncated)"
        print(f"    {key}: {value}")
    print("}")


def antique_filter(image: Image, intensity: float) -> Image:
    return get_filtered_image("antique", image, intensity)


def vibrant_filter(image: Image, intensity: float) -> Image:
    return get_filtered_image("vibrant", image, intensity)


def monochrome_filter(image: Image, intensity: float) -> Image:
    return get_filtered_image("monochrome", image, intensity)


def get_filtered_image(filter: str, image: Image, intensity: float = 1) -> Image:
    host = service_index[filter]["host"]
    port = service_index[filter]["port"]

    if host is None or port is None:
        raise ValueError("couldn't find configuration for filter: ", filter)

    print(f"[zmq] 🖼️  preparing request for image filter: {filter}")

    payload = json.dumps({"image": base64_encode_image(image), "intensity": intensity})
    response = send_recv_zmq(host, port, payload)

    if not response or response["status"] == "error":
        raise SystemError("antique_filter failed")
    return base64_decode_image(response["image"])


def send_recv_zmq(host: str, port: str, payload: str) -> Optional[Any]:
    connection = f"tcp://{host}:{port}"

    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.setsockopt(zmq.CONNECT_TIMEOUT, timeouts["connect"])
    socket.setsockopt(zmq.SNDTIMEO, timeouts["send"])
    socket.setsockopt(zmq.RCVTIMEO, timeouts["recv"])
    socket.connect(connection)
    print(f"[zmq] 🔌 {connection} | timeouts = {timeouts}")

    try:
        socket.send_string(payload)
        response = socket.recv_json()
        print("[zmq] recieved response:")
        pretty_print(response)  # type: ignore
        return response
    except zmq.ZMQError as z:
        print("[zmq error]", z)
        return None
    finally:
        context.destroy()  # this may be enough


def email_image(payload: ImageEmailPayload) -> bool:
    """contact email service w/ contract info"""
    host = service_index["email"]["host"]
    port = service_index["email"]["port"]

    response = send_recv_zmq(host, port, payload.to_microservice_json())

    if not response or not response["success"]:
        raise SystemError("send_email failed")
    return response["success"]
