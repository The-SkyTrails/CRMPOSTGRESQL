from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView,ListView,UpdateView,DetailView,TemplateView,
)
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
class subagent_dashboard(LoginRequiredMixin, TemplateView):
    template_name = "SubAgent/Dashboard/dashboard.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     enq_enrolled_count = 0
    #     enq_count = 0

    #     leadaccept_count = Enquiry.objects.filter(
    #         Q(lead_status="Enrolled")
    #         | Q(lead_status="Inprocess")
    #         | Q(lead_status="Ready To Submit")
    #         | Q(lead_status="Appointment")
    #         | Q(lead_status="Ready To Collection")
    #         | Q(lead_status="Result")
    #         | Q(lead_status="Delivery"),
    #         created_by=self.request.user,
    #     ).count()
    #     context["leadaccept_count"] = leadaccept_count

    #     lead_count = Enquiry.objects.filter(created_by=self.request.user).count()
    #     context["lead_count"] = lead_count

    #     package = Package.objects.filter(approval = "Yes").order_by("-last_updated_on")[
    #         :10
    #     ]
    #     context["package"] = package

    #     url = "https://back.theskytrails.com/skyTrails/packages/getAllcrm"
    #     response = requests.get(url)
    #     data = response.json()
    #     webpackages = data["data"]["pakage"]

    #     for webpackage in webpackages:
    #         webpackage["id"] = webpackage.pop("_id")
    #         context["webpackages"] = webpackages

    #     story = SuccessStory.objects.all()
    #     context["story"] = story
        
    #     user = self.request.user
    #     faq_count = FAQ.objects.filter(user=user).count()
    #     context["faq_count"] = faq_count

    #     if user.user_type == "4":
    #         enrolled_monthly_counts = defaultdict(int)
    #         all_enquiries_monthly_counts = defaultdict(int)
    #         agent = Agent.objects.get(users=user)
    #         latest_news = News.objects.filter(agent__in=[True]).order_by("-created_at")[:10]

    #         enrolled_monthly_enquiries =  Enquiry.objects.filter(
    #                 Q(
    #                     lead_status="Enrolled",
    #                     assign_to_agent=user.agent,
    #                 )
    #                 | Q(lead_status="Enrolled", created_by=user)
    #             )
            
    #         all_monthly_enquiries =   Enquiry.objects.filter(
    #                 Q(assign_to_agent=user.agent) | Q(created_by=user)
    #             )
            
    #         for enquiry in enrolled_monthly_enquiries:
    #             month_year = datetime(enquiry.registered_on.year, enquiry.registered_on.month, 1)
    #             enrolled_monthly_counts[month_year] += 1

    #         for enquiry in all_monthly_enquiries:
    #             month_year = datetime(enquiry.registered_on.year, enquiry.registered_on.month, 1)
    #             all_enquiries_monthly_counts[month_year] += 1

    #         sorted_enrolled_counts = sorted(enrolled_monthly_counts.items())
    #         enrolled_months = [date.strftime("%B %Y") for date, _ in sorted_enrolled_counts]
    #         enrolled_counts = [count for _, count in sorted_enrolled_counts]
            
    #         sorted_all_counts = sorted(all_enquiries_monthly_counts.items())
    #         all_months = [date.strftime("%B %Y") for date, _ in sorted_all_counts if date.year == datetime.now().year]  # Filter by current year
    #         all_counts = [count for _, count in sorted_all_counts if _.year == datetime.now().year]  # Filter by current year
            
    #         enq_count = sum(all_counts)
    #         enq_enrolled_count = sum(enrolled_counts)

    #         context["agent"] = agent
    #         context["latest_news"] = latest_news
    #         context["enrolled_months"] = enrolled_months
    #         context["enrolled_counts"] = enrolled_counts
    #         context["all_months"] = all_months
    #         context["all_counts"] = all_counts
    #         context["enq_count"] = enq_count
    #         context["enq_enrolled_count"] = enq_enrolled_count



    #     if user.user_type == "5":
    #         outagent = OutSourcingAgent.objects.get(users=user)
    #         news = News.objects.filter(outsource_Agent__in=[True]).order_by("-created_at")[
    #             :10
    #         ]

    #         todo = Todo.objects.filter(user=self.request.user).order_by("-id")

    #         enrolled_monthly_enquiries = Enquiry.objects.filter(
    #                 Q(
    #                     lead_status="Enrolled",
    #                     assign_to_outsourcingagent=user.outsourcingagent,
    #                 )
    #                 | Q(lead_status="Enrolled", created_by=user)
    #             )
            
    #         all_monthly_enquiries =   Enquiry.objects.filter(
    #                 Q(assign_to_outsourcingagent=user.outsourcingagent)
    #                 | Q(created_by=user)
    #             )
            
    #         for enquiry in enrolled_monthly_enquiries:
    #             month_year = datetime(enquiry.registered_on.year, enquiry.registered_on.month, 1)
    #             enrolled_monthly_counts[month_year] += 1

    #         for enquiry in all_monthly_enquiries:
    #             month_year = datetime(enquiry.registered_on.year, enquiry.registered_on.month, 1)
    #             all_enquiries_monthly_counts[month_year] += 1

    #         sorted_enrolled_counts = sorted(enrolled_monthly_counts.items())
    #         enrolled_months = [date.strftime("%B %Y") for date, _ in sorted_enrolled_counts]
    #         enrolled_counts = [count for _, count in sorted_enrolled_counts]
            
    #         sorted_all_counts = sorted(all_enquiries_monthly_counts.items())
    #         all_months = [date.strftime("%B %Y") for date, _ in sorted_all_counts if date.year == datetime.now().year]  # Filter by current year
    #         all_counts = [count for _, count in sorted_all_counts if _.year == datetime.now().year]  # Filter by current year
            
    #         enq_count = sum(all_counts)
    #         enq_enrolled_count = sum(enrolled_counts)
    #         context["agent"] = outagent
    #         context["latest_news"] = news
    #         context["enrolled_months"] = enrolled_months
    #         context["enrolled_counts"] = enrolled_counts
    #         context["all_months"] = all_months
    #         context["all_counts"] = all_counts
    #         context["enq_count"] = enq_count
    #         context["enq_enrolled_count"] = enq_enrolled_count
            
             
    #         context["todo"] = todo

    #     return context





