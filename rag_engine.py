import json
import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



class WifiChatbot:
    def __init__(self):
        # Configure genai to list models
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.vector_store = None
        
        # Dynamically find available models
        available_models = [m.name for m in genai.list_models()]
        
        # Select best available chat model (prefer flash then pro)
        chat_candidates = ["models/gemini-1.5-flash", "models/gemini-2.0-flash-exp", "models/gemini-pro"]
        self.chat_model_name = next((m for m in chat_candidates if m in available_models), 
                                   next((m for m in available_models if "generateContent" in [method for method in [mod.supported_generation_methods for mod in genai.list_models() if mod.name == m][0]]), "gemini-1.5-flash"))
        
        # Select best available embedding model
        embed_candidates = ["models/text-embedding-004", "models/embedding-001"]
        self.embed_model_name = next((m for m in embed_candidates if m in available_models),
                                    next((m for m in available_models if "embedContent" in [method for method in [mod.supported_generation_methods for mod in genai.list_models() if mod.name == m][0]]), "models/embedding-001"))

        self.llm = ChatGoogleGenerativeAI(
            model=self.chat_model_name, 
            google_api_key=os.environ.get("GOOGLE_API_KEY"),
            temperature=0.3
        )
        self.initialize_vector_store()

    def load_data(self):
        """Loads and processes the products.json file"""
        with open('products.json', 'r') as f:
            data = json.load(f)
        
        documents = []
        for item in data:
            # We combine all fields into a single text block for the AI to read
            page_content = (
                f"Product Name: {item['name']}\n"
                f"Speed: {item['speed']}\n"
                f"Price: {item['price']}\n"
                f"Category: {item['category']}\n"
                f"Description: {item['description']}\n"
                f"Features: {', '.join(item['features'])}\n"
                f"Ideal For: {', '.join(item['ideal_for'])}\n"
            )
            documents.append(Document(page_content=page_content))
        return documents

    def initialize_vector_store(self):
        """Creates the FAISS vector store from the product data"""
        print("Initializing Vector Database...")
        docs = self.load_data()
        
        # Use the dynamically selected embedding model
        embeddings = GoogleGenerativeAIEmbeddings(
            model=self.embed_model_name,
            google_api_key=os.environ.get("GOOGLE_API_KEY")
        )
        
        # Create the vector store
        self.vector_store = FAISS.from_documents(docs, embeddings)
        print("Vector Database Ready!")

    def get_response(self, user_query):
        """Retrieves context and generates a response"""
        
        # 1. Retrieve relevant products
        docs = self.vector_store.similarity_search(user_query, k=5)
        context_text = "\n\n".join([d.page_content for d in docs])

        # 2. Define the Indonesian Prompt
        # We instruct the AI to speak informal but polite Indonesian ("Bahasa Indonesia yang luwes/sopan")
        prompt_template = """
        Anda adalah asisten customer service (CS) yang ramah untuk 'Bizzy Wifi Product', sebuah penyedia layanan internet di Indonesia.
        
        Gunakan 'Informasi Produk' berikut untuk menjawab pertanyaan pengguna.
        Jika jawabannya tidak ada di dalam informasi, katakan "Maaf, saya belum memiliki informasi tersebut."
        Jangan mengarang harga atau kecepatan yang tidak ada di data.
        
        Selalu rekomendasikan nama paket spesifik (contoh: Murmer, Seamless) yang sesuai dengan kebutuhan mereka.
        Gunakan Bahasa Indonesia yang alami, sopan, dan sedikit persuasif.
        
        Gunakan tag HTML untuk memformat jawaban agar lebih rapi:
        - Gunakan <b> atau <strong> untuk penekanan/nama produk.
        - Gunakan <br> untuk baris baru.
        - Gunakan <ul> dan <li> untuk daftar fitur atau rincian.
        
        Informasi Produk:
        {context}
        Informasi Tambahan: kecepatan internet itu 1:1 antara download dan upload, menjangkau area jakarta, depok, bogor, bekasi, tangerang, biaya pemasangan gratis.
        ganti kata "anda" menjadi "kamu", "saya" menjadi "aku", "kita" menjadi "kami", "Bapak/Ibu" menjadi "kak".
        jam operasional customer service senin-jumat 08.00-21.00 WIB, sabtu-minggu 08.00-17.00 WIB.
        nomor whatsapp customer service +628123456789, email cs@bizzy.com

        Pertanyaan Pengguna: {question}
        
        Jawaban (Bahasa Indonesia):
        """
        
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        
        # 3. Generate Answer
        chain = prompt | self.llm | StrOutputParser()
        response = chain.invoke({"context": context_text, "question": user_query})
        
        return response

# Singleton instance to avoid reloading DB on every request
chatbot_instance = WifiChatbot()