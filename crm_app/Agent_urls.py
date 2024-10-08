from django.urls import path, include
from .AgentViews import *
from .API_views import AgentWebsitePackage


urlpatterns = [
    path("Dashboard/", agent_dashboard.as_view(), name="agent_dashboard"),
    path("AddEnquiry/", Enquiry1View.as_view(), name="agent_enquiry_form1"),
    path("AddEnquiry2/", Enquiry2View.as_view(), name="agent_enquiry_form2"),
    path("AddEnquiry3/", Enquiry3View.as_view(), name="agent_enquiry_form3"),
    path("enquiry_form4/<int:id>/", agentdocument, name="agent_enquiry_form4"),
    path("Uploaddocument/", upload_document, name="agent_uploaddocument"),
    path("Delete/UploadFile/<int:id>", delete_docfile, name="agent_docfile"),
    # ---------------------------------------------------------------
    path(
        "PacAddEnquiry/", agent_PackageEnquiry1View, name="agent_packageenquiry_form1"
    ),
    path(
        "PacAddEnquiry2/", agent_PackageEnquiry2View, name="agent_packageenquiry_form2"
    ),
    path(
        "PacAddEnquiry3/", agent_PackageEnquiry3View, name="agent_packageenquiry_form3"
    ),
    # ------------------------------- LEADS ------------------------
    path("AllNewLeads", agent_new_leads_details, name="agent_new_leads_details"),
    path("AddNotes/", agent_add_notes, name="agent_add_notes"),
    path("Resend/<int:id>/", resend, name="resend"),
    path(
        "edit/Enrolled/Application/<int:id>",
        edit_enrolled_application,
        name="agent_edit_enrolled_application",
    ),
    path("Educaion/Summary/<int:id>", combined_view, name="agent_education_summary"),
    path(
        "Test/Score/Delete/<int:id>", delete_test_score, name="agent_delete_test_score"
    ),
    path("Product/<int:id>", editproduct_details, name="agent_edit_product_details"),
    path(
        "enrolled_document/<int:id>/", enrolleddocument, name="agent_enrolled_document"
    ),
    path(
        "enrolledUploaddocument/",
        enrolled_upload_document,
        name="agent_enrolleduploaddocument",
    ),
    path(
        "Delete/enrolledUploadFile/<int:id>",
        enrolled_delete_docfile,
        name="agent_enrolleddocfile",
    ),
    path("PackageList/", PackageListView.as_view(), name="Agent_Package_list"),
    path(
        "packages/<int:pk>/", PackageDetailView.as_view(), name="Agent_package_detail"
    ),
    path(
        "Agent/packages/<int:id>/apply/",
        agent_PackageApplyView,
        name="agent_PackageApplyView",
    ),
    path("logout", agent_logout, name="agent_logout"),
    path("ChangePassword", ChangePassword, name="AgentChangePassword"),
    path("AddQueries/", FAQCreateView.as_view(), name="Agent_addfaq"),
    path("resolved-queries/", ResolvedFAQListView.as_view(), name="resolved_queries"),
    path("pending-queries/", PendingFAQListView.as_view(), name="pending_queries"),
    path("profile", profileview.as_view(), name="Agent_profile"),
    path("edit_profile/", edit_profile, name="edit_agent_profile"),
    # ------------------------ Appointment url -----------------------
    path("appointmentlist/", AppointmentListView.as_view(), name="Appointment_list"),
    path("appointmentgrid/", AppointmentGridView.as_view(), name="Appointment_grid"),
    path("AddPackage/", PackageCreateView.as_view(), name="Agent_Package"),
    path("News_list/", NewsList.as_view(), name="Agent_News_list"),
    path(
        "Success_StoryList/", SuccessStoryList.as_view(), name="Agent_SuccessStoryList"
    ),
    path("create_report/", create_report, name="create_report"),
    path("reportlist/", ReportList.as_view(), name="Agent_reportlist"),
    path("lead_update/<int:id>", agent_lead_updated, name="agent_lead_updated"),
    # ----------------------------- TODO -----------------------------
    path("Todo/", Agent_add_todo, name="Agent_add_todo"),
    path("Update/Todo/<int:id>/", Agent_update_todo, name="Agent_update_todo"),
    path("Delete/Todo/<int:id>/", Agent_delete_todo, name="Agent_delete_todo"),
    path("NewLead/Save/", submit, name="agent_newlead_save"),
    path("WebsitePackage/", AgentWebsitePackage, name="Agent_websitepackage"),


    # ---------------------------------- SubAgent -------------------------

    
    path("Add/SubAgent/", add_subagent, name="add_subagent"),
    path("SubAgent/List", subagent_list, name="subagent_list"),
    path("SubAgent/Delete/<int:id>/", subagent_delete, name="subagent_delete"),
    path("SubAgent/Details/<int:id>", subagent_details, name="subagent_details"),
    path("SubAgent/Agreement/<int:id>", subagent_agreement, name="subagent_agreement"),
    path("SubAgent/Agreement/update/<int:id>/",subagent_agreement_update,name="subagent_agreement_update",),
    path("SubAgent/Agreement/Delete/<int:id>/",subagent_agreement_delete,name="subagent_agreement_delete",),
    path("SubAgent/Kyc/<int:id>", subagent_kyc, name="subagent_kyc"),
    

    # ----------------------------------- Agent Employee --------------------------
    
    path("Add/Employee/", agent_add_employee, name="agent_add_employee"),
    path("Employee/List", agent_emp_list.as_view(), name="agent_emp_list"),
    path("Employee/Edit/<int:pk>/", agent_emp_edit, name="agent_emp_edit"),
    path("Employee/Delete/<int:id>/", agent_emp_delete, name="agent_emp_delete"),
    path("HolidayPackageList/", HolidayPackageListView.as_view(), name="Agent_HolidayPackage_list"),
    path("VisitorPackageList/", VisitorPackageListView.as_view(), name="Agent_VisitorPackage_list"),
    path("WorkPackageList/", WorkPackageListView.as_view(), name="Agent_WorkPackage_list"),
    path("StudyPackageList/", StudyPackageListView.as_view(), name="Agent_StudyPackage_list"),
    path("InvestmentPackageList/", InvestmentPackageListView.as_view(), name="Agent_InvestmentPackage_list"),
    path("SettlementPackageList/", SettlementPackageListView.as_view(), name="Agent_SettlementPackage_list"),
    
]
