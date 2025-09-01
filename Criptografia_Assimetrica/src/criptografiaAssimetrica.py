from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import os
import tkinter as tk
from tkinter import filedialog, messagebox

private_key = ec.generate_private_key(public_exponent=65537, key_size=3072, backend=default_backend(), )
public_key = private_key.public_key()

