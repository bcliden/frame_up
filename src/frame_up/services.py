import json
import sys
from typing import Any, Optional

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


def antique_filter(image: Image, intensity: float) -> Image:
    return get_filtered_image("antique", image, intensity)


def vibrant_filter(image: Image, intensity: float) -> Image:
    return get_filtered_image("vibrant", image, intensity)


def monochrome_filter(image: Image, intensity: float) -> Image:
    return get_filtered_image("monochrome", image, intensity)


def send_recv_zmq(host: str, port: str, payload: str) -> Optional[Any]:
    connection = f"tcp://{host}:{port}"

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.CONNECT_TIMEOUT, timeouts["connect"])
    socket.setsockopt(zmq.SNDTIMEO, timeouts["send"])
    socket.setsockopt(zmq.RCVTIMEO, timeouts["recv"])
    print(f"[zmq] 🔌 {connection} | timeouts = {timeouts}")

    socket.connect(connection)
    try:
        print(f"[zmq] sending payload of size {sys.getsizeof(payload)}")
        socket.send_string(payload)
        print(f"[zmq] sent string of size {sys.getsizeof(payload)}")
        response = socket.recv_json()
        print(f"[zmq] recieved json of size {sys.getsizeof(response)}")
        return response
    except zmq.ZMQError as z:
        print("[zmq error]", z)
        return None
    finally:
        # socket.disconnect(connection)
        # socket.close()
        context.destroy()  # this may be enough


def get_filtered_image(filter: str, image: Image, intensity: float = 1) -> Image:
    host = service_index[filter]["host"]
    port = service_index[filter]["port"]

    if host is None or port is None:
        raise ValueError("couldn't find configuration for filter: ", filter)

    payload = json.dumps({"image": base64_encode_image(image), "intensity": intensity})
    response = send_recv_zmq(host, port, payload)

    if not response or response["status"] == "error":
        raise SystemError("antique_filter failed")
    return base64_decode_image(response["image"])


def email_image(payload: ImageEmailPayload) -> bool:
    """contact email service w/ contract info"""
    host = service_index["email"]["host"]
    port = service_index["email"]["port"]

    response = send_recv_zmq(host, port, payload.to_microservice_json())

    if not response or not response["success"]:
        raise SystemError("send_email failed")
    return response["success"]