class Enquiry1View(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = EnquiryForm1()
        user = request.user
        faq_count = FAQ.objects.filter(user=user).count()
        return render(
            request,
            "SubAgent/Enquiry/lead1.html",
            {"form": form, "faq_count": faq_count},
        )

    def post(self, request):
        form = EnquiryForm1(request.POST)
        if form.is_valid():
            cleaned_data = {
                "FirstName": form.cleaned_data["FirstName"],
                "LastName": form.cleaned_data["LastName"],
                "email": form.cleaned_data["email"],
                "contact": form.cleaned_data["contact"],
                "Dob": form.cleaned_data["Dob"].strftime("%Y-%m-%d"),
                "Gender": form.cleaned_data["Gender"],
                "Country": form.cleaned_data["Country"],
                "passport_no": form.cleaned_data["passport_no"],
            }
            request.session["subagent_enquiry_form1"] = cleaned_data
            return redirect("agent_enquiry_form2")

        return render(
            request,
            "SubAgent/Enquiry/lead2.html",
            {"form": form},
        )


class Enquiry2View(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = EnquiryForm2()
        user = request.user
        faq_count = FAQ.objects.filter(user=user).count()
        return render(
            request,
            "SubAgent/Enquiry/lead2.html",
            {"form": form, "faq_count": faq_count},
        )

    def post(self, request):
        form = EnquiryForm2(request.POST)
        if form.is_valid():
            # Retrieve personal details from session
            enquiry_form1 = request.session.get("subagent_enquiry_form1", {})

            # Safely retrieve spouse_dob and format it if available
            cleaned_data = {
                "spouse_name": form.cleaned_data["spouse_name"],
                "spouse_no": form.cleaned_data["spouse_no"],
                "spouse_email": form.cleaned_data["spouse_email"],
                "spouse_passport": form.cleaned_data["spouse_passport"],
                "spouse_relation": form.cleaned_data["spouse_relation"],
                "spouse_name1": form.cleaned_data["spouse_name1"],
                "spouse_no1": form.cleaned_data["spouse_no1"],
                "spouse_email1": form.cleaned_data["spouse_email1"],
                "spouse_passport1": form.cleaned_data["spouse_passport1"],
                "spouse_relation1": form.cleaned_data["spouse_relation1"],
                "spouse_name2": form.cleaned_data["spouse_name2"],
                "spouse_no2": form.cleaned_data["spouse_no2"],
                "spouse_email2": form.cleaned_data["spouse_email2"],
                "spouse_passport2": form.cleaned_data["spouse_passport2"],
                "spouse_relation2": form.cleaned_data["spouse_relation2"],
                "spouse_name3": form.cleaned_data["spouse_name3"],
                "spouse_no3": form.cleaned_data["spouse_no3"],
                "spouse_email3": form.cleaned_data["spouse_email3"],
                "spouse_passport3": form.cleaned_data["spouse_passport3"],
                "spouse_relation3": form.cleaned_data["spouse_relation3"],
                "spouse_name4": form.cleaned_data["spouse_name4"],
                "spouse_no4": form.cleaned_data["spouse_no4"],
                "spouse_email4": form.cleaned_data["spouse_email4"],
                "spouse_passport4": form.cleaned_data["spouse_passport4"],
                "spouse_relation4": form.cleaned_data["spouse_relation4"],
                "spouse_name5": form.cleaned_data["spouse_name5"],
                "spouse_no5": form.cleaned_data["spouse_no5"],
                "spouse_email5": form.cleaned_data["spouse_email5"],
                "spouse_passport5": form.cleaned_data["spouse_passport5"],
                "spouse_relation5": form.cleaned_data["spouse_relation5"],
            }

            for i in range(1, 6):
                spouse_dob = form.cleaned_data.get("spouse_dob")
                spouse_dob = form.cleaned_data.get(f"spouse_dob{i}")

                if spouse_dob:
                    cleaned_data["spouse_dob"] = spouse_dob.strftime("%Y-%m-%d")
                    cleaned_data[f"spouse_dob{i}"] = spouse_dob.strftime("%Y-%m-%d")
            # Merge personal details with receiver details
            merged_data = {**enquiry_form1, **cleaned_data}

            # Save the merged data to the session
            request.session["agent_enquiry_form2"] = merged_data
            return redirect("agent_enquiry_form3")

        return render(
            request,
            "SubAgent/Enquiry/lead2.html",
            {"form": form},
        )


class Enquiry3View(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = EnquiryForm3()
        user = request.user
        faq_count = FAQ.objects.filter(user=user).count()
        return render(
            request,
            "SubAgent/Enquiry/lead3.html",
            {"form": form, "faq_count": faq_count},
        )

    def post(self, request):
        form1_data = request.session.get("subagent_enquiry_form1", {})
        form2_data = request.session.get("agent_enquiry_form2", {})
        form3 = EnquiryForm3(request.POST)

        if form3.is_valid():
            user = self.request.user

            # Merge data from all three forms
            merged_data = {
                **form1_data,
                **form2_data,
                **form3.cleaned_data,
            }

            # Save the merged data to the database
            enquiry = Enquiry(**merged_data)
            # ---------------------------------------

            # ------------------------------
            enquiry.created_by = user
            if user.user_type == "5":
                enquiry.assign_to_outsourcingagent = user.outsourcingagent
            enquiry.lead_status = "New Lead"
            enquiry.save()
            messages.success(request, "Enquiry Added successfully")

            # Clear session data after successful submission
            request.session.pop("subagent_enquiry_form1", None)
            request.session.pop("agent_enquiry_form2", None)

            return redirect("agent_enquiry_form4", id=enquiry.id)

        return render(
            request,
            "SubAgent/Enquiry/lead3.html",
            {"form": form3},
        )

    def get_success_url(self):
        enquiry_id = self.object.id
        return reverse_lazy("agent_enquiry_form4", kwargs={"id": enquiry_id})

 
def subagent_new_leads_details(request):
    # user = request.user
    # excluded_statuses = ["Accept", "Case Initiated"]
    # lead = [status for status in leads_status if status[0] not in excluded_statuses]

    # faq_count = FAQ.objects.filter(user=user).count()
    # user_type = user.user_type
    # if user_type == "5":
    #     enquiry = Enquiry.objects.filter(
    #         Q(assign_to_outsourcingagent=user.outsourcingagent) | Q(created_by=user)
    #     ).order_by("-id")
    # elif user_type == "4":
    #     enquiry = Enquiry.objects.filter(
    #         Q(assign_to_agent=user.agent) | Q(created_by=user)
    #     ).order_by("-id")

    # context = {"enquiry": enquiry, "faq_count": faq_count, "lead": lead}

    return render(request, "SubAgent/Enquiry/lead-details.html")

