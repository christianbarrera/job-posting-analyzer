import matplotlib.pyplot as plt
from wordcloud import WordCloud

def plot_wordcloud_and_frequencies(unigrams, bigrams, text):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))  # Three side-by-side plots

    # Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    axes[0].imshow(wordcloud, interpolation='bilinear')
    axes[0].axis('off')  # Hide axes
    axes[0].set_title("Word Cloud")

    # Unigrams Bar Chart
    top_unigrams = unigrams.most_common(10)
    words_u, counts_u = zip(*top_unigrams)
    axes[1].bar(words_u, counts_u, color='tab:blue')
    axes[1].set_title("Top Unigrams")
    axes[1].set_xlabel("Words")
    axes[1].set_ylabel("Frequency")
    axes[1].tick_params(axis='x', rotation=45)

    # Bigrams Bar Chart
    top_bigrams = bigrams.most_common(10)
    words_b, counts_b = zip(*[(" ".join(phrase), count) for phrase, count in top_bigrams])
    axes[2].bar(words_b, counts_b, color='tab:green')
    axes[2].set_title("Top Bigrams")
    axes[2].set_xlabel("Phrases")
    axes[2].set_ylabel("Frequency")
    axes[2].tick_params(axis='x', rotation=90)

    plt.tight_layout()

    # Save the figure
    plt.savefig("output/example_output.png", dpi=300, bbox_inches="tight")
    plt.show()  # Commented out