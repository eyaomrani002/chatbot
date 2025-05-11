import json
import os
from langchain_ollama import OllamaEmbeddings
#import requests
import pandas as pd
#from langchain.vectorstores.chroma import Chroma
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage, ChatResponse
#from llama_index.core import ServiceContext
#from llama_index.core import Document, VectorStoreIndex

#from llama_index.core import StorageContext, load_index_from_storage
#from llama_index.core.query_engine import CustomQueryEngine
#from llama_index.core.retrievers import VectorIndexRetriever
#from llama_index.core import get_response_synthesizer
#from llama_index.core.response_synthesizers import BaseSynthesizer
#from llama_index.core.retrievers import BaseRetriever
#from langchain.prompts import ChatPromptTemplate
from langchain_core.documents import Document as LCDocument  


SYSTEM_PROMPT = """
Vous êtes un assistant virtuel de l'ISET Sfax (Institut Supérieur des Études Technologiques), établissement public sous tutelle du Ministère Tunisien de l'Enseignement Supérieur. Votre rôle est de fournir des informations précises et officielles aux étudiants et visiteurs en  utilisant la langue de l'utilisateur.

Directives :
1. Analyser automatiquement la langue de la question et répondre DANS LA MÊME LANGUE que la question. Vous parlez Français, Anglais, Arabe et Autres langues.
2. Répondez EXCLUSIVEMENT à partir des données fournies. 
3. Structurez les réponses de manière claire
4. Incluez toujours les liens officiels pertinents
5. En cas d'information manquante, proposez de contacter l'administration

Base de connaissances :

[HORAIRE ET PLANNING]
- Les horaires des cours d'informatique : Consultez le portail étudiant section Horaires. Lien: http://iset.example.com/horaires
- Cours d'Algorithmique : Lundi 8h-10h. Vérifiez le portail. Lien: http://iset.example.com/horaires
- Cours de Python (lundi) : 10h-12h en salle A-101. Lien: http://iset.example.com/horaires
- Cours de Réseaux : Mercredi 14h-16h. Lien: http://iset.example.com/horaires
- Cours le samedi : Certains cours pratiques possibles. Lien: http://iset.example.com/horaires

[ORGANISATION ACADÉMIQUE]
- Début du semestre : 1er septembre. Lien: http://iset.example.com/calendrier
- Calendrier universitaire : Consultez le portail. Lien: http://iset.example.com/calendrier
- Changement de branche : Demande au bureau académique avant date limite. Lien: http://iset.example.com/administration
- Cours en ligne/présentiel : Majorité en présentiel. Lien: http://iset.example.com/horaires

[ENSEIGNANTS ET DÉPARTEMENTS]
- Responsable Génie Civil : Pr. Martin. Lien: http://iset.example.com/departements
- Enseignant Python : Pr. Dupont. Lien: http://iset.example.com/programmes
- Contact professeurs : Portail enseignant. Lien: http://iset.example.com/enseignants
- Horaires de bureau : Portail enseignant. Lien: http://iset.example.com/enseignants

[INFRASTRUCTURES]
- Salle Bases de Données : B-204. Lien: http://iset.example.com/salles
- Réservation salles : Bureau administratif. Lien: http://iset.example.com/salles
- Plan des salles : Section Infrastructures. Lien: http://iset.example.com/infrastructures
- Équipement salles : Projecteurs disponibles. Lien: http://iset.example.com/salles

[EXAMENS ET ÉVALUATIONS]
- Dates examens : Calendrier universitaire. Lien: http://iset.example.com/examens
- Résultats : Portail étudiant. Lien: http://iset.example.com/resultats
- Rattrapages : Contact bureau académique. Lien: http://iset.example.com/examens
- Contestation note : Demande sous 7 jours. Lien: http://iset.example.com/examens

[SERVICES ÉTUDIANTS]
- Certificat scolarité : Bureau administratif. Lien: http://iset.example.com/administration
- Carte étudiante : Après inscription. Lien: http://iset.example.com/administration
- Bibliothèque : 8h-18h (Lun-Ven). Lien: http://iset.example.com/bibliotheque
- Wi-Fi : Identifiants étudiants. Lien: http://iset.example.com/services-it

[VIE ÉTUDIANTE]
- Clubs : Robotique, Culture, Sports. Lien: http://iset.example.com/activites
- Journée portes ouvertes : Mars. Lien: http://iset.example.com/evenements
- Cafétéria : 7h-17h. Lien: http://iset.example.com/ressources
- Sport : Gymnase 10h-20h. Lien: http://iset.example.com/activites

[STAGES ET CARRIÈRE]
- Offres de stage : Portail carrière. Lien: http://iset.example.com/carriere
- Rapport de stage : Consignes en ligne. Lien: http://iset.example.com/carriere
- Foire emploi : Annuelle. Lien: http://iset.example.com/evenements

[CONTACT ADMINISTRATION]
Addresse: Route de Mahdia Km 2.5 BP 88 A - 3099 Sfax
Phone: (+216) 74 431 425
Fax: (+216) 74 431 673
email: iset.sfax@sfax.r-iset.tn

Répondez uniquement avec les informations fournies. Si une question ne peut être répondue, suggérez de contacter l'administration.

"""

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""




