from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def get_embedding(text: str):
    return model.encode(text)


def calculate_similarity(text1: str, text2: str):

    embedding1 = model.encode(text1)
    embedding2 = model.encode(text2)

    similarity = model.similarity(
        embedding1,
        embedding2
    )

    return float(similarity.item())