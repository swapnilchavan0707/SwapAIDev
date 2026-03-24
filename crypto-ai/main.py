import os
from src.engine import generate_key, encrypt_message, decrypt_message
from src.analyst import save_entropy_graph


def main():
    os.makedirs('data/crypto_reports', exist_ok=True)

    # 1. Input
    secret_text = "This is a highly confidential AI project message!"
    print(f"Original: {secret_text}")

    # 2. Key Generation & Encryption
    key = generate_key()
    encrypted = encrypt_message(secret_text, key)
    print(f"Encrypted (Hash-like): {encrypted.decode()[:50]}...")

    # 3. AI Analysis (Generate Figures)
    graph_path = 'data/crypto_reports/security_analysis.png'
    save_entropy_graph(secret_text, encrypted, graph_path)
    print(f"AI Security Figure generated at: {graph_path}")

    # 4. Decryption
    decrypted = decrypt_message(encrypted, key)
    print(f"Decrypted Result: {decrypted}")


if __name__ == "__main__":
    main()