import base64
import hashlib
import hmac
import secrets


ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 600_000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
    )

    return "$".join(
        (
            ALGORITHM,
            str(ITERATIONS),
            base64.b64encode(salt).decode("ascii"),
            base64.b64encode(password_hash).decode("ascii"),
        )
    )


def verify_password(password: str, stored_password: str) -> bool:
    try:
        algorithm, iterations, encoded_salt, encoded_hash = stored_password.split("$", 3)
        if algorithm != ALGORITHM:
            return False

        salt = base64.b64decode(encoded_salt, validate=True)
        expected_hash = base64.b64decode(encoded_hash, validate=True)
        candidate_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(iterations),
        )
    except (TypeError, ValueError):
        return False

    return hmac.compare_digest(candidate_hash, expected_hash)
