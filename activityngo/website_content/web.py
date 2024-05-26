from django.shortcuts import render

from activityngo.website_content.models import WebsiteContent, WebsiteCoverPhoto


def get_index_page(request):
    return render(
        request,
        "website/index.html",
    )


def website_content_pages(request):
    db_page_name = {
        "what": "what",
        "where": "where",
        "how": "how",
        "list": "list",
        "who": "who",
        "": "what",
    }.get(request.path.strip("/"), "okay")
    current_domain = request.META.get('HTTP_HOST', '')

    try:
        if current_domain == "activitypointsengg.com":
            domain = "activity_points_engg"
        else:
            domain = "lgs_research_foundation"
    except:
        domain = "activity_points_engg"

    web_content = {
        "web_content": WebsiteContent.objects.filter(
            domain=domain, page_name=db_page_name
        ).first(),
        "web_cover_photos": WebsiteCoverPhoto.objects.filter(
            domain=domain,
        )
    }
    return render(request, "website/web_content.html", web_content)
