client = genai.Client()

# Desteklenen modelleri güvenli şekilde listele
models = client.models.list()

for model in models:
    print("MODEL:", model.name)
    # Eğer method özelliği varsa yaz
    if hasattr(model, "supported_generation_methods"):
        print("METHODS:", model.supported_generation_methods)
    elif hasattr(model, "methods"):
        print("METHODS:", model.methods)
    else:
        print("METHODS: Bilinmiyor")
    print("-" * 40)
