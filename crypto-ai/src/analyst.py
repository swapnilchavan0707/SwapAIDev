import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


def save_entropy_graph(original, encrypted, output_path):
    # Count frequency of characters
    orig_counts = Counter(original)
    enc_counts = Counter(str(encrypted))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Original Text Distribution
    ax1.bar(orig_counts.keys(), orig_counts.values(), color='skyblue')
    ax1.set_title("Original Text Pattern")

    # Encrypted Text Distribution (Should look like random noise)
    ax2.hist(list(enc_counts.values()), bins=10, color='salmon')
    ax2.set_title("Encrypted 'Noise' Distribution")

    plt.suptitle("AI Cryptography Analysis: Pattern Destruction", fontsize=14)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