class llm_config:
    def __init__(self):
        super().__init__()
        llm_provider = "ollama3.1"
        self.llm = Ollama(model=llm_provider, request_timeout=100.0)
        self.chat_history = [
        ChatMessage(
            role="system",
            content=(SYSTEM_PROMPT))
        ]

        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.normpath(os.path.join(base_dir, '../data/iset_rag.csv'))
        embeddings = OllamaEmbeddings(model="llama3.2")
        """self.db = Chroma(persist_directory="chroma", embedding_function=embeddings)

        df = pd.read_csv(data_dir, sep=",", encoding="utf-8")
        if "combined" not in df.columns:
            df["combined"] = df["Question"] + "\n" + df["Réponse"] + "\nLien: " + df["Lien"]
            df.to_csv(data_dir, sep=",", encoding="utf-8", index=False)

        if not os.path.isfile("chroma/chroma.sqlite3"):
            documents = [LCDocument(page_content=row["combined"], metadata={"row_id": idx}) for idx, row in df.iterrows()]
            self.db.add_documents(documents)
            self.db.persist()
            print("Documents added to Chroma and persisted.")"""
    	


        #index = VectorStoreIndex.from_documents(documents)
        #index.storage_context.persist("faculty_index")

        #storage_context = StorageContext.from_defaults(persist_dir="faculty_index")
        #index = load_index_from_storage(storage_context)
        #service_context = ServiceContext.from_defaults(llm_predictor=, prompt_helper=prompt_helper,
        #                                       embed_model=embed_model)

        #retriever = VectorIndexRetriever(index=index, similarity_top_k=5)
        #response_synthesizer = get_response_synthesizer()

        #self.query_engine = RAGQueryEngine(
        #    retriever=retriever,
        #    response_synthesizer=response_synthesizer
        #)

    def ask_question_to_llm(self, question: str) -> ChatResponse:
        try:

            #results = self.db.similarity_search_with_score(question, k=5)
            #print("Similarity search results:", results)
            #context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            #prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            #prompt = prompt_template.format(context=context_text, question=question)

            #self.chat_history.append(ChatMessage(role="user", content=question))
            #response_obj = self.query_engine.query(prompt)
            #response_content = str(response_obj)
            #self.chat_history.append(ChatMessage(role="assistant", content=response_content))
            #print(response_content)
            #return ChatResponse(message=ChatMessage(role="assistant", content=response_content))
            self.chat_history.append(ChatMessage(role="user", content=question))


            # Query the LLM with the current chat history
            if isinstance(self.llm, Ollama):
                conversation = "\n".join(
                    f"{msg.role.capitalize()}: {msg.content}"
                    for msg in self.chat_history
                )
                response = self.llm.complete(conversation)
                response_content = response.text
            else:
                response = self.llm.chat(self.chat_history)
                response_content = response.message.content

            # Add the LLM's response to the chat history
            self.chat_history.append(ChatMessage(role="assistant", content=response_content))

            # Print the response content for debugging
            print(response_content)

            # Create and return a ChatResponse object
            return ChatResponse(message=ChatMessage(role="assistant", content=response_content))

        except Exception as e:
            # Handle errors and return a fallback response
            error_message = f"Error during LLM query: {e}"

            # Log the error in the chat history
            self.chat_history.append(ChatMessage(role="assistant", content=error_message))

            # Return a fallback error response as a ChatResponse object
            return ChatResponse(message=ChatMessage(role="assistant", content=error_message))

        except Exception as e:
            error_message = f"Error during LLM query: {e}"
            self.chat_history.append(ChatMessage(role="assistant", content=error_message))
            return ChatResponse(message=ChatMessage(role="assistant", content=error_message))

    def reset_interaction_log(self):
        self.chat_history = [
            ChatMessage(role="system", content=(
                SYSTEM_PROMPT
            ))
        ]    
