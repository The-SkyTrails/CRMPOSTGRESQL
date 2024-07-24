from django.urls import path, include
from .SubAgentViews import *
urlpatterns = [

    path("Dashboard/", subagent_dashboard.as_view(), name="subagent_dashboard"),
    # --------------------------- Enquiry ----------------------------------
    path("AddEnquiry/", Enquiry1View.as_view(), name="subagent_enquiry_form1"),
    path("AddEnquiry2/", Enquiry2View.as_view(), name="subagent_enquiry_form2"),
    path("AddEnquiry3/", Enquiry3View.as_view(), name="subagent_enquiry_form3"),
    # path("enquiry_form4/<int:id>/", agentdocument, name="subagent_enquiry_form4"),
    # path("Uploaddocument/", upload_document, name="subagent_uploaddocument"),
    # path("Delete/UploadFile/<int:id>", delete_docfile, name="subagent_docfile"),


    path("AllNewLeads/", subagent_new_leads_details, name="subagent_new_leads_details"),
]