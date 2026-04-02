from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Document
from companies.models import Company
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .loader import Load_Documents
from .vectorStore import VectorStore
from .embeddings import Embeddings


User = get_user_model()

class DocumentsView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            files = request.FILES.getlist("files")
            user_id = request.data.get("user_id")
            company_id = request.data.get("company_id")

            #  Get actual objects
            user = User.objects.get(id=user_id)
            company = Company.objects.get(id=company_id)

            saved_docs = []

            #  Save files first
            for file in files:
                doc = Document.objects.create(
                    company=company,
                    uploaded_by=user,
                    file_name=file.name,
                    file=file,
                )
                saved_docs.append(doc)

            print(f" {len(saved_docs)} files saved")

            #  Load documents
            all_docs = Load_Documents(saved_docs)

            embed = Embeddings()

            chunks = embed.Split_generation(all_docs)
            texts = [doc.page_content for doc in chunks]

            embeddings = embed.generate_embeddings(texts)

            vector_store = VectorStore()

            
            vector_store.add_documents(
                chunks,
                embeddings,
                metadata={
                    "user_id": str(user_id),
                    "company_id": str(company_id)
                }
            )

            return Response({
                "message": "Files uploaded & embeddings stored",
                "files_count": len(files)
            })

        except Exception as e:
            print(" Error:", str(e))
            return Response({"error": str(e)}, status=500)